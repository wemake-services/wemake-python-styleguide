# -*- coding: utf-8 -*-

from wemake_python_styleguide.errors.base import TokenStyleViolation


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
    error_template = '{0} Found unicode string prefix: {1}'


class UnderscoredNumberViolation(TokenStyleViolation):
    """
    Forbids to use ``_`` in numbers.

    Reasoning:
        It is possible to write ``1000`` in three different ways:
        ``1_000``, ``10_00``, and ``100_0``. It all depends on cultural
        habits of the author.

    Solution:
        Numbers should be written as numbers: ``1000``.
        If you have a very big number with a lot of zeros, use multiplication.

    Example::
        # Correct:
        phone = 88313443
        million = 1000000

        # Wrong:
        phone = 883_134_43
        million = 100_00_00

    Note:
        Returns Z002 as error code

    """

    code = 2
    error_template = '{0} Found underscored number: {1}'
