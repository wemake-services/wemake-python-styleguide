# -*- coding: utf-8 -*-

from wemake_python_styleguide.constants import UNUSED_VARIABLE


def is_magic(name: str) -> bool:
    """
    Checks whether the given ``name`` is magic.

    >>> is_magic('__init__')
    True

    >>> is_magic('some')
    False

    >>> is_magic('cli')
    False

    >>> is_magic('_')
    False

    >>> is_magic('__version__')
    True

    >>> is_magic('__main__')
    True

    """
    return name.startswith('__') and name.endswith('__')


def is_private(name: str) -> bool:
    """
    Checks if name has private name pattern.

    >>> is_private('regular')
    False

    >>> is_private('__private')
    True

    >>> is_private('_protected')
    False

    >>> is_private('__magic__')
    False

    >>> is_private('_')
    False

    """
    return name.startswith('__') and not is_magic(name)


def is_protected(name: str) -> bool:
    """
    Checks if name has protected name pattern.

    >>> is_protected('_protected')
    True

    >>> is_protected('__private')
    False

    >>> is_protected('__magic__')
    False

    >>> is_protected('common_variable')
    False

    >>> is_protected('_')
    False

    """
    if not name.startswith('_'):
        return False

    if name == UNUSED_VARIABLE:
        return False

    return not is_private(name) and not is_magic(name)
