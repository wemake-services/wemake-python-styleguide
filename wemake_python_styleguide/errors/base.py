# -*- coding: utf-8 -*-

import ast
from typing import Optional, Tuple


class BaseStyleViolation(object):
    """
    Base class for all style errors.

    It basically just defines how to create any error and how to format
    this error later on.

    Each subclass must define ``error_template`` and ``code`` fields.
    """

    error_template: str
    code: int
    should_use_text: bool = True

    def __init__(self, node: Optional[ast.AST], text: str = None) -> None:
        """Creates new instance of AST style violation."""
        self._node = node

        if text is None:
            self._text = node.__class__.__name__.lower()
        else:
            self._text = text

    def _full_code(self) -> str:
        """Returns fully formated code."""
        return 'Z' + str(self.code)

    def message(self) -> str:
        """Returns error's formatted message."""
        if self.should_use_text:
            return self.error_template.format(self._full_code(), self._text)
        return self.error_template.format(self._full_code())

    def node_items(self) -> Tuple[int, int, str]:
        """Returns tuple to match ``flake8`` API format."""
        line_number = getattr(self._node, 'lineno', 0)
        column_offset = getattr(self._node, 'col_offset', 0)
        return line_number, column_offset, self.message()


class ASTStyleViolation(BaseStyleViolation):
    """AST based style violations."""

    def __init__(self, node: ast.AST, text: str = None) -> None:
        """Creates new instance of AST style violation."""
        super().__init__(node, text=text)


class SimpleStyleViolation(BaseStyleViolation):
    """Style violation for cases where there's no AST nodes."""

    def __init__(self, node=None, text: str = None) -> None:
        """Creates new instance of simple style violation."""
        super().__init__(node, text=text)
