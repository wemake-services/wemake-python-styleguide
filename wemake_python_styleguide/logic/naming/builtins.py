import builtins
import inspect
import keyword

from typing_extensions import Final

from wemake_python_styleguide.constants import UNUSED_PLACEHOLDER
from wemake_python_styleguide.logic.naming.access import is_magic, is_unused

_BUILTINS_WHITELIST: Final = frozenset((
    UNUSED_PLACEHOLDER,
))

_BUILTINS: Final = frozenset((
    builtin[0]
    for builtin in inspect.getmembers(builtins)
    if builtin[0] not in _BUILTINS_WHITELIST
))

_ALL_BUILTINS: Final = frozenset((
    *keyword.kwlist,
    *_BUILTINS,

    # Special case.
    # Some python version have them, some do not have them:
    'async',
    'await',
))


def is_builtin_name(variable_name: str) -> bool:
    """
    Tells whether a variable name is builtin or not.

    >>> is_builtin_name('str')
    True

    >>> is_builtin_name('_')
    False

    >>> is_builtin_name('custom')
    False

    >>> is_builtin_name('Exception')
    True

    >>> is_builtin_name('async')
    True

    """
    return variable_name in _ALL_BUILTINS


def is_wrong_alias(variable_name: str) -> bool:
    """
    Tells whether a variable is wrong builtins alias or not.

    >>> is_wrong_alias('regular_name_')
    True

    >>> is_wrong_alias('_')
    False

    >>> is_wrong_alias('_async')
    False

    >>> is_wrong_alias('_await')
    False

    >>> is_wrong_alias('regular_name')
    False

    >>> is_wrong_alias('class_')
    False

    >>> is_wrong_alias('list_')
    False

    >>> is_wrong_alias('list')
    False

    >>> is_wrong_alias('__spec__')
    False

    """
    if is_magic(variable_name):
        return False

    if is_unused(variable_name) or not variable_name.endswith('_'):
        return False

    return not is_builtin_name(variable_name[:-1])
