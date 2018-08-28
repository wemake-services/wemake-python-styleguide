# -*- coding: utf-8 -*-


def has_just_exceeded_limit(current_value: int, limit: int) -> bool:
    """
    Check either value has just exceeded its limit or not.

    >>> has_just_exceeded_limit(1, 2)
    False

    >>> has_just_exceeded_limit(1, 1)
    False

    >>> has_just_exceeded_limit(2, 1)
    True

    >>> has_just_exceeded_limit(3, 1)
    False

    """
    return current_value == limit + 1
