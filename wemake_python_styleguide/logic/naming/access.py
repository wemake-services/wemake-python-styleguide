import re

from typing_extensions import Final

#: Used as a special name patterns for unused variables, like `_` and `__`.
_UNUSED_VARIABLE_REGEX: Final = re.compile(r'^_+$')


def is_unused(name: str) -> bool:
    """
    Checks whether the given ``name`` is unused.

    >>> is_unused('_')
    True

    >>> is_unused('___')
    True

    >>> is_unused('_protected')
    False

    >>> is_unused('__private')
    False

    """
    return _UNUSED_VARIABLE_REGEX.match(name) is not None


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

    >>> is_protected('__')
    False

    """
    if not name.startswith('_'):
        return False

    if is_unused(name):
        return False

    return not is_private(name) and not is_magic(name)


def is_public(name: str) -> bool:
    """
    Tells if this name is public.

    >>> is_public('public')
    True

    >>> is_public('_')
    False

    >>> is_public('_protected')
    False

    >>> is_public('__private')
    False

    >>> is_public('__magic__')
    False

    """
    return (
        not is_protected(name) and
        not is_private(name) and
        not is_magic(name) and
        not is_unused(name)
    )
