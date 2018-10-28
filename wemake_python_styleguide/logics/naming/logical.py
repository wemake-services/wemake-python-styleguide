# -*- coding: utf-8 -*-

from typing import Iterable

from wemake_python_styleguide import constants
from wemake_python_styleguide.options import defaults


def is_wrong_name(name: str, to_check: Iterable[str]) -> bool:
    """
    Checks that name is not prohibited by explicitly listing it's name.

    >>> is_wrong_name('wrong', ['wrong'])
    True

    >>> is_wrong_name('correct', ['wrong'])
    False

    >>> is_wrong_name('_wrong', ['wrong'])
    True

    >>> is_wrong_name('wrong_', ['wrong'])
    True

    >>> is_wrong_name('wrong__', ['wrong'])
    False

    >>> is_wrong_name('__wrong', ['wrong'])
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


def is_upper_case_name(name: str) -> bool:
    """
    Checks that attribute name has no upper-case letters.

    >>> is_upper_case_name('camelCase')
    True

    >>> is_upper_case_name('UPPER_CASE')
    True

    >>> is_upper_case_name('camel_Case')
    True

    >>> is_upper_case_name('snake_case')
    False

    >>> is_upper_case_name('snake')
    False

    >>> is_upper_case_name('snake111')
    False

    >>> is_upper_case_name('__variable_v2')
    False

    """
    return any(character.isupper() for character in name)


def is_too_short_name(
    name: str,
    min_length: int = defaults.MIN_NAME_LENGTH,
) -> bool:
    """
    Checks for too short variable names.

    >>> is_too_short_name('test')
    False

    >>> is_too_short_name('o')
    True

    >>> is_too_short_name('_')
    False

    >>> is_too_short_name('z1')
    False

    >>> is_too_short_name('z', min_length=1)
    False

    """
    return name != constants.UNUSED_VARIABLE and len(name) < min_length


def does_contain_underscored_number(name: str) -> bool:
    """
    Checks for variable names with underscored number.

    >>> does_contain_underscored_number('star_wars_episode2')
    False

    >>> does_contain_underscored_number('come2_me')
    False

    >>> does_contain_underscored_number('_')
    False

    >>> does_contain_underscored_number('z1')
    False

    >>> does_contain_underscored_number('star_wars_episode_2')
    True

    >>> does_contain_underscored_number('come_2_me')
    True

    >>> does_contain_underscored_number('iso_123_456')
    False

    >>> does_contain_underscored_number('iso123_456')
    False

    """
    pattern = constants.UNDERSCORED_NUMBER_PATTERN
    return pattern.match(name) is not None


def does_contain_consecutive_underscores(name: str) -> bool:
    """
    Checks if variable contains consecutive underscores in middle of name.

    >>> does_contain_consecutive_underscores('name')
    False

    >>> does_contain_consecutive_underscores('__magic__')
    False

    >>> does_contain_consecutive_underscores('__private')
    False

    >>> does_contain_consecutive_underscores('name')
    False

    >>> does_contain_consecutive_underscores('some__value')
    True

    >>> does_contain_consecutive_underscores('some_value__')
    True

    """
    if name.startswith('__'):
        return False

    if '__' in name:
        return True

    return False
