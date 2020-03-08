import re
from typing import Iterable

from typing_extensions import Final

from wemake_python_styleguide.logic.naming import access

# Used to specify a pattern which checks variables and modules for underscored
# numbers in their names:
_UNDERSCORED_NUMBER_PATTERN: Final = re.compile(r'.+\D\_\d+(\D|$)')


def does_contain_underscored_number(name: str) -> bool:
    """
    Checks for names with underscored number.

    >>> does_contain_underscored_number('star_wars_episode2')
    False

    >>> does_contain_underscored_number('come2_me')
    False

    >>> does_contain_underscored_number('_')
    False

    >>> does_contain_underscored_number('z1')
    False

    >>> does_contain_underscored_number('iso123_456')
    False

    >>> does_contain_underscored_number('star_wars_episode_2')
    True

    >>> does_contain_underscored_number('come_2_me')
    True

    >>> does_contain_underscored_number('come_44_me')
    True

    >>> does_contain_underscored_number('iso_123_456')
    True

    """
    return _UNDERSCORED_NUMBER_PATTERN.match(name) is not None


def does_contain_consecutive_underscores(name: str) -> bool:
    """
    Checks if name contains consecutive underscores in middle of name.

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

    >>> does_contain_consecutive_underscores('__some__value__')
    True

    >>> does_contain_consecutive_underscores('__private__value')
    True

    >>> does_contain_consecutive_underscores('some_value__')
    True

    """
    if access.is_magic(name) or access.is_private(name):
        return '__' in name.strip('_')
    return '__' in name


def does_contain_unicode(name: str) -> bool:
    """
    Check if name contains unicode characters.

    >>> does_contain_unicode('hello_world1')
    False

    >>> does_contain_unicode('')
    False

    >>> does_contain_unicode('привет_мир1')
    True

    >>> does_contain_unicode('russian_техт')
    True

    """
    try:
        name.encode('ascii')
    except UnicodeEncodeError:
        return True
    else:
        return False


def does_contain_unreadable_characters(
    name: str,
    character_combinations: Iterable[str],
) -> bool:
    """
    Check if name contains unreadable characters.

    >>> does_contain_unreadable_characters('hello_world', [])
    False

    >>> does_contain_unreadable_characters('BaseViews', [])
    False

    >>> does_contain_unreadable_characters('StillItems', ['lI'])
    True

    >>> does_contain_unreadable_characters('Ilustration', ['Il'])
    True

    >>> does_contain_unreadable_characters('Be1lead', ['1l'])
    True

    >>> does_contain_unreadable_characters('Still1Name', ['l1'])
    True

    >>> does_contain_unreadable_characters('Base1Item', ['1I'])
    True

    >>> does_contain_unreadable_characters('Jusr1item', ['1i'])
    True

    >>> does_contain_unreadable_characters('0Operations', ['0O'])
    True

    >>> does_contain_unreadable_characters('O0', ['O0'])
    True

    """
    for unreadable_combination in character_combinations:

        if unreadable_combination in name:
            return True

    return False
