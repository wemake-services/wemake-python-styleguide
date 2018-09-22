# -*- coding: utf-8 -*-

import ast
import tokenize
from typing import Tuple, Union

ErrorNode = Union[
    ast.AST,
    tokenize.TokenInfo,
    None,
]


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

    def __init__(self, node: ErrorNode, text: str = None) -> None:
        """Creates new instance of style violation."""
        self._node = node

        if text is None:
            self._text = node.__class__.__name__.lower()
        else:
            self._text = text

    def _full_code(self) -> str:
        """Returns fully formatted code."""
        return 'Z' + str(self.code).zfill(3)

    def _location(self) -> Tuple[int, int]:
        return 0, 0

    def message(self) -> str:
        """Returns error's formatted message."""
        if self.should_use_text:
            return self.error_template.format(self._full_code(), self._text)
        return self.error_template.format(self._full_code())

    def node_items(self) -> Tuple[int, int, str]:
        """Returns tuple to match ``flake8`` API format."""
        return (*self._location(), self.message())


class ASTStyleViolation(BaseStyleViolation):
    """AST based style violations."""

    _node: ast.AST

    def _location(self) -> Tuple[int, int]:
        line_number = getattr(self._node, 'lineno', 0)
        column_offset = getattr(self._node, 'col_offset', 0)
        return line_number, column_offset


class SimpleStyleViolation(BaseStyleViolation):
    """Style violation for cases where there's no AST nodes."""

    _node: None

    def __init__(self, node=None, text: str = None) -> None:
        """Creates new instance of simple style violation."""
        super().__init__(node, text=text)


class TokenStyleViolation(BaseStyleViolation):
    """Style violation for ``tokenize`` errors."""

    _node: tokenize.TokenInfo

    def _location(self) -> Tuple[int, int]:
        return self._node.start
