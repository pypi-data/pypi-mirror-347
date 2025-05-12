import numpy as np
import numpy.typing as npt
import sympy

from .types import TStructureTensor


def get_gamma(generators: npt.NDArray) -> npt.NDArray:
    """
    Given a 3D tensor of generators, where the first index is the generator index, the
    structure constants of the Lie algebra are computed. The structure constants are
    defined as gamma_ijk in the relation [g_i, g_j] = sum_k gamma_ijk g_k.

    This function has a logic that has only been tested with generators of the SU(N)
    group in one Cartan basis where the generators are Eij = delta_ij, for i!=0 and
    j!=0, and Hi = delta_i,i - delta_i+1,i+1, where delta_ij is the Kronecker delta.
    This function also checks that the decomposition of the commutator on the generator
    basis has been successful. If not, it raises an error.

    Args:
        generators (npt.NDArray): _description_

    Returns:
        npt.NDArray: _description_
    """
    num_generators = generators.shape[0]
    dim_generators = generators.shape[1]
    assert dim_generators == generators.shape[2], (
        "The generators tensor must be a 3D tensor with the last two dimensions "
        "being equal."
    )
    gamma = np.zeros((num_generators, num_generators, num_generators), dtype=complex)

    # G will be explained later.
    G = generators.transpose(1, 2, 0).reshape(dim_generators**2, num_generators)
    for i in range(num_generators):
        gi = generators[i]
        for j in range(i + 1, num_generators):
            gj = generators[j]
            commutator = gi @ gj - gj @ gi
            if np.all(np.isclose(commutator, 0)):
                continue
            # Now we check if the commutator overlaps with any of the generators
            # To do this, we flatten the commutator, call it c. What we need to do is
            # come up with a vector a such that c = G a, where G is an N^2xL matrix
            # where the rows indicate the index of vector c, and the columns indicate
            # the index of the generator. We need to solve this linear system for a.
            # Since the generators are a basis, the linear system is always solvable.

            c = commutator.flatten()
            try:
                a = sympy.Matrix(G).gauss_jordan_solve(sympy.Matrix(c))[0]
            except ValueError:
                raise ValueError(
                    "The commutator does not decompose on the generator basis.\n"
                    f"Look at generators {i} and {j}:\n{gi}\n{gj}\nand the commutator\n"
                    f"{commutator}"
                )
            a = sympy.lambdify(tuple(), a, "numpy")().flatten()
            assert a.shape == (num_generators,)
            gamma[i, j] = a
            # Check that the decomposition is correct
            assert np.allclose(commutator, np.einsum("lij,l->ij", generators, a))
    for i in range(num_generators):
        for j in range(i + 1, num_generators):
            for k in range(num_generators):
                if gamma[i, j, k] != 0:
                    gamma[j, i, k] = -gamma[i, j, k]
    return gamma


def fill_gamma(gamma: TStructureTensor) -> TStructureTensor:
    """
    Fills the gamma tensor with the missing values. The user can provide only the upper
    triangle of the gamma tensor (or the lower triangle, it doesn't matter). This
    function fills the missing values by using the antisymmetry of the structure
    constants.

    Args:
        gamma (TStructureTensor): A 3D tensor with the structure constants of a Lie
            algebra.

    Returns:
        TStructureTensor: The gamma tensor with the missing values filled.
    """
    dim = gamma.shape[0]
    for i in range(dim):
        for j in range(i + 1, dim):
            for k in range(dim):
                if gamma[i, j, k] != 0:
                    if gamma[j, i, k] != 0:
                        assert gamma[j, i, k] == -gamma[i, j, k]  # type: ignore
                    else:
                        gamma[j, i, k] = -gamma[i, j, k]  # type: ignore
                elif gamma[j, i, k] != 0:
                    gamma[i, j, k] = -gamma[j, i, k]  # type: ignore
    return gamma


def get_TEO(generators: npt.NDArray) -> sympy.Matrix:
    """
    Given a 3D tensor of generators, where the first index is the generator index, the
    time evolution operator is computed. The time evolution operator is defined as
    U = exp(Lambda_1 E_1) exp(Lambda_2 E_2) ... exp(Lambda_{n} E_{n}),


    Args:
        generators (npt.NDArray): array of generators of the Lie algebra.

    Returns:
        sympy.Matrix: The time evolution operator.
    """
    U = sympy.eye(generators.shape[1])
    for i in range(generators.shape[0]):
        U = sympy.MatMul(
            U,
            sympy.exp(
            sympy.Matrix(generators[i]) * sympy.Symbol(f"\\Lambda_{{{i+1}}}")
        ), evaluate=True
        )
    return U