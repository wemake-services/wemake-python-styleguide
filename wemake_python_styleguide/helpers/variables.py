# -*- coding: utf-8 -*-

from typing import Iterable, Optional


def is_wrong_variable_name(name: str, to_check: Iterable[str]) -> bool:
    """
    Checks that variable is not prohibited by explicitly listing it's name.

    >>> is_wrong_variable_name('wrong', ['wrong'])
    True

    >>> is_wrong_variable_name('correct', ['wrong'])
    False

    """
    return name in to_check


def is_too_short_variable_name(
    name: Optional[str],
    min_length: int = 2,  # TODO: config
) -> bool:
    """
    Checks for too short variable names.

    >>> is_too_short_variable_name('test')
    False

    >>> is_too_short_variable_name(None)
    False

    >>> is_too_short_variable_name('o')
    True

    >>> is_too_short_variable_name('_')
    False

    >>> is_too_short_variable_name('z1')
    False

    >>> is_too_short_variable_name('z', min_length=1)
    False

    """
    return name is not None and name != '_' and len(name) < min_length
