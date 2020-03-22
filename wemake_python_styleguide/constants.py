"""
This module contains list of white- and black-listed ``python`` members.

We add values here when we want to make them public.
Or when a value is reused in several places.
Then, we automatically have to add it here and document it.

Other constants that are not used across modules
and does not require to be documented can be defined where they are used.

All values here must be documented with ``#:`` comments.
"""

import math
import re

from typing_extensions import Final

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
    'print',
    'pprint',
    'input',
    'breakpoint',

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

    # Mypy:
    'reveal_type',
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
    'param',
    'params',
    'parameters',

    # Confuseables:
    'no',
    'true',
    'false',

    # Names from examples:
    'foo',
    'bar',
    'baz',
))

#: List of characters sequences that are hard to read.
UNREADABLE_CHARACTER_COMBINATIONS: Final = frozenset((
    '1l',
    '1I',
    '0O',
    'O0',
    # Not included: 'lI', 'l1', 'Il'
    # Because these names are quite common in real words.
))

#: List of special names that are used only as first argument in methods.
SPECIAL_ARGUMENT_NAMES_WHITELIST: Final = frozenset((
    'self',
    'cls',
    'mcs',
))

#: List of all magic methods from the python docs.
ALL_MAGIC_METHODS: Final = frozenset((
    '__new__',
    '__init__',
    '__del__',

    '__repr__',
    '__str__',
    '__bytes__',
    '__format__',

    '__lt__',
    '__le__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',

    '__hash__',
    '__bool__',

    '__getattr__',
    '__getattribute__',
    '__setattr__',
    '__delattr__',
    '__dir__',

    '__get__',
    '__set__',
    '__delete__',
    '__set_name__',

    '__init_subclass__',
    '__instancecheck__',
    '__subclasscheck__',
    '__class_getitem__',

    '__call__',
    '__len__',
    '__length_hint__',
    '__getitem__',
    '__setitem__',
    '__delitem__',
    '__missing__',
    '__iter__',
    '__reversed__',
    '__contains__',

    '__add__',
    '__sub__',
    '__mul__',
    '__matmul__',
    '__truediv__',
    '__floordiv__',
    '__mod__',
    '__divmod__',
    '__pow__',
    '__lshift__',
    '__rshift__',
    '__and__',
    '__xor__',
    '__or__',
    '__radd__',
    '__rsub__',
    '__rmul__',
    '__rmatmul__',
    '__rtruediv__',
    '__rfloordiv__',
    '__rmod__',
    '__rdivmod__',
    '__rpow__',
    '__rlshift__',
    '__rrshift__',
    '__rand__',
    '__rxor__',
    '__ror__',
    '__iadd__',
    '__isub__',
    '__imul__',
    '__imatmul__',
    '__itruediv__',
    '__ifloordiv__',
    '__imod__',
    '__ipow__',
    '__ilshift__',
    '__irshift__',
    '__iand__',
    '__ixor__',
    '__ior__',
    '__neg__',
    '__pos__',
    '__abs__',
    '__invert__',
    '__complex__',
    '__int__',
    '__float__',
    '__index__',
    '__round__',
    '__trunc__',
    '__floor__',
    '__ceil__',

    '__enter__',
    '__exit__',

    '__await__',
    '__aiter__',
    '__anext__',
    '__aenter__',
    '__aexit__',
))

#: List of magic methods that are forbidden to use.
MAGIC_METHODS_BLACKLIST: Final = frozenset((
    # Since we don't use `del`:
    '__del__',
    '__delitem__',
    '__delete__',

    # Since we don't use `pickle`:
    '__reduce__',
    '__reduce_ex__',

    '__dir__',  # since we don't use `dir()`
    '__delattr__',  # since we don't use `delattr()`
))

#: List of magic methods that are not allowed to be generators.
YIELD_MAGIC_METHODS_BLACKLIST: Final = ALL_MAGIC_METHODS.difference({
    # Allowed to be used with ``yield`` keyowrd:
    '__iter__',
})

#: List of magic methods that are not allowed to be async.
ASYNC_MAGIC_METHODS_BLACKLIST: Final = ALL_MAGIC_METHODS.difference({
    # In order of appearance on
    # https://docs.python.org/3/reference/datamodel.html#basic-customization
    # Allowed magic methods are:
    '__anext__',
    '__aenter__',
    '__aexit__',
})

#: List of builtin classes that are allowed to subclass.
ALLOWED_BUILTIN_CLASSES: Final = frozenset((
    'type',
    'object',
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

#: List of bad magic module functions.
MAGIC_MODULE_NAMES_BLACKLIST: Final = frozenset((
    '__getattr__',
    '__dir__',
))

#: Regex pattern to name modules.
MODULE_NAME_PATTERN: Final = re.compile(r'^_?_?[a-z][a-z\d_]*[a-z\d](__)?$')

#: Common numbers that are allowed to be used without being called "magic".
MAGIC_NUMBERS_WHITELIST: Final = frozenset((
    0,  # both int and float
    0.1,
    0.5,
    1.0,
    100,
    1000,
    1024,  # bytes
    24,  # hours
    60,  # seconds, minutes

    1j,  # imaginary part of a complex number
))

#: Maximum amount of ``pragma`` no-cover comments per module.
MAX_NO_COVER_COMMENTS: Final = 5

#: Maximum length of ``yield`` ``tuple`` expressions.
MAX_LEN_YIELD_TUPLE: Final = 5

#: Maximum number of compare nodes in a single expression.
MAX_COMPARES: Final = 2

#: Maximum number of conditions in a single ``if`` or ``while`` statement.
MAX_CONDITIONS: Final = 4

#: Maximum number of `elif` blocks in a single `if` condition:
MAX_ELIFS: Final = 3

#: Maximum number of ``except`` cases in a single ``try`` clause.
MAX_EXCEPT_CASES: Final = 3

#: Approximate constants which real values should be imported from math module.
MATH_APPROXIMATE_CONSTANTS: Final = frozenset((
    math.pi,
    math.e,
    math.tau,
))

#: List of vague method names that may cause confusion if imported as is:
VAGUE_IMPORTS_BLACKLIST = frozenset((
    'read',
    'write',
    'load',
    'loads',
    'dump',
    'dumps',
    'parse',
    'safe_load',
    'safe_dump',
    'load_all',
    'dump_all',
    'safe_load_all',
    'safe_dump_all',
))

#: List of literals without arguments we forbid to use.
LITERALS_BLACKLIST: Final = frozenset((
    'int',
    'float',
    'str',
    'bytes',
    'bool',
    'complex',
))

#: List of functions in which arguments must be tuples.
TUPLE_ARGUMENTS_METHODS: Final = frozenset((
    'frozenset',
))


# Internal variables
# ==================

# Please, do not touch values beyond this line!
# ---------------------------------------------

# They are not publicly documented since they are not used by the end user.
# But, we still need them to be defined here.

# Used as a default filename, when it is not passed by flake8:
STDIN: Final = 'stdin'

# Used to specify as a placeholder for `__init__`:
INIT: Final = '__init__'

# Used to determine when we are running on Windows:
WINDOWS_OS: Final = 'nt'

# Used as a placeholder for special `_` variable:
UNUSED_PLACEHOLDER: Final = '_'
