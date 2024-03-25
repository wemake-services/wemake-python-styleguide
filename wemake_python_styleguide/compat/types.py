import ast
from typing import Union

from typing_extensions import TypeAlias

from wemake_python_styleguide.compat.nodes import MatchAs, MatchStar, TryStar

#: When used with `visit_Try` and visit_TryStar`.
AnyTry: TypeAlias = Union[ast.Try, TryStar]

#: Used when named matches are needed.
NamedMatch: TypeAlias = Union[MatchAs, MatchStar]
