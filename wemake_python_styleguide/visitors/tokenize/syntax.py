# -*- coding: utf-8 -*-

import keyword
import tokenize

from typing_extensions import final

from wemake_python_styleguide.violations.consistency import (
    LineStartsWithDotViolation,
    MissingSpaceBetweenKeywordAndParenViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongKeywordTokenVisitor(BaseTokenVisitor):
    """Visits keywords and finds violations related to their usage."""

    def visit_name(self, token: tokenize.TokenInfo) -> None:
        """
        Check keywords related rules.

        Raises:
            MissingSpaceBetweenKeywordAndParenViolation

        """
        self._check_space_before_open_paren(token)

    def visit_dot(self, token: tokenize.TokenInfo) -> None:
        """
        Checks newline related rules.

        Raises:
            LineStartsWithDotViolation

        """
        self._check_line_starts_with_dot(token)

    def _check_space_before_open_paren(self, token: tokenize.TokenInfo) -> None:
        if not keyword.iskeyword(token.string):
            return

        if token.line[token.end[1]:].startswith('('):
            self.add_violation(
                MissingSpaceBetweenKeywordAndParenViolation(token),
            )

    def _check_line_starts_with_dot(self, token: tokenize.TokenInfo) -> None:
        line = token.line.lstrip()
        if line.startswith('.') and not line.startswith('...'):
            self.add_violation(LineStartsWithDotViolation(token))
