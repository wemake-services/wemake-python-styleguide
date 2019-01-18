# -*- coding: utf-8 -*-

import keyword

from flake8_builtins import BUILTINS

from wemake_python_styleguide.constants import UNUSED_VARIABLE
from wemake_python_styleguide.logics.naming.access import is_magic

ALL_BUILTINS = frozenset((
    *keyword.kwlist,
    *BUILTINS,

    # Special case.
    # Some python version have them, some do not have them:
    'async',
    'await',
))


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

    if variable_name == UNUSED_VARIABLE or not variable_name.endswith('_'):
        return False

    return variable_name[:-1] not in ALL_BUILTINS
