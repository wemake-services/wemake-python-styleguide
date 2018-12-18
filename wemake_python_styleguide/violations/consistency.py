# -*- coding: utf-8 -*-

"""
These checks limit the Python's inconsistency.

We can do the same things differently in Python.
For example, there are three ways to format a string.
There are several ways to write the same number.

We like our code to be consistent.
It is easier to bare with your code base if you follow these rules.

So, we choose a single way to do things.
It does not mean that we choose the best way to do it.
But, we value consistency more than being 100% right.
And we are ready to suffer all trade-offs that might come.

Once again, these rules are highly subjective. But, we love them.

.. currentmodule:: wemake_python_styleguide.violations.consistency

Summary
-------

.. autosummary::
   :nosignatures:

   LocalFolderImportViolation
   DottedRawImportViolation
   UnicodeStringViolation
   UnderscoredNumberViolation
   PartialFloatViolation
   FormattedStringViolation
   RequiredBaseClassViolation
   MultipleIfsInComprehensionViolation
   ConstantComparisonViolation
   ComparisonOrderViolation
   BadNumberSuffixViolation
   MultipleInComparisonViolation
   RedundantComparisonViolation
   MissingSpaceBetweenKeywordAndParenViolation
   WrongConditionalViolation
   ObjectInBaseClassesListViolation
   MultipleContextManagerAssignmentsViolation
   ParametersIndentationViolation
   ExtraIndentationViolation
   WrongBracketPositionViolation
   MultilineFunctionAnnotationViolation
   UppercaseStringModifierViolation

Consistency checks
------------------

.. autoclass:: LocalFolderImportViolation
.. autoclass:: DottedRawImportViolation
.. autoclass:: UnicodeStringViolation
.. autoclass:: UnderscoredNumberViolation
.. autoclass:: PartialFloatViolation
.. autoclass:: FormattedStringViolation
.. autoclass:: RequiredBaseClassViolation
.. autoclass:: MultipleIfsInComprehensionViolation
.. autoclass:: ConstantComparisonViolation
.. autoclass:: ComparisonOrderViolation
.. autoclass:: BadNumberSuffixViolation
.. autoclass:: MultipleInComparisonViolation
.. autoclass:: RedundantComparisonViolation
.. autoclass:: MissingSpaceBetweenKeywordAndParenViolation
.. autoclass:: WrongConditionalViolation
.. autoclass:: ObjectInBaseClassesListViolation
.. autoclass:: MultipleContextManagerAssignmentsViolation
.. autoclass:: ParametersIndentationViolation
.. autoclass:: ExtraIndentationViolation
.. autoclass:: WrongBracketPositionViolation
.. autoclass:: MultilineFunctionAnnotationViolation
.. autoclass:: UppercaseStringModifierViolation

"""

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    TokenizeViolation,
)


@final
class LocalFolderImportViolation(ASTViolation):
    """
    Forbids to have imports relative to the current folder.

    Reasoning:
        We should pick one style and stick to it.
        We have decided to use the explicit one.

    Solution:
        Refactor your imports to use the absolute path.

    Example::

        # Correct:
        from my_package.version import get_version

        # Wrong:
        from .version import get_version
        from ..drivers import MySQLDriver

    .. versionadded:: 0.1.0
    """

    error_template = 'Found local folder import'
    code = 300


@final
class DottedRawImportViolation(ASTViolation):
    """
    Forbids to use imports like ``import os.path``.

    Reasoning:
        There too many different ways to import something.
        We should pick one style and stick to it.
        We have decided to use the readable one.

    Solution:
        Refactor your import statement.

    Example::

        # Correct:
        from os import path

        # Wrong:
        import os.path

    .. versionadded:: 0.1.0
    """

    error_template = 'Found dotted raw import: {0}'
    code = 301


@final
class UnicodeStringViolation(TokenizeViolation):
    """
    Forbids to use ``u`` string prefix.

    Reasoning:
        We do not need this prefix since ``python2``.
        But, it is still possible to find it inside the codebase.

    Solution:
        Remove this prefix.

    Example::

        # Correct:
        nickname = 'sobolevn'
        file_contents = b'aabbcc'

        # Wrong:
        nickname = u'sobolevn'

    .. versionadded:: 0.1.0

    """

    code = 302
    error_template = 'Found unicode string prefix: {0}'


@final
class UnderscoredNumberViolation(TokenizeViolation):
    """
    Forbids to use underscores (``_``) in numbers.

    Reasoning:
        It is possible to write ``1000`` in three different ways:
        ``1_000``, ``10_00``, and ``100_0``.
        And it would be still the same number.
        Count how many ways there are to write bigger numbers.
        Currently, it all depends on cultural habits of the author.
        We enforce a single way to write numbers: without the underscore.

    Solution:
        Numbers should be written as numbers: ``1000``.
        If you have a very big number with a lot of zeros, use multiplication.

    Example::

        # Correct:
        phone = 88313443
        million = 1000000

        # Wrong:
        phone = 8_83_134_43
        million = 100_00_00

    .. versionadded:: 0.1.0

    """

    code = 303
    error_template = 'Found underscored number: {0}'


@final
class PartialFloatViolation(TokenizeViolation):
    """
    Forbids to use partial floats like ``.05`` or ``23.``.

    Reasoning:
        Partial numbers are hard to read and they can be confused with
        other numbers. For example, it is really
        easy to confuse ``0.5`` and ``.05`` when reading
        through the source code.

    Solution:
        Use full versions with leading and starting zeros.

    Example::

        # Correct:
        half = 0.5
        ten_float = 10.0

        # Wrong:
        half = .5
        ten_float = 10.

    .. versionadded:: 0.1.0

    """

    code = 304
    error_template = 'Found partial float: {0}'


@final
class FormattedStringViolation(ASTViolation):
    """
    Forbids to use ``f`` strings.

    Reasoning:
        ``f`` strings looses context too often and they are hard to lint.
        Imagine that you have a string that breaks
        when you move it two lines above.
        That's not how a string should behave.
        Also, they promote a bad practice:
        putting your logic inside the template.

    Solution:
        Use ``.format()`` with indexed params instead.

    See also:
        https://github.com/xZise/flake8-string-format

    Example::

        # Wrong:
        f'Result is: {2 + 2}'

        # Correct:
        'Result is: {0}'.format(2 + 2)
        'Hey {user}! How are you?'.format(user='sobolevn')

    .. versionadded:: 0.1.0

    """

    error_template = 'Found `f` string'
    code = 305


@final
class RequiredBaseClassViolation(ASTViolation):
    """
    Forbids to write classes without base classes.

    Reasoning:
        We just need to decide how to do it.
        We need a single and unified rule about base classes.
        We have decided to stick to the explicit base class notation.

    Solution:
        Add a base class.

    Example::

        # Correct:
        class Some(object): ...

        # Wrong:
        class Some: ...

    .. versionadded:: 0.1.0

    """

    error_template = 'Found class without a base class: {0}'
    code = 306


@final
class MultipleIfsInComprehensionViolation(ASTViolation):
    """
    Forbids to have multiple ``if`` statements inside list comprehensions.

    Reasoning:
        It is very hard to read multiple ``if`` statements inside
        a list comprehension. Since, it is even hard to tell all of them
        should pass or fail.

    Solution:
        Use a single ``if`` statement inside list comprehensions.
        Use ``filter()`` if you have complicated logic.

    Example::

        # Wrong:
        nodes = [node for node in html if node != 'b' if node != 'i']

        # Correct:
        nodes = [node for node in html if node not in ('b', 'i')]

    .. versionadded:: 0.1.0

    """

    error_template = 'Found list comprehension with multiple `if`s'
    code = 307


@final
class ConstantComparisonViolation(ASTViolation):
    """
    Forbids to have comparisons between two literals.

    Reasoning:
        When two constants are compared it is typically an indication of a
        mistake, since the Boolean value of the comparison will always be
        the same.

    Solution:
        Remove the constant comparison and any associated dead code.

    Example::

        # Wrong:
        if 60 * 60 < 1000:
            do_something()
        else:
            do_something_else()

        # Correct:
        do_something_else()

    .. versionadded:: 0.3.0

    """

    error_template = 'Found constant comparison'
    code = 308


@final
class ComparisonOrderViolation(ASTViolation):
    """
    Forbids comparision where argument doesn't come first.

    Reasoning:
        It is hard to read the code when
        you have to shuffle ordering of the arguments all the time.
        Bring a consistency to the comparison!

    Solution:
        Refactor your comparison expression, place the argument first.

    Example::

        # Correct:
        if some_x > 3:
        if 3 < some_x < 10:

        # Wrong:
        if 3 < some_x:

    .. versionadded:: 0.3.0

    """

    error_template = 'Found reversed comparison order'
    code = 309


@final
class BadNumberSuffixViolation(TokenizeViolation):
    """
    Forbids to use capital ``X``, ``O``, ``B``, and ``E`` in numbers.

    Reasoning:
        Octal, hex, binary and scientific notation suffixes could
        be written in two possible notations: lowercase and uppercase.
        Which brings confusion and decreases code consistency and readability.
        We enforce a single way to write numbers with suffixes:
        suffix with lowercase chars.

    Solution:
        Octal, hex, binary and scientific notation suffixes in numbers
        should be written lowercase.

    Example::

        # Correct:
        hex_number = 0xFF
        octal_number = 0o11
        binary_number = 0b1001
        number_with_scientific_notation = 1.5e+10

        # Wrong:
        hex_number = 0XFF
        octal_number = 0O11
        binary_number = 0B1001
        number_with_scientific_notation = 1.5E+10

    .. versionadded:: 0.3.0

    """

    error_template = 'Found bad number suffix: {0}'
    code = 310


@final
class MultipleInComparisonViolation(ASTViolation):
    """
    Forbids comparision where multiple ``in`` checks.

    Reasoning:
        Using multiple ``in`` is unreadable.

    Solution:
        Refactor your comparison expression to use several ``and`` conditions
        or separate ``if`` statements in case it is appropriate.

    Example::

        # Correct:
        if item in bucket and bucket in master_list_of_buckets:
        if x_coord in line and line in square:

        # Wrong:
        if item in bucket in master_list_of_buckets:
        if x_cord in line in square:

    .. versionadded:: 0.3.0

    """

    error_template = 'Found multiple `in` comparisons'
    code = 311


@final
class RedundantComparisonViolation(ASTViolation):
    """
    Forbids to have comparisons between the same variable.

    Reasoning:
        When the same variables are compared it is typically an indication
        of a mistake, since the Boolean value of the comparison will always be
        the same.

    Solution:
        Remove the same variable comparison and any associated dead code.

    Example::

        # Wrong:
        a = 1
        if a < a:
            do_something()
        else:
            do_something_else()

        # Correct:
        do_something()

    .. versionadded:: 0.3.0

    """

    error_template = 'Found comparison between same variable'
    code = 312


@final
class MissingSpaceBetweenKeywordAndParenViolation(TokenizeViolation):
    """
    Forbid opening parenthesis from following keyword without space in between.

    Reasoning:
        Some people use ``return`` and ``yield`` keywords as functions.
        The same happened to good old ``print`` in Python2.
    Solution:
        Insert space symbol between keyword and open paren.

    Example::

        # Wrong:
        def func():
            a = 1
            b = 2
            del(a, b)
            yield(1, 2, 3)

        # Correct:
        def func():
            a = 1
            del (a, b)
            yield (1, 2, 3)

    .. versionadded:: 0.3.0

    """

    error_template = 'Found parens right after a keyword'
    code = 313


class WrongConditionalViolation(ASTViolation):
    """
    Forbids using ``if`` statements that use invalid conditionals.

    Reasoning:
        When invalid conditional arguments are used
        it is typically an indication of a mistake, since
        the value of the conditional result will always be the same.

    Solution:
        Remove the conditional and any associated dead code.

    Example::

        # Correct:
        if value is True: ...

        # Wrong:
        if True: ...

    .. versionadded:: 0.3.0

    """

    error_template = 'Conditional always evaluates to same result'
    code = 314


class ObjectInBaseClassesListViolation(ASTViolation):
    """
    Forbids extra ``object`` in parent classes list.

    Reasoning:
        We should allow object only when
        we explicitly use it as a single parent class.
        When there is an other class or there are multiple
        parents - we should not allow it for the consistency reasons.

    Solution:
        Remove extra ``object`` parent class from the list.

    Example::

       # Correct:
       class SomeClassName(object): ...
       class SomeClassName(FirstParentClass, SecondParentClass): ...

       # Wrong:
       class SomeClassName(FirstParentClass, SecondParentClass, object): ...

    .. versionadded:: 0.3.0

    """

    error_template = 'Founded extra `object` in parent classes list'
    code = 315


@final
class MultipleContextManagerAssignmentsViolation(ASTViolation):
    """
    Forbids multiple assignment targets for context managers.

    Reasoning:
        It is hard to distinguish whether ``as`` should unpack into
        tuple, or we are just using two context managers.

    Solution:
        Use several context managers. Or explicit brackets.

    Example::

        # Correct:
        with open('') as first:
            with second:
                ...

        with some_context as (first, second):
            ...

        # Wrong:
        with open('') as first, second:
            ...

    .. versionadded:: 0.6.0

    """

    error_template = 'Found context manager with too many assignments'
    code = 316


@final
class ParametersIndentationViolation(ASTViolation):
    """
    Forbids to use incorrect parameters indentation.

    Reasoning:
        It is really easy to spoil your perfect, readable code with
        incorrect multi-line parameters indentation.
        Since, it is really easy to style them in any of 100 possible ways.
        We enforce a strict rule about how it is possible to write these
        multi-line parameters.

    Solution:
        Use consistent multi-line parameters indentation.

    Example::

        # Correct:
        def my_function(arg1, arg2, arg3) -> None:
            return None

        print(1, 2, 3, 4, 5, 6)

        def my_function(
            arg1, arg2, arg3,
        ) -> None:
            return None

        print(
            1, 2, 3, 4, 5, 6,
        )

        def my_function(
            arg1,
            arg2,
            arg3,
        ) -> None:
            return None

        print(
            first_variable,
            2,
            third_value,
            4,
            5,
            last_item,
        )

        # Special case:

        print('some text', 'description', [
            first_variable,
            second_variable,
            third_variable,
            last_item,
        ], end='')

    Everything else is considered a violation.
    This rule checks: lists, sets, tuples, dicts, calls,
    functions, methods, and classes.

    .. versionadded:: 0.6.0

    """

    error_template = 'Found incorrect multi-line parameters'
    code = 317


@final
class ExtraIndentationViolation(TokenizeViolation):
    """
    Forbids to use extra indentation.

    Reasoning:
        You can use extra indentation for lines of code.
        Python allows you to do that in case you will keep the indentation
        level equal for this specific node.
        But, that's insane!

    Solution:
        We should stick to 4 spaces for an indentation block.
        Each next block should be indented by just 4 extra spaces.

    Example::

        # Correct:
        def test():
            print('test')

        # Wrong:
        def test():
                    print('test')

    .. versionadded:: 0.6.0

    """

    error_template = 'Found extra indentation'
    code = 318


@final
class WrongBracketPositionViolation(TokenizeViolation):
    """
    Forbids to use extra indentation.

    Reasoning:
        You can use extra indentation for lines of code.
        Python allows you to do that in case you will keep the indentation
        level equal for this specific node.
        But, that's insane!

    Solution:
        Place bracket on the same line, when a single line expression.
        Or place bracket on a new line when a multi-line expression.

    Example::

        # Correct:
        print([
            1, 2, 3,
        ])

        print(
            1,
            2,
        )

        def _annotate_brackets(
            tokens: List[tokenize.TokenInfo],
        ) -> TokenLines:
            ...

        # Wrong:
        print([
            1, 2, 3],
        )

        print(
            1,
            2)

        def _annotate_brackets(
            tokens: List[tokenize.TokenInfo]) -> TokenLines:
            ...

    We check round, square, and curly brackets.

    .. versionadded:: 0.6.0

    """

    error_template = 'Found bracket in wrong position'
    code = 319


@final
class MultilineFunctionAnnotationViolation(ASTViolation):
    """
    Forbids to use multi-line function type annotations.

    Reasoning:
        Functions with multi-line type annotations are unreadable.

    Solution:
        Use type annotations that fit into a single line to annotate functions.
        If your annotation is too long, then use type aliases.

    Example::

        # Correct:
        def create_list(length: int) -> List[int]:
            ...

        # Wrong:
        def create_list(length: int) -> List[
            int,
        ]:
            ...

    This rule checks argument and return type annotations.

    .. versionadded:: 0.6.0

    """

    error_template = 'Found multi-line function type annotation'
    code = 320


@final
class UppercaseStringModifierViolation(TokenizeViolation):
    """
    Forbids to use uppercase string modifiers.

    Reasoning:
        String modifiers should be consistent.

    Solution:
        Use lowercase modifiers should be written in lowercase.

    Example::

        # Correct:
        some_string = r'/regex/'
        some_bytes = b'123'

        # Wrong:
        some_string = R'/regex/'
        some_bytes = B'123'

    .. versionadded:: 0.6.0

    """

    error_template = 'Found uppercase string modifier: {0}'
    code = 321
