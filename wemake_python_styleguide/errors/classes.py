# -*- coding: utf-8 -*-

"""
These rules checks that ``class``es are defined correctly.

Beautiful is better than ugly.
Explicit is better than implicit.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class StaticMethodViolation(ASTStyleViolation):
    """
    This rule forbids to use ``@staticmethod`` decorator.

    Use regular methods, ``classmethods``, or raw functions instead.

    Note:
        Returns Z300 as error code

    """

    should_use_text = False
    error_template = '{0} Found using `@staticmethod`'
    code = 'Z300'


class BadMagicMethodViolation(ASTStyleViolation):
    """
    This rule forbids to use some magic methods.

    See ``BAD_MAGIC_METHODS`` for the full blacklist of the magic methods.

    Note:
        Returns Z301 as error code

    """

    error_template = '{0} Found using restricted magic method "{1}"'
    code = 'Z301'


class RequiredBaseClassViolation(ASTStyleViolation):
    """
    This rule forbids to write classes without base classes.

    Example::

        # Correct:
        class Some(object): ...

        # Wrong:
        class Some: ...

    Note:
        Returns Z302 as error code

    """

    error_template = '{0} Found class without a base class "{1}"'
    code = 'Z302'
