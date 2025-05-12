import itertools
from functools import reduce
from typing import Literal

import numpy as np
import numpy.typing as npt
import sympy


def get_sun_generators(n: int) -> npt.NDArray:
    """
    Generate a Cartan-Weyl basis for the SU(N) Lie algebra.
    The generators are organized as follows:
    -   For $0 \leq l \leq (n-2)(n-3)/2$ we take $g_0 = \delta_{0,1}$,
        $g_1 = \delta_{0,2}$, and the next generators come from iterating
        over the upper right part of an n by n matrix; iterate first over
        the columns and then over the rows.
    -   For $(n-2)(n-3)/2 < l \leq (n-2)(n-3)/2 + n$, take
        $g_l = H_{l - (n-2)(n-3)/2}$, where $H_i$ is the matrix with
        1 in the ith entry of the diagonal and -1 in the $i + 1$ entry
        of the diagonal.
    -   For $(n-2)(n-3)/2 + n \leq l \leq n^2$ we take
        $g_{(n-2)(n-3)/2 + n} = \delta_{0,1}$,
        $g_{(n-2)(n-3)/2 + n +1} = \delta_{0,2}$,
        and the next generators come from iterating
        over the lower left part of an n by n matrix; iterate first over
        the rows and then over the columns.
    """
    Eplus = []
    Eminus = []
    for i in range(n):
        for j in range(i + 1, n):
            generator = np.zeros((n, n))
            generator[i, j] = 1
            Eplus.append(generator)
            generator = np.zeros((n, n))
            generator[j, i] = 1
            Eminus.append(generator)
    Hs = []
    for i in range(n - 1):
        generator = np.zeros((n, n))
        generator[i, i] = 1
        generator[i + 1, i + 1] = -1
        Hs.append(generator)

    generators = np.stack(Eplus + Hs + Eminus)
    return generators


def TEO(Lambda: npt.NDArray, n: int) -> npt.NDArray:
    """
    Computes the time evolution operator for the SU(n) decomposition as
    U = exp(Lambda_1 E_1) exp(Lambda_2 E_2) ... exp(Lambda_{n^2 - 1} E_{n^2 - 1}),
    where the E_i are the generators of the SU(n) group in the Cartan-Weyl basis.

    Args:
        Lambda (npt.NDArray): The parameters for the time evolution operator.
        n (int): The size of the SU(n) group.

    Returns:
        npt.NDArray: The time evolution operator.
    """
    assert Lambda.size == n * n - 1, (
        "The Lambda array must have size n^2 - 1, where n is the size of the "
        "SU(n) group."
    )
    U = np.eye(n, dtype=complex)
    idx = 0
    # First the off-diagonal elements from the upper triangle
    for i in range(n):
        for j in range(i + 1, n):
            expg = np.eye(n, dtype=complex)
            expg[i, j] = Lambda[idx]
            idx += 1
            U = U @ expg
    # Now the diagonal elements
    for i in range(n - 1):
        expg = np.eye(n, dtype=complex)
        expg[i, i] = np.exp(Lambda[idx])
        expg[i + 1, i + 1] = np.exp(-Lambda[idx])
        idx += 1
        U = U @ expg
    # Now the off-diagonal elements from the lower triangle
    for i in range(n):
        for j in range(i + 1, n):
            expg = np.eye(n, dtype=complex)
            expg[j, i] = Lambda[idx]
            idx += 1
            U = U @ expg
    return U


def TEO_symbolic(
    n: int, init_idx: int = 1, type: Literal["Pauli", "Cartan"] = "Cartan"
) -> sympy.Matrix:
    """
    Computes the time evolution operator for the SU(n) decomposition as
    U = exp(Lambda_1 E_1) exp(Lambda_2 E_2) ... exp(Lambda_{n^2 - 1} E_{n^2 - 1}),
    where the E_i are the generators of the SU(n) group in the Cartan-Weyl basis.

    Args:
        Lambda (npt.NDArray): The parameters for the time evolution operator.
        n (int): The size of the SU(n) group.

    Returns:
        npt.NDArray: The time evolution operator.
    """
    U = sympy.Matrix(np.eye(n, dtype=complex))
    idx = init_idx
    if type == "Cartan":
        # First the off-diagonal elements from the upper triangle
        for i in range(n):
            for j in range(i + 1, n):
                expg = sympy.Matrix(np.eye(n, dtype=complex))
                expg[i, j] = sympy.Symbol(f"\\Lambda_{{{idx}}}")
                idx += 1
                U = sympy.MatMul(U, expg, evaluate=True)
        # Now the diagonal elements
        for i in range(n - 1):
            expg = sympy.Matrix(np.eye(n, dtype=complex))
            expg[i, i] = sympy.exp(sympy.Symbol(f"\\Lambda_{{{idx}}}"))
            expg[i + 1, i + 1] = sympy.exp(-sympy.Symbol(f"\\Lambda_{{{idx}}}"))
            idx += 1
            U = sympy.MatMul(U, expg, evaluate=True)
        # Now the off-diagonal elements from the lower triangle
        for i in range(n):
            for j in range(i):
                expg = sympy.Matrix(np.eye(n, dtype=complex))
                expg[i, j] = sympy.Symbol(f"\\Lambda_{{{idx}}}")
                idx += 1
                U = sympy.MatMul(U, expg, evaluate=True)
    else:
        assert (n & (n - 1)) == 0, "The number of generators must be a power of 2."
        # First the off-diagonal elements from the upper triangle
        str_2_array = {
            "I": np.eye(2),
            "X": np.array([[0, 1], [1, 0]]),
            "Y": np.array([[0, -1j], [1j, 0]]),
            "Z": np.array([[1, 0], [0, -1]]),
        }
        power = int(np.log2(n))
        generators_str = list(itertools.product("IXYZ", repeat=power))[1:]
        generators = [
            reduce(
                np.kron,
                [str_2_array[gen] for gen in generator[1:]],
                str_2_array[generator[0]],
            )
            for generator in generators_str
        ]
        for gen in generators:
            expg = sympy.exp(
                1j * sympy.Symbol(f"\\Lambda_{{{idx}}}") * sympy.Matrix(gen)
            )
            idx += 1
            U = sympy.MatMul(U, expg, evaluate=True)
    return U
