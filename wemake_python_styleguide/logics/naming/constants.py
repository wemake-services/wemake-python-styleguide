# -*- coding: utf-8 -*-


def is_constant(name: str) -> bool:
    """
    Checks whether the given ``name`` is a constant.

    >>> is_constant('CONST')
    True

    >>> is_constant('Some')
    False

    >>> is_constant('_')
    False

    >>> is_constant('lower_case')
    False

    """
    return all(character.isupper() for character in name)
