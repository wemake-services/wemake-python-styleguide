# -*- coding: utf-8 -*-

"""
These rules checks that ``class`` definitions are correct.

Note:

    Beautiful is better than ugly.
    Explicit is better than implicit.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.

"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class StaticMethodViolation(ASTStyleViolation):
    """
    Forbids to use ``@staticmethod`` decorator.

    Reasoning:
        Static methods are not required to be inside the class.
        Because it even does not an access to the current instance.

    Solution:
        Use instance methods, ``@classmethod``, or functions instead.

    Note:
        Returns Z300 as error code

    """

    should_use_text = False
    error_template = '{0} Found using `@staticmethod`'
    code = 300


class BadMagicMethodViolation(ASTStyleViolation):
    """
    Forbids to use some magic methods.

    Reasoning:
        We forbid to use magic methods related to the forbidden language parts.
        Like, we forbid to use ``del`` keyword, so we forbid to use all
        magic methods related to it.

    See
    :py:data:`~wemake_python_styleguide.constants.BAD_MAGIC_METHODS`
    for the full blacklist of the magic methods.

    Note:
        Returns Z301 as error code

    """

    error_template = '{0} Found using restricted magic method "{1}"'
    code = 301


class RequiredBaseClassViolation(ASTStyleViolation):
    """
    Forbids to write classes without base classes.

    Reasoning:
        We just need to decide how to do it.
        We need a single and unified rule about base classes.
        We have decided to stick to the explicit base class notation.

    Example::

        # Correct:
        class Some(object): ...

        # Wrong:
        class Some: ...

    Note:
        Returns Z302 as error code

    """

    error_template = '{0} Found class without a base class "{1}"'
    code = 302
