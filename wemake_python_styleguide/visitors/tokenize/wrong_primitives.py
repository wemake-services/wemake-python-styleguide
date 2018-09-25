# -*- coding: utf-8 -*-

import tokenize

from wemake_python_styleguide.errors.tokens import (
    PartialFloatViolation,
    UnderscoredNumberViolation,
    UnicodeStringViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


class WrongPrimitivesVisitor(BaseTokenVisitor):
    """Visits primitive types to find incorrect usages."""

    def _check_underscored_number(self, token: tokenize.TokenInfo) -> None:
        if '_' in token.string:
            self.add_error(
                UnderscoredNumberViolation(token, text=token.string),
            )

    def _check_partial_float(self, token: tokenize.TokenInfo) -> None:
        if token.string.startswith('.') or token.string.endswith('.'):
            self.add_error(PartialFloatViolation(token, text=token.string))

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Checks string declarations.

        ``u`` can only be the only prefix.
        You can not combine it with ``r``, ``b``, or ``f``.

        Raises:
            UnicodeStringViolation

        """
        if token.string.startswith('u'):
            self.add_error(UnicodeStringViolation(token, text=token.string))

    def visit_number(self, token: tokenize.TokenInfo) -> None:
        """
        Checks number declarations.

        Raises:
            UnderscoredNumberViolation
            PartialFloatViolation

        """
        self._check_underscored_number(token)
        self._check_partial_float(token)
