from typing import Union

from wemake_python_styleguide.compat.nodes import NamedExpr
from wemake_python_styleguide.types import AnyAssign

#: When we search for assign elements, we also need typed assign.
AnyAssignWithWalrus = Union[AnyAssign, NamedExpr]
