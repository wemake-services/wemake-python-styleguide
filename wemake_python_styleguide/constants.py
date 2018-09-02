# -*- coding: utf-8 -*-

"""
This module contains list of white- and black-listed ``python`` members.

It contains lists of keywords and built-in functions we discourage to use.
It also contains some exceptions that we allow to use in our codebase.
"""

import sys
from typing import Tuple

#: List of functions we forbid to use.
BAD_FUNCTIONS = frozenset((
    # Code generation:
    'eval',
    'exec',
    'compile',

    # Magic:
    'globals',
    'locals',
    'vars',
    'dir',

    # IO:
    'input',

    # Attribute access:
    'hasattr',
    'delattr',

    # Misc:
    'copyright',
    'help',

    # Dynamic imports:
    '__import__',

    # OOP:
    'staticmethod',
))

#: List of module metadata we forbid to use.
BAD_MODULE_METADATA_VARIABLES = frozenset((
    '__author__',
    '__all__',
    '__version__',
    '__about__',
))


_BAD_VARIABLE_NAMES: Tuple[str, ...] = (
    'data',
    'result',
    'results',
    'item',
    'items',
    'value',
    'values',
    'val',
    'vals',
    'var',
    'vars',
    'content',
    'contents',
    'info',
    'handle',
    'handler',
    'file',
    'klass',
)

if sys.version_info < (3, 7):  # pragma: no cover
    _BAD_VARIABLE_NAMES += (
        # Compatibility with `python3.7`:
        'async',
        'await',
    )

#: List of variable names we forbid to use.
BAD_VARIABLE_NAMES = frozenset(_BAD_VARIABLE_NAMES)

#: List of magic methods that are forbiden to use.
BAD_MAGIC_METHODS = frozenset((
    '__del__',  # since we don't use `del`
    '__delitem__',  # since we don't use `del`
    '__delete__',  # since we don't use `del`

    '__dir__',  # since we don't use `dir()`
    '__delattr__',  # since we don't use `delattr()`
))

#: List of nested classes' names we allow to use.
NESTED_CLASSES_WHITELIST = frozenset((
    'Meta',
))

#: List of nested functions' names we allow to use.
NESTED_FUNCTIONS_WHITELIST = frozenset((
    'decorator',
    'factory',
))

#: List of allowed ``__future__`` imports.
FUTURE_IMPORTS_WHITELIST = frozenset((
    'annotations',
    'generator_stop',
))
