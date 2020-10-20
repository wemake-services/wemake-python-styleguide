import ast
from typing import Iterable, Optional


def _chained_item(iterator: ast.AST) -> Optional[ast.Call]:
    children = list(ast.iter_child_nodes(iterator))
    if isinstance(children[0], ast.Call):
        return children[0]
    return None


def parts(node: ast.Call) -> Iterable[ast.Call]:
    """Returns all consecutive function calls."""
    iterator: ast.Call = node

    while True:
        yield iterator

        chained_item = _chained_item(iterator)
        if chained_item is None:
            return
        iterator = chained_item
