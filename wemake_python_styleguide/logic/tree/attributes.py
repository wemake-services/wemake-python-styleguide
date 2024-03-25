import ast
from typing import Iterable, Optional

from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.types import AnyChainable, AnyVariableDef


def _chained_item(iterator: ast.AST) -> Optional[ast.AST]:
    if isinstance(iterator, (ast.Attribute, ast.Subscript)):
        return iterator.value
    elif isinstance(iterator, ast.Call):
        return iterator.func
    return None


def parts(node: AnyChainable) -> Iterable[ast.AST]:
    """
    Returns all ``.`` separated elements for attributes, subscripts and calls.

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


def is_foreign_attribute(node: AnyVariableDef) -> bool:
    """Tells whether this node is a foreign attribute."""
    if not isinstance(node, ast.Attribute):
        return False

    if not isinstance(node.value, ast.Name):
        return True

    # This condition finds attributes like `point.x`,
    # but, ignores all other cases like `self.x`.
    # So, we change the strictness of this rule,
    # based on the attribute source.
    return node.value.id not in SPECIAL_ARGUMENT_NAMES_WHITELIST
