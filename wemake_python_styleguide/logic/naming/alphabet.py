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


def get_unreadable_characters(
    name: str,
    character_combinations: Iterable[str],
) -> str:
    """
    Check if name contains unreadable characters.

    >>> get_unreadable_characters('hello_world', [])
    ''

    >>> get_unreadable_characters('BaseViews', ['O0'])
    ''

    >>> get_unreadable_characters('StillItems', ['lI', '0O'])
    'lI'

    >>> get_unreadable_characters('_', ['O0', '1l'])
    ''

    """
    for combination in character_combinations:
        if combination in name:
            return combination
    return ''
