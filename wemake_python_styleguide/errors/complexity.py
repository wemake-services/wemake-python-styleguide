# -*- coding: utf-8 -*-

"""
These checks finds flaws in your application design.

We try to stick to "the magical 7 ± 2 number".
https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two

That's how many objects we can keep in our memory at a time.
We try hard not to exceed the limit.

What we call "design flaws":

1. Complex code (there are a lof of complexity checks!)
2. Nested classes, functions

Note:

    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.

"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class NestedFunctionViolation(ASTStyleViolation):
    """
    This rule forbids to have nested functions.

    We also disallow to nest ``lambda``.

    Reasoning:
        Nesting functions is a bad practice.
        It is hard to test them, it is hard then to separate them.
        People tend to overuse closures, so it's hard to manage the dataflow.

    Solution:
        Just write flat functions, there's no need to nest them.
        Pass parameters as normal arguments, do not use closures.
        Until you need them for decorators or factories.

    However, there are some whitelisted names like,
    see ``NESTED_FUNCTIONS_WHITELIST`` for the whole list.

    Example::

        # Correct:
        def do_some(): ...
        def other(): ...

        # Wrong:
        def do_some():
            def inner():
                ...

    Note:
        Returns Z200 as error code

    """

    error_template = '{0} Found nested function "{1}"'
    code = 'Z200'


class NestedClassViolation(ASTStyleViolation):
    """
    This rule forbids to have nested classes.

    Reasoning:
        Nested classes are really hard to manage.
        You can not even create an instance of this class in many cases.
        Testing them is also really hard.

    Solution:
        Just write flat classes, there's no need nest them.
        If you are nesting classes inside a function for parametrization,
        then you will probably need to use different design (or metaclasses).

    However, there are some whitelisted class names like: ``Meta``.
    See ``NESTED_CLASSES_WHITELIST`` for the full list of names.

    Example::

        # Correct:
        class Some(object): ...
        class Other(object): ...

        # Wrong:
        class Some(object):
            class Inner(object):
                ...

    Note:
        Returns Z201 as error code

    """

    error_template = '{0} Found nested class "{1}"'
    code = 'Z201'


class TooManyLocalsViolation(ASTStyleViolation):
    """
    This rule forbids to have too many local variables in the unit of code.

    Reasoning:
        Having too many variables in a single function is bad thing.
        Soon, you will find troubles to understand what this variable means.
        It will also become hard to name new variables.

    Solution:
        If you have too many variables in a function, you have to refactor it.

    What counts as a local variable? We only count variable as local
    in the following case: it is assigned inside the function body.

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

    Please, note that `_` is a special case. It is not counted as a local
    variable. Since by design it means: do not count me as a real variable.

    This rule is configurable with ``--max-local-variables``.

    Note:
        Returns Z202 as error code

    """

    error_template = '{0} Found too many local variables "{1}"'
    code = 'Z202'


class TooManyArgumentsViolation(ASTStyleViolation):
    """
    This rule forbids to have too many arguments for a function or method.

    Reasoning:
        This is an indicator of a bad desing. When function requires many
        arguments it shows that it is required to refactor this piece of code.
        It also indicates that function does to many things at once.

    Solution:
        Split function into several functions.
        Then it will be easier to use them.

    This rule is configurable with ``--max-arguments``.

    Note:
        Returns Z203 as error code

    """

    error_template = '{0} Found too many arguments "{1}"'
    code = 'Z203'


class TooManyElifsViolation(ASTStyleViolation):
    """
    This rule forbids to use many ``elif`` branches.

    Reasoning:
        This rule is specifically important, because many ``elif``
        branches indicate a complex flow in your design:
        you are reimplementing ``switch`` in python.

    Solution:
        There are different design patters to use instead.
        For example, you can use some interface that
        just call a specific method without ``if``.

    This rule is configurable with ``--max-elifs``.

    Note:
        Returns Z204 as error code

    """

    error_template = '{0} Found too many "{1}" branches'
    code = 'Z204'


class TooManyReturnsViolation(ASTStyleViolation):
    """
    This rule forbids placing too many ``return`` statements into the function.

    Reasoning:
        When there are too many ``return`` keywords,
        functions are hard to test. They are also hard to read and
        hard to change and keep everything inside your head at once.

    Solution:
        Change your design.

    This rule is configurable with ``--max-returns``.

    Note:
        Returns Z205 as error code

    """

    error_template = '{0} Found too many return statements "{1}"'
    code = 'Z205'


class TooManyExpressionsViolation(ASTStyleViolation):
    """
    This rule forbids putting to many expression is a unit of code.

    Reasoning:
        When there are too many expression it means that this specific
        function does too many things at once. It has too many logics.

    Solution:
        Split function into several functions, refactor your API.

    This rule is configurable with ``--max-expressions``.

    Note:
        Returns Z206 as error code

    """

    error_template = '{0} Found too many expressions "{1}"'
    code = 'Z206'


class TooDeepNestingViolation(ASTStyleViolation):
    """
    This rule forbids nesting blocks too deep.

    Reasoning:
        If nesting is too deep that indicates of a complex logic
        and language constructions. This means that our design is not
        suited to handle such construction.

    Solution:
        We need to refactor our complex construction into simplier ones.
        We can use new functions or different constructions.

    This rule is configurable with ``--max-offset-blocks``.

    Note:
        Returns Z207 as error code

    """

    error_template = '{0} Found too deep nesting "{1}"'
    code = 'Z207'


class TooManyModuleMembersViolation(ASTStyleViolation):
    """
    This rule forbids to have many classes and functions in a single module.

    Reasoning:
        Having many classes and functions in a single module is a bad thing.
        Soon it will be hard to read through this code and understand it.

    Solution:
        It is better to split this module into several modules or a package.

    We do not make any differences between classes and functions in this check.
    They are treated as the same unit of logic.
    We also do no care about functions and classes been public or not.
    However, methods are counted separately on a per-class basis.

    This rule is configurable with ``--max-module-members``.

    Note:
        Returns Z208 as error code

    """

    error_template = '{0} Found too many members "{1}"'
    code = 'Z208'


class TooManyMethodsViolation(ASTStyleViolation):
    """
    This rule forbids to have many methods in a single class.

    Reasoning:
        Having too many methods might lead to the "God object".
        This kind of objects can handle everything.
        So, in the end your code becomes to hard to maintain and test.

    Solution:
        What to do if you have too many methods in a single class?
        Split this class into several classes.
        Then use composition or inheritance to refactor your code.
        This will protect you from "God object" anti-pattern.
        See: https://en.wikipedia.org/wiki/God_object

    We do not make any difference between instance and class methods.
    We also do no care about functions and classes been public or not.
    We also do not count inherited methods from parents.
    This rule do not count attributes of a class.

    This rule is configurable with ``--max-methods``.

    Note:
        Returns Z209 as error code

    """

    error_template = '{0} Found too many methods "{1}"'
    code = 'Z209'
