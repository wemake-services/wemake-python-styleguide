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

# General

#: Minimum variable's name length:
MIN_VARIABLE_LENGTH = 2

#: Either or not you control ones who use your code:
I_CONTROL_CODE = True


# Complexity

#: Maximum number of `return` statements allowed in a single function:
MAX_RETURNS = 5

#: Maximum number of local variables in a function:
MAX_LOCAL_VARIABLES = 5

#: Maximum number of expressions in a single function:
MAX_EXPRESSIONS = 9

#: Maximum number of arguments for functions or method, `self` is not counted:
MAX_ARGUMENTS = 5

#: Maximum number of blocks to nest different structures:
MAX_OFFSET_BLOCKS = 5

#: Maximum number of `elif` blocks in a single `if` condition:
MAX_ELIFS = 3

#: Maximum number of classes and functions in a single module:
MAX_MODULE_MEMBERS = 7

#: Maximum number of methods in a single class:
MAX_METHODS = 7

#: Maximum line complexity:
MAX_LINE_COMPLEXITY = 14  # 7 * 2, also almost guessed

#: Maximum median module Jones complexity:
MAX_JONES_SCORE = 12  # this value was "guessed" based on existing source code

#: Maximum number of imports in a single module:
MAX_IMPORTS = 12

#: Maximum number of conditions in a single ``if`` or ``while`` statement:
MAX_CONDITIONS = 4


# Modules

#: Minimum required module's name length:
MIN_MODULE_NAME_LENGTH = 3
