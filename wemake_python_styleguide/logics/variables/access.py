# -*- coding: utf-8 -*-


def is_private_variable(name: str) -> bool:
    """
    Checks if variable has private name pattern.

    >>> is_private_variable('regular')
    False

    >>> is_private_variable('__private')
    True

    >>> is_private_variable('_protected')
    False

    >>> is_private_variable('__magic__')
    False

    """
    return name.startswith('__') and not name.endswith('__')


def is_protected_variable(name: str) -> bool:
    """
    Checks if variable has protected name pattern.

    >>> is_protected_variable('_protected')
    True

    >>> is_protected_variable('__private')
    False

    >>> is_protected_variable('__magic__')
    False

    >>> is_protected_variable('common_variable')
    False
    """
    return name.startswith('_') and not name.startswith('__')
