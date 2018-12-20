# -*- coding: utf-8 -*-

import tokenize
from typing import ClassVar, FrozenSet

from flake8_quotes.docstring_detection import get_docstring_tokens

from wemake_python_styleguide.logics.tokens import (
    has_triple_string_quotes,
    split_prefixes,
)
from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    IncorrectMultilineStringViolation,
    PartialFloatViolation,
    UnderscoredNumberViolation,
    UnicodeStringViolation,
    UppercaseStringModifierViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongPrimitivesVisitor(BaseTokenVisitor):
    """Visits primitive types to find incorrect usages."""

    _bad_number_suffixes: ClassVar[FrozenSet[str]] = frozenset((
        'X', 'O', 'B', 'E',
    ))

    _bad_string_modifiers: ClassVar[FrozenSet[str]] = frozenset((
        'R', 'F', 'B',
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

    def _check_string_modifiers(self, token: tokenize.TokenInfo) -> None:
        if token.string.startswith('u'):
            self.add_violation(
                UnicodeStringViolation(token, text=token.string),
            )

        modifiers, _ = split_prefixes(token)
        if modifiers:
            for mod in self._bad_string_modifiers:
                if mod in modifiers:
                    self.add_violation(
                        UppercaseStringModifierViolation(token, text=mod),
                    )

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Checks string declarations.

        ``u`` can only be the only prefix.
        You can not combine it with ``r``, ``b``, or ``f``.
        Since it will raise a ``SyntaxError`` while parsing.

        Raises:
            UnicodeStringViolation

        """
        self._check_string_modifiers(token)

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


@final
class MultilineStringVisitor(BaseTokenVisitor):
    """Checks multiline strings."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new visitor and saves all docstrings."""
        super().__init__(*args, **kwargs)
        self._docstrings = get_docstring_tokens(self.file_tokens)

    def _check_correct_multiline(self, token: tokenize.TokenInfo) -> None:
        _, string_def = split_prefixes(token)
        if has_triple_string_quotes(string_def):
            if '\n' not in string_def and token not in self._docstrings:
                self.add_violation(IncorrectMultilineStringViolation(token))

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Finds incorrect multiline string usages.

        Raises:
            IncorrectMultilineStringViolation

        """
        self._check_correct_multiline(token)
