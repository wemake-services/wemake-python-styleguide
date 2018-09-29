# -*- coding: utf-8 -*-

"""
These rules check different small syntax things.

Note:

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Readability counts.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.

"""

from wemake_python_styleguide.errors.base import (
    SimpleStyleViolation,
    TokenStyleViolation,
)


class UnicodeStringViolation(TokenStyleViolation):
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
        Returns Z001 as error code

    """

    code = 1
    #: Error message shown to the user.
    error_template = 'Found unicode string prefix: {0}'


class UnderscoredNumberViolation(TokenStyleViolation):
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
        Returns Z002 as error code

    """

    code = 2
    #: Error message shown to the user.
    error_template = 'Found underscored number: {0}'


class WrongMagicCommentViolation(SimpleStyleViolation):
    """
    Restricts to use several control (or magic) comments.

    We do not allow to use:

    1. ``# noqa`` comment without specified errors
    2. ``# type: some_type`` comments to specify a type for ``typed_ast``

    Reasoning:
        We cover several different use-cases in a single rule.
        ``# noqa`` comment is restricted because it can hide other errors.
        ``# type: some_type`` comment is restricted because
        we can already use type annotations instead.

    Solution:
        Use ``# noqa`` comments with specified error types.
        Use type annotations to specify types.

    We still allow to use ``# type: ignore`` comment.
    Since sometimes it is totally required.

    Example::

        # Correct:
        type = MyClass.get_type()  # noqa: A001
        coordinate: int = 10
        some.int_field = 'text'  # type: ignore

        # Wrong:
        type = MyClass.get_type()  # noqa
        coordinate = 10  # type: int

    Note:
        Returns Z003 as error code

    """

    code = 3
    #: Error message shown to the user.
    error_template = 'Found wrong magic comment: {0}'


class PartialFloatViolation(TokenStyleViolation):
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
        Returns Z004 as error code

    """

    code = 4
    #: Error message shown to the user.
    error_template = 'Found partial float: {0}'


class WrongDocCommentViolation(TokenStyleViolation):
    """
    Forbids to use empty doc comments (``#:``).

    Reasoning:
        Doc comments are used to provide a documentation.
        But supling empty doc comments breaks this use-case.
        It is unclear why they can be used with no contents.

    Solution:
        Add some documentation to this comment. Or remove it.

    Empty doc comments are not caught by the default ``pycodestyle`` checks.

    Example::

        # Correct:
        #: List of allowed names:
        NAMES_WHITELIST = ['feature', 'bug', 'research']

        # Wrong:
        #:
        NAMES_WHITELIST = ['feature', 'bug', 'research']

    Note:
        Returns Z005 as error code

    """

    code = 5
    should_use_text = False
    #: Error message shown to the user.
    error_template = 'Found wrong doc comment'
