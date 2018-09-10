# -*- coding: utf-8 -*-

"""
These rules checks some general rules.

Like:

1. Naming
2. Using some builtins
3. Using keywords
4. Working with exceptions

Beautiful is better than ugly.
Explicit is better than implicit.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class WrongKeywordViolation(ASTStyleViolation):
    """
    This rule forbids to use some keywords from ``python``.

    We do this, since some keywords are anti-patterns.

    Example::

        # Wrong:
        pass
        del
        nonlocal
        global

    Note:
        Returns Z110 as error code

    """

    error_template = '{0} Found wrong keyword "{1}"'
    code = 'Z110'


class BareRiseViolation(ASTStyleViolation):
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

    error_template = '{0} Found bare raise outside of except "{1}"'
    code = 'Z111'


class RaiseNotImplementedViolation(ASTStyleViolation):
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

    error_template = '{0} Found raise NotImplemented "{1}"'
    code = 'Z112'


class WrongFunctionCallViolation(ASTStyleViolation):
    """
    This rule forbids to call some built-in functions.

    Since some functions are only suitable for very specific usecases,
    we forbid to use them in a free manner.

    See ``BAD_FUNCTIONS`` for the full list of blacklisted functions.

    Note:
        Returns Z113 as error code

    """

    error_template = '{0} Found wrong function call "{1}"'
    code = 'Z113'


class WrongVariableNameViolation(ASTStyleViolation):
    """
    This rule forbids to have blacklisted variable names.

    See ``BAD_VARIABLE_NAMES`` for the full list of blacklisted variable names.

    Example::

        # Correct:
        html_node = None

        # Wrong:
        item = None

    Note:
        Returns Z114 as error code

    """

    error_template = '{0} Found wrong variable name "{1}"'
    code = 'Z114'


class TooShortVariableNameViolation(ASTStyleViolation):
    """
    This rule forbids to have too short variable names.

    This rule is configurable with ``--min-variable-length``.

    Example::

        # Correct:
        x_coord = 1

        # Wrong:
        x = 1

    Note:
        Returns Z115 as error code

    """

    error_template = '{0} Found too short name "{1}"'
    code = 'Z115'


class PrivateNameViolation(ASTStyleViolation):
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

    error_template = '{0} Found private name pattern "{1}"'
    code = 'Z116'


class WrongModuleMetadataViolation(ASTStyleViolation):
    """
    This rule forbids to have some module level variables.

    We discourage using module variables like ``__author__``, because
    there's no need in them. Use proper docstrings and classifiers.
    Packaging should not be done in code.

    See ``BAD_MODULE_METADATA_VARIABLES`` for full list of bad names.

    Example::

        # Wrong:
        __author__ = 'Nikita Sobolev'

    Note:
        Returns Z117 as error code

    """

    error_template = '{0} Found wrong metadata variable {1}'
    code = 'Z117'


class FormattedStringViolation(ASTStyleViolation):
    """
    This rule forbids to use `f` strings.

    `f` strings looses context to often, they are hard to lint.
    Also, they promote a bad practice: putting a logic into the template.
    Use `.format()` instead.

    Example::

        # Wrong:
        f'Result is: {2 + 2}'

        # Correct:
        'Result is: {0}'.format(2 + 2)

    Note:
        Returns Z118 as error code

    """

    should_use_text = False
    error_template = '{0} Found `f` string'
    code = 'Z118'


class EmptyModuleViolation(ASTStyleViolation):
    """
    This rule forbids to have empty modules.

    If you have an empty module there are two ways to handle that:

    1. delete it, why is it even there?
    2. drop some documentation in it, so you will explain why it is there

    Note:
        Returns Z119 as error code

    """

    should_use_text = False
    error_template = '{0} Found empty module'
    code = 'Z119'


class InitModuleHasLogicViolation(ASTStyleViolation):
    """
    This rule forbids to have logic inside `__init__` module.

    If you have logic inside the `__init__` module it means several things:

    1. you are keeping some outdated stuff there, you need to refactor
    2. you are placing this logic into the wrong file, just create another one
    3. you are doing some dark magic, and you should not do that

    However, we allow to have some contents inside the `__init__` module:

    1. comments, since they are dropped before AST comes in play
    2. docs string, because sometimes it is required to state something

    Note:
        Returns Z120 as error code

    """

    should_use_text = False
    error_template = '{0} Found `__init__` module with logic'
    code = 'Z120'
