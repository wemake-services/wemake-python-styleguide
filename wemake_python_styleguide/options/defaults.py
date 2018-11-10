# -*- coding: utf-8 -*-

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

from wemake_python_styleguide.types import Final

# General:

#: Minimum variable's name length.
MIN_NAME_LENGTH: Final = 2

#: Maximum variable and module name length:
MAX_NAME_LENGTH: Final = 45

#: Whether you control ones who use your code.
I_CONTROL_CODE: Final = True


# Complexity:

#: Maximum number of `return` statements allowed in a single function.
MAX_RETURNS: Final = 5

#: Maximum number of local variables in a function.
MAX_LOCAL_VARIABLES: Final = 5

#: Maximum number of expressions in a single function.
MAX_EXPRESSIONS: Final = 9

#: Maximum number of arguments for functions or method, `self` is not counted.
MAX_ARGUMENTS: Final = 5

#: Maximum number of classes and functions in a single module.
MAX_MODULE_MEMBERS: Final = 7

#: Maximum number of methods in a single class.
MAX_METHODS: Final = 7

#: Maximum line complexity.
MAX_LINE_COMPLEXITY: Final = 14  # 7 * 2, also almost guessed

#: Maximum median module Jones complexity.
MAX_JONES_SCORE: Final = 12  # this value was "guessed"

#: Maximum number of imports in a single module.
MAX_IMPORTS: Final = 12

#: Maximum number of base classes.
MAX_BASE_CLASSES: Final = 3

#: Maximum number of decorators.
MAX_DECORATORS: Final = 5
