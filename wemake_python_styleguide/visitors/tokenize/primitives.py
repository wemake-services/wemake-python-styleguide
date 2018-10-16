# -*- coding: utf-8 -*-

import tokenize
from typing import ClassVar, FrozenSet

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    PartialFloatViolation,
    UnderscoredNumberViolation,
    UnicodeStringViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongPrimitivesVisitor(BaseTokenVisitor):
    """Visits primitive types to find incorrect usages."""

    _bad_number_suffixes: ClassVar[FrozenSet[str]] = frozenset((
        'X', 'O', 'B', 'E',
    ))

    def _check_underscored_number(self, token: tokenize.TokenInfo) -> None:
        if '_' in token.string:
            self.add_violation(
                UnderscoredNumberViolation(token, text=token.string),
            )

    def _check_partial_float(self, token: tokenize.TokenInfo) -> None:
        if token.string.startswith('.') or token.string.endswith('.'):
            self.add_violation(PartialFloatViolation(token, text=token.string))

    def _check_bad_number_suffixes(self, token: tokenize.TokenInfo) -> None:
        if any(char in token.string for char in self._bad_number_suffixes):
            self.add_violation(
                BadNumberSuffixViolation(token, text=token.string),
            )

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Checks string declarations.

        ``u`` can only be the only prefix.
        You can not combine it with ``r``, ``b``, or ``f``.

        Raises:
            UnicodeStringViolation

        """
        if token.string.startswith('u'):
            self.add_violation(UnicodeStringViolation(token, text=token.string))

    def visit_number(self, token: tokenize.TokenInfo) -> None:
        """
        Checks number declarations.

        Raises:
            UnderscoredNumberViolation
            PartialFloatViolation
            BadNumberSuffixViolation

        """
        self._check_underscored_number(token)
        self._check_partial_float(token)
        self._check_bad_number_suffixes(token)
