from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import lru_cache

import jax
import jax.numpy as jnp
import numpy as np
import numpy.typing as npt
import sympy
from scipy.integrate import solve_ivp

from .types import Coefficients, StructureTensor
from .utils import fill_gamma


@dataclass
class DiffEqs:
    """
    Dataclass to store the differential equations.
    Attributes:
        latex_code (list[str]): List of strings with the latex code for the equations.
        sympy_code (sympy.Matrix): Sympy matrix with the equations.
    """

    latex_code: list[str]
    sympy_code: sympy.Matrix


@dataclass
class KnownSolution:
    known_solution: jax.Array


@dataclass
class Partition:
    variables: list[str]
    indices: list[int]

    def __eq__(self, value: "Partition") -> bool:
        cond_vars = set(self.variables) == set(value.variables)
        cond_inds = set(self.indices) == set(value.indices)
        return cond_vars and cond_inds


def _check_gamma_dims(gamma: StructureTensor) -> bool:
    dim_condition = len(gamma.shape) == 3
    shape_condition = gamma.shape[0] == gamma.shape[1] == gamma.shape[2]
    return dim_condition and shape_condition


def _get_b_matrices(gamma: StructureTensor) -> list[sympy.Matrix]:
    dim = gamma.shape[0]
    b_matrices = []
    for i in range(dim):
        upsilon = gamma[i, :, :]
        b_matrix = sympy.exp(
            sympy.Matrix(upsilon) * sympy.Symbol(f"\\Lambda_{{{i+1}}}")
        )
        b_matrices.append(b_matrix)
    return b_matrices


def _get_beta_matrices(
    gamma: StructureTensor,
) -> tuple[list[sympy.Matrix], list[sympy.Matrix]]:
    dim = gamma.shape[0]
    b_matrices = _get_b_matrices(gamma)
    beta_matrices = [sympy.eye(dim)]
    for i in range(len(b_matrices)):
        beta_matrices.append(b_matrices[i] * beta_matrices[-1])
    return beta_matrices, b_matrices


def _get_xi_matrix(
    gamma: StructureTensor,
) -> tuple[sympy.Matrix, list[sympy.Matrix], list[sympy.Matrix]]:
    """
    Compute the xi matrix
    """
    beta_matrices, b_matrices = _get_beta_matrices(gamma)
    xi_matrix = sympy.zeros(beta_matrices[0].shape[0])
    for i, j in np.ndindex(*xi_matrix.shape):
        xi_matrix[i, j] = beta_matrices[i][i, j]
    return xi_matrix, beta_matrices, b_matrices


def _is_gamma_valid(gamma: StructureTensor) -> bool:
    dim = gamma.shape[0]
    for i in range(dim):
        for j in range(i, dim):
            for k in range(dim):
                if gamma[i, j, k] != -gamma[j, i, k]:
                    return False
    return True


class Algebra:
    def __init__(self, gamma: StructureTensor, bch_cache_size: int = 1_000_000):
        """
        Initialize the Algebra class.

        Args:
            gamma (StructureTensor): Structure tensor of the algebra. Must be a 3D
                tensor of shape (L, L, L).
            bch_cache_size (int, optional): Size of the cache for the BCH computations.
                Defaults to 1_000_000.
        """
        assert _check_gamma_dims(
            gamma
        ), "Gamma must be an LxLxL tensor containing the structure constants gamma_ijk"
        if not _is_gamma_valid(gamma):
            gamma = fill_gamma(gamma)
        self._gamma = gamma
        self._dim = gamma.shape[0]
        self._beta_matrices = None
        self._b_matrices = None
        self._xi_matrix = None
        self._decoupled_symbolic_field = None
        self._decoupled_diff_eqs = None
        self._coupled_diff_eqs = None
        self._get_similarity_transform = lru_cache(maxsize=bch_cache_size)(
            lambda i, j: self._primitive_similarity_transform(i, j)
        )
        self._get_bch = lru_cache(maxsize=bch_cache_size)(
            lambda i, j: self._primitive_bch(i, j)
        )

    @property
    def xi_matrix(self):
        """
        Obtains the xi matrix of the algebra.
        """
        if self._xi_matrix is None:
            self._xi_matrix, self._beta_matrices, self._b_matrices = _get_xi_matrix(
                self._gamma
            )
        return self._xi_matrix

    @property
    def beta_matrices(self):
        """
        Obtains the beta matrices of the algebra.
        """
        if self._beta_matrices is None:
            self.xi_matrix  # triggers the computation of beta_matrices
        return self._beta_matrices

    @property
    def b_matrices(self) -> list[sympy.Matrix]:
        """
        Obtains the b matrices of the algebra.
        """
        if self._b_matrices is None:
            self.xi_matrix  # triggers the computation of b_matrices
        assert self._b_matrices is not None
        return self._b_matrices

    def get_xi_matrix(self) -> sympy.Matrix:
        """
        Obtains the xi matrix of the algebra.
        """
        return self.xi_matrix

    def change_generators_order(self, new_order: list[int]) -> "Algebra":
        """
        Change the order of the generators in the algebra, returning a new Algebra
        object.

        Args:
            new_order (list[int]): List with the new order of the generators. The
                elements of the list must be integers from 1 to the dimension of the
                algebra.

        Example: if working with an algebra that has 3 generators, i.e.,
            g_1, g_2, g_3, then, provide the list [2,3,1] to tell the algebra
            that you want to use the new order g_2, g_3, g_1
        """
        assert len(new_order) == self._dim
        assert set(new_order) == set(range(1, self._dim + 1))
        new_gamma = sympy.MutableDenseNDimArray(np.zeros_like(self._gamma))
        for ii in range(self._dim):
            for jj in range(self._dim):
                for kk in range(self._dim):
                    new_gamma[ii, jj, kk] = self._gamma[
                        new_order[ii] - 1, new_order[jj] - 1, new_order[kk] - 1
                    ]
        return Algebra(new_gamma)

    def get_coupled_differential_equations(
        self, subs: Sequence[tuple[str | sympy.Expr, str | sympy.Expr]] | None = None
    ) -> DiffEqs:
        """
        Returns the coupled differential equations for the generators of the algebra.

        Args:
            subs (Sequence[tuple[str | sympy.Expr, str | sympy.Expr]] | None):
                List of substitutions to be applied to the equations. Each substitution
                is a tuple of the form (old, new), where old is the expression to be
                replaced and new is the expression to replace it with.
                If None, no substitutions are applied. Defaults to None.
        Returns:
            DiffEqs: The coupled differential equations for the generators of the
                algebra.
        """
        if self._coupled_diff_eqs is not None:
            return self._coupled_diff_eqs
        right_side_of_equations: sympy.Matrix = sympy.MatMul(  # type: ignore
            self.xi_matrix.T,
            sympy.Matrix(
                [sympy.Symbol(f"\\dot{{\\Lambda}}_{{{i+1}}}") for i in range(self._dim)]
            ),
            evaluate=True,
        )
        if subs is not None:
            for sub in subs:
                right_side_of_equations = right_side_of_equations.subs(sub)
        # sum i*eta:
        right_side_of_equations = right_side_of_equations + 1j * sympy.Matrix(
            [sympy.Symbol(f"\\eta_{i+1}") for i in range(self._dim)]
        )
        latex_code = [
            f"{sympy.latex(right_side_of_equations[i])} = 0" for i in range(self._dim)
        ]

        self._coupled_diff_eqs = DiffEqs(
            latex_code=latex_code, sympy_code=right_side_of_equations
        )
        return self._coupled_diff_eqs

    def get_decoupled_differential_equations(self) -> DiffEqs:
        """
        Returns the decoupled differential equations for the generators of the algebra.
        """
        if self._decoupled_diff_eqs is not None:
            return self._decoupled_diff_eqs
        self._decoupled_symbolic_field = self.xi_matrix.T.gauss_jordan_solve(
            sympy.Matrix([sympy.Symbol(f"\\eta_{i+1}") for i in range(self._dim)])
        )[0]
        right_side_of_equations = (
            sympy.Matrix(
                [
                    1j * sympy.Symbol(f"\\dot{{\\Lambda}}_{{{i+1}}}")
                    for i in range(self._dim)
                ]
            )
            - self._decoupled_symbolic_field
        )
        latex_code = [
            f"{sympy.latex(right_side_of_equations[i])} = 0" for i in range(self._dim)
        ]
        self._decoupled_diff_eqs = DiffEqs(
            latex_code=latex_code, sympy_code=right_side_of_equations
        )
        return self._decoupled_diff_eqs

    def get_similarity_transform(
        self, i: int, j: int
    ) -> tuple[sympy.Expr, sympy.Matrix]:
        """
        Retrieves the similarity transform between generators i and j, where counting
        starts from 1. The similarity transformation is given by
        e^{Lambdai g_i}g_je^{-Lambda g_i}.

        Args:
            i (int): Index of the first generator. Start counting from 1.
            j (int): Index of the second generator. Start counting from 1.

        Returns:
            Returns a tuple with the result of the similarity transform as a sympy
            expression, and the corresponding vector of coefficients so that the
            similarity transform can be written as the dot product of the coefficients
            and the generators.
        """
        return self._get_similarity_transform(i, j)

    def get_bch(self, i: int, j: int) -> sympy.Expr:
        """
        Retrieves the Baker-Campbell-Hausdorff formula for the generators i and j, where
        counting starts from 1. The formula is given by e^gi e^gj = e^Z, where
        Z = gi + integral dLambda_i e^(Lambda_i gi) gj e^(-Lambda_i gi) evaluated at
        Lambda_i = 1.

        Args:
            i (int): Index of the first generator. Start counting from 1.
            j (int): Index of the second generator. Start counting from 1.

        Returns:
            sympy.Expr: The result of the Baker-Campbell-Hausdorff formula as a sympy
            expression.
        """
        return self._get_bch(i, j)

    def _primitive_similarity_transform(
        self, i: int, j: int
    ) -> tuple[sympy.Expr, sympy.Matrix]:
        # sympy.Matrix added to avoid type error
        bch_vector = sympy.Matrix(self.b_matrices[i - 1][j - 1, :]).T
        expr = sympy.sympify(0)
        for k in range(self._dim):
            expr += sympy.Symbol(f"\\hat{{g}}_{k+1}") * bch_vector[k]  # type: ignore
        return expr, bch_vector

    def _primitive_bch(self, i: int, j: int) -> sympy.Expr:
        # compute Z in e^gi e^gj = e^Z using the similarity transform:
        # Z = gi + integral dLambda_i e^(Lambda_i gi) gj e^(-Lambda_i gi) evaluated
        # at Lambda_i = 1
        variable = sympy.Symbol(f"\\Lambda_{{{i}}}")
        integrand = self.get_similarity_transform(i, j)[0]
        gi = sympy.Symbol(f"\\hat{{g}}_{i}")
        Z = gi + sympy.integrate(integrand, variable).subs(variable, 1)  # type: ignore
        return Z

    def get_nested_similarity_transform(
        self,
        operator_vector: Coefficients,
        heisenberg_vector: Coefficients | None = None,
    ) -> tuple[sympy.Expr, sympy.Matrix]:
        r"""
        Calculates an operator in the Heisenberg picture using similarity transforms.
        The operator is characterised by an operator_vector with components [a1,...,aL]
        such that the operator is sum_k a_k g_k, where g_k are the generators of the
        algebra. The Heisenberg picture is taken with respect to another operator
        characterised by heisenberg_vector, which has the same structure as
        operator_vector. This function can be used to calculate nested similarity
        transforms. In particular, if the heisenberg_vector contains the components
        [Lambda1,...,LambdaL], we will compute

        e^{LambdaL gL}...e^{Lambda1 g1}(sum_k a_k g_k)e^{-Lambda1 g1}...e^{-LambdaL gL}
        =
        sum_k e^{LambdaL gL}...e^{Lambda1 g1}(a_k g_k)e^{-Lambda1 g1}...e^{-LambdaL gL}

        Notice that the standard Heisenberg picture is achieved transforming
        Lambdai -> -Lambdai.

        Args:
            operator_vector (Coefficients): Vector with components [a1,..,aL] such that
                the operator is sum_k a_k g_k

            heisenberg_vector (Coefficients): Vector with components
                [Lambda1,..,LambdaL] such that the Heisenberg operator is
                prod_k exp(Lambda_k g_k). If None, the vector will be
                [-Lambda1,...,-LambdaL] written symbolically, and the nested BCH will
                correspond to the operator written in the standard Heisenberg picture.

        Returns:
            tuple[sympy.Expr, sympy.Matrix]: Result of the nested similarity transform
            as a sympy expression, and the corresponding vector of coefficients so that
            the nested similarity transform can be written as the dot product of the
            coefficients and the generators.
        """
        if heisenberg_vector is None:
            heisenberg_vector = sympy.Matrix(
                [
                    -1 * sympy.Symbol(f"\\Lambda_{i+1}")  # type: ignore
                    for i in range(self._dim)
                ]
            ).T
        assert heisenberg_vector is not None
        for i in range(1, self._dim + 1):
            Lambdai = heisenberg_vector[i - 1]
            if Lambdai == 0:  # this results in applying the identity
                continue
            bch_vector = sympy.MutableDenseMatrix(np.zeros(self._dim, dtype=complex))
            for j in range(1, self._dim + 1):
                ai = operator_vector[j - 1]
                if ai == 0:
                    continue
                expr, bch = self.get_similarity_transform(i, j)
                bch_vector += ai * bch.subs(sympy.Symbol(f"\\Lambda_{i}"), Lambdai)
            operator_vector = bch_vector

        # Now we obtain the expression from the resulting operator_vector:
        expr = sympy.sympify(0)
        for k in range(self._dim):
            expr += (
                sympy.Symbol(f"\\hat{{g}}_{k+1}") * operator_vector[k]
            )  # type: ignore

        # We cast the resulting operator_vector to a sympy.Matrix to avoid type errors
        return expr, sympy.Matrix(operator_vector).T

    def _get_decoupled_diff_eqs_partition(self) -> list[Partition]:

        # First we get a dict of dependencies:
        dependencies = {}

        for equation in self.get_decoupled_differential_equations().sympy_code:
            indeps = []
            dep = None
            for sym in equation.free_symbols:  # type:ignore
                if "dot" in sym.name:  # type:ignore
                    dep = sym.name.split("}")[-2].split("{")[-1]  # type:ignore
                elif "Lambda" in sym.name:  # type:ignore
                    indeps.append(sym.name.split("}")[-2].split("{")[-1])  # type:ignore
            dependencies[dep] = indeps

        # Now we partition the equations:
        partitions = []
        for dep, indeps in dependencies.items():
            is_in_partition = False
            for partition in partitions:
                if dep in partition:
                    partition.update(indeps)
                    is_in_partition = True
                    break
            if not is_in_partition:
                if set(indeps) not in partitions:
                    partitions.append(set(indeps))

        vars_and_indices = []
        for partition in partitions:
            variables = [f"\\Lambda_{{{i}}}" for i in partition]
            indices = [int(i) - 1 for i in partition]
            vars_and_indices.append(Partition(variables, indices))

        return vars_and_indices

    def _get_str_field(self, partition_indices, known_vars):
        import re

        str_reprs = []
        old_to_new = {index + 1: i for i, index in enumerate(partition_indices)}
        for ind in partition_indices:
            eq = str(self._decoupled_symbolic_field[ind])
            eq = re.sub(r"\\Lambda_{(\d+)}", r"y[\1]", eq)
            for kv in known_vars:
                eq = eq.replace(f"y[{kv+1}]", f"k(t)[{kv}]")
            for o, n in old_to_new.items():
                eq = eq.replace(f"y[{o}]", f"y[{n}]")
            eq = re.sub(r"\\eta_(\d+)", r"eta[\1]", eq)
            for i in range(self._dim):
                eq = eq.replace(f"eta[{i+1}]", f"eta(t)[{i}]")
            str_reprs.append(eq)
        return str_reprs

    @staticmethod
    def _get_fn_from_eqs(
        equations: list[str],
    ) -> Callable[[Sequence, int], Callable[[float, npt.ArrayLike], npt.ArrayLike]]:
        function = "import jax.numpy as jnp\n\ndef get_field_fn(eta, k):\n"
        function += "  def f(t, y):\n"
        function += "    return jnp.array(["
        for eq in equations:
            function += f"{eq}, "
        function = function[:-2]
        function += "])\n"
        function += "  return f\n"

        # Since we are using the jax.numpy backend, we convert potentially appearing
        # functions to jax.numpy functions; this will need to be updated as more
        # use cases are explored:
        function = function.replace("exp", "jnp.exp")
        d = {}

        exec(function, d)
        return d["get_field_fn"]

    def _solve_ivp(
        self,
        equations,
        etas,
        t_init,
        t_final,
        t_eval,
        known_solutions: KnownSolution,
        Lambdas0,
        current_indices,
        solved_variables,
    ):

        def k(t):
            idx = (
                jnp.round((t - t_init) / (t_final - t_init) * t_eval.shape[0]).astype(
                    int
                )
                - 1
            )
            return known_solutions.known_solution[:, idx]

        field_fn = self._get_fn_from_eqs(equations)(etas, k)
        fast_field_fn = jax.jit(field_fn)
        jacobian = jax.jit(jax.jacobian(fast_field_fn, argnums=1))

        result = solve_ivp(
            fast_field_fn,
            (t_init, t_final),
            Lambdas0[current_indices],
            t_eval=t_eval,
            jac=jacobian,
        )

        # Use the solution as known values:
        known_solutions.known_solution = known_solutions.known_solution.at[
            jnp.asarray(current_indices)
        ].set(result.y * -1j)
        solved_variables.extend(current_indices)

    def scipy_solve(
        self,
        t_eval: npt.NDArray,
        etas: list[Callable[[float], complex]],
        Lambdas0: npt.NDArray,
        known_solutions: KnownSolution | None = None,
        partitions: list[Partition] | None = None,
        solved_variables: list[int] | None = None,
        verbose: bool = False,
    ):
        """
        Numerically solve the decoupled differential equations using scipy's solve_ivp
        function.

        Args:
            t_eval (npt.NDArray): Evaluation times for the solution.
            etas (list[Callable[[float], complex]]): List of Hamiltonian coefficients,
                which are functions of time.
            Lambdas0 (npt.NDArray): Initial values for the Wei-Norman coefficients.
            known_solutions (KnownSolution, optional): Array of shape (L, time_steps).
                containing known solutions. If None, the array will be initialised to
                zeros. Defaults to None.
            partitions (list[Partition] | None, optional): Partitions of the equations.
                If None, they are automatically calculated. Defaults to None.
            solved_variables (list[int] | None, optional): Indices of the variables for
                which solutions have already been found. If None, defaults to an empty
                list. Defaults to None.
            verbose (bool, optional): If True, print additional information. Defaults to
                False.

        Returns:
            Array, list: An array of shape (L, time_steps) containing the known
                solutions, and a list of the solved variables.
        """

        if known_solutions is None:
            known_solutions = KnownSolution(
                jnp.zeros((self._dim, t_eval.shape[0]), dtype=complex)
            )
        if partitions is None:
            partitions = self._get_decoupled_diff_eqs_partition()
        if solved_variables is None:
            solved_variables = []
        partition_size = float("inf")
        smallest_partition = None
        for partition in partitions:
            if len(partition.indices) < partition_size:
                partition_size = len(partition.indices)
                smallest_partition = partition
        assert isinstance(smallest_partition, Partition)
        # 1. Obtain equations, must be of the form y as variables from 0 to the length
        # of the partition, also k will hold known values at a given time, i.e., k(t)[i]
        # for known value i at time t.
        equations = self._get_str_field(smallest_partition.indices, solved_variables)
        if verbose:
            print(
                "Equations for partition with variables", smallest_partition.variables
            )
            print("are")
            for eq in equations:
                print(eq)
                print()
        t_init = t_eval[0]
        t_final = t_eval[-1]

        # 2. Solve equations with integrator. Solution should be input to
        # known_solutions at the positions indicated by the partition.indices.
        self._solve_ivp(
            equations,
            etas,
            t_init,
            t_final,
            t_eval,
            known_solutions,
            Lambdas0,
            smallest_partition.indices,
            solved_variables,
        )

        # 3. Modify the remaining partitions to remove the solved variables as variables
        # in each partition.
        if len(partitions) > 1:
            new_partitions = []
            vars_to_remove = set(smallest_partition.variables)
            inds_to_remove = set(smallest_partition.indices)
            for partition in partitions:
                if partition == smallest_partition:
                    continue
                new_vars = set(partition.variables) - vars_to_remove
                new_inds = set(partition.indices) - inds_to_remove
                assert len(new_vars) == len(new_inds)
                if len(new_inds) > 0:
                    new_partitions.append(Partition(list(new_vars), list(new_inds)))
            self.scipy_solve(
                t_eval,
                etas,
                Lambdas0,
                known_solutions,
                new_partitions,
                solved_variables,
                verbose,
            )
        # 4. If len(partitions)==1 it means that we just solved it in step 2. So there
        # are no remaining partitions. Now we can check the solved variables and solve
        # the equations for unsolved equations.
        # We need to go through each of the equations of the unsolved variables and
        # write them in terms of the known variables.
        for i in range(self._dim):
            if i in solved_variables:
                continue
            # Get the equation:
            equation = self._get_str_field([i], solved_variables)
            if verbose:
                print("Equation for the Lambda", i + 1)
                print(equation[0])
                print()
            self._solve_ivp(
                equation,
                etas,
                t_init,
                t_final,
                t_eval,
                known_solutions,
                Lambdas0,
                [i],
                solved_variables,
            )
        return known_solutions.known_solution, sorted(solved_variables)
