# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from wemake_python_styleguide.options.defaults import MIN_VARIABLE_LENGTH


def is_wrong_variable_name(name: str, to_check: Iterable[str]) -> bool:
    """
    Checks that variable is not prohibited by explicitly listing it's name.

    >>> is_wrong_variable_name('wrong', ['wrong'])
    True
    >>> is_wrong_variable_name('correct', ['wrong'])
    False
    >>> is_wrong_variable_name('_wrong', ['wrong'])
    True
    >>> is_wrong_variable_name('wrong_', ['wrong'])
    True
    >>> is_wrong_variable_name('wrong__', ['wrong'])
    False
    >>> is_wrong_variable_name('__wrong', ['wrong'])
    False

    """
    for name_to_check in to_check:
        choices_to_check = [
            name_to_check,
            '_{0}'.format(name_to_check),
            '{0}_'.format(name_to_check),
        ]
        if name in choices_to_check:
            return True
    return False


def is_too_short_variable_name(
    name: Optional[str],
    min_length: int = MIN_VARIABLE_LENGTH,
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


def is_private_variable(name: Optional[str]) -> bool:
    """
    Checks if variable has private name pattern.

    >>> is_private_variable(None)
    False
    >>> is_private_variable('regular')
    False
    >>> is_private_variable('__private')
    True
    >>> is_private_variable('_protected')
    False
    >>> is_private_variable('__magic__')
    False

    """
    return (
        name is not None and name.startswith('__') and not name.endswith('__')
    )
