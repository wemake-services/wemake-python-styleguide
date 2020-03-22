from typing import Iterable

from wemake_python_styleguide.constants import UNUSED_PLACEHOLDER
from wemake_python_styleguide.logic.naming import access


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
        choices_to_check = {
            name_to_check,
            '_{0}'.format(name_to_check),
            '{0}_'.format(name_to_check),
        }
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
    min_length: int,
    *,
    trim: bool = True,
) -> bool:
    """
    Checks for too short names.

    >>> is_too_short_name('test', min_length=2)
    False

    >>> is_too_short_name('o', min_length=2)
    True

    >>> is_too_short_name('_', min_length=2)
    False

    >>> is_too_short_name('_', min_length=1)
    False

    >>> is_too_short_name('z1', min_length=2)
    False

    >>> is_too_short_name('z', min_length=1)
    False

    >>> is_too_short_name('_z', min_length=2, trim=True)
    True

    >>> is_too_short_name('z_', min_length=2, trim=True)
    True

    >>> is_too_short_name('z_', min_length=2, trim=False)
    False

    >>> is_too_short_name('__z', min_length=2, trim=True)
    True

    >>> is_too_short_name('xy', min_length=2, trim=True)
    False

    """
    if access.is_unused(name):
        return False

    if trim:
        name = name.strip(UNUSED_PLACEHOLDER)

    return len(name) < min_length


def is_too_long_name(
    name: str,
    max_length: int,
) -> bool:
    """
    Checks for too long names.

    >>> is_too_long_name('test', max_length=4)
    False

    >>> is_too_long_name('_', max_length=4)
    False

    >>> is_too_long_name('test', max_length=3)
    True

    >>> is_too_long_name('this_is_twentynine_characters', max_length=29)
    False

    """
    return len(name) > max_length
