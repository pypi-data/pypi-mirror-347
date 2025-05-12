import typing

import numpy.typing as npt
import sympy

StructureTensor = npt.NDArray | sympy.MutableDenseNDimArray
Coefficients = npt.NDArray | sympy.Matrix
TStructureTensor = typing.TypeVar("TStructureTensor", bound=StructureTensor)
