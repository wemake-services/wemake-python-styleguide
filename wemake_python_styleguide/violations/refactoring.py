# -*- coding: utf-8 -*-

"""
These checks ensure that you don't have patterns that can be refactored.

There are so many ways of doing the same thing in Python.
Here we collect know patterns that can be rewritten into
much easier or just more pythonic version.

.. currentmodule:: wemake_python_styleguide.violations.refactoring

Summary
-------

.. autosummary::
   :nosignatures:

   UselessLoopElseViolation
   UselessFinallyViolation
   SimplifiableIfViolation
   UselessReturningElseViolation
   NegatedConditionsViolation
   NestedTryViolation
   UselessLambdaViolation
   UselessLenCompareViolation
   NotOperatorWithCompareViolation
   NestedTernaryViolation
   WrongInCompareTypeViolation
   UnmergedIsinstanceCallsViolation
   WrongIsinstanceWithTupleViolation
   ImplicitElifViolation
   ImplicitInConditionViolation
   OpenWithoutContextManagerViolation
   TypeCompareViolation
   PointlessStarredViolation
   ImplicitEnumerateViolation
   ImplicitSumViolation
   FalsyConstantCompareViolation
   WrongIsCompareViolation

Refactoring opportunities
-------------------------

.. autoclass:: UselessLoopElseViolation
.. autoclass:: UselessFinallyViolation
.. autoclass:: SimplifiableIfViolation
.. autoclass:: UselessReturningElseViolation
.. autoclass:: NegatedConditionsViolation
.. autoclass:: NestedTryViolation
.. autoclass:: UselessLambdaViolation
.. autoclass:: UselessLenCompareViolation
.. autoclass:: NotOperatorWithCompareViolation
.. autoclass:: NestedTernaryViolation
.. autoclass:: WrongInCompareTypeViolation
.. autoclass:: UnmergedIsinstanceCallsViolation
.. autoclass:: WrongIsinstanceWithTupleViolation
.. autoclass:: ImplicitElifViolation
.. autoclass:: ImplicitInConditionViolation
.. autoclass:: OpenWithoutContextManagerViolation
.. autoclass:: TypeCompareViolation
.. autoclass:: PointlessStarredViolation
.. autoclass:: ImplicitEnumerateViolation
.. autoclass:: ImplicitSumViolation
.. autoclass:: FalsyConstantCompareViolation
.. autoclass:: WrongIsCompareViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    TokenizeViolation,
)


@final
class UselessLoopElseViolation(ASTViolation):
    """
    Forbids to use ``else`` without ``break`` in a loop.

    We use the same logic for ``for`` and ``while`` loops.

    Reasoning:
        When there's no ``break`` keyword in loop's body it means
        that ``else`` will always be called.
        This rule will reduce complexity, improve readability,
        and protect from possible errors.

    Solution:
        Refactor your ``else`` case logic to be inside the loop's body.
        Or right after it.

    Example::

        # Correct:
        for letter in 'abc':
            if letter == 'b':
                break
        else:
            print('"b" is not found')

        for letter in 'abc':
            print(letter)
        print('always called')

        # Wrong:
        for letter in 'abc':
            print(letter)
        else:
            print('always called')

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found `else` in a loop without `break`'
    code = 500
    previous_codes = {436}


@final
class UselessFinallyViolation(ASTViolation):
    """
    Forbids to use ``finally`` in ``try`` block without ``except`` block.

    Reasoning:
        This rule will reduce complexity and improve readability.

    Solution:
        Refactor your ``try`` logic.
        Replace the ``try-finally`` statement with a ``with`` statement.

    Example::

        # Correct:
        with open("filename") as f:
            f.write(...)

        # Wrong:
        try:
            f = open("filename")
            f.write(...)
        finally:
            f.close()

    .. versionadded:: 0.3.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found `finally` in `try` block without `except`'
    code = 501
    previous_codes = {437}


@final
class SimplifiableIfViolation(ASTViolation):
    """
    Forbids to have simplifiable ``if`` conditions.

    Reasoning:
        This complex construction can cause frustration among other developers.
        It is longer, more verbose, and more complex.

    Solution:
        Use ``bool()`` to convert test values to boolean values.
        Or just leave it as it is in case
        when your test already returns a boolean value.
        Use can also use ``not`` keyword to switch boolean values.

    Example::

        # Correct:
        my_bool = bool(some_call())
        other_value = 8 if some_call() else None

        # Wrong:
        my_bool = True if some_call() else False

    We only check ``if`` nodes where ``True`` and ``False`` values are used.
    We check both ``if`` nodes and ``if`` expressions.

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found simplifiable `if` condition'
    code = 502
    previous_codes = {451}


@final
class UselessReturningElseViolation(ASTViolation):
    """
    Forbids to use useless ``else`` cases in returning functions.

    We check single ``if`` statements that all contain
    ``return`` or ``raise`` or ``break`` statements with this rule.
    We do not check ``if`` statements with ``elif`` cases.

    Reasoning:
        Using extra ``else`` creates a situation when
        the whole node could and should be dropped
        without any changes in logic.
        So, we prefer to have less code than more code.

    Solution:
        Remove useless ``else`` case.

    Example::

        # Correct:
        def some_function():
            if some_call():
                return 'yeap'
            return 'nope'

        # Wrong:
        def some_function():
            if some_call():
                raise ValueError('yeap')
            else:
                raise ValueError('nope')

    .. versionadded:: 0.7.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found useless returning `else` statement'
    code = 503
    previous_codes = {457}


@final
class NegatedConditionsViolation(ASTViolation):
    """
    Forbids to use negated conditions together with ``else`` clause.

    Reasoning:
        It easier to read and name regular conditions. Not negated ones.

    Solution:
        Move actions from the negated ``if`` condition to the ``else``
        condition.

    Example::

        # Correct:
        if some == 1:
             ...
        else:
             ...

        if not some:
             ...

        # Wrong:
        if not some:
             ...
        else:
             ...

    .. versionadded:: 0.8.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found negated condition'
    code = 504
    previous_codes = {463}


@final
class NestedTryViolation(ASTViolation):
    """
    Forbids to use nested ``try`` blocks.

    Notice, we check all possible slots for ``try`` block:
    1. the ``try`` block itself
    2. all ``except`` cases
    3. ``else`` case
    4. and ``finally`` case

    Reasoning:
        Nesting ``try`` blocks indicates
        that something really bad happens to your logic.
        Why does it require two separate exception handlers?
        It is a perfect case to refactor your code.

    Solution:
        Collapse two exception handlers together.
        Or create a separate function that will handle this second nested case.

    Example::

        # Wrong:
        try:
            try:
                ...
            except SomeException:
                ...
        except SomeOtherException:
            ...

        try:
            ...
        except SomeOtherException:
            try:
                ...
            except SomeException:
                ...

    .. versionadded:: 0.8.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found nested `try` block'
    code = 505
    previous_codes = {464}


@final
class UselessLambdaViolation(ASTViolation):
    """
    Forbids to define useless proxy ``lambda`` expressions.

    Reasoning:
        Sometimes developers tend to overuse ``lambda`` expressions
        and they wrap code that can be passed as is, without extra wrapping.
        The code without extra ``lambda`` is easier
        to read and is more performant.

    Solution:
        Remove wrapping ``lambda`` declaration, use just the internal function.

    Example::

        # Correct:
        numbers = map(int, ['1', '2'])

        # Wrong:
        numbers = map(lambda string: int(string), ['1', '2'])

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found useless lambda declaration'
    code = 506
    previous_codes = {467}


@final
class UselessLenCompareViolation(ASTViolation):
    """
    Forbids to have unpythonic zero-length compare.

    Note, that we allow to check arbitrary length, like ``len(arr) == 3``.

    Reasoning:
        Python's structures like dicts, lists, sets, and tuples
        all have ``__bool__`` method to checks their length.
        So, there's no point in wrapping them into ``len(...)``
        and checking that it is bigger that ``0`` or less then ``1``, etc.

    Solution:
        Remove extra ``len()`` call.

    Example::

        # Correct:
        if some_array or not other_array or len(third_array) == 1:
            ...

        # Wrong:
        if len(some_array) > 0 or len(other_array) < 1:
            ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found useless `len()` compare'
    code = 507
    previous_codes = {468}


@final
class NotOperatorWithCompareViolation(ASTViolation):
    """
    Forbids to use ``not`` with compare expressions.

    Reasoning:
        This version of ``not`` operator is unreadable.

    Solution:
        Refactor the expression without ``not`` operator.
        Change the compare signs.

    Example::

        # Correct:
        if x <= 5:
            ...

        # Wrong:
        if not x > 5:
            ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found incorrect `not` with compare usage'
    code = 508
    previous_codes = {470}


@final
class NestedTernaryViolation(ASTViolation):
    """
    Forbids to nest ternary expressions in some places.

    Note, that we restrict to nest ternary expressions inside:

    - ``if`` conditions
    - boolean and binary operations like ``and`` or ``+``
    - unary operators

    Reasoning:
        Nesting ternary in random places can lead to very hard
        debug and testing problems.

    Solution:
        Refactor the ternary expression to be either a new variable,
        or nested ``if`` statement, or a new function.

    Example::

        # Correct:
        some = x if cond() else y

        # Wrong:
        if x if cond() else y:
            ...

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found incorrectly nested ternary'
    code = 509
    previous_codes = {472}


@final
class WrongInCompareTypeViolation(ASTViolation):
    """
    Forbids to use ``in`` with static containers except ``set`` nodes.

    We enforce people to use sets as a static containers.
    You can also use variables, calls, methods, etc.
    Dynamic values are not checked.

    Reasoning:
        Using static ``list``, ``tuple``, or ``dict`` elements
        to check that some element is inside the container is a bad practice.
        Because we need to iterate all over the container to find the element.
        Sets are the best suit for this task.
        Moreover, it makes your code consistent.

    Solution:
        Use ``set`` elements or comprehensions to check that something
        is contained in a container.

    Example::

        # Correct:
        print(needle in {'one', 'two'})

        # Wrong:
        print(needle in ['one', 'two'])

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found `in` used with a non-set container'
    code = 510
    previous_codes = {473}


@final
class UnmergedIsinstanceCallsViolation(ASTViolation):
    """
    Forbids to multiple ``isinstance`` calls with the same variable.

    Reasoning:
        The best practice is to use ``isinstance`` with tuple
        as the second argument, instead of multiple conditions
        joined with ``or``.

    Solution:
        Use tuple of types as the second argument.

    Example::

        # Correct:
        isinstance(some, (int, float))

        # Wrong:
        isinstance(some, int) or isinstance(some, float)

    See also:
        https://docs.python.org/3/library/functions.html#isinstance

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = (
        'Found separate `isinstance` calls that can be merged for: {0}'
    )
    code = 511
    previous_codes = {474}


@final
class WrongIsinstanceWithTupleViolation(ASTViolation):
    """
    Forbids to multiple ``isinstance`` calls with tuples of a single item.

    Reasoning:
        There's no need to use tuples with single elements.
        You can use single variables or tuples with multiple elements.

    Solution:
        Use tuples with multiple elements or a single varaible.

    Example::

        # Correct:
        isinstance(some, (int, float))
        isisntance(some, int)

        # Wrong:
        isinstance(some, (int, ))

    See: https://docs.python.org/3/library/functions.html#isinstance

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.11.0

    """

    error_template = 'Found `isinstance` call with a single element tuple'
    code = 512
    previous_codes = {475}


@final
class ImplicitElifViolation(TokenizeViolation):
    """
    Forbids to have implicit ``elif`` conditions.

    Reasoning:
        Nested ``if`` in ``else`` cases are bad
        for readability because of the nesting level.

    Solution:
        Use ``elif`` on the same level.

    Example::

        # Correct:
        if some:
            ...
        elif other:
            ...

        # Wrong:
        if some:
            ...
        else:
            if other:
                ...

    .. versionadded:: 0.12.0

    """

    error_template = 'Found implicit `elif` condition'
    code = 513


@final
class ImplicitInConditionViolation(ASTViolation):
    """
    Forbids to use multiple equality compare with the same variable name.

    Reasoning:
        Using double+ equality compare with ``or``
        or double+ non-equality compare with ``and``
        indicates that you have implicit ``in`` or ``not in`` condition.
        It is just hidden from you.

    Solution:
        Refactor compares to use ``in`` or ``not in`` clauses.


    Example::

        # Correct:
        print(some in {'first', 'second'})
        print(some not in {'first', 'second'})

        # Wrong:
        print(some == 'first' or some == 'second')
        print(some != 'first' and some != 'second')

    .. versionadded:: 0.10.0
    .. versionchanged:: 0.12.0

    """

    code = 514
    error_template = 'Found implicit `in` condition'
    previous_codes = {336}


@final
class OpenWithoutContextManagerViolation(ASTViolation):
    """
    Forbids to use ``open()`` with a context manager.

    Reasoning:
        When you ``open()`` something, you need to close it.
        When using a context manager - it is automatically done for you.
        When not using it - you might find yourself in a situation
        when file is not closed and is not accessable anymore.

    Solution:
        Refactor ``open()`` call to use ``with``.

    Example::

        # Correct:
        with open(filename) as file_obj:
            ...

        # Wrong:
        file_obj = open(filename)

    .. versionadded:: 0.12.0

    """

    code = 515
    error_template = 'Found `open()` used without a context manager'


@final
class TypeCompareViolation(ASTViolation):
    """
    Forbids to compare types with ``type()`` function.

    Reasoning:
        When you compare types with ``type()`` function call
        it means that you break polymorphism and dissallow child classes
        of a node to work here. That's incorrect.

    Solution:
        Use ``isinstance`` to compare types.

    Example::

        # Correct:
        print(something, type(something))

        # Wrong:
        if type(something) == int:
            ...

    .. versionadded:: 0.12.0

    """

    code = 516
    error_template = 'Found `type()` used to compare types'


@final
class PointlessStarredViolation(ASTViolation):
    """
    Forbids to have useless starred expressions.

    Reasoning:
        Using starred expression with constants is useless.
        This piece of code can be rewritten to be flat.
        Eg.: ``print(*[1, 2, 3])`` is ``print(1, 2, 3)``.

    Solution:
        Refactor your code not to use starred expressions
        with ``list``, ``dict``, ``tuple``, and ``set`` constants.
        Use regular argument passing instead.

    Example::

        # Correct:
        my_list = [1, 2, 3, *other_iterable]

        # Wrong:
        print(*[1, 2, 3], **{{}})

    .. versionadded:: 0.12.0

    """

    code = 517
    error_template = 'Found pointless starred expression'


@final
class ImplicitEnumerateViolation(ASTViolation):
    """
    Forbids to have implicit ``enumerate()`` calls.

    Reasoning:
        Using ``range(len(...))`` is not pythonic.
        Python uses collection iterators, not index-based loops.

    Solution:
        Use ``enumerate(...)`` instead of ``range(len(...))``.

    Example::

        # Correct:
        for index, person in enumerate(people):
            ...

        # Wrong:
        for index in range(len(people)):
            ...

    See also:
        https://docs.python.org/3/library/functions.html#enumerate

    .. versionadded:: 0.12.0

    """

    code = 518
    error_template = 'Found implicit `enumerate()` call'


@final
class ImplicitSumViolation(ASTViolation):
    """
    Forbids to have implicit ``sum()`` calls.

    When summing types different from numbers, you might need to provide
    the second argument to the ``sum`` function: ``sum([[1], [2], [3]], [])``

    You might also use ``str.join`` to join iterable of strings.

    Reasoning:
        Using ``for`` loops with ``+=`` assign inside indicates
        that you iteratively sum things inside your collection.
        That's what ``sum()`` builtin function does.

    Solution:
        Use ``sum(...)`` instead of a loop with ``+=`` operation.

    Example::

        # Correct:
        sum_result = sum(get_elements())

        # Wrong:
        sum_result = 0
        for to_sum in get_elements():
            sum_result += to_sum

    See also:
        https://docs.python.org/3/library/functions.html#sum
        https://docs.python.org/3/library/stdtypes.html#str.join

    .. versionadded:: 0.12.0

    """

    code = 519
    error_template = 'Found implicit `sum()` call'


@final
class FalsyConstantCompareViolation(ASTViolation):
    """
    Forbids to compare with explicit falsy constants.

    We allow to compare with falsy numbers, strings, booleans, ``None``.
    We disallow complex constants like tuple, dicts, and lists.

    Reasoning:
        When comparing ``something`` with explicit falsy constants
        what we really mean is ``not something``.

    Solution:
        Use ``not`` with your variable.
        Fix your data types.

    Example::

        # Correct:
        if not my_check:
            ...

        if some_other is None:
            ...

        if some_num == 0:
            ...

        # Wrong:
        if my_check == []:
            ...

    .. versionadded:: 0.12.0

    """

    code = 520
    error_template = 'Found compare with falsy constant'


@final
class WrongIsCompareViolation(ASTViolation):
    """
    Forbids to compare values with constants using ``is`` or ``is not``.

    However, we allow to compare with ``None`` and booleans.

    Reasoning:
        ``is`` compares might not do what you want them to do.
        Firstly, they check for the same object, not equality.
        Secondly, they behave unexpectedly even
        with the simple values like ``257``.

    Solution:
        Use ``==`` to compare with constants.

    Example::

        # Correct:
        if my_check == [1, 2, 3]:
            ...

        # Wrong:
        if my_check is [1, 2, 3]:
            ...

    See also:
        https://stackoverflow.com/a/33130014/4842742

    .. versionadded:: 0.12.0

    """

    code = 521
    error_template = 'Found wrong `is` compare'
