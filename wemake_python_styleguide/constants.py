# -*- coding: utf-8 -*-

"""
This module contains list of white- and black-listed ``python`` members.

It contains lists of keywords and built-in functions we discourage to use.
It also contains some exceptions that we allow to use in our codebase.
"""

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
    'help',

    # Attribute access:
    'hasattr',
    'delattr',

    # Misc:
    'copyright',
))

#: List of module metadata we forbid to use.
BAD_MODULE_METADATA_VARIABLES = frozenset((
    '__author__',
    '__all__',
    '__version__',
    '__about__',
))

#: List of variable names we forbid to use.
BAD_VARIABLE_NAMES = frozenset((
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
