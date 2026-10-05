"""
Constants with default values for plugin's configuration.

We try to stick to "the magical 7 ± 2 number".
https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two

What does it mean? It means that we choose these values based on our mind
capacity. And it is really hard to keep in mind more that 9 objects
at the same time.

These values can be changed in the ``setup.cfg`` file on a per-project bases,
if you find them too strict or too permissive.
"""

from typing import Final

# ========
# General:
# ========

MIN_NAME_LENGTH: Final = 2  # reasonable enough
"""Minimum variable's name length."""

MAX_NAME_LENGTH: Final = 45  # reasonable enough
"""Maximum variable and module name length:"""

MAX_NOQA_COMMENTS: Final = 10  # guessed
"""Maximum amount of ``noqa`` comments per module."""

NESTED_CLASSES_WHITELIST: Final = (
    'Meta',  # django forms, models, drf, etc
    'Params',  # factoryboy specific
    'Config',  # pydantic specific
)
"""List of nested classes' names we allow to use."""

KNOWN_ENUM_BASES: Final = ()
"""List of additional enum-like base class names."""

ALLOWED_DOMAIN_NAMES: Final = ()
"""Domain names that are removed from variable names' blacklist."""

FORBIDDEN_DOMAIN_NAMES: Final = ()
"""Domain names that extends variable names' blacklist."""

FORBIDDEN_INLINE_IGNORE: Final = ()
"""Violation codes that are forbidden to use."""

EXPS_FOR_ONE_EMPTY_LINE: Final = 2
"""Count of available expressions for one empty line
in function or method body."""

ALLOWED_MODULE_METADATA: Final = ()
"""List of module metadata we allow to use."""

FORBIDDEN_MODULE_METADATA: Final = ()
"""List of module metadata we forbid to use."""

# ===========
# Complexity:
# ===========

MAX_LINES_IN_FINALLY: Final = 2  # best practice
"""Maximum amount of `finally` block body length."""

MAX_RETURNS: Final = 5  # 7-2
"""Maximum number of `return` statements allowed in a single function."""

MAX_LOCAL_VARIABLES: Final = 5  # 7-2
"""Maximum number of local variables in a function."""

MAX_EXPRESSIONS: Final = 9  # 7+2
"""Maximum number of expressions in a single function."""

MAX_ARGUMENTS: Final = 5  # 7-2
"""Maximum number of arguments for functions or methods."""

MAX_MODULE_MEMBERS: Final = 7  # 7
"""Maximum number of classes and functions in a single module."""

MAX_METHODS: Final = 7  # the same as module members
"""Maximum number of methods in a single class."""

MAX_LINE_COMPLEXITY: Final = 14  # 7 * 2, also almost guessed
"""Maximum line complexity."""

MAX_JONES_SCORE: Final = 12  # guessed
"""Maximum median module Jones complexity."""

MAX_IMPORTS: Final = 12  # guessed
"""Maximum number of imports in a single module."""

MAX_IMPORTED_NAMES: Final = 50  # guessed
"""Maximum number of imported names in a single module."""

MAX_BASE_CLASSES: Final = 3  # guessed
"""Maximum number of base classes."""

MAX_DECORATORS: Final = 5  # 7-2
"""Maximum number of decorators."""

MAX_STRING_USAGES: Final = 3  # guessed
"""Maximum number of same string usage in code."""

MAX_AWAITS: Final = 5  # the same as returns
"""Maximum number of ``await`` expressions for functions or methods."""

MAX_TRY_BODY_LENGTH: Final = 1  # best practice
"""Maximum amount of ``try`` node body length."""

MAX_MODULE_EXPRESSIONS: Final = 7  # the same as module elements
"""Maximum amount of same expressions per module."""

MAX_FUNCTION_EXPRESSIONS: Final = 4  # guessed
"""Maximum amount of same expressions per function."""

MAX_ASSERTS: Final = 5  # 7-2
"""Maximum number of ``assert`` statements in a function."""

MAX_ACCESS_LEVEL: Final = 4  # guessed
"""Maximum number of access level in an expression."""

MAX_ATTRIBUTES: Final = 6  # guessed
"""Maximum number of public attributes in a single class."""

MAX_RAISES: Final = 3  # guessed
"""Maximum number of raises in a function."""

MAX_EXCEPT_EXCEPTIONS: Final = 3  # guessed
"""Maximum number of exceptions in `except`."""

MAX_COGNITIVE_SCORE: Final = 12  # based on this code statistics
"""Maximum amount of cognitive complexity per function."""

MAX_COGNITIVE_AVERAGE: Final = 8  # based on this code statistics
"""Maximum amount of average cognitive complexity per module."""

MAX_CALL_LEVEL: Final = 3  # reasonable enough
"""Maximum number of call chains."""

MAX_ANN_COMPLEXITY: Final = 3  # reasonable enough
"""Maximum number of nested annotations."""

MAX_IMPORT_FROM_MEMBERS: Final = 8  # guessed
"""Maximum number of names that can be imported from module."""

MAX_TUPLE_UNPACK_LENGTH: Final = 4  # guessed
"""Maximum number of variables in a ``tuple`` unpacking statement."""

MAX_TYPE_PARAMS: Final = 6  # 7-1, guessed
"""Maximum number of PEP695 type parameters."""

MAX_MATCH_SUBJECTS: Final = 7  # 7 +- 0, guessed
"""Maximum number of subjects in a ``match`` statement."""

MAX_MATCH_CASES: Final = 7  # guessed
"""Maximum number of subjects in match statement."""

MAX_CONDITIONS: Final = 4  # reasonable enough
"""Maximum number of conditions in a single ``if`` or ``while`` statement."""

# ==========
# Formatter:
# ==========

SHOW_VIOLATION_LINKS: Final = False
"""Whether to show violation shortlinks in the formatter output."""
