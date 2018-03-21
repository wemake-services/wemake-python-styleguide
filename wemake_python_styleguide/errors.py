# -*- coding: utf-8 -*-
# TODO(@sobolevn): write docs for each error, remove ignore from setup.cfg

"""
All style errors are defined here.

They should be sorted by `_code`.
"""

from ast import AST
from typing import Tuple


class BaseStyleViolation(object):
    """This is a base class for all style errors."""

    _error_tmpl: str
    _code: str

    def __init__(self, node: AST, text: str = None) -> None:
        """Creates new instance."""
        self.node = node

        if text is None:
            self._text = node.__class__.__name__.lower()
        else:
            self._text = text

    def message(self) -> str:
        """Returns formated message."""
        return self._error_tmpl.format(self._code, self._text)

    def items(self) -> Tuple[int, int, str]:
        """Returns `tuple` to match `flake8` API format."""
        lineno = getattr(self.node, 'lineno', 0)
        col_offset = getattr(self.node, 'col_offset', 0)
        return lineno, col_offset, self.message()


class WrongKeywordViolation(BaseStyleViolation):
    _error_tmpl = '{} Found wrong keyword "{}"'
    _code = 'WPS100'


class WrongFunctionCallViolation(BaseStyleViolation):
    _error_tmpl = '{} Found wrong function call "{}"'
    _code = 'WPS110'


class WrongVariableNameViolation(BaseStyleViolation):
    _error_tmpl = '{} Found wrong variable name "{}"'
    _code = 'WPS120'


class TooShortVariableNameViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too short variable name "{}"'
    _code = 'WPS121'


class WrongArgumentNameViolation(BaseStyleViolation):
    _error_tmpl = '{} Found wrong argument name "{}"'
    _code = 'WPS122'


class TooShortArgumentNameViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too short argument name "{}"'
    _code = 'WPS123'


class WrongAttributeNameViolation(BaseStyleViolation):
    _error_tmpl = '{} Found wrong attribute name "{}"'
    _code = 'WPS124'


class TooShortAttributeNameViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too short attribute name "{}"'
    _code = 'WPS125'


class LocalFolderImportViolation(BaseStyleViolation):
    _error_tmpl = '{} Found local folder import "{}"'
    _code = 'WPS130'


class NestedImportViolation(BaseStyleViolation):
    _error_tmpl = '{} Found nested import "{}"'
    _code = 'WPS131'


class DynamicImportViolation(BaseStyleViolation):
    _error_tmpl = '{} Found dynamic import "{}"'
    _code = 'WPS132'


class NestedFunctionViolation(BaseStyleViolation):
    _error_tmpl = '{} Found nested function "{}"'
    _code = 'WPS140'


class NestedClassViolation(BaseStyleViolation):
    _error_tmpl = '{} Found nested class "{}"'
    _code = 'WPS141'


class TooManyLocalsViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too many local variables "{}"'
    _code = 'WPS150'


class TooManyArgumentsViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too many arguments "{}"'
    _code = 'WPS151'


class TooManyBranchesViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too many branches "{}"'
    _code = 'WPS152'


class TooManyReturnsViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too many return statements "{}"'
    _code = 'WPS153'


class TooManyStatementsViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too many statements "{}"'
    _code = 'WPS154'


class TooDeepNestingViolation(BaseStyleViolation):
    _error_tmpl = '{} Found too deep nesting "{}"'
    _code = 'WPS155'
