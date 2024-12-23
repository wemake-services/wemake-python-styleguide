import ast
from typing import NamedTuple, final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.nodes import TryStar
from wemake_python_styleguide.logic.naming import logical
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.types import AnyImport


@final
class ImportedObjectInfo(NamedTuple):
    """Information about imported object."""

    module: str
    node: AnyImport


def get_module_name(node: ast.ImportFrom) -> str:
    """
    Returns module name for any ``ImportFrom``.

    Handles all corner cases, including:
    - `from . import a` -> `.`
    - `from ..sub import b` -> `..sub`
    """
    return '{}{}'.format(
        '.' * node.level,
        node.module or '',
    )


def get_import_parts(node: AnyImport) -> list[str]:
    """Returns list of import modules."""
    module_path = getattr(node, 'module', '') or ''
    return module_path.split('.')


def is_vague_import(name: str) -> bool:
    """
    Tells whether this import name is vague or not.

    >>> is_vague_import('a')
    True

    >>> is_vague_import('from_model')
    True

    >>> is_vague_import('dumps')
    True

    >>> is_vague_import('regular')
    False

    """
    blacklisted = name in constants.VAGUE_IMPORTS_BLACKLIST
    with_from_or_to = name.startswith(('from_', 'to_'))
    too_short = logical.is_too_short_name(name, 2, trim=True)
    return blacklisted or with_from_or_to or too_short


def is_nested_typing_import(parent: ast.AST) -> bool:
    """Tells whether ``if`` checks for ``TYPE_CHECKING``."""
    checked_condition = None
    if isinstance(parent, ast.If):
        if isinstance(parent.test, ast.Name):
            checked_condition = parent.test.id
        elif isinstance(parent.test, ast.Attribute):
            checked_condition = parent.test.attr
    return checked_condition in constants.ALLOWED_NESTED_IMPORTS_CONDITIONS


def is_import_in_try(node: AnyImport) -> bool:
    """
    Same import names in `try` / `except` block should be ignored.

    Example::

        try:
            from typing import Final
        except ImportError:
            from typing_extensions import Final

    """
    parent = get_parent(node)
    if not isinstance(parent, ast.Try | ast.ExceptHandler):
        return False
    # We don't use `ast.TryStar` here because it is not a common
    # pattern to have imports in `try/except*` blocks.
    is_nested_in_try_star = isinstance(
        parent, ast.ExceptHandler
    ) and isinstance(get_parent(parent), TryStar)
    if is_nested_in_try_star:  # pragma: no cover
        return False
    # We still require imports to be top-level:
    return isinstance(get_context(parent), ast.Module)
