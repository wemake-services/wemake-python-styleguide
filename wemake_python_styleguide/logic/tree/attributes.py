import ast
from collections.abc import Iterable

from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.types import AnyNodes, AnyVariableDef


def _chained_item(iterator: ast.AST) -> ast.AST | None:
    if isinstance(iterator, ast.Attribute | ast.Subscript):
        return iterator.value
    if isinstance(iterator, ast.Call):
        return iterator.func
    return None


def parts(node: ast.AST) -> Iterable[ast.AST]:
    """
    Returns all ``.`` separated elements for attributes, subscripts and calls.

    Attributes might be complex:

    .. code:: python

      self.profiler._store[cache_id].execute()

    We need all parts from it.
    """
    iterator = node

    while True:
        yield iterator

        chained_item = _chained_item(iterator)
        if chained_item is None:
            return
        iterator = chained_item


def only_consists_of_parts(node: ast.AST, allowed: AnyNodes) -> bool:
    """Returns `True` if some node consists of only given parts."""
    return all(isinstance(part, allowed) for part in parts(node))


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


def is_special_attr(node: ast.Attribute) -> bool:
    """Finds attributes that are assigned to `self`, `cls`, etc."""
    if not isinstance(node.value, ast.Name):
        return False
    return node.value.id in SPECIAL_ARGUMENT_NAMES_WHITELIST
