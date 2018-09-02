# -*- coding: utf-8 -*-

"""These rules checks ``class``es to be defined correctly."""

from wemake_python_styleguide.errors.base import BaseStyleViolation


class StaticMethodViolation(BaseStyleViolation):
    """
    This rule forbids to use ``@staticmethod`` decorator.

    Use regular methods, ``classmethods``, or raw functions instead.

    Note:
        Returns Z300 as error code

    """

    _error_tmpl = '{0} Found using staticmethod "{1}"'
    _code = 'Z300'


class BadMagicMethodViolation(BaseStyleViolation):
    """
    This rule forbids to use some magic methods.

    Note:
        Returns Z301 as error code

    """

    _error_tmpl = '{0} Found using restricted magic method "{1}"'
    _code = 'Z301'


class RequiredBaseClassViolation(BaseStyleViolation):
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

    _error_tmpl = '{0} Found class without a base class "{1}"'
    _code = 'Z302'
