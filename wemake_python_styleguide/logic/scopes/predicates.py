import ast
from typing import Final

from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.nodes import TryStar
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.logic.source import node_to_string

#: That's what we expect from `@overload` decorator:
_OVERLOAD_EXCEPTIONS: Final = frozenset(('overload', 'typing.overload'))

#: That's what we expect from `@property` decorator:
_PROPERTY_EXCEPTIONS: Final = frozenset(('property', '.setter'))


# Name predicates:


def is_function_overload(node: ast.AST) -> bool:
    """Check that function decorated with `typing.overload`."""
    if isinstance(node, FunctionNodes):
        for decorator in node.decorator_list:
            if node_to_string(decorator) in _OVERLOAD_EXCEPTIONS:
                return True
    return False


def is_no_value_annotation(node: ast.AST) -> bool:
    """Check that variable has annotation without value."""
    return isinstance(node, ast.AnnAssign) and not node.value


def is_property_setter(node: ast.AST) -> bool:
    """Check that function decorated with ``@property.setter``."""
    if isinstance(node, FunctionNodes):
        for decorator in node.decorator_list:
            if node_to_string(decorator) in _PROPERTY_EXCEPTIONS:
                return True
    return False


# Scope predicates:


def is_same_value_reuse(node: ast.AST, names: set[str]) -> bool:
    """Checks if the given names are reused by the given node."""
    if isinstance(node, AssignNodes) and node.value:
        used_names = {
            name_node.id
            for name_node in ast.walk(node.value)
            if isinstance(name_node, ast.Name)
        }
        if not names.difference(used_names):
            return True
    return False


def is_same_try_except_cases(node: ast.AST, names: set[str]) -> bool:
    """Same names in different ``except`` blocks are not counted."""
    if not isinstance(node, ast.ExceptHandler):
        return False

    for except_handler in getattr(get_parent(node), 'handlers', []):
        if (
            except_handler.name
            and except_handler.name == node.name
            and except_handler is not node
        ):
            return True
    return False


def is_import_in_try(node: ast.AST) -> bool:
    """
    Same import names in `try` / `except` block should be ignored.

    Example:
        try:
            from typing import Final
        except ImportError:
            from typing_extensions import Final

    """
    if not isinstance(node, ast.Import | ast.ImportFrom):
        return False
    parent = get_parent(node)
    if not isinstance(parent, ast.Try | ast.ExceptHandler):
        return False
    # We don't use `ast.TryStar` here because it is not a common
    # pattern to have imports in `try/except*` blocks.
    if isinstance(parent, ast.ExceptHandler) and isinstance(
        get_parent(parent),
        TryStar,
    ):
        return False
    # We still require imports to be top-level:
    return isinstance(get_context(parent), ast.Module)
