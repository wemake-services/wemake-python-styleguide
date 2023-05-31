"""
These checks limit Python's inconsistencies.

We can do the same things differently in Python.
For example, there are three ways to format a string.
There are several ways to write the same number.

We like our code to be consistent.
It is easier to work with your code base if you follow these rules.

So, we choose a single way to do things.
It does not mean that we choose the best way to do it.
But, we value consistency more than being 100% right
and we are ready to suffer all trade-offs that might come.

Once again, these rules are highly subjective, but we love them.

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
   ConstantCompareViolation
   CompareOrderViolation
   BadNumberSuffixViolation
   MultipleInCompareViolation
   UselessCompareViolation
   MissingSpaceBetweenKeywordAndParenViolation
   ConstantConditionViolation
   ObjectInBaseClassesListViolation
   MultipleContextManagerAssignmentsViolation
   ParametersIndentationViolation
   ExtraIndentationViolation
   WrongBracketPositionViolation
   MultilineFunctionAnnotationViolation
   UppercaseStringModifierViolation
   WrongMultilineStringViolation
   ModuloStringFormatViolation
   InconsistentReturnViolation
   InconsistentYieldViolation
   ImplicitStringConcatenationViolation
   UselessContinueViolation
   UselessNodeViolation
   UselessExceptCaseViolation
   UselessOperatorsViolation
   InconsistentReturnVariableViolation
   WalrusViolation
   ImplicitComplexCompareViolation
   ReversedComplexCompareViolation
   WrongLoopIterTypeViolation
   ExplicitStringConcatViolation
   MultilineConditionsViolation
   WrongMethodOrderViolation
   NumberWithMeaninglessZeroViolation
   PositiveExponentViolation
   WrongHexNumberCaseViolation
   ImplicitRawStringViolation
   BadComplexNumberSuffixViolation
   ZeroDivisionViolation
   MeaninglessNumberOperationViolation
   OperationSignNegationViolation
   VagueImportViolation
   LineStartsWithDotViolation
   RedundantSubscriptViolation
   AugmentedAssignPatternViolation
   UnnecessaryLiteralsViolation
   MultilineLoopViolation
   IncorrectYieldFromTargetViolation
   ConsecutiveYieldsViolation
   BracketBlankLineViolation
   IterableUnpackingViolation
   LineCompriseCarriageReturnViolation
   FloatZeroViolation
   UnpackingIterableToListViolation
   RawStringNotNeededViolation
   InconsistentComprehensionViolation
   AssignToSliceViolation

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
.. autoclass:: ConstantCompareViolation
.. autoclass:: CompareOrderViolation
.. autoclass:: BadNumberSuffixViolation
.. autoclass:: MultipleInCompareViolation
.. autoclass:: UselessCompareViolation
.. autoclass:: MissingSpaceBetweenKeywordAndParenViolation
.. autoclass:: ConstantConditionViolation
.. autoclass:: ObjectInBaseClassesListViolation
.. autoclass:: MultipleContextManagerAssignmentsViolation
.. autoclass:: ParametersIndentationViolation
.. autoclass:: ExtraIndentationViolation
.. autoclass:: WrongBracketPositionViolation
.. autoclass:: MultilineFunctionAnnotationViolation
.. autoclass:: UppercaseStringModifierViolation
.. autoclass:: WrongMultilineStringViolation
.. autoclass:: ModuloStringFormatViolation
.. autoclass:: InconsistentReturnViolation
.. autoclass:: InconsistentYieldViolation
.. autoclass:: ImplicitStringConcatenationViolation
.. autoclass:: UselessContinueViolation
.. autoclass:: UselessNodeViolation
.. autoclass:: UselessExceptCaseViolation
.. autoclass:: UselessOperatorsViolation
.. autoclass:: InconsistentReturnVariableViolation
.. autoclass:: WalrusViolation
.. autoclass:: ImplicitComplexCompareViolation
.. autoclass:: ReversedComplexCompareViolation
.. autoclass:: WrongLoopIterTypeViolation
.. autoclass:: ExplicitStringConcatViolation
.. autoclass:: MultilineConditionsViolation
.. autoclass:: WrongMethodOrderViolation
.. autoclass:: NumberWithMeaninglessZeroViolation
.. autoclass:: PositiveExponentViolation
.. autoclass:: WrongHexNumberCaseViolation
.. autoclass:: ImplicitRawStringViolation
.. autoclass:: BadComplexNumberSuffixViolation
.. autoclass:: ZeroDivisionViolation
.. autoclass:: MeaninglessNumberOperationViolation
.. autoclass:: OperationSignNegationViolation
.. autoclass:: VagueImportViolation
.. autoclass:: LineStartsWithDotViolation
.. autoclass:: RedundantSubscriptViolation
.. autoclass:: AugmentedAssignPatternViolation
.. autoclass:: UnnecessaryLiteralsViolation
.. autoclass:: MultilineLoopViolation
.. autoclass:: IncorrectYieldFromTargetViolation
.. autoclass:: ConsecutiveYieldsViolation
.. autoclass:: BracketBlankLineViolation
.. autoclass:: IterableUnpackingViolation
.. autoclass:: LineCompriseCarriageReturnViolation
.. autoclass:: FloatZeroViolation
.. autoclass:: UnpackingIterableToListViolation
.. autoclass:: RawStringNotNeededViolation
.. autoclass:: InconsistentComprehensionViolation
.. autoclass:: AssignToSliceViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    TokenizeViolation,
)


@final
class LocalFolderImportViolation(ASTViolation):
    """
    Forbid imports relative to the current folder.

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
    Forbid imports like ``import os.path``.

    Reasoning:
        There are too many ways to import something.
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
    Forbid ``u`` string prefix.

    Reasoning:
        We haven't needed this prefix since ``python2``,
        but it is still possible to find it in a codebase.

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
    Forbid underscores (``_``) in numbers.

    Reasoning:
        It is possible to write ``1000`` in three different ways:
        ``1_000``, ``10_00``, and ``100_0``.
        And it would be still the same number.
        Count how many ways there are to write bigger numbers.
        Currently, it all depends on the cultural habits of the author.
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
    Forbid partial floats like ``.05`` or ``23.``.

    Reasoning:
        Partial numbers are hard to read and they can be confused with
        other numbers. For example, it is really
        easy to confuse ``0.5`` and ``.05`` when reading
        through the source code.

    Solution:
        Use full versions with leading and trailing zeros.

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
    Forbid ``f`` strings.

    Reasoning:
        ``f`` strings implicitly rely on the context around them.
        Imagine that you have a string that breaks
        when you move it two lines above.
        That's not how a string should behave.
        Also, they promote a bad practice:
        putting your logic inside the template.
        Moreover, they do two things at once:
        declare a template and format it in a single action.

    Solution:
        Use ``.format()`` with indexed params instead.

    See also:
        https://github.com/xZise/flake8-string-format

    Example::

        # Correct:
        'Result is: {0}'.format(2 + 2)
        'Hey {user}! How are you?'.format(user='sobolevn')

        # Wrong:
        f'Result is: {2 + 2}'

    .. versionadded:: 0.1.0

    """

    error_template = 'Found `f` string'
    code = 305


@final
class RequiredBaseClassViolation(ASTViolation):
    """
    Forbid writing classes without base classes.

    Please, note that this rule has nothing to do with ``python2``.
    We care only about consistency here.

    Reasoning:
        We just need to decide how to do it.
        We need a single and unified rule about base classes.
        We have decided to stick to the explicit base class notation.
        Why? Because it is consistent with other use-cases.
        When we have a base class ``A``, we write ``class MyClass(A):``.
        When we have no base class, we have an implicit ``object`` base class.
        So, we still use the same syntax: ``class MyClass(object):``.

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
    Forbid multiple ``if`` statements inside list comprehensions.

    Reasoning:
        It is very hard to read multiple ``if`` statements inside
        a list comprehension. Since it is even hard to tell all of them
        should pass or fail.

    Solution:
        Use a single ``if`` statement inside list comprehensions.
        Use ``filter()`` if you have complicated logic.

    Example::

        # Correct:
        nodes = [node for node in html if node not in {'b', 'i'}]

        # Wrong:
        nodes = [node for node in html if node != 'b' if node != 'i']

    .. versionadded:: 0.1.0

    """

    error_template = 'Found list comprehension with multiple `if`s'
    code = 307


@final
class ConstantCompareViolation(ASTViolation):
    """
    Forbid comparing between two literals.

    Reasoning:
        When two constants are compared it is typically an indication of a
        mistake, since the Boolean value of the comparison, will always be
        the same.

    Solution:
        Remove the constant comparison and any associated dead code.

    Example::

        # Correct:
        do_something_else()

        # Wrong:
        if 60 * 60 < 1000:
            do_something()
        else:
            do_something_else()

    .. versionadded:: 0.3.0

    """

    error_template = 'Found constant comparison'
    code = 308


@final
class CompareOrderViolation(ASTViolation):
    """
    Forbid comparisons where the argument doesn't come first.

    Reasoning:
        It is hard to read the code when
        you have to shuffle the ordering of the arguments all the time.
        Bring consistency to the comparison!

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

    error_template = 'Found reversed compare order'
    code = 309


@final
class BadNumberSuffixViolation(TokenizeViolation):
    """
    Forbid uppercase ``X``, ``O``, ``B``, and ``E`` in numbers.

    Reasoning:
        Octal, hex, binary and scientific notation suffixes could
        be written in two possible notations: lowercase and uppercase
        which brings confusion and decreases code consistency and readability.
        We enforce a single way to write numbers with suffixes:
        suffix with lowercase chars.

    Solution:
        Octal, hex, binary and scientific notation suffixes in numbers
        should be written in lowercase.

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
class MultipleInCompareViolation(ASTViolation):
    """
    Forbid comparisons with multiple ``in`` checks.

    Reasoning:
        Using multiple ``in`` checks is unreadable.

    Solution:
        Refactor your comparison expression to use several ``and`` conditions
        or separate ``if`` statements in cases where it is appropriate.

    Example::

        # Correct:
        if item in bucket and bucket in master_list_of_buckets:
        if x_coord not in line and line not in square:

        # Wrong:
        if item in bucket in master_list_of_buckets:
        if x_cord not in line not in square:

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.10.0

    """

    error_template = 'Found multiple `in` compares'
    code = 311


@final
class UselessCompareViolation(ASTViolation):
    """
    Forbid comparisons of a variable to itself.

    Reasoning:
        When a variable is compared to itself, it is typically an indication
        of a mistake since the Boolean value of the comparison will always be
        the same.

    Solution:
        Remove the comparison and any associated dead code.

    Example::

        # Correct:
        do_something()

        # Wrong:
        if a < a:
            do_something()
        else:
            do_something_else()

    .. versionadded:: 0.3.0

    """

    error_template = 'Found comparison of a variable to itself'
    code = 312


@final
class MissingSpaceBetweenKeywordAndParenViolation(TokenizeViolation):
    """
    Enforce separation of parenthesis from keywords with spaces.

    Reasoning:
        Some people use ``return`` and ``yield`` keywords as functions.
        The same happened to good old ``print`` in Python2.

    Solution:
        Insert space symbol between the keyword and opening parenthesis.

    Example::

        # Correct:
        def func():
            a = 1
            del (a, b)
            yield (1, 2, 3)

        # Wrong:
        def func():
            a = 1
            b = 2
            del(a, b)
            yield(1, 2, 3)

    .. versionadded:: 0.3.0

    """

    error_template = 'Found parenthesis immediately after a keyword'
    code = 313


@final
class ConstantConditionViolation(ASTViolation):
    """
    Forbid using ``if`` statements that use invalid conditionals.

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

    error_template = 'Found conditional that always evaluates the same'
    code = 314


@final
class ObjectInBaseClassesListViolation(ASTViolation):
    """
    Forbid extra ``object`` in parent classes list.

    Reasoning:
        We should allow object only when
        we explicitly use it as a single parent class.
        When there is another class or there are multiple
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

    error_template = 'Found extra `object` in parent classes list'
    code = 315


@final
class MultipleContextManagerAssignmentsViolation(ASTViolation):
    """
    Forbid multiple assignment targets for context managers.

    Reasoning:
        It is hard to distinguish whether ``as`` should unpack into
        a tuple or if we are just using two context managers.

    Solution:
        Use several context managers or explicit brackets.

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
    Forbid incorrect indentation for parameters.

    Reasoning:
        It is really easy to spoil your perfect, readable code with
        incorrect multi-line parameters indentation.
        Since it is really easy to style them in any of 100 possible ways.
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

        # Correct complex case:

        @pytest.mark.parametrize(('boolean_arg', 'string_arg'), [
             (True, "string"),
             (False, "another string"),
        ])

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
    Forbid extra indentation.

    Reasoning:
        You can use extra indentation for lines of code.
        Python allows you to do that in case you want to keep the
        indentation level equal for this specific node,
        but that's insane!

    Solution:
        We should stick to 4 spaces for an indentation block.
        Each next block level should be indented by just 4 extra spaces.

    Example::

        # Correct:
        def test():
            print('test')

        # Wrong:
        def test():
                    print('test')

    This rule is consistent with the "Vertical Hanging Indent" option for
    ``multi_line_output`` setting of ``isort``. To avoid conflicting rules,
    you should set ``multi_line_output = 3`` in the ``isort`` settings.

    See also:
        https://github.com/timothycrosley/isort#multi-line-output-modes
        https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/isort.toml

    .. versionadded:: 0.6.0

    """

    error_template = 'Found extra indentation'
    code = 318


@final
class WrongBracketPositionViolation(TokenizeViolation):
    """
    Forbid brackets in the wrong position.

    Reasoning:
        You can do bizarre things with bracket positioning in python.
        We require all brackets to be consistent.

    Solution:
        Place bracket on the same line, in case of a single line expression.
        Or place the bracket on a new line in case of a multi-line expression.

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
    Forbid multi-line function type annotations.

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
    Forbid uppercase string modifiers.

    Reasoning:
        String modifiers should be consistent.

    Solution:
        Use lowercase string modifiers.

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


@final
class WrongMultilineStringViolation(TokenizeViolation):
    '''
    Forbid triple quotes for singleline strings.

    Reasoning:
        String quotes should be consistent.

    Solution:
        Use single quotes for single-line strings.
        Triple quotes are only allowed for real multiline strings.

    Example::

        # Correct:
        single_line = 'abc'
        multiline = """
            one
            two
        """

        # Wrong:
        some_string = """abc"""
        some_bytes = b"""123"""

    Docstrings are ignored from this rule.
    You must use triple quotes strings for docstrings.

    .. versionadded:: 0.7.0

    '''

    error_template = 'Found incorrect multi-line string'
    code = 322


@final
class ModuloStringFormatViolation(ASTViolation):
    """
    Forbid ``%`` formatting on strings.

    We check for string formatting. We try not to issue false positives.
    It is better for us to ignore a real (but hard to detect) case,
    then marking a valid one as incorrect.

    Internally we check for this pattern in string definitions::

        %[(name)] [flags] [width] [.precision] [{h | l}] type

    This is a ``C`` format specification.
    Related to :class:`~FormattedStringViolation` and solves the same problem.

    Reasoning:
        You must use a single formatting method across your project.

    Solution:
        We enforce to use string ``.format()`` method for this task.

    Example::

        # Correct:
        'some string', 'your name: {0}', 'data: {data}'

        # Wrong:
        'my name is: %s', 'data: %(data)d'

    It might be a good idea to disable this rule
    and switch to ``flake8-pep3101`` in case your project
    has a lot of false-positives due
    to some specific string chars that uses ``%`` a lot.

    See also:
        https://github.com/gforcada/flake8-pep3101
        https://msdn.microsoft.com/en-us/library/56e442dc.aspx
        https://docs.python.org/3/library/stdtypes.html#old-string-formatting
        https://pyformat.info/

    .. versionadded:: 0.14.0

    """

    error_template = 'Found `%` string formatting'
    code = 323


@final
class InconsistentReturnViolation(ASTViolation):
    """
    Enforce consistent ``return`` statements.

    Rules are:
    1. If any ``return`` has a value, all ``return`` nodes should have a value
    2. Do not place ``return`` without a value at the end of a function
    3. Do not use ``return None`` where just ``return`` is good enough

    This rule respects ``mypy`` style of placing ``return`` statements.
    There should be no conflict with these two checks.

    Reasoning:
        This is done for pure consistency and readability of your code.
        Eventually, this rule may also find some bugs in your code.

    Solution:
        Add or remove values from the ``return`` statements
        to make them consistent.
        Remove ``return`` statement from the function end.

    Example::

        # Correct:
        def function():
            if some:
                return 2
            return 1

        # Wrong:
        def function():
            if some:
                return
            return 1

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.16.0

    """

    error_template = 'Found inconsistent `return` statement'
    code = 324


@final
class InconsistentYieldViolation(ASTViolation):
    """
    Enforce consistent ``yield`` statements.

    Rules are:
    1. if any ``yield`` has a value, all ``yield`` nodes should have a value
    2. Use ``yield`` instead of ``yield None`` where possible

    This rule respects ``mypy`` style of placing ``yield`` statements.
    There should be no conflict with these two checks.

    Reasoning:
        This is done for pure consistency and readability of your code.
        Eventually, this rule may also find some bugs in your code.

    Solution:
        Add or remove values from the ``yield`` statements
        to make them consistent.

    Example::

        # Correct:
        def function():
            if some:
                yield 2
            yield 1

        # Wrong:
        def function():
            if some:
                yield
            yield 1

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.16.0

    """

    error_template = 'Found inconsistent `yield` statement'
    code = 325


@final
class ImplicitStringConcatenationViolation(TokenizeViolation):
    """
    Forbid implicit string concatenation.

    Reasoning:
        This is error-prone, since you can possibly miss a comma
        in a collection of strings and get an implicit concatenation.
        And because there are safer ways to do the same thing
        it is better to use them instead.

    Solution:
        Use ``+`` or ``.format()`` to join strings.

    Example::

        # Correct:
        text = 'first' + 'second'

        # Wrong:
        text = 'first' 'second'

    .. versionadded:: 0.7.0

    """

    error_template = 'Found implicit string concatenation'
    code = 326


@final
class UselessContinueViolation(ASTViolation):
    """
    Forbid meaningless ``continue`` in loops.

    Reasoning:
        Placing this keyword at the end of any loop won't make any difference
        to your code. And we prefer not to have meaningless
        constructs in our code.

    Solution:
        Remove useless ``continue`` from the loop.

    Example::

        # Correct:
        for number in [1, 2, 3]:
            if number < 2:
                continue
            print(number)

        for number in [1, 2, 3]:
            with suppress(Exception):
                do_smth(some_obj)

        # Wrong:
        for number in [1, 2, 3]:
            print(number)
            continue

        for number in [1, 2, 3]:
            try:
                do_smth(some_obj)
            except Exception:
                continue

    .. versionadded:: 0.7.0

    """

    error_template = 'Found useless `continue` at the end of the loop'
    code = 327


@final
class UselessNodeViolation(ASTViolation):
    """
    Forbid meaningless nodes.

    Reasoning:
        Some nodes might be completely useless. They will literally do nothing.
        Sometimes they are hard to find, because this situation can be caused
        by a recent refactoring or just by accident.
        This might be also an overuse of syntax.

    Solution:
        Remove node or make sure it makes sense.

    Example::

        # Wrong:
        for number in [1, 2, 3]:
            break

    .. versionadded:: 0.7.0

    """

    error_template = 'Found useless node: {0}'
    code = 328


@final
class UselessExceptCaseViolation(ASTViolation):
    """
    Forbid meaningless ``except`` cases.

    Reasoning:
        Using ``except`` cases that just reraise the same exception
        is error-prone. You can increase your stacktrace,
        silence some potential exceptions, and screw things up.
        It also does not make any sense to do so.

    Solution:
        Remove ``except`` case or make sure it makes sense.

    Example::

        # Correct:
        try:
            ...
        except IndexError:
            sentry.log()
            raise ValueError()

        try:
            ...
        except ValueError as exc:
            raise CustomReadableException from exc

        # Wrong:
        try:
            ...
        except TypeError:
            raise

    .. versionadded:: 0.7.0

    """

    error_template = 'Found useless `except` case'
    code = 329


@final
class UselessOperatorsViolation(ASTViolation):
    """
    Forbid unnecessary operators in your code.

    You can write: ``5.4`` and ``+5.4``. There's no need to use the second
    version. Similarly ``--5.4``, ``---5.4``, ``not not foo``, and ``~~42``
    contain unnecessary operators.

    Reasoning:
        This is done for consistency reasons.

    Solution:
        Omit unnecessary operators.

    Example::

        # Correct:
        profit = 3.33
        profit = -3.33
        inverse = ~5
        complement = not foo

        # Wrong:
        profit = +3.33
        profit = --3.33
        profit = ---3.33
        number = ~~42
        bar = not not foo

    .. versionadded:: 0.8.0

    """

    code = 330
    error_template = 'Found unnecessary operator: {0}'


@final
class InconsistentReturnVariableViolation(ASTViolation):
    """
    Forbid local variables that are only used in ``return`` statements.

    We also allow cases when a variable is assigned,
    then there are some other statements without direct variable access
    and the variable is returned.
    We reserve this use-case to be able
    to do some extra work before the function returns.

    We also allow the return of partial, sorted,
    or modified tuple items that are defined just above.

    Reasoning:
        This is done for consistency and more readable source code.

    Solution:
        Return the expression itself, instead of creating a temporary variable.

    Example::

        # Correct:
        def some_function():
            return 1

        def other_function():
            some_value = 1
            do_something(some_value)
            return some_value

        # Wrong:
        def some_function():
            some_value = 1
            return some_value


    .. versionadded:: 0.9.0
    .. versionchanged:: 0.14.0

    """

    error_template = 'Found variables that are only used for `return`: {0}'
    code = 331


@final
class WalrusViolation(ASTViolation):
    """
    Forbid walrus operator.

    Reasoning:
        Code with ``:=`` is hardly readable.
        It has big problems with scoping and reading order.
        And it can lead to a huge mess inside your code.
        Python is not expression-based.

    Solution:
        Don't use fancy stuff, use good old assignments.

    Example::

        # Correct:
        some = call()
        if some:
            print(some)

        # Wrong:
        if some := call():
            print(some)

    .. versionadded:: 0.14.0

    """

    error_template = 'Found walrus operator'
    code = 332


@final
class ImplicitComplexCompareViolation(ASTViolation):
    """
    Forbid implicit complex comparison expressions.

    Reasoning:
        Two comparisons in python that are joined with ``and`` operator
        mean that you have a complex comparison with tree operators.

    Solution:
        Refactor your comparison without ``and`` but with the third operator.
        Notice that you might have to change the ordering.

    Example::

        # Correct:
        if three < two < one:
            ...

        # Wrong:
        if one > two and two > three:
            ...

    .. versionadded:: 0.10.0

    """

    code = 333
    error_template = 'Found implicit complex compare'


@final
class ReversedComplexCompareViolation(ASTViolation):
    """
    Forbid reversed order complex comparison expressions.

    Reasoning:
        Comparisons where comparators start from the lowest element
        are easier to read than one that start from the biggest one.
        It is also possible to write the same expression
        in two separate way, which is inconsistent.

    Solution:
        Reverse the order, so the smallest element comes first
        and the biggest one comes last.

    Example::

        # Correct:
        if three < two < one:
            ...

        # Wrong:
        if one > two > three:
            ...

    .. versionadded:: 0.10.0

    """

    code = 334
    error_template = 'Found reversed complex comparison'


@final
class WrongLoopIterTypeViolation(ASTViolation):
    """
    Forbid wrong ``for`` loop iter targets.

    We forbid to use:

    - Lists and list comprehensions
    - Sets and set comprehensions
    - Dicts and dict comprehensions
    - Generator expressions
    - Empty tuples

    Reasoning:
        Using lists, dicts, and sets do not make much sense.
        You can use tuples instead.
        Using comprehensions implicitly creates a two level loop,
        that is hard to read and deal with.

    Solution:
        Use tuples to create explicit iterables for ``for`` loops.
        In case you are using a comprehension, create a new variable.

    Example::

        # Correct:
        for person in ('Kim', 'Nick'):
            ...

        # Wrong:
        for person in ['Kim', 'Nick']:
            ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.12.0

    """

    code = 335
    error_template = 'Found incorrect `for` loop iter type'


@final
class ExplicitStringConcatViolation(ASTViolation):
    """
    Forbid explicit string concatanation in favour of ``.format`` method.

    However, we still allow multiline string concatanation
    as a way to write long strings that does not fit the 80-chars rule.

    Reasoning:
        When formatting strings one must use ``.format``
        and not any other formatting methods like ``%``, ``+``, or ``f``.
        This is done for consistency reasons.

    Solution:
        Join strings together if you can, or use ``.format`` method.

    Example::

        # Correct:
        x = 'ab: {0}'.format(some_data)

        # Wrong:
        x = 'a' + 'b: ' + some_data

    .. versionadded:: 0.12.0

    """

    code = 336
    error_template = 'Found explicit string concatenation'


@final
class MultilineConditionsViolation(ASTViolation):
    """
    Forbid multiline conditions.

    Reasoning:
        This way of writing conditions hides the inner complexity this line has
        and it decreases readability of the code.

    Solution:
        Divide multiline conditions to some ``if`` condition or use variables.

    Example::

        # Correct:
        if isinstance(node.test, ast.UnaryOp):
            if isinstance(node.test.op, ast.Not):
                ...

        # Wrong:
        if isinstance(node.test, ast.UnaryOp) and isinstance(
            node.test.op,
            ast.Not,
        ):
            ...

    .. versionadded:: 0.9.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found multiline conditions'
    code = 337
    previous_codes = {465}


@final
class WrongMethodOrderViolation(ASTViolation):
    """
    Forbid incorrect order of methods inside a class.

    We follow the same ordering:

    - ``__init_subclass__``
    - ``__new__``
    - ``__init__``
    - ``__call__``
    - ``__await__``
    - public and magic methods
    - protected methods
    - private methods (we discourage using them)

    We follow "Newspaper order" where the most important things come first.

    Reasoning:
        It is hard to read classes where API declarations are bloated with
        implementation details. We need to see the important stuff first,
        then we can go deeper in case we are interested.

    Solution:
        Reorder methods inside your class to match our format.

    .. versionadded:: 0.12.0

    """

    error_template = 'Found incorrect order of methods in a class'
    code = 338


@final
class NumberWithMeaninglessZeroViolation(TokenizeViolation):
    """
    Forbid meaningless zeros.

    We discourage using meaningless zeros in
    float, binary, octal, hex, and exponential numbers.

    Reasoning:
        There are ~infinite ways to write these numbers
        by adding meaningless leading zeros to the number itself.
        ``0b1`` is the same as ``0b01`` and ``0b001``.
        How can a language be called consistent
        if you can write numbers in an infinite ways?
        It hurts readability and understanding of your code.

    Solution:
        Remove meaningless leading zeros.

    Example::

        # Correct:
        numbers = [1.5, 0b1, 0o2, 0x5, 10e10]

        # Wrong:
        numbers = [1.50, 0b00000001, 0o0002, 0x05, 10e010]

    .. versionadded:: 0.12.0

    """

    error_template = 'Found number with meaningless zeros: {0}'
    code = 339


@final
class PositiveExponentViolation(TokenizeViolation):
    """
    Forbid extra ``+`` signs in the exponent.

    Reasoning:
        Positive exponent is positive by default,
        there's no need to write an extra ``+`` sign.
        We enforce consistency with this rule.

    Solution:
        Remove meaningless ``+`` sign from the exponent.

    Example::

        # Correct:
        number = 1e1 + 1e-1

        # Wrong:
        number = 1e+1

    .. versionadded:: 0.12.0

    """

    error_template = 'Found exponent number with positive exponent: {0}'
    code = 340


@final
class WrongHexNumberCaseViolation(TokenizeViolation):
    """
    Forbid letters as hex numbers.

    Reasoning:
        One can write ``0xA`` and ``0xa`` which is inconsistent.
        This rule enforces upper-case letters in hex numbers.

    Solution:
        Use uppercase letters in hex numbers.

    Example::

        # Correct:
        number = 0xABCDEF

        # Wrong:
        number = 0xabcdef

    .. versionadded:: 0.12.0

    """

    error_template = 'Found wrong hex number case: {0}'
    code = 341


@final
class ImplicitRawStringViolation(TokenizeViolation):
    r"""
    Forbid ``\\`` escape sequences inside regular strings.

    Reasoning:
        It is hard to read escape sequences inside regular strings,
        because they use ``\\`` double backslash for a single character escape.

    Solution:
        Use raw strings ``r''`` to rewrite
        the escape sequence with a ``\`` single backslash.

    Example::

        # Correct:
        escaped = [r'\n', '\n']

        # Wrong:
        escaped = '\\n'

    .. versionadded:: 0.12.0

    """

    error_template = 'Found implicit raw string: {0}'
    code = 342


@final
class BadComplexNumberSuffixViolation(TokenizeViolation):
    """
    Forbid uppercase complex number suffix.

    Reasoning:
        Numbers should be consistent.

    Solution:
        Use lowercase suffix for imaginary part.

    Example::

        # Correct:
        complex_number = 1j

        # Wrong:
        complex_number = 1J

    .. versionadded:: 0.12.0

    """

    error_template = 'Found wrong complex number suffix: {0}'
    code = 343


@final
class ZeroDivisionViolation(ASTViolation):
    """
    Forbid explicit division (or modulo) by zero.

    Reasoning:
        This will just throw ``ZeroDivisionError``.
        If that's what you need: just throw it.
        No need to use undefined math behaviours.
        Or it might be just a typo / mistake, then fix it.

    Solution:
        Use ``ZeroDivisionError`` or make your number something besides ``0``.

    Example::

        # Correct:
        raise ZeroDivisionError()

        # Wrong:
        1 / 0
        1 % 0

    .. versionadded:: 0.12.0
    .. versionchanged: 0.15.0

    """

    error_template = 'Found explicit zero division'
    code = 344


@final
class MeaninglessNumberOperationViolation(ASTViolation):
    """
    Forbid meaningless math operations with ``0`` and ``1``.

    Reasoning:
        Adding and subtracting zero does not change the value.
        There's no need to do that.
        Multiplying by zero is also redundant:
        it can be replaced with explicit ``0`` assign.
        Multiplying and dividing by ``1`` is also meaningless.
        Likewise, using ``|`` or ``^`` with ``0``, and using
        the ``%`` operator with ``1`` are unnecessary.

    Solution:
        Remove useless operations.

    Example::

        # Correct:
        number = 1
        zero = 0
        one = 1
        three = 3

        # Wrong:
        number = 1 + 0 * 1
        zero = some * 0 / 1
        one = some ** 0 ** 1
        three = 3 ^ 0
        three = 3 | 0
        three = 3 % 1

    .. versionadded:: 0.12.0
    .. versionchanged:: 0.15.0

    """

    error_template = 'Found meaningless number operation'
    code = 345


@final
class OperationSignNegationViolation(ASTViolation):
    """
    Forbid double minus operations.

    Reasoning:
        Having two operations is harder than having just one.
        Two negations are harder than one positive expression.
        Two negations equal to one positive expression.
        Positive and negative equal to one negative.

    Solution:
        Replace double minus operation to a single one with plus.
        Replace 'plus-minus' operation to a single one with minus.

    Example::

        # Correct:
        number = 3 + 1
        number += 6
        number -= 2

        # Wrong:
        number = 3 - -1
        number -= -6
        number += -2

    .. versionadded:: 0.12.0

    """

    error_template = 'Found wrong operation sign'
    code = 346


@final
class VagueImportViolation(ASTViolation):
    """
    Forbid imports that may cause confusion outside of the module.

    Names that we forbid to import:

    - Common names like ``dumps`` and ``loads``
    - Names starting with ``to_`` and ``from_``
    - Too short names like ``Q`` or ``F``, but we are fine with ``_``

    Reasoning:
        See ``datetime.*`` in code? You know that it's from datetime.
        See ``BaseView`` in a Django project? You know where it is from.
        See ``loads``? It can be anything: ``yaml``, ``toml``, ``json``, etc.
        We are also enforcing consistency with our naming too-short rules here.

    Solution:
        Use package level imports or import aliases.

    See
    :py:data:`~wemake_python_styleguide.constants.VAGUE_IMPORTS_BLACKLIST`
    for the full list of bad import names.

    Example::

        # Correct:
        import json
        import dumps  # package names are not checked
        from json import loads as json_loads

        # Wrong:
        from json import loads

    .. versionadded:: 0.13.0
    .. versionchanged:: 0.14.0

    """

    error_template = 'Found vague import that may cause confusion: {0}'
    code = 347


@final
class LineStartsWithDotViolation(TokenizeViolation):
    """
    Forbid starting lines with a dot.

    Reasoning:
        We enforce strict consistency rules about how to break lines.
        We also enforce strict rules about multi-line parameters.
        Starting new lines with the dot means that this rule is broken.

    Solution:
        Use ``()`` to break lines in a complex expression.

    Example::

        # Correct:
        some = MyModel.objects.filter(
            ...,
        ).exclude(
            ...,
        ).annotate(
            ...,
        )

        # Wrong:
        some = (
            MyModel.objects.filter(...)
                .exclude(...)
                .annotate(...)
        )

    .. versionadded:: 0.13.0

    """

    error_template = 'Found a line that starts with a dot'
    code = 348


@final
class RedundantSubscriptViolation(ASTViolation):
    """
    Forbid redundant components in a subscript's slice.

    Reasoning:
        We do it for consistency reasons.

    Example::

        # Correct:
        array[:7]
        array[3:]

        # Wrong:
        x[0:7]
        x[3:None]

    .. versionadded:: 0.13.0

    """

    error_template = 'Found redundant subscript slice'
    code = 349


@final
class AugmentedAssignPatternViolation(ASTViolation):
    """
    Enforce using augmented assign pattern.

    Reasoning:
        ``a += b`` is short and correct version of ``a = a + b``.
        Why not using the short version?

    Example::

        # Correct:
        a += b

        # Wrong:
        a = a + b

    .. versionadded:: 0.13.0

    """

    error_template = 'Found usable augmented assign pattern'
    code = 350


@final
class UnnecessaryLiteralsViolation(ASTViolation):
    """
    Forbid unnecessary literals in your code.

    Reasoning:
        We discourage using primitive calls to get default type values.
        There are better ways to get these values.

    Solution:
        Use direct default values of the given type

    Example::

        # Correct:
        default = 0

        # Wrong:
        default = int()

    .. versionadded:: 0.13.0

    """

    error_template = 'Found unnecessary literals'
    code = 351


@final
class MultilineLoopViolation(ASTViolation):
    """
    Forbid multiline loops.

    Reasoning:
        It decreased the readability of the code.

    Solution:
        Use single line loops and create new variables
        in case you need to fit too many logic inside the loop definition.

    Example::

        # Correct:
        for num in some_function(arg1, arg2):
            ...

        # Wrong:
        for num in range(
            arg1,
            arg2,
        ):
            ...

    .. versionadded:: 0.13.0

    """

    error_template = 'Found multiline loop'
    code = 352


@final
class IncorrectYieldFromTargetViolation(ASTViolation):
    """
    Forbid ``yield from`` with several nodes.

    We allow to ``yield from`` tuples,
    names, attributes, calls, and subscripts.

    Reasoning:
        We enforce consistency when yielding values
        from tuple instead of any other types.
        It also might be an error when you try to ``yield from`` something
        that is not iterable.

    Solution:
        Use allowed node types with ``yield from``.

    Example::

        # Correct:
        yield from (1, 2, 3)
        yield from some

        # Wrong:
        yield from [1, 2, 3]

    .. versionadded:: 0.13.0

    """

    error_template = 'Found incorrect `yield from` target'
    code = 353


@final
class ConsecutiveYieldsViolation(ASTViolation):
    """
    Forbid consecutive ``yield`` expressions.

    We raise this violation when we find at least
    two consecutive ``yield`` expressions.

    Reasoning:
        One can write multiple ``yield`` nodes in a row.
        That's inconsistent. Because we have ``yield from`` form.

    Solution:
        It can be easily changed to ``yield from (...)`` format.

    .. versionadded:: 0.13.0

    """

    error_template = 'Found consecutive `yield` expressions'
    code = 354


@final
class BracketBlankLineViolation(TokenizeViolation):
    """
    Forbid useless blank lines before and after brackets.

    Reasoning:
        We do this for consistency.

    Solution:
        Remove blank lines from the start and from the end of a collection.

    Example::

        # Correct:
        arr = [
            1,
            2,
        ]

        # Wrong:
        arr = [

            1,
            2,

        ]

    .. versionadded:: 0.13.0

    """

    error_template = 'Found an unnecessary blank line before a bracket'
    code = 355


@final
class IterableUnpackingViolation(ASTViolation):
    """
    Forbid unnecessary iterable unpacking.

    Reasoning:
        We do this for consistency.

    Solution:
        Do not use iterable unpacking when it's not necessary.

    Example::

        # Correct:
        [1, *numbers, 99]
        {*iterable, *other_iterable}
        list(iterable)
        first, *iterable = other_iterable

        # Wrong:
        [*iterable]
        *iterable, = other_iterable

    .. versionadded:: 0.13.0

    """

    error_template = 'Found an unnecessary iterable unpacking'
    code = 356


@final
class LineCompriseCarriageReturnViolation(TokenizeViolation):
    r"""
    Forbid using ``\r`` (carriage return) in line breaks.

    Reasoning:
        We enforce Unix-style newlines.
        We only use newlines (``\n``), not carriage returns.
        So ``\r`` line breaks not allowed in code.

    Solution:
        Use only ``\n`` (not ``\r\n`` or ``\r``) to break lines.

    .. versionadded:: 0.14.0

    """

    error_template = r'Found a ``\r`` (carriage return) line break'
    code = 357


@final
class FloatZeroViolation(TokenizeViolation):
    """
    Forbid using float zeros: ``0.0``.

    Reasoning:
        Float zeros can be used as variable values which may lead to
        typing bugs when trying to perform an operation between
        an int number and the float zero.

    Solution:
        Use int zeros (0). If a float is needed, it should be cast
        explicitly.

    Example::

        # Correct:
        zero = 0

        # Wrong:
        zero = 0.0

    .. versionadded:: 0.15.0

    """

    code = 358
    error_template = 'Found a float zero (0.0)'


@final
class UnpackingIterableToListViolation(ASTViolation):
    """
    Forbids to unpack iterable objects to lists.

    Reasoning:
        We do this for consistency.

    Solution:
        Do not unpack iterables to lists, use tuples for that.

    Example::

        # Correct:
        first, second = (7, 4)
        first, *iterable = other_iterable

        # Wrong:
        [first, second] = (7, 4)
        [first, *iterable] = other_iterable

    .. versionadded:: 0.15.0

    """

    error_template = 'Found an iterable unpacking to list'
    code = 359


@final
class RawStringNotNeededViolation(TokenizeViolation):
    r"""
    Forbid the use of raw strings when there is no backslash in the string.

    Reasoning:
        Raw string are only needed when dealing with ``\`` in the string.

    Solution:
        Do not prefix the string with ``r``. Use a normal string instead.

    Example::

        # Correct:
        r'This is a correct use \n'

        # Wrong:
        r'This string should not be prefixed with r.'

    .. versionadded:: 0.15.0

    """

    error_template = 'Found an unnecessary use of a raw string: {0}'
    code = 360


@final
class InconsistentComprehensionViolation(TokenizeViolation):
    """
    Forbids inconsistent newlines in comprehensions.

    Reasoning:
        We do this for consistency.

    Solution:
        Either place comprehension on a single line or ensure that action,
        for loops, and condition are all on different lines.

    Example::

        # Correct:
        list = [some(number) for number in numbers]

        list = [
           some(number)
           for numbers in matrix
           for number in numbers
           if number > 0
        ]

        # Wrong:
        list = [
            some(number) for number in numbers
            if number > 0
        ]

    .. versionadded:: 0.15.0

    """

    error_template = 'Found an inconsistently structured comprehension'
    code = 361


@final
class AssignToSliceViolation(ASTViolation):
    """
    Forbid assignment to a subscript slice.

    Reasoning:
        Assignment to a slice may lead to a list changing its size
        implicitly and strangely which makes it hard to spot bugs.

    Solution:
        Use explicit index assignment in place of slice assignment.

    Why you may disable or inline-ignore this rule?

    The quite common and useful example which violates this rule
    is inplace list replacement via ``[:]`` - this helps
    to keep the same object reference while it content could be completely
    erased or replaced with the new one.

    One more thing: slice assignment is the only way
    for inplace array multiple replacement when you need that.

    Example::

        # Correct:
        a[5] = 1

        # Wrong:
        a[1:3] = [1, 2]
        a[slice(1)] = [1, 3]

    .. versionadded:: 0.15.0

    """

    error_template = 'Found assignment to a subscript slice'
    code = 362
