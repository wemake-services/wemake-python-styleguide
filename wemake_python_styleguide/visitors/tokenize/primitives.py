# -*- coding: utf-8 -*-

import re
import tokenize
from typing import ClassVar, FrozenSet, Optional
from typing.re import Pattern

from flake8_quotes.docstring_detection import get_docstring_tokens
from typing_extensions import final

from wemake_python_styleguide.logic.tokens import (
    has_triple_string_quotes,
    split_prefixes,
)
from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    ImplicitStringConcatenationViolation,
    NumberWithMeaninglessZeroViolation,
    PartialFloatViolation,
    PositiveExponentViolation,
    UnderscoredNumberViolation,
    UnicodeStringViolation,
    UppercaseStringModifierViolation,
    WrongHexNumberCaseViolation,
    WrongMultilineStringViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongNumberTokenVisitor(BaseTokenVisitor):
    """Visits number tokens to find incorrect usages."""

    _bad_number_suffixes: ClassVar[Pattern] = re.compile(
        r'^[0-9\.]+[BOXE]',
    )

    _leading_zero_pattern: ClassVar[Pattern] = re.compile(
        r'^[0-9\.]+([box]|e\+?\-?)0.+', re.IGNORECASE,
    )
    _leading_zero_float_pattern: ClassVar[Pattern] = re.compile(
        r'^[0-9]*\.[0-9]+0+$',
    )

    _positive_exponent_pattens: ClassVar[Pattern] = re.compile(
        r'^[0-9\.]+e\+', re.IGNORECASE,
    )

    _bad_hex_numbers: ClassVar[FrozenSet[str]] = frozenset((
        'a', 'b', 'c', 'd', 'e', 'f',
    ))

    def visit_number(self, token: tokenize.TokenInfo) -> None:
        """
        Checks number declarations.

        Raises:
            UnderscoredNumberViolation
            PartialFloatViolation
            BadNumberSuffixViolation
            NumberWithMeaninglessZeroViolation
            PositiveExponentViolation

        Regressions:
        https://github.com/wemake-services/wemake-python-styleguide/issues/557

        """
        self._check_underscored_number(token)
        self._check_partial_float(token)
        self._check_bad_number_suffixes(token)

    def _check_underscored_number(self, token: tokenize.TokenInfo) -> None:
        if '_' in token.string:
            self.add_violation(
                UnderscoredNumberViolation(token, text=token.string),
            )

    def _check_partial_float(self, token: tokenize.TokenInfo) -> None:
        if token.string.startswith('.') or token.string.endswith('.'):
            self.add_violation(PartialFloatViolation(token, text=token.string))

    def _check_bad_number_suffixes(self, token: tokenize.TokenInfo) -> None:
        if self._bad_number_suffixes.match(token.string):
            self.add_violation(
                BadNumberSuffixViolation(token, text=token.string),
            )

        float_zeros = self._leading_zero_float_pattern.match(token.string)
        other_zeros = self._leading_zero_pattern.match(token.string)
        if float_zeros or other_zeros:
            self.add_violation(
                NumberWithMeaninglessZeroViolation(token, text=token.string),
            )

        if self._positive_exponent_pattens.match(token.string):
            self.add_violation(
                PositiveExponentViolation(token, text=token.string),
            )

        if token.string.startswith('0x') or token.string.startswith('0X'):
            has_wrong_hex_numbers = any(
                char in self._bad_hex_numbers
                for char in token.string
            )
            if has_wrong_hex_numbers:
                self.add_violation(
                    WrongHexNumberCaseViolation(token, text=token.string),
                )


@final
class WrongStringTokenVisitor(BaseTokenVisitor):
    """Checks incorrect string tokens usages."""

    _bad_string_modifiers: ClassVar[FrozenSet[str]] = frozenset((
        'R', 'F', 'B', 'U',
    ))

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new visitor and saves all docstrings."""
        super().__init__(*args, **kwargs)
        self._docstrings = get_docstring_tokens(self.file_tokens)

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Finds incorrect string usages.

        ``u`` can only be the only prefix.
        You can not combine it with ``r``, ``b``, or ``f``.
        Since it will raise a ``SyntaxError`` while parsing.

        Raises:
            UnicodeStringViolation
            WrongMultilineStringViolation

        """
        self._check_correct_multiline(token)
        self._check_string_modifiers(token)

    def _check_correct_multiline(self, token: tokenize.TokenInfo) -> None:
        _, string_def = split_prefixes(token)
        if has_triple_string_quotes(string_def):
            if '\n' not in string_def and token not in self._docstrings:
                self.add_violation(WrongMultilineStringViolation(token))

    def _check_string_modifiers(self, token: tokenize.TokenInfo) -> None:
        if token.string.lower().startswith('u'):
            self.add_violation(
                UnicodeStringViolation(token, text=token.string),
            )

        modifiers, _ = split_prefixes(token)
        for mod in modifiers:
            if mod in self._bad_string_modifiers:
                self.add_violation(
                    UppercaseStringModifierViolation(token, text=mod),
                )


@final
class WrongStringConcatenationVisitor(BaseTokenVisitor):
    """Checks incorrect string concatenation."""

    _ignored_tokens: ClassVar[FrozenSet[int]] = frozenset((
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.INDENT,
    ))

    def __init__(self, *args, **kwargs) -> None:
        """Adds extra ``_previous_token`` property."""
        super().__init__(*args, **kwargs)
        self._previous_token: Optional[tokenize.TokenInfo] = None

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Ensures that all string are concatenated as we allow.

        Raises:
            ImplicitStringConcatenationViolation

        """
        self._check_concatenation(token)

    def _check_concatenation(self, token: tokenize.TokenInfo) -> None:
        if token.exact_type in self._ignored_tokens:
            return

        if token.exact_type == tokenize.STRING:
            if self._previous_token:
                self.add_violation(ImplicitStringConcatenationViolation(token))
            self._previous_token = token
        else:
            self._previous_token = None
