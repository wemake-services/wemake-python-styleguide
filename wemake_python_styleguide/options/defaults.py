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

from typing_extensions import Final

# ========
# General:
# ========

#: Minimum variable's name length.
MIN_NAME_LENGTH: Final = 2  # reasonable enough

#: Maximum variable and module name length:
MAX_NAME_LENGTH: Final = 45  # reasonable enough

#: Whether you control ones who use your code.
I_CONTROL_CODE: Final = True

#: Maximum amount of ``noqa`` comments per module.
MAX_NOQA_COMMENTS: Final = 10  # guessed

#: List of nested classes' names we allow to use.
NESTED_CLASSES_WHITELIST: Final = (
    'Meta',  # django forms, models, drf, etc
    'Params',  # factoryboy specific
)

#: Domain names that are removed from variable names' blacklist.
ALLOWED_DOMAIN_NAMES: Final = ()

#: Domain names that extends variable names' blacklist.
FORBIDDEN_DOMAIN_NAMES: Final = ()


# ===========
# Complexity:
# ===========

#: Maximum number of `return` statements allowed in a single function.
MAX_RETURNS: Final = 5  # 7-2

#: Maximum number of local variables in a function.
MAX_LOCAL_VARIABLES: Final = 5  # 7-2

#: Maximum number of expressions in a single function.
MAX_EXPRESSIONS: Final = 9  # 7+2

#: Maximum number of arguments for functions or methods.
MAX_ARGUMENTS: Final = 5  # 7-2

#: Maximum number of classes and functions in a single module.
MAX_MODULE_MEMBERS: Final = 7  # 7

#: Maximum number of methods in a single class.
MAX_METHODS: Final = 7  # the same as module members

#: Maximum line complexity.
MAX_LINE_COMPLEXITY: Final = 14  # 7 * 2, also almost guessed

#: Maximum median module Jones complexity.
MAX_JONES_SCORE: Final = 12  # guessed

#: Maximum number of imports in a single module.
MAX_IMPORTS: Final = 12  # guessed

#: Maximum number of imported names in a single module.
MAX_IMPORTED_NAMES: Final = 50  # guessed

#: Maximum number of base classes.
MAX_BASE_CLASSES: Final = 3  # guessed

#: Maximum number of decorators.
MAX_DECORATORS: Final = 5  # 7-2

#: Maximum number of same string usage in code.
MAX_STRING_USAGES: Final = 3  # guessed

#: Maximum number of ``await`` expressions for functions or methods.
MAX_AWAITS: Final = 5  # the same as returns

#: Maximum amount of ``try`` node body length.
MAX_TRY_BODY_LENGTH: Final = 1  # best practice

#: Maximum amount of same expressions per module.
MAX_MODULE_EXPRESSIONS: Final = 7  # the same as module elements

#: Maximum amount of same expressions per function.
MAX_FUNCTION_EXPRESSIONS: Final = 4  # guessed

#: Maximum number of ``assert`` statements in a function.
MAX_ASSERTS: Final = 5  # 7-2

#: Maximum number of access level in an expression.
MAX_ACCESS_LEVEL: Final = 4  # guessed

#: Maximum number of public attributes in a single class.
MAX_ATTRIBUTES: Final = 6  # guessed

#: Maximum amount of cognitive complexity per function.
MAX_COGNITIVE_SCORE: Final = 12  # based on this code statistics

#: Maximum amount of average cognitive complexity per module.
MAX_COGNITIVE_AVERAGE: Final = 8  # based on this code statistics

#: Maximum number of call chains.
MAX_CALL_LEVEL: Final = 3  # reasonable enough

#: Maximum number of nested annotations.
MAX_ANN_COMPLEXITY: Final = 3  # reasonable enough

#: Maximum number of names that can be imported from module.
MAX_IMPORT_FROM_MEMBERS: Final = 8  # guessed
