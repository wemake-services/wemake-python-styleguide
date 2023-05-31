import ast
from typing import Union

from typing_extensions import TypeAlias

from wemake_python_styleguide.types import AnyAssign

#: When we search for assign elements, we also need typed assign.
AnyAssignWithWalrus: TypeAlias = Union[AnyAssign, ast.NamedExpr]
