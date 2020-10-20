import ast
from typing import Iterator, Sequence


def get_all_args(call: ast.Call) -> Sequence[ast.AST]:
    """Gets all arguments (args and kwargs) from ``ast.Call``."""
    return [
        *call.args,
        *[kw.value for kw in call.keywords],
    ]


def get_starred_args(call: ast.Call) -> Iterator[ast.Starred]:
    """Gets ``ast.Starred`` arguments from ``ast.Call``."""
    for argument in call.args:
        if isinstance(argument, ast.Starred):
            yield argument
