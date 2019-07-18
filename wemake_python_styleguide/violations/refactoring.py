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

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import ASTViolation


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
