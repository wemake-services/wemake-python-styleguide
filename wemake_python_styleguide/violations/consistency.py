# -*- coding: utf-8 -*-

"""
These checks limit the Python's inconsistency.

We can do the same things differently in Python.
For example, there are three ways to format a string.
There are several ways to write the same number.

We like our code to be consistent.
It is easier to bare with your code base if you follow these rules.

Note:

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.

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
   BadNumberSuffixViolation
   ComparisonOrderViolation

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
.. autoclass:: BadNumberSuffixViolation
.. autoclass:: ComparisonOrderViolation

"""

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    TokenizeViolation,
)


class LocalFolderImportViolation(ASTViolation):
    """
    Forbids to have imports relative to the current folder.

    Reasoning:
        We should pick one style and stick to it.
        We have decided to use the explicit one.

    Example::

        # Correct:
        from my_package.version import get_version

        # Wrong:
        from .version import get_version
        from ..drivers import MySQLDriver

    Note:
        Returns Z300 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found local folder import "{0}"'
    code = 300


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

    Note:
        Returns Z301 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found dotted raw import "{0}"'
    code = 301


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

    Note:
        Returns Z302 as error code

    """

    code = 302
    #: Error message shown to the user.
    error_template = 'Found unicode string prefix: {0}'


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

    Note:
        Returns Z303 as error code

    """

    code = 303
    #: Error message shown to the user.
    error_template = 'Found underscored number: {0}'


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

    Note:
        Returns Z304 as error code

    """

    code = 304
    #: Error message shown to the user.
    error_template = 'Found partial float: {0}'


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

    Note:
        Returns Z305 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found `f` string'
    code = 305


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

    Note:
        Returns Z306 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found class without a base class "{0}"'
    code = 306


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

    Note:
        Returns Z307 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found list comprehension with multiple `if`s'
    code = 307


# TODO: move to `best_practices.py`
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

    Note:
        Returns Z308 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found constant comparison'
    code = 308


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

    Note:
        Returns Z309 as error code

    """

    code = 309
    #: Error message shown to the user.
    error_template = 'Found underscored number: {0}'


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

    Note:
        Returns Z310 as error code

    """

    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found reversed comparison order'
    code = 310
