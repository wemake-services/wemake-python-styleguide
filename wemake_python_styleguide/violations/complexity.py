"""
These checks find flaws in your application design.

We try to stick to "the magical 7 ± 2 number" when counting things.
https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two

That's how many objects we can keep in our memory at a time.
We try hard not to exceed the memory capacity limit.

You can also find interesting reading about "Cognitive complexity":
https://www.sonarsource.com/docs/CognitiveComplexity.pdf

Note:
    Simple is better than complex.
    Complex is better than complicated.

See also:
    https://sobolevn.me/2019/10/complexity-waterfall

.. currentmodule:: wemake_python_styleguide.violations.complexity

Summary
-------

.. autosummary::
   :nosignatures:

   JonesScoreViolation
   TooManyImportsViolation
   TooManyModuleMembersViolation
   TooManyImportedNamesViolation
   OverusedExpressionViolation
   TooManyLocalsViolation
   TooManyArgumentsViolation
   TooManyReturnsViolation
   TooManyExpressionsViolation
   TooManyMethodsViolation
   TooManyBaseClassesViolation
   TooManyDecoratorsViolation
   TooManyAwaitsViolation
   TooManyAssertsViolation
   TooDeepAccessViolation
   TooDeepNestingViolation
   LineComplexityViolation
   TooManyConditionsViolation
   TooManyElifsViolation
   TooManyForsInComprehensionViolation
   TooManyExceptCasesViolation
   OverusedStringViolation
   TooLongYieldTupleViolation
   TooLongCompareViolation
   TooLongTryBodyViolation
   TooManyPublicAttributesViolation
   CognitiveComplexityViolation
   CognitiveModuleComplexityViolation
   TooLongCallChainViolation
   TooComplexAnnotationViolation
   TooManyImportedModuleMembersViolation


Module complexity
-----------------

.. autoclass:: JonesScoreViolation
.. autoclass:: TooManyImportsViolation
.. autoclass:: TooManyModuleMembersViolation
.. autoclass:: TooManyImportedNamesViolation
.. autoclass:: OverusedExpressionViolation

Structure complexity
--------------------

.. autoclass:: TooManyLocalsViolation
.. autoclass:: TooManyArgumentsViolation
.. autoclass:: TooManyReturnsViolation
.. autoclass:: TooManyExpressionsViolation
.. autoclass:: TooManyMethodsViolation
.. autoclass:: TooManyBaseClassesViolation
.. autoclass:: TooManyDecoratorsViolation
.. autoclass:: TooManyAwaitsViolation
.. autoclass:: TooManyAssertsViolation
.. autoclass:: TooDeepAccessViolation
.. autoclass:: TooDeepNestingViolation
.. autoclass:: LineComplexityViolation
.. autoclass:: TooManyConditionsViolation
.. autoclass:: TooManyElifsViolation
.. autoclass:: TooManyForsInComprehensionViolation
.. autoclass:: TooManyExceptCasesViolation
.. autoclass:: OverusedStringViolation
.. autoclass:: TooLongYieldTupleViolation
.. autoclass:: TooLongCompareViolation
.. autoclass:: TooLongTryBodyViolation
.. autoclass:: TooManyPublicAttributesViolation
.. autoclass:: CognitiveComplexityViolation
.. autoclass:: CognitiveModuleComplexityViolation
.. autoclass:: TooLongCallChainViolation
.. autoclass:: TooComplexAnnotationViolation
.. autoclass:: TooManyImportedModuleMembersViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    MaybeASTViolation,
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


@final
class TooManyImportedNamesViolation(SimpleViolation):
    """
    Forbids to have modules with too many imported names.

    Namespaces are one honking great idea -- let's do more of those!

    Reasoning:
        Having too many imported names without prefixes is quite expensive.
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

    Example::

        # Correct:
        import module  # 1 imported name

        # Wrong:
        from module import func1, func2, ..., funcN  # N imported names

    We do not make any differences between
    ``import`` and ``from ... import ...``.

    Configuration:
        This rule is configurable with ``--max-imported-names``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_IMPORTED_NAMES`

    .. versionadded:: 0.12.0

    """

    error_template = 'Found module with too many imported names: {0}'
    code = 203


@final
class OverusedExpressionViolation(ASTViolation):
    """
    Forbids to have overused expressions in a module, function or method.

    What do we call an "overused expression"? When you use any expression
    (like ``user_dict['age']`` for example) inside your code,
    you always have to track that you are not using it "too much".
    Because if that expression is everywhere inside your code,
    it is a sign of a problem. It means that you are missing an abstraction.

    We check overused expression on two levels:

    - per each function
    - per all module

    Related to :class:`~TooManyExpressionsViolation`.

    Reasoning:
        Overusing expression lead to losing the parts that can and should
        be refactored into variables, methods, and properties of objects.

    Solution:
        Refactor expressions to be an attribute, a method, or a new variable.

    Configuration:
        This rule is configurable with ``--max-module-expressions``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_MODULE_EXPRESSIONS`

        And with ``--max-function-expressions``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_FUNCTION_EXPRESSIONS`

    .. versionadded:: 0.12.0
    .. versionchanged:: 0.14.0

    """

    error_template = 'Found overused expression: {0}'
    code = 204


# Functions and classes:

@final
class TooManyLocalsViolation(ASTViolation):
    """
    Forbids to have too many local variables in the unit of code.

    Reasoning:
        Having too many variables in a single function is a bad thing.
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
        This is an indicator of a bad design. When a function requires many
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
        Change your design. Split functions into multiple ones.

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
    Forbids putting too many expressions in a single function.

    This rule is quite similar to "max lines" in a function,
    but is much nicer. Because we don't count lines,
    we count real code entities. This way adding just several extra empty
    lines for readability will never trigger this violation.

    Related to :class:`~OverusedExpressionViolation`.

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

    See also:
        https://en.wikipedia.org/wiki/Expression_(computer_science)

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
        So, in the end, your code becomes too hard to maintain and test.

    Solution:
        What to do if you have too many methods in a single class?
        Split this class into several classes.
        Then use composition or inheritance to refactor your code.
        This will protect you from "God object" anti-pattern.

    We do not make any difference between instance and class methods.
    We also do not care about functions and classes being public or not.
    We also do not count inherited methods from parents.
    This rule does not count the attributes of a class.

    Configuration:
        This rule is configurable with ``--max-methods``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_METHODS`

    .. versionadded:: 0.1.0

    See also:
        https://en.wikipedia.org/wiki/God_object

    """

    error_template = 'Found too many methods: {0}'
    code = 214


@final
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


@final
class TooManyDecoratorsViolation(ASTViolation):
    """
    Restrict the maximum number of decorators.

    Reasoning:
        When you are using too many decorators it means that
        you try to overuse the magic.
        You have to ask yourself: do I really know what happens inside
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


@final
class TooManyAwaitsViolation(ASTViolation):
    """
    Forbids placing too many ``await`` expressions into a function.

    Reasoning:
        When there are too many ``await`` keywords,
        functions are starting to get really complex.
        It is hard to tell where are we and what is going on.

    Solution:
        Change your design. Split functions into multiple ones.

    Configuration:
        This rule is configurable with ``--max-awaits``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_AWAITS`

    .. versionadded:: 0.10.0

    """

    error_template = 'Found too many await expressions: {0}'
    code = 217


@final
class TooManyAssertsViolation(ASTViolation):
    """
    Forbids placing too many ``asseert`` statements into a function.

    Reasoning:
        When there are too many ``assert`` keywords,
        functions are starting to get really complex.
        It might indicate that your tests or contracts are too big.

    Solution:
        Create rich ``assert`` statements, use higher-level contracts,
        or create special guard functions.

    Configuration:
        This rule is configurable with ``--max-asserts``.
        Default: :str:`wemake_python_styleguide.options.defaults.MAX_ASSERTS`

    .. versionadded:: 0.12.0

    """

    error_template = 'Found too many `assert` statements: {0}'
    code = 218


@final
class TooDeepAccessViolation(ASTViolation):
    """
    Forbids to have consecutive expressions with too deep access level.

    We consider only these expressions as accesses:

    - ``ast.Subscript``
    - ``ast.Attribute``

    We do not treat ``ast.Call`` as an access, since there are
    a lot of call-based APIs like Django ORM, builder patterns, etc.

    Reasoning:
        Having too deep access level indicates a bad design
        and overcomplicated data without proper API.

    Solution:
        Split the expression into variables, functions or classes.
        Refactor the API for your data layout.

    Example::

        # Correct: access level = 4
        self.attr.inner.wrapper[1]

        # Correct: access level = 1
        manager.filter().exclude().annotate().values().first()

        # Wrong: access level = 5
        self.attr.inner.wrapper.method.call()

        # Wrong: access level = 5
        # `obj` has access level of 2:
        # `.attr`, `.call`
        # `call()` has access level of 5:
        # `.other`, `[0]`, `.field`, `.type`, `.boom`
        obj.attr.call().other[0].field.type.boom

    Configuration:
        This rule is configurable with ``--max-access-level``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_ACCESS_LEVEL`

    .. versionadded:: 0.12.0

    """

    error_template = 'Found too deep access level: {0}'
    code = 219


@final
class TooDeepNestingViolation(ASTViolation):
    """
    Forbids nesting blocks too deep.

    Reasoning:
        If nesting is too deep that indicates usage of complex logic
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
    3. type annotations, since they do not increase the complexity

    Reasoning:
        Having a complex line indicates that you somehow managed to put too
        much logic inside a single line.
        At some point in time, you will no longer be able to understand
        what this line means and what it does.

    Solution:
        Split a single line into several lines: by creating new variables,
        statements or functions. Note, this might trigger new complexity issues.
        With this technique, a single new node in a line might trigger a complex
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

    We use :str:`wemake_python_styleguide.constants.MAX_CONDITIONS`
    as a default value.

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

    We use :str:`wemake_python_styleguide.constants.MAX_ELIFS`
    as a default value.

    Reasoning:
        This rule is specifically important because of many ``elif``
        branches indicate a complex flow in your design:
        you are reimplementing ``switch`` in python.

    Solution:
        There are different design patterns to use instead.
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
        We can reduce the complexity of comprehension by reducing the
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


@final
class TooManyExceptCasesViolation(ASTViolation):
    """
    Forbids to have too many ``except`` cases in a single ``try`` clause.

    We use :str:`wemake_python_styleguide.constants.MAX_EXCEPT_CASES`
    as a default value.

    Reasoning:
        Handling too many exceptions in a single place
        is a good indicator of a bad design.
        Since this way, one controlling structure will become too complex.
        And you will need to test a lot of paths your application might go.

    Solution:
        We can reduce the complexity of this case by splitting it into multiple
        ``try`` cases, functions or using a decorator
        to handle different exceptions.

    .. versionadded:: 0.7.0

    """

    error_template = 'Found too many `except` cases: {0}'
    code = 225


@final
class OverusedStringViolation(MaybeASTViolation):
    """
    Forbids to over-use string constants.

    We allow to use strings without any restrictions as annotations for
    variables, arguments, return values, and class attributes.

    Reasoning:
        When some string is used more than several time in your code,
        it probably means that this string is a meaningful constant.
        And should be treated like one.

    Solution:
        Deduplicate you string usages
        by defining new functions or constants.

    Configuration:
        This rule is configurable with ``--max-string-usages``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_STRING_USAGES`

    .. versionadded:: 0.10.0

    """

    error_template = 'Found string constant over-use: {0}'
    code = 226


@final
class TooLongYieldTupleViolation(ASTViolation):
    """
    Forbids to yield too long tuples.

    Reasoning:
        Long yield tuples complicate generator using.
        This rule helps to reduce complication.

    Solution:
        Use lists of similar type or wrapper objects.

    .. versionadded:: 0.10.0

    """

    error_template = 'Found too long yield tuple: {0}'
    code = 227


@final
class TooLongCompareViolation(ASTViolation):
    """
    Forbids to have too long compare expressions.

    Reasoning:
        To long compare expressions indicate
        that there's something wrong going on in the code.
        Compares should not be longer than 3 or 4 items.

    Solution:
        Use several conditions, seprate variables, or functions.

    .. versionadded:: 0.10.0

    """

    error_template = 'Found too long compare'
    code = 228


@final
class TooLongTryBodyViolation(ASTViolation):
    """
    Forbids to have ``try`` blocks with too long bodies.

    Reasoning:
        Having too many statements inside your ``try`` block
        can lead to situations when some different statement
        raises an exception and you are not aware of it
        since it is not expected.

    Solution:
        Move things out of the ``try`` block or create new functions.
        The less lines you have in your ``try`` block - the safer
        you are from accidental errors.

    Configuration:
        This rule is configurable with ``--max-try-body-length``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_TRY_BODY_LENGTH`

    See also:
        https://adamj.eu/tech/2019/10/02/limit-your-try-clauses-in-python/

    .. versionadded:: 0.12.0

    """

    error_template = 'Found too long ``try`` body length: {0}'
    code = 229


@final
class TooManyPublicAttributesViolation(ASTViolation):
    """
    Forbids to have ``try`` blocks with too long bodies.

    We only check static definitions in a form of ``self.public = ...``.
    We do not count parent attributes.
    We do not count properties.
    We do not count annotations.
    We do not count class attributes.
    We do not count duplicates.

    Reasoning:
        Having too many public instance attributes means
        that your class is too complex in terms of coupling.
        Other classes and functions will rely on these concrete fields
        instead of better abstraction layers.

    Solution:
        Make some attributes protected.
        Split this class into several ones.
        If class is a Data Transfer Object, then use ``@dataclass`` decorator.

    Configuration:
        This rule is configurable with ``--max-attributes``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_ATTRIBUTES`

    See also:
        https://en.wikipedia.org/wiki/Coupling_(computer_programming)

    .. versionadded:: 0.12.0

    """

    error_template = 'Found too many public instance attributes: {0}'
    code = 230


@final
class CognitiveComplexityViolation(ASTViolation):
    """
    Forbids to have functions with too high cognitive complexity.

    Reasoning:
        People are not great at reading and iterpretating code in their heads.
        That's why code with a lot of nested loops,
        conditions, exceptions handlers,
        and context managers is hard to read and understand.

    Solution:
        Rewrite your code to be simplier.
        Use flat structures and conditions, remove nested loops.

    Configuration:
        This rule is configurable with ``--max-cognitive-score``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_COGNITIVE_SCORE`

    See also:
        https://en.wikipedia.org/wiki/Cognitive_complexity
        https://pypi.org/project/cognitive-complexity/
        https://github.com/Melevir/flake8-cognitive-complexity

    .. versionadded:: 0.13.0

    """

    error_template = 'Found too high function cognitive complexity: {0}'
    code = 231


@final
class CognitiveModuleComplexityViolation(SimpleViolation):
    """
    Forbids to have modules with too high average cognitive complexity.

    Reasoning:
        Modules with lots of functions might hide cognitive complexity
        inside many small and relatevely simple functions.

    Solution:
        Rewrite your code to be simplier.
        Or use several modules.

    Configuration:
        This rule is configurable with ``--max-cognitive-average``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_COGNITIVE_AVERAGE`

    See also:
        https://en.wikipedia.org/wiki/Cognitive_complexity

    .. versionadded:: 0.13.0

    """

    error_template = 'Found too high module cognitive complexity: {0}'
    code = 232


@final
class TooLongCallChainViolation(ASTViolation):
    """
    Forbids too long call chains.

    Reasoning:
        Too long call chains are overcomplicated and
        indicators of bad API design.

    Solution:
        Split the expression into variables, functions or classes.
        Refactor the API to allow higher-level access to functions.

    Configuration:
        This rule is configurable with ``--max-call-level``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_CALL_LEVEL`

    .. versionadded:: 0.13.0

    """

    error_template = 'Found too lang call chain length: {0}'
    code = 233


@final
class TooComplexAnnotationViolation(ASTViolation):
    """
    Forbids too complex annotations.

    Annotation complexity is maximum annotation nesting level.
    Example: ``List[int]`` has complexity of 2
    and ``Tuple[List[Optional[str]], int]`` has complexity of 4.

    Reasoning:
        Too complex annotations make your types unreadable.
        And make developers afraid of types.

    Solution:
        Create type aliases. And use them a lot!

    Configuration:
        This rule is configurable with ``--max-annotation-complexity``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_ANN_COMPLEXITY`

    See also:
        https://mypy.readthedocs.io/en/stable/kinds_of_types.html#type-aliases
        https://github.com/best-doctor/flake8-annotations-complexity

    .. versionadded:: 0.14.0

    """

    error_template = 'Found too complex annotation: {0}'
    code = 234


@final
class TooManyImportedModuleMembersViolation(ASTViolation):
    """
    Forbids ``from ... import ...`` with too many imported names.

    Reasoning:
        Importing too many names from one import is easy way to cause
        violation ``WPS203`` - too many imported names.

    Solution:
        Refactor the imports to import a common namespace. Something like
        ``from package import module`` and then
        use it like ``module.function()``.

    Example::

        # Correct:
        import module  # 1 imported name

        # Wrong:
        from module import func1, func2, ..., funcN  # N imported names

    Configuration:
        This rule is configurable with ``--max-import-from-members``.
        Default:
        :str:`wemake_python_styleguide.options.defaults.MAX_IMPORT_FROM_MEMBERS`

    .. versionadded:: 0.14.0

    """

    error_template = 'Found too many imported names from a module: {0}'
    code = 235
