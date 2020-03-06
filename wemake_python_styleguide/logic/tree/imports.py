from typing import List

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.naming import logical
from wemake_python_styleguide.types import AnyImport


def get_import_parts(node: AnyImport) -> List[str]:
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
    with_from_or_to = (
        name.startswith('from_') or
        name.startswith('to_')
    )
    too_short = logical.is_too_short_name(name, 2, trim=True)
    return blacklisted or with_from_or_to or too_short
