# -*- coding: utf-8 -*-

from wemake_python_styleguide.constants import UNUSED_VARIABLE


def is_constant(name: str) -> bool:
    """
    Checks whether the given ``name`` is a constant.

    >>> is_constant('CONST')
    True

    >>> is_constant('ALLOWED_EMPTY_LINE_TOKEN')
    True

    >>> is_constant('Some')
    False

    >>> is_constant('_')
    False

    >>> is_constant('lower_case')
    False

    """
    if name == UNUSED_VARIABLE:
        return False

    return all(
        # We check that constant names consist of:
        # UPPERCASE LETTERS and `_` char
        character.isupper() or character == '_'
        for character in name
    )
