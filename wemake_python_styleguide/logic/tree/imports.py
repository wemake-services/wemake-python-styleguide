import ast
from typing import NamedTuple, final

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.naming import logical
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
