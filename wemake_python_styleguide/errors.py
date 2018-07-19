# -*- coding: utf-8 -*-
# TODO(@sobolevn): write docs for each error, remove ignore from setup.cfg

"""
All style errors are defined here.

They should be sorted by ``_code``.
"""

from ast import AST
from typing import Tuple


class BaseStyleViolation(object):
    """
    This is a base class for all style errors.

    It basically just defines how to create any error and how to format
    this error later on.
    """

    _error_tmpl: str
    _code: str

    def __init__(self, node: AST, text: str = None) -> None:
        """Creates new instance of style error."""
        self.node = node

        if text is None:
            self._text = node.__class__.__name__.lower()
        else:
            self._text = text

    def message(self) -> str:
        """
        Returns error's formated message.

        >>> import ast
        >>> error = WrongKeywordViolation(ast.Pass())
        >>> error.message()
        'Z110 Found wrong keyword "pass"'

        >>> error = WrongKeywordViolation(ast.Delete(), text='del')
        >>> error.message()
        'Z110 Found wrong keyword "del"'

        """
        return self._error_tmpl.format(self._code, self._text)

    def node_items(self) -> Tuple[int, int, str]:
        """Returns `Tuple` to match `flake8` API format."""
        lineno = getattr(self.node, 'lineno', 0)
        col_offset = getattr(self.node, 'col_offset', 0)
        return lineno, col_offset, self.message()


# Imports:
# These errors represent

class LocalFolderImportViolation(BaseStyleViolation):
    """
    This rule forbids to have imports relative to the current folder.

    Example::

        # Correct:
        from my_package.version import get_version

        # Wrong:
        from .version import get_version
        from ..drivers import MySQLDriver

    Note:
        Returns Z100 as error code

    """

    _error_tmpl = '{0} Found local folder import "{1}"'
    _code = 'Z100'


class NestedImportViolation(BaseStyleViolation):
    """
    This rule forbids to have nested imports in functions.

    Nested imports show that there's an issue with you design.
    So, you don't need nested imports, you need to refactor your code.

    Example::

        # Wrong:
        def some():
            from my_module import some_function

    Note:
        Returns Z101 as error code

    """

    _error_tmpl = '{0} Found nested import "{1}"'
    _code = 'Z101'


class FutureImportViolation(BaseStyleViolation):
    """
    This rule forbids to use ``__future__`` imports.

    Almost all ``__future__`` imports are legacy ``python2`` compatibility
    tools that are no longer required.

    Except, there are some new ones for ``python4`` support.

    Example::

        # Correct:
        from __future__ import annotations

        # Wrong:
        from __future__ import print_function

    Note:
        Returns Z102 as error code

    """

    _error_tmpl = '{0} Found future import "{1}"'
    _code = 'Z102'


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
        raise ValueError('Value is to low')

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


# Design:
# These errors finds flaws in your application design and reports them.

class NestedFunctionViolation(BaseStyleViolation):
    """
    This rule forbids to have nested functions.

    Just write flat functions, there's no need to nest them.
    However, there are some whitelisted names like: ``decorator``.

    Example::

        # Wrong:
        def do_some():
            def inner():
                ...

    Note:
        Returns Z200 as error code

    """

    _error_tmpl = '{0} Found nested function "{1}"'
    _code = 'Z200'


class NestedClassViolation(BaseStyleViolation):
    """
    This rule forbids to have nested classes.

    Just write flat classes, there's no need nest them.
    However, there are some whitelisted class names like: ``Meta``.

    Example::

        # Wrong:
        class Some:
            class Inner:
                ...

    Note:
        Returns Z201 as error code

    """

    _error_tmpl = '{0} Found nested class "{1}"'
    _code = 'Z201'


class TooManyLocalsViolation(BaseStyleViolation):
    """
    This rule forbids to have too many local variables in the unit of code.

    If you have too many variables in a function, you have to refactor it.

    Note:
        Returns Z202 as error code

    """

    _error_tmpl = '{0} Found too many local variables "{1}"'
    _code = 'Z202'


class TooManyArgumentsViolation(BaseStyleViolation):
    """
    This rule forbids to have too many arguments for a function or method.

    This is an indecator of a bad desing.
    When function requires many arguments
    it shows that it is required to refactor this piece of code.

    Note:
        Returns Z203 as error code

    """

    _error_tmpl = '{0} Found too many arguments "{1}"'
    _code = 'Z203'


class TooManyBranchesViolation(BaseStyleViolation):
    """
    This rule forbids to have to many branches in a function.

    When there are too many branches, functions are hard to test.
    They are also hard to read and hard to change and read.

    Note:
        Returns Z204 as error code

    """

    _error_tmpl = '{0} Found too many branches "{1}"'
    _code = 'Z204'


class TooManyReturnsViolation(BaseStyleViolation):
    """
    This rule forbids placing too many ``return`` statements into the function.

    When there are too many ``return`` keywords, functions are hard to test.
    They are also hard to read and hard to change and read.

    Note:
        Returns Z205 as error code

    """

    _error_tmpl = '{0} Found too many return statements "{1}"'
    _code = 'Z205'


class TooManyExpressionsViolation(BaseStyleViolation):
    """
    This rule forbids putting to many expression is a unit of code.

    Because when there are too many expression, it means, that code has
    some logical or structural problems.
    We only have to identify them.

    Note:
        Returns Z206 as error code

    """

    _error_tmpl = '{0} Found too many expressions "{1}"'
    _code = 'Z206'


class TooDeepNestingViolation(BaseStyleViolation):
    """
    This rule forbids nesting blocks too deep.

    If nesting is too deep that indicates of another problem,
    that there's to many things going on at the same time.
    So, we need to check these cases before
    they have made their way to production.

    Note:
        Returns Z207 as error code

    """

    _error_tmpl = '{0} Found too deep nesting "{1}"'
    _code = 'Z207'


# Classes:
# These rules are related to defining valid classes


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
