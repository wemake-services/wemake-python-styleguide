# -*- coding: utf-8 -*-

"""
These rules check some general issues.

Like:

1. Incorrect naming
2. Using wrong builtins
3. Using wrong keywords
4. Working with exceptions "the bad way"

Note:

    Beautiful is better than ugly.
    Explicit is better than implicit.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.

"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class WrongKeywordViolation(ASTStyleViolation):
    """
    Forbids to use some keywords from ``python``.

    Reasoning:
        We believe, tha some keywords are anti-patterns.
        They promote bad-practices like ``global``  and ``pass``,
        or just not user-friendly like ``del``.

    Solution:
        Solutions differ from keyword to keyword.
        ``pass`` should be replaced with docstring or ``contextlib.suppress``.
        ``del`` should be replaced with specialized methods like ``.pop()``.
        ``global`` and ``nonlocal`` usages should be refactored.

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
    code = 110


class RaiseNotImplementedViolation(ASTStyleViolation):
    """
    Forbids to use ``NotImplemented`` error.

    Reasoning:
        These two errors look so similar.
        But, these errors have different use cases.
        Use cases of ``NotImplemented`` is too limited
        to be generally available.

    Example::

        # Correct:
        raise NotImplementedError('To be done')

        # Wrong:
        raise NotImplemented

    See Also:
        https://stackoverflow.com/a/44575926/4842742

    Note:
        Returns Z111 as error code

    """

    should_use_text = False
    error_template = '{0} Found raise NotImplemented'
    code = 111


class WrongFunctionCallViolation(ASTStyleViolation):
    """
    Forbids to call some built-in functions.

    Reasoning:
        Some functions are only suitable
        for very specific usecases,
        we forbid to use them in a free manner.

    See
    :py:data:`~wemake_python_styleguide.constants.BAD_FUNCTIONS`
    for the full list of blacklisted functions.

    Note:
        Returns Z112 as error code

    """

    error_template = '{0} Found wrong function call "{1}"'
    code = 112


class WrongVariableNameViolation(ASTStyleViolation):
    """
    Forbids to have blacklisted variable names.

    Reasoning:
        We have found some names that are not expressive enough.
        However, they appear in the code more than offten.
        All names from ``BAD_VARIABLE_NAMES`` could be improved.

    Solution:
        If you really want to use any of the names from the list,
        add a prefix or suffix to it. It will serve you well.

    See
    :py:data:`~wemake_python_styleguide.constants.BAD_VARIABLE_NAMES`
    for the full list of blacklisted variable names.

    Example::

        # Correct:
        html_node_item = None

        # Wrong:
        item = None

    Note:
        Returns Z113 as error code

    """

    error_template = '{0} Found wrong variable name "{1}"'
    code = 113


class TooShortVariableNameViolation(ASTStyleViolation):
    """
    Forbids to have too short variable names.

    Reasoning:
        Naming is hard.
        It is hard to understand what the variable means and why it is used,
        if it's name is too short.

    This rule is configurable with ``--min-variable-length``.

    Example::

        # Correct:
        x_coord = 1

        # Wrong:
        x = 1

    Note:
        Returns Z114 as error code

    """

    error_template = '{0} Found too short name "{1}"'
    code = 114


class PrivateNameViolation(ASTStyleViolation):
    """
    Forbids to have private name pattern.

    Reasoning:
        Private is not private in ``python``.
        So, why should we pretend it is?
        This might lead to some serious design flaws.

    This rule checks: variables, attributes, functions, and methods.

    Example::

        # Correct:
        def _collect_coverage(self): ...

        # Wrong:
        def __collect_coverage(self): ...

    Note:
        Returns Z115 as error code

    """

    error_template = '{0} Found private name pattern "{1}"'
    code = 115


class WrongModuleMetadataViolation(ASTStyleViolation):
    """
    Forbids to have some module level variables.

    Reasoning:
        We discourage using module variables like ``__author__``,
        because code should not contain any metadata.

    Solution:
        Use proper docstrings and packaging classifiers.
        Use ``pkg_resources`` if you need to import this data into your app.

    See
    :py:data:`~wemake_python_styleguide.constants.BAD_MODULE_METADATA_VARIABLES`
    for full list of bad names.

    Example::

        # Wrong:
        __author__ = 'Nikita Sobolev'
        __version__ = 0.1.2

    Note:
        Returns Z116 as error code

    """

    error_template = '{0} Found wrong metadata variable {1}'
    code = 116


class FormattedStringViolation(ASTStyleViolation):
    """
    Forbids to use ``f`` strings.

    Reasoning:
        ``f`` strings looses context too often and they are hard to lint.
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

    Note:
        Returns Z117 as error code

    """

    should_use_text = False
    error_template = '{0} Found `f` string'
    code = 117


class EmptyModuleViolation(ASTStyleViolation):
    """
    Forbids to have empty modules.

    Reasoning:
        Why is it even there?

    Solution:
        If you have an empty module there are two ways to handle that:

        1. delete it
        2. drop some documentation in it, so you will explain why it is there

    Note:
        Returns Z118 as error code

    """

    should_use_text = False
    error_template = '{0} Found empty module'
    code = 118


class InitModuleHasLogicViolation(ASTStyleViolation):
    """
    Forbids to have logic inside ``__init__`` module.

    Reasoning:
        If you have logic inside the ``__init__`` module
        it means several things:

        1. you are keeping some outdated stuff there, you need to refactor
        2. you are placing this logic into the wrong file,
           just create another one
        3. you are doing some dark magic, and you should not do that

    Solution:
        Put your code in other modules.

    However, we allow to have some contents inside the ``__init__`` module:

    1. comments, since they are dropped before AST comes in play
    2. docs string, because sometimes it is required to state something

    Note:
        Returns Z119 as error code

    """

    should_use_text = False
    error_template = '{0} Found `__init__` module with logic'
    code = 119
