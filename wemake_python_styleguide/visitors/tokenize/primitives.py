# -*- coding: utf-8 -*-

import tokenize
from typing import ClassVar, FrozenSet, Optional

from flake8_quotes.docstring_detection import get_docstring_tokens
from typing_extensions import final

from wemake_python_styleguide.logic.tokens import (
    has_triple_string_quotes,
    split_prefixes,
)
from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    ImplicitStringConcatenationViolation,
    PartialFloatViolation,
    UnderscoredNumberViolation,
    UnicodeStringViolation,
    UppercaseStringModifierViolation,
    WrongMultilineStringViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongNumberTokenVisitor(BaseTokenVisitor):
    """Visits number tokens to find incorrect usages."""

    _bad_number_suffixes: ClassVar[FrozenSet[str]] = frozenset((
        '0X', '0O', '0B',
    ))

    # The thing is that `E` can be used as both a number and a suffix.
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/557
    _possibly_bad_number_suffixes = frozenset((
        'E',
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
        else:
            # Now we handle possible suffixes:
            contains_correct_suffix = any(
                char.lower() in token.string
                for char in self._bad_number_suffixes
            )
            contains_e = any(
                char in token.string
                for char in self._possibly_bad_number_suffixes
            )
            if not contains_correct_suffix and contains_e:
                self.add_violation(
                    BadNumberSuffixViolation(token, text=token.string),
                )

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
class WrongStringTokenVisitor(BaseTokenVisitor):
    """Checks incorrect string tokens usages."""

    _bad_string_modifiers: ClassVar[FrozenSet[str]] = frozenset((
        'R', 'F', 'B', 'U',
    ))

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new visitor and saves all docstrings."""
        super().__init__(*args, **kwargs)
        self._docstrings = get_docstring_tokens(self.file_tokens)

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

    def _check_concatenation(self, token: tokenize.TokenInfo) -> None:
        if token.exact_type in self._ignored_tokens:
            return

        if token.exact_type == tokenize.STRING:
            if self._previous_token:
                self.add_violation(ImplicitStringConcatenationViolation(token))
            self._previous_token = token
        else:
            self._previous_token = None

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Ensures that all string are concatenated as we allow.

        Raises:
            ImplicitStringConcatenationViolation

        """
        self._check_concatenation(token)
