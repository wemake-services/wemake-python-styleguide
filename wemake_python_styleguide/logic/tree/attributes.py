import ast
from typing import Iterable, Optional

from wemake_python_styleguide.types import AnyAccess


def _chained_item(iterator: ast.AST) -> Optional[ast.AST]:
    if isinstance(iterator, (ast.Attribute, ast.Subscript)):
        return iterator.value
    elif isinstance(iterator, ast.Call):
        return iterator.func
    return None


def parts(node: AnyAccess) -> Iterable[ast.AST]:
    """
    Returns all ``.`` separated elements for attributes and subscripts.

    Attributes might be complex:

    .. code:: python

      self.profiler._store[cache_id].execute()

    We need all parts from it.
    """
    iterator: ast.AST = node

    while True:
        yield iterator

        chained_item = _chained_item(iterator)
        if chained_item is None:
            return
        iterator = chained_item
