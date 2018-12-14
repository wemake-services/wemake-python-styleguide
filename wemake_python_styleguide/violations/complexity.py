# -*- coding: utf-8 -*-

"""
These checks finds flaws in your application design.

We try to stick to "the magical 7 ± 2 number" when counting things.
https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two

That's how many objects we can keep in our memory at a time.
We try hard not to exceed the memory capacity limit.

You can also find interesting reading about "Cognitive complexity":
https://www.sonarsource.com/docs/CognitiveComplexity.pdf

Note:

    Simple is better than complex.
    Complex is better than complicated.

.. currentmodule:: wemake_python_styleguide.violations.complexity

Summary
-------

.. autosummary::
   :nosignatures:

   JonesScoreViolation
   TooManyImportsViolation
   TooManyModuleMembersViolation
   TooManyLocalsViolation
   TooManyArgumentsViolation
   TooManyReturnsViolation
   TooManyExpressionsViolation
   TooManyMethodsViolation
   TooManyBaseClassesViolation
   TooManyDecoratorsViolation
   TooDeepNestingViolation
   LineComplexityViolation
   TooManyConditionsViolation
   TooManyElifsViolation
   TooManyForsInComprehensionViolation

Module complexity
-----------------

.. autoclass:: JonesScoreViolation
.. autoclass:: TooManyImportsViolation
.. autoclass:: TooManyModuleMembersViolation

Function and class complexity
-----------------------------

.. autoclass:: TooManyLocalsViolation
.. autoclass:: TooManyArgumentsViolation
.. autoclass:: TooManyReturnsViolation
.. autoclass:: TooManyExpressionsViolation
.. autoclass:: TooManyMethodsViolation
.. autoclass:: TooManyBaseClassesViolation
.. autoclass:: TooManyDecoratorsViolation

Structures complexity
---------------------

.. autoclass:: TooDeepNestingViolation
.. autoclass:: LineComplexityViolation
.. autoclass:: TooManyConditionsViolation
.. autoclass:: TooManyElifsViolation
.. autoclass:: TooManyForsInComprehensionViolation

"""

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    SimpleViolation,
)


@final
class JonesScoreViolation(SimpleViolation):
    """
    Forbids to have modules with complex lines.

    We are using Jones Complexity algorithm to count module's score.
    See
    :py:class:`~.LineComplexityViolation` for details of per-line-complexity.
    How it is done: we count complexity per line, then measuring the median
    complexity across the lines in the whole module.

    Reasoning:
        Having complex modules will decrease your code maintainability.

    Solution:
        Refactor the module contents.

    Configuration:
        This rule is configurable with ``--max-jones-score``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_JONES_SCORE`

    .. versionadded:: 0.1.0

    See also:
        https://github.com/Miserlou/JonesComplexity

    """

    error_template = 'Found module with high Jones Complexity score: {0}'
    code = 200


@final
class TooManyImportsViolation(SimpleViolation):
    """
    Forbids to have modules with too many imports.

    Namespaces are one honking great idea -- let's do more of those!

    Reasoning:
        Having too many imports without prefixes is quite expensive.
        You have to memorize all the source locations of the imports.
        And sometimes it is hard to remember what kind of functions and classes
        are already injected into your context.

        It is also a questionable design if a single module has a lot of
        imports. Why a single module has so many dependencies?
        So, it becomes too coupled.

    Solution:
        Refactor the imports to import a common namespace. Something like
        ``from package import module`` and then
        use it like ``module.function()``.

        Or refactor your code and split the complex module into several ones.

    We do not make any differences between
    ``import`` and ``from ... import ...``.

    Configuration:
        This rule is configurable with ``--max-imports``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_IMPORTS`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found module with too many imports: {0}'
    code = 201


@final
class TooManyModuleMembersViolation(SimpleViolation):
    """
    Forbids to have many classes and functions in a single module.

    Reasoning:
        Having many classes and functions in a single module is a bad thing.
        Soon it will be hard to read through this code and understand it.

    Solution:
        It is better to split this module into several modules or a package.

    We do not make any differences between classes and functions in this check.
    They are treated as the same unit of logic.
    We also do not care about functions and classes being public or not.
    However, methods are counted separately on a per-class basis.

    Configuration:
        This rule is configurable with ``--max-module-members``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_MODULE_MEMBERS`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found too many module members: {0}'
    code = 202


# Functions and classes:

@final
class TooManyLocalsViolation(ASTViolation):
    """
    Forbids to have too many local variables in the unit of code.

    Reasoning:
        Having too many variables in a single function is bad thing.
        Soon, you will find troubles to understand what this variable means.
        It will also become hard to name new variables.

    Solution:
        If you have too many variables in a function, you have to refactor it.

    What counts as a local variable? We only count variable as local
    in the following case: it is assigned inside the function body.
    We do not count variables defined inside comprehensions as local variables,
    since it is impossible to use them outside of the comprehension.

    Example::

        def first_function(param):
            first_var = 1

        def second_function(argument):
            second_var = 1
            argument = int(argument)
            third_var, _ = some_call()

    In this example we will count as locals only several variables:

    1. ``first_var``, because it is assigned inside the function's body
    2. ``second_var``, because it is assigned inside the function's body
    3. ``argument``, because it is reassigned inside the function's body
    4. ``third_var``, because it is assigned inside the function's body

    Please, note that ``_`` is a special case. It is not counted as a local
    variable. Since by design it means: do not count me as a real variable.

    Configuration:
        This rule is configurable with ``--max-local-variables``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_LOCAL_VARIABLES`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found too many local variables: {0}'
    code = 210


@final
class TooManyArgumentsViolation(ASTViolation):
    """
    Forbids to have too many arguments for a function or method.

    Reasoning:
        This is an indicator of a bad design. When function requires many
        arguments it shows that it is required to refactor this piece of code.
        It also indicates that function does too many things at once.

    Solution:
        Split function into several functions.
        Then it will be easier to use them.

    Configuration:
        This rule is configurable with ``--max-arguments``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_ARGUMENTS`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found too many arguments: {0}'
    code = 211


@final
class TooManyReturnsViolation(ASTViolation):
    """
    Forbids placing too many ``return`` statements into the function.

    Reasoning:
        When there are too many ``return`` keywords,
        functions are hard to test. They are also hard to read and
        hard to change and keep everything inside your head at once.

    Solution:
        Change your design.

    Configuration:
        This rule is configurable with ``--max-returns``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_RETURNS`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found too many return statements: {0}'
    code = 212


@final
class TooManyExpressionsViolation(ASTViolation):
    """
    Forbids putting too many expressions in a unit of code.

    Reasoning:
        When there are too many expressions it means that this specific
        function does too many things at once. It has too much logic.

    Solution:
        Split function into several functions, refactor your API.

    Configuration:
        This rule is configurable with ``--max-expressions``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_EXPRESSIONS`

    .. versionadded:: 0.1.0

    """

    error_template = 'Found too many expressions: {0}'
    code = 213


@final
class TooManyMethodsViolation(ASTViolation):
    """
    Forbids to have many methods in a single class.

    Reasoning:
        Having too many methods might lead to the "God object".
        This kind of objects can handle everything.
        So, in the end your code becomes too hard to maintain and test.

    Solution:
        What to do if you have too many methods in a single class?
        Split this class into several classes.
        Then use composition or inheritance to refactor your code.
        This will protect you from "God object" anti-pattern.

    We do not make any difference between instance and class methods.
    We also do not care about functions and classes being public or not.
    We also do not count inherited methods from parents.
    This rule does not count attributes of a class.

    Configuration:
        This rule is configurable with ``--max-methods``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_METHODS`

    .. versionadded:: 0.1.0

    See also:
        https://en.wikipedia.org/wiki/God_object

    """

    error_template = 'Found too many methods: {0}'
    code = 214


class TooManyBaseClassesViolation(ASTViolation):
    """
    Restrict the maximum number of base classes.

    Reasoning:
        It is almost never possible to navigate
        to the desired method of a parent class
        when you need it with multiple mixins.
        It is hard to understand ``mro`` and ``super`` calls.
        Do not overuse this technique.

    Solution:
        Reduce the number of base classes.
        Use composition over inheritance.

    Example::

       # Correct:
       class SomeClassName(First, Second, Mixin): ...

       # Wrong:
       class SomeClassName(
           FirstParentClass,
           SecondParentClass,
           ThirdParentClass,
           CustomClass,
           AddedClass,
        ): ...

    Configuration:
        This rule is configurable with ``--max-base-classes``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_BASE_CLASSES`

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.5.0

    See also:
        https://en.wikipedia.org/wiki/Composition_over_inheritance

    """

    error_template = 'Too many base classes: {0}'
    code = 215


class TooManyDecoratorsViolation(ASTViolation):
    """
    Restrict the maximum number of decorators.

    Reasoning:
        When you are using too many decorators it means that
        you try to overuse the magic.
        You have to ask youself: do I really know what happens inside
        this decorator tree? Typically, the answer will be "no".

    Solution:
        Using too many decorators typically means that
        you try to configure the behavior from outside of the class.
        Do not do that too much.
        Split functions or classes into multiple ones.
        Use higher order decorators.

    Configuration:
        This rule is configurable with ``--max-decorators``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_DECORATORS`

    This rule checks: functions, methods, and classes.

    .. versionadded:: 0.5.0

    """

    error_template = 'Too many decorators: {0}'
    code = 216


# Structures:

@final
class TooDeepNestingViolation(ASTViolation):
    """
    Forbids nesting blocks too deep.

    Reasoning:
        If nesting is too deep that indicates usage of a complex logic
        and language constructions. This means that our design is not
        suited to handle such construction.

    Solution:
        We need to refactor our complex construction into simpler ones.
        We can use new functions or different constructions.

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.5.0

    """

    error_template = 'Found too deep nesting: {0}'
    code = 220


@final
class LineComplexityViolation(ASTViolation):
    """
    Forbids to have complex lines.

    We are using Jones Complexity algorithm to count complexity.
    What is Jones Complexity? It is a simple yet powerful method to count
    the number of ``ast`` nodes per line.
    If the complexity of a single line is higher than a threshold,
    then an error is raised.

    What nodes do we count? All except the following:

    1. modules
    2. function and classes, since they are checked differently
    3. type annotations, since they do not increase complexity

    Reasoning:
        Having a complex line indicates that you somehow managed to put too
        much logic inside a single line.
        At some point in time you will no longer be able to understand
        what this line means and what it does.

    Solution:
        Split a single line into several lines: by creating new variables,
        statements or functions. Note, this might trigger new complexity issues.
        With this technique a single new node in a line might trigger a complex
        refactoring process including several modules.

    Configuration:
        This rule is configurable with ``--max-line-complexity``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_LINE_COMPLEXITY`

    .. versionadded:: 0.1.0

    See also:
        https://github.com/Miserlou/JonesComplexity

    """

    error_template = 'Found line with high Jones Complexity: {0}'
    code = 221


@final
class TooManyConditionsViolation(ASTViolation):
    """
    Forbids to have conditions with too many logical operators.

    Reasoning:
        When reading through the complex conditions you will fail
        to understand all the possible branches. And you will end up putting
        debug breakpoint on this line just to figure out how it works.

    Solution:
        We can reduce the complexity of a single ``if`` by doing two things:
        creating new variables or creating nested ``if`` statements.
        Both of these actions will trigger other complexity checks.

    We count ``and`` and ``or`` keywords as conditions.

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.5.0

    """

    error_template = 'Found a condition with too much logic: {0}'
    code = 222


@final
class TooManyElifsViolation(ASTViolation):
    """
    Forbids to use many ``elif`` branches.

    Reasoning:
        This rule is specifically important, because many ``elif``
        branches indicate a complex flow in your design:
        you are reimplementing ``switch`` in python.

    Solution:
        There are different design patters to use instead.
        For example, you can use some interface that
        just call a specific method without ``if``.
        Or separate your ``if`` into multiple functions.

    .. versionadded:: 0.1.0
    .. versionchanged:: 0.5.0

    """

    error_template = 'Found too many `elif` branches: {0}'
    code = 223


@final
class TooManyForsInComprehensionViolation(ASTViolation):
    """
    Forbids to have too many ``for`` statement within a comprehension.

    Reasoning:
        When reading through the complex comprehension you will fail
        to understand it.

    Solution:
        We can reduce the complexity of a comprehension by reducing the
        amount of ``for`` statements. Refactor your code to use several
        ``for`` loops, comprehensions, or different functions.

    Example::

        # Wrong:
        ast_nodes = [
            target
            for assignment in top_level_assigns
            for target in assignment.targets
            for _ in range(10)
        ]

    .. versionadded:: 0.3.0

    """

    error_template = 'Found a comprehension with too many `for` statements'
    code = 224
