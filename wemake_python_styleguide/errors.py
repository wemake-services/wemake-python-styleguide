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
        'WPS100 Found wrong keyword "pass"'

        >>> error = WrongKeywordViolation(ast.Delete(), text='del')
        >>> error.message()
        'WPS100 Found wrong keyword "del"'

        """
        return self._error_tmpl.format(self._code, self._text)

    def node_items(self) -> Tuple[int, int, str]:
        """Returns `Tuple` to match `flake8` API format."""
        lineno = getattr(self.node, 'lineno', 0)
        col_offset = getattr(self.node, 'col_offset', 0)
        return lineno, col_offset, self.message()


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
        Returns WPS100 as error code

    """

    _error_tmpl = '{0} Found wrong keyword "{1}"'
    _code = 'WPS100'


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
        Returns WPS101 as error code

    """

    _error_tmpl = '{0} Found bare raise outside of except "{1}"'
    _code = 'WPS101'


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
        Returns WPS102 as error code

    """

    _error_tmpl = '{0} Found raise NotImplemented "{1}"'
    _code = 'WPS102'


class WrongFunctionCallViolation(BaseStyleViolation):
    """
    This rule forbids to call some built-in functions.

    Since some functions are only suitable for very specific usecases,
    we forbid to use them in a free manner.

    Note:
        Returns WPS110 as error code

    """

    _error_tmpl = '{0} Found wrong function call "{1}"'
    _code = 'WPS110'


class WrongVariableNameViolation(BaseStyleViolation):
    """
    This rule forbids to have blacklisted variable names.

    Example::

        # Correct:
        html_node = None
        # Wrong:
        item = None

    Note:
        Returns WPS120 as error code

    """

    _error_tmpl = '{0} Found wrong variable name "{1}"'
    _code = 'WPS120'


class TooShortVariableNameViolation(BaseStyleViolation):
    """
    This rule forbids to have too short variable names.

    Example::

        # Correct:
        x_coord = 1
        # Wrong:
        x = 1

    Note:
        Returns WPS121 as error code

    """

    _error_tmpl = '{0} Found too short variable name "{1}"'
    _code = 'WPS121'


class WrongArgumentNameViolation(BaseStyleViolation):
    """
    This rule forbids to have blacklisted function argument names.

    Example::

        # Correct:
        def parse(xml_tree): ...
        # Wrong:
        def parse(value): ...

    Note:
        Returns WPS122 as error code

    """

    _error_tmpl = '{0} Found wrong argument name "{1}"'
    _code = 'WPS122'


class TooShortArgumentNameViolation(BaseStyleViolation):
    """
    This rule forbids to have short argument names.

    Example::

        # Correct:
        def test(username): ...
        # Wrong:
        def test(a): ...

    Note:
        Returns WPS123 as error code

    """

    _error_tmpl = '{0} Found too short argument name "{1}"'
    _code = 'WPS123'


class WrongAttributeNameViolation(BaseStyleViolation):
    """
    This rule forbids to have attributes with blacklisted names.

    Example::

        # Correct:
        class NormalClass:
            request_payload = None
        # Wrong:
        class WithBlacklisted:
            data = None

    Note:
        Returns WPS124 as error code

    """

    _error_tmpl = '{0} Found wrong attribute name "{1}"'
    _code = 'WPS124'


class TooShortAttributeNameViolation(BaseStyleViolation):
    """
    This rule forbids to have attributes with short names.

    Example::

        # Correct:
        class WithAttributes:
            def __init__(self):
                self.room_number = 1
        # Wrong:
        class WithAttributes:
            def __init__(self):
                self.a = 1

    Note:
        Returns WPS125 as error code

    """

    _error_tmpl = '{0} Found too short attribute name "{1}"'
    _code = 'WPS125'


class WrongFunctionNameViolation(BaseStyleViolation):
    """
    This rule forbids to have functions with blacklisted names.

    Example::

        # Correct:
        def request_dispatcher(): ...
        # Wrong:
        def handler(): ...

    Note:
        Returns WPS126 as error code

    """

    _error_tmpl = '{0} Found wrong function name "{1}"'
    _code = 'WPS126'


class TooShortFunctionNameViolation(BaseStyleViolation):
    """
    This rule forbids to have functions with short names.

    Example::

        # Correct:
        def collect_coverage(): ...
        # Wrong:
        def c(): ...

    Note:
        Returns WPS127 as error code

    """

    _error_tmpl = '{0} Found too short function name "{1}"'
    _code = 'WPS127'


class WrongModuleMetadataViolation(BaseStyleViolation):
    """
    This rule forbids to have some module level variables.

    We discourage using module variables like ``__author__``, because
    there's no need in them. Use proper docstrings and classifiers.

    Example::

        # Wrong:
        __author__ = 'Nikita Sobolev'

    Note:
        Returns WPS126 as error code

    """

    _error_tmpl = '{0} Found wrong metadata variable {1}'
    _code = 'WPS126'


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
        Returns WPS130 as error code

    """

    _error_tmpl = '{0} Found local folder import "{1}"'
    _code = 'WPS130'


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
        Returns WPS131 as error code

    """

    _error_tmpl = '{0} Found nested import "{1}"'
    _code = 'WPS131'


class DynamicImportViolation(BaseStyleViolation):
    """
    This rule forbids importing your code with ``__import__()`` function.

    This is almost never a good idea. So, it is an error by default.
    Use regular imports instead.
    Or use ``importlib.import_module()`` in case you know what you are doing.

    Example::

        # Wrong:
        my_module = __import__('my_module')

    See Also:
        https://docs.python.org/3/library/functions.html#__import__

    Note:
        Returns WPS132 as error code

    """

    _error_tmpl = '{0} Found dynamic import "{1}"'
    _code = 'WPS132'


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
        Returns WPS140 as error code

    """

    _error_tmpl = '{0} Found nested function "{1}"'
    _code = 'WPS140'


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
        Returns WPS141 as error code

    """

    _error_tmpl = '{0} Found nested class "{1}"'
    _code = 'WPS141'


class TooManyLocalsViolation(BaseStyleViolation):
    """
    This rule forbids to have too many local variables in the unit of code.

    If you have too many variables in a function, you have to refactor it.

    Note:
        Returns WPS150 as error code

    """

    _error_tmpl = '{0} Found too many local variables "{1}"'
    _code = 'WPS150'


class TooManyArgumentsViolation(BaseStyleViolation):
    """
    This rule forbids to have too many arguments for a function or method.

    This is an indecator of a bad desing.
    When function requires many arguments
    it shows that it is required to refactor this piece of code.

    Note:
        Returns WPS10 as error code

    """

    _error_tmpl = '{0} Found too many arguments "{1}"'
    _code = 'WPS151'


class TooManyBranchesViolation(BaseStyleViolation):
    """
    This rule forbids to have to many branches in a function.

    When there are too many branches, functions are hard to test.
    They are also hard to read and hard to change and read.

    Note:
        Returns WPS152 as error code

    """

    _error_tmpl = '{0} Found too many branches "{1}"'
    _code = 'WPS152'


class TooManyReturnsViolation(BaseStyleViolation):
    """
    This rule forbids placing too many ``return`` statements into the function.

    When there are too many ``return`` keywords, functions are hard to test.
    They are also hard to read and hard to change and read.

    Note:
        Returns WPS153 as error code

    """

    _error_tmpl = '{0} Found too many return statements "{1}"'
    _code = 'WPS153'


class TooManyExpressionsViolation(BaseStyleViolation):
    """
    This rule forbids putting to many expression is a unit of code.

    Because when there are too many expression, it means, that code has
    some logical or structural problems.
    We only have to identify them.

    Note:
        Returns WPS154 as error code

    """

    _error_tmpl = '{0} Found too many expressions "{1}"'
    _code = 'WPS154'


class TooDeepNestingViolation(BaseStyleViolation):
    """
    This rule forbids nesting blocks too deep.

    If nesting is too deep that indicates of another problem,
    that there's to many things going on at the same time.
    So, we need to check these cases before
    they have made their way to production.

    Note:
        Returns WPS155 as error code

    """

    _error_tmpl = '{0} Found too deep nesting "{1}"'
    _code = 'WPS155'
