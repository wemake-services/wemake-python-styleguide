# -*- coding: utf-8 -*-

"""
These rules checks some general rules.

Like:

1. Naming
2. Using some builtins
3. Using keywords
4. Working with exceptions

"""

from wemake_python_styleguide.errors.base import BaseStyleViolation


class WrongKeywordViolation(BaseStyleViolation):
    """
    This rule forbids to use some keywords from ``python``.

    We do this, since some keywords are anti-patterns.

    Example::

        # Wrong:
        pass
        exec
        eval

    Note:
        Returns Z110 as error code

    """

    _error_tmpl = '{0} Found wrong keyword "{1}"'
    _code = 'Z110'


class BareRiseViolation(BaseStyleViolation):
    """
    This rule forbids using bare `raise` keyword outside of `except` block.

    This may be a serious error in your application,
    so we should prevent that.

    Example::

        # Correct:
        raise ValueError('Value is too low')

        # Wrong:
        raise

    Note:
        Returns Z111 as error code

    """

    _error_tmpl = '{0} Found bare raise outside of except "{1}"'
    _code = 'Z111'


class RaiseNotImplementedViolation(BaseStyleViolation):
    """
    This rule forbids to use `NotImplemented` error.

    These two errors have different use cases.
    Use cases of `NotImplemented` is too limited to be generally available.

    Example::

        # Correct:
        raise NotImplementedError('To be done')

        # Wrong:
        raise NotImplemented

    See Also:
        https://stackoverflow.com/a/44575926/4842742

    Note:
        Returns Z112 as error code

    """

    _error_tmpl = '{0} Found raise NotImplemented "{1}"'
    _code = 'Z112'


class WrongFunctionCallViolation(BaseStyleViolation):
    """
    This rule forbids to call some built-in functions.

    Since some functions are only suitable for very specific usecases,
    we forbid to use them in a free manner.

    Note:
        Returns Z113 as error code

    """

    _error_tmpl = '{0} Found wrong function call "{1}"'
    _code = 'Z113'


class WrongVariableNameViolation(BaseStyleViolation):
    """
    This rule forbids to have blacklisted variable names.

    Example::

        # Correct:
        html_node = None

        # Wrong:
        item = None

    Note:
        Returns Z114 as error code

    """

    _error_tmpl = '{0} Found wrong variable name "{1}"'
    _code = 'Z114'


class TooShortVariableNameViolation(BaseStyleViolation):
    """
    This rule forbids to have too short variable names.

    Example::

        # Correct:
        x_coord = 1

        # Wrong:
        x = 1

    Note:
        Returns Z115 as error code

    """

    _error_tmpl = '{0} Found too short name "{1}"'
    _code = 'Z115'


class PrivateNameViolation(BaseStyleViolation):
    """
    This rule forbids to have private name pattern.

    It includes: variables, attributes, functions, and methods.

    Example::

        # Correct:
        def _collect_coverage(self): ...
        # Wrong:
        def __collect_coverage(self): ...

    Note:
        Returns Z116 as error code

    """

    _error_tmpl = '{0} Found private name pattern "{1}"'
    _code = 'Z116'


class WrongModuleMetadataViolation(BaseStyleViolation):
    """
    This rule forbids to have some module level variables.

    We discourage using module variables like ``__author__``, because
    there's no need in them. Use proper docstrings and classifiers.
    Packaging should not be done in code.

    Example::

        # Wrong:
        __author__ = 'Nikita Sobolev'

    Note:
        Returns Z117 as error code

    """

    _error_tmpl = '{0} Found wrong metadata variable {1}'
    _code = 'Z117'


class FormattedStringViolation(BaseStyleViolation):
    """
    This rule forbids to use `f` strings.

    Example::

        # Wrong:
        f'Result is: {2 + 2}'

        # Correct:
        'Result is: {0}'.format(2 + 2)

    Note:
        Returns Z118 as error code

    """

    _error_tmpl = '{0} Found `f` string {1}'
    _code = 'Z118'
