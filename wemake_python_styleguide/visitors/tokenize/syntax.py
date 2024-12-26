import tokenize
from typing import final

from wemake_python_styleguide.violations.consistency import (
    LineCompriseCarriageReturnViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias(
    'visit_any_newline',
    (
        'visit_newline',
        'visit_nl',
    ),
)
class WrongKeywordTokenVisitor(BaseTokenVisitor):
    """Visits keywords and finds violations related to their usage."""

    def visit_any_newline(self, token: tokenize.TokenInfo) -> None:
        r"""Checks ``\r`` (carriage return) in line breaks."""
        self._check_line_comprise_carriage_return(token)

    def _check_line_comprise_carriage_return(
        self,
        token: tokenize.TokenInfo,
    ) -> None:
        if '\r' in token.string:
            self.add_violation(LineCompriseCarriageReturnViolation(token))
