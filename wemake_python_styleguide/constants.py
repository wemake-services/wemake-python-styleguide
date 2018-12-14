# -*- coding: utf-8 -*-

"""
This module contains list of white- and black-listed ``python`` members.

It contains lists of keywords and built-in functions we discourage to use.
It also contains some exceptions that we allow to use in our codebase.
"""

import re

from wemake_python_styleguide.types import Final

#: List of functions we forbid to use.
FUNCTIONS_BLACKLIST: Final = frozenset((
    # Code generation:
    'eval',
    'exec',
    'compile',

    # Termination:
    'exit',
    'quit',

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

    # Gratis:
    'copyright',
    'help',
    'credits',

    # Dynamic imports:
    '__import__',

    # OOP:
    'staticmethod',
))

#: List of module metadata we forbid to use.
MODULE_METADATA_VARIABLES_BLACKLIST: Final = frozenset((
    '__author__',
    '__all__',
    '__version__',
    '__about__',
))

#: List of variable names we forbid to use.
VARIABLE_NAMES_BLACKLIST: Final = frozenset((
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
    'variable',
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
    'do',

    # Confuseables:
    'no',
    'true',
    'false',

    # Names from examples:
    'foo',
    'bar',
    'baz',
))

#: List of special names that are used only as first argument in methods.
SPECIAL_ARGUMENT_NAMES_WHITELIST: Final = frozenset((
    'self',
    'cls',
    'mcs',
))

#: List of magic methods that are forbidden to use.
MAGIC_METHODS_BLACKLIST: Final = frozenset((
    # Since we don't use `del`:
    '__del__',
    '__delitem__',
    '__delete__',

    '__dir__',  # since we don't use `dir()`
    '__delattr__',  # since we don't use `delattr()`
))

#: List of nested classes' names we allow to use.
NESTED_CLASSES_WHITELIST: Final = frozenset((
    'Meta',  # django forms, models, drf, etc
    'Params',  # factoryboy specific
))

#: List of nested functions' names we allow to use.
NESTED_FUNCTIONS_WHITELIST: Final = frozenset((
    'decorator',
    'factory',
))

#: List of allowed ``__future__`` imports.
FUTURE_IMPORTS_WHITELIST: Final = frozenset((
    'annotations',
    'generator_stop',
))

#: List of blacklisted module names.
MODULE_NAMES_BLACKLIST: Final = frozenset((
    'util',
    'utils',
    'utilities',
    'helpers',
))

#: List of allowed module magic names.
MAGIC_MODULE_NAMES_WHITELIST: Final = frozenset((
    '__init__',
    '__main__',
))

#: Regex pattern to name modules.
MODULE_NAME_PATTERN: Final = re.compile(r'^_?_?[a-z][a-z\d_]+[a-z\d](__)?$')

#: Common numbers that are allowed to be used without being called "magic".
MAGIC_NUMBERS_WHITELIST: Final = frozenset((
    0.5,
    100,
    1000,
    1024,  # bytes
    24,  # hours
    60,  # seconds, minutes
))


# Internal variables
# They are not publicly documented since they are not used by the end user.

# Used as a default filename, when it is not passed by flake8:
STDIN: Final = 'stdin'

# Used as a special name for unused variables:
UNUSED_VARIABLE: Final = '_'

# Used to specify as a placeholder for `__init__`:
INIT: Final = '__init__'

# Allowed magic number modulo:
NON_MAGIC_MODULO: Final = 10

# Used to specify a pattern which checks variables and modules for underscored
# numbers in their names:
UNDERSCORED_NUMBER_PATTERN: Final = re.compile(r'.+\D\_\d+(\D|$)')
