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
    _error_tmpl = '{0} Found wrong keyword "{1}"'
    _code = 'WPS100'


class BareRiseViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found bare raise outside of except "{1}"'
    _code = 'WPS101'


class RiseNotImplementedViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found raise NotImplemented "{1}"'
    _code = 'WPS102'


class WrongFunctionCallViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found wrong function call "{1}"'
    _code = 'WPS110'


class WrongVariableNameViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found wrong variable name "{1}"'
    _code = 'WPS120'


class TooShortVariableNameViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too short variable name "{1}"'
    _code = 'WPS121'


class WrongArgumentNameViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found wrong argument name "{1}"'
    _code = 'WPS122'


class TooShortArgumentNameViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too short argument name "{1}"'
    _code = 'WPS123'


class WrongAttributeNameViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found wrong attribute name "{1}"'
    _code = 'WPS124'


class TooShortAttributeNameViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too short attribute name "{1}"'
    _code = 'WPS125'


class WrongModuleMetadataViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found wrong metadata variable {1}'
    _code = 'WPS126'


class LocalFolderImportViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found local folder import "{1}"'
    _code = 'WPS130'


class NestedImportViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found nested import "{1}"'
    _code = 'WPS131'


class DynamicImportViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found dynamic import "{1}"'
    _code = 'WPS132'


class NestedFunctionViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found nested function "{1}"'
    _code = 'WPS140'


class NestedClassViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found nested class "{1}"'
    _code = 'WPS141'


class TooManyLocalsViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too many local variables "{1}"'
    _code = 'WPS150'


class TooManyArgumentsViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too many arguments "{1}"'
    _code = 'WPS151'


class TooManyBranchesViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too many branches "{1}"'
    _code = 'WPS152'


class TooManyReturnsViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too many return statements "{1}"'
    _code = 'WPS153'


class TooManyExpressionsViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too many expressions "{1}"'
    _code = 'WPS154'


class TooDeepNestingViolation(BaseStyleViolation):
    _error_tmpl = '{0} Found too deep nesting "{1}"'
    _code = 'WPS155'
