import ast
from typing import TypeAlias

from wemake_python_styleguide.compat.nodes import TryStar
from wemake_python_styleguide.compat.nodes import TypeAlias as TypeAliasNode

AnyTry: TypeAlias = ast.Try | TryStar
"""When used with `visit_Try` and visit_TryStar`."""

NamedMatch: TypeAlias = ast.MatchAs | ast.MatchStar
"""Used when named matches are needed."""

NodeWithTypeParams: TypeAlias = (
    ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef | TypeAliasNode
)
"""These nodes have `.type_params` on python3.12+:"""
