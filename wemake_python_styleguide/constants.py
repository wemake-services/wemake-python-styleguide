# -*- coding: utf-8 -*-

"""
This module contains list of white- and black-listed ``python`` members.

It contains lists of keywords and built-in functions we discourage to use.
It also contains some exceptions that we allow to use in our codebase.
"""

import re

# TODO: use consistent `.` for the `#:` comments
# TODO: use consistent names: `*_BLACKLIST` and `*_WHITELIST`

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
    'credits',

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

#: List of variable names we forbid to use.
BAD_VARIABLE_NAMES = frozenset((
    # Meaningless words:
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
    'obj',
    'objects',
    'objs',
    'some',

    # Confusables:
    'no',
    'true',
    'false',

    # Names from examples:
    'foo',
    'bar',
    'baz',
))

#: List of magic methods that are forbiden to use.
BAD_MAGIC_METHODS = frozenset((
    # Since we don't use `del`:
    '__del__',
    '__delitem__',
    '__delete__',

    '__dir__',  # since we don't use `dir()`
    '__delattr__',  # since we don't use `delattr()`
))

#: List of nested classes' names we allow to use.
NESTED_CLASSES_WHITELIST = frozenset((
    'Meta',  # django forms, models, drf, etc
    'Params',  # factoryboy specific
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

#: List of blacklisted module names:
BAD_MODULE_NAMES = frozenset((
    'util',
    'utils',
    'utilities',
    'helpers',
))

#: List of allowed module magic names:
MAGIC_MODULE_NAMES_WHITELIST = frozenset((
    '__init__',
    '__main__',
))

#: Regex pattern to name modules:
MODULE_NAME_PATTERN = re.compile(r'^_?_?[a-z][a-z\d_]+[a-z\d](__)?$')

#: Common numbers that are allowed to be used without being called "magic":
MAGIC_NUMBERS_WHITELIST = frozenset((
    0.5,
    100,
    1000,
    1024,  # bytes
    24,  # hours
    60,  # seconds, minutes
))


# Internal variables
# They are not publicly documented since they are not used by the end user.

# This variable is used as a default filename, when it is not passed by flake8:
STDIN = 'stdin'

# TODO: rename to `INIT_MODULE`
# This variable is used to specify as a placeholder for `__init__.py`:
INIT = '__init__'
