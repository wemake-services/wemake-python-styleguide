# -*- coding: utf-8 -*-

from ast import AST
from typing import Tuple


class BaseStyleViolation(object):
    """
    This is a base class for all style errors.

    It basically just defines how to create any error and how to format
    this error later on.

    Each subclass must define ``_error_tmpl`` and ``_code`` fields.
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
        >>> from wemake_python_styleguide.errors.general import (
        ...     WrongKeywordViolation,
        ... )
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
