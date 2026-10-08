'''
This module contains list of white- and black-listed ``python`` members.

We add values here when we want to make them public.
Or when a value is reused in several places.
Then, we automatically have to add it here and document it.

Other constants that are not used across modules
and does not require to be documented can be defined where they are used.

All values here must be documented with ``"""Docs."""`` style.

See also:
    https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#doc-comments-and-docstrings
'''

import math
import re
from typing import Final

# Internal variables
# ==================

# Please, do not touch values beyond this line!
# ---------------------------------------------

# They are not publicly documented since they are not used by the end user.
# But, we still need them to be defined here.

STDIN: Final = 'stdin'
"""Used as a default filename, when it is not passed by flake8."""

INIT: Final = '__init__'
"""Used to specify as a placeholder for `__init__`."""

WINDOWS_OS: Final = 'nt'
"""Used to determine when we are running on Windows."""

UNUSED_PLACEHOLDER: Final = '_'
"""Used as a placeholder for special `_` variable."""

# Public variables
# ================

# Values beyond this line are public and should be used.
# ------------------------------------------------------

SHORTLINK_TEMPLATE: Final = 'https://pyflak.es/{0}'
"""This url points to the specific violation page."""

FUNCTIONS_BLACKLIST: Final = frozenset(
    (
        # Code generation:
        'compile',
        'eval',
        'exec',
        # Termination:
        'exit',
        'quit',
        # Magic:
        'dir',
        'globals',
        'locals',
        'vars',
        # IO:
        'breakpoint',
        'input',
        'pprint',
        'pprint.pprint',
        'print',
        # Attribute access:
        'delattr',
        # Gratis:
        'copyright',
        'credits',
        'help',
        # Dynamic imports:
        '__import__',
        # OOP:
        'staticmethod',
        # Mypy:
        'reveal_locals',
        'reveal_type',
    ),
)
"""List of functions we forbid to use."""

MODULE_METADATA_VARIABLES_BLACKLIST: Final = frozenset(
    (
        '__about__',
        '__all__',
        '__author__',
        '__copyright__',
        '__version__',
    ),
)
"""List of module metadata we forbid to use."""

VARIABLE_NAMES_BLACKLIST: Final = frozenset(
    (
        # Meaningless words:
        'arr',
        'content',
        'contents',
        'data',
        'do',
        'file',
        'handle',
        'handler',
        'info',
        'item',
        'items',
        'obj',
        'objects',
        'objs',
        'param',
        'parameters',
        'params',
        'result',
        'results',
        'some',
        'val',
        'vals',
        'value',
        'values',
        'var',
        'variable',
        'vars',
        # Confusables:
        'false',
        'no',
        'true',
        'yes',
        # Names from examples:
        'bar',
        'baz',
        'foo',
        'ham',
        'spam',
        'temp',
        'tmp',
    ),
)
"""List of variable names we forbid to use."""

UNREADABLE_CHARACTER_COMBINATIONS: Final = frozenset(
    (
        '0O',
        '1I',
        '1l',
        'O0',
        # Not included: 'lI', 'l1', 'Il'
        # Because these names are quite common in real words.
    ),
)
"""List of character sequences that are hard to read."""

SPECIAL_ARGUMENT_NAMES_WHITELIST: Final = frozenset(
    (
        'self',
        'cls',
        'mcs',
    ),
)
"""List of special names that are used only as first argument in methods."""

ALL_MAGIC_METHODS: Final = frozenset(
    (
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
        '__mro_entries__',
        '__class_getitem__',
        '__call__',
        '__len__',
        '__length_hint__',
        '__getitem__',
        '__setitem__',
        '__delitem__',
        '__missing__',
        '__iter__',
        '__next__',
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
        '__oct__',
        '__hex__',
        '__enter__',
        '__exit__',
        '__await__',
        '__aiter__',
        '__anext__',
        '__aenter__',
        '__aexit__',
        # pickling
        '__getinitargs__',
        '__getnewargs__',
        '__getnewargs_ex__',
        '__getstate__',
        '__reduce__',
        '__reduce_ex__',
        '__setstate__',
        # Python 2
        '__cmp__',
        '__coerce__',
        '__long__',
        '__nonzero__',
        '__unicode__',
        # copy
        '__copy__',
        '__deepcopy__',
        '__replace__',
        # typing
        '__annotate__',
        # dataclasses
        '__post_init__',
        # attrs:
        '__attrs_init__',
        '__attrs_post_init__',
        '__attrs_pre_init__',
        # inspect
        '__signature__',
        # os.path
        '__fspath__',
        # sys
        '__sizeof__',
    ),
)
"""List of all magic methods from the python docs."""

MAGIC_METHODS_BLACKLIST: Final = frozenset(
    (
        # Since we don't use `del`:
        '__del__',
        '__delete__',
        '__delitem__',
        # Since we don't use `pickle`:
        '__reduce__',
        '__reduce_ex__',
        '__delattr__',  # since we don't use `delattr()`
        '__dir__',  # since we don't use `dir()`
    ),
)
"""List of magic methods that are forbidden to use."""

YIELD_MAGIC_METHODS_BLACKLIST: Final = ALL_MAGIC_METHODS.difference(
    {
        # Allowed to be used with ``yield`` keyword:
        '__aiter__',
        '__call__',
        '__iter__',
    },
)
"""List of magic methods that are not allowed to be generators."""

ASYNC_MAGIC_METHODS_BLACKLIST: Final = ALL_MAGIC_METHODS.difference(
    {
        # See https://docs.python.org/3/reference/datamodel.html#coroutines
        # Allowed async magic methods are:
        '__aenter__',
        '__aexit__',
        '__aiter__',
        '__anext__',
        '__call__',
    },
)
"""List of magic methods that are not allowed to be async."""

ALLOWED_BUILTIN_CLASSES: Final = frozenset(
    (
        'object',
        'type',
    ),
)
"""List of builtin classes that are allowed to subclass."""

NESTED_FUNCTIONS_WHITELIST: Final = frozenset(
    (
        'decorator',
        'factory',
        'wrapper',
    ),
)
"""List of nested functions' names we allow to use."""

FUTURE_IMPORTS_WHITELIST: Final = frozenset(
    (
        'annotations',
        'generator_stop',
    ),
)
"""List of allowed ``__future__`` imports."""

MODULE_NAMES_BLACKLIST: Final = frozenset(
    (
        'helpers',
        'util',
        'utilities',
        'utils',
    ),
)
"""List of blacklisted module names."""

MAGIC_MODULE_NAMES_WHITELIST: Final = frozenset(
    (
        '__init__',
        '__main__',
    ),
)
"""List of allowed module magic names."""

MAGIC_MODULE_NAMES_BLACKLIST: Final = frozenset(
    (
        '__dir__',
        '__getattr__',
    ),
)
"""List of bad magic module functions."""

MODULE_NAME_PATTERN: Final = re.compile(r'^_?_?[a-z][a-z\d_]*[a-z\d](__)?$')
"""Regex pattern to name modules."""

MAGIC_NUMBERS_WHITELIST: Final = frozenset(
    (
        0,  # both int and float
        0.1,
        0.5,
        1.0,
        24,  # hours
        60,  # seconds, minutes
        100,
        1000,
        1024,  # bytes
        1j,  # imaginary part of a complex number
    ),
)
"""Common numbers that are allowed to be used without being called "magic"."""

MAX_NO_COVER_COMMENTS: Final = 5
"""Maximum amount of ``pragma`` no-cover comments per module."""

MAX_LEN_TUPLE_OUTPUT: Final = 5
"""Maximum length of ``yield`` or ``return`` ``tuple`` expressions."""

MAX_COMPARES: Final = 2
"""Maximum number of compare nodes in a single expression."""

MAX_ELIFS: Final = 3
"""Maximum number of `elif` blocks in a single `if` condition."""

MAX_EXCEPT_CASES: Final = 3
"""Maximum number of ``except`` cases in a single ``try`` clause."""

MATH_APPROXIMATE_CONSTANTS: Final = frozenset(
    (
        math.e,
        math.pi,
        math.tau,
    ),
)
"""Approximate constants which real values
should be imported from math module."""

VAGUE_IMPORTS_BLACKLIST: Final = frozenset(
    (
        'dump',
        'dump_all',
        'dumps',
        'load',
        'load_all',
        'loads',
        'parse',
        'read',
        'safe_dump',
        'safe_dump_all',
        'safe_load',
        'safe_load_all',
        'write',
    ),
)
"""List of vague method names that may cause confusion if imported as is."""

TUPLE_ARGUMENTS_METHODS: Final = frozenset(('frozenset',))
"""List of functions in which arguments must be tuples."""

ALIAS_NAMES_WHITELIST: Final = frozenset(
    (
        'cv',
        'df',
        'np',
        'pd',
        'plt',
        'sns',
        'tf',
    ),
)
"""List of commonly used aliases."""
