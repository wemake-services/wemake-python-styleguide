import re
import tokenize
from collections.abc import Callable, Sequence
from typing import ClassVar, final

from wemake_python_styleguide.logic.tokens.numbers import (
    has_correct_underscores,
)
from wemake_python_styleguide.logic.tokens.strings import (
    split_prefixes,
)
from wemake_python_styleguide.violations import consistency
from wemake_python_styleguide.violations.base import TokenizeViolation
from wemake_python_styleguide.violations.best_practices import (
    MultilineFormattedStringViolation,
    WrongUnicodeEscapeViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


def _replace_braces(string: str) -> str:
    if string.startswith('"'):
        return string.lstrip('"').rstrip('"')
    return string.lstrip("'").rstrip("'")


@final
class WrongNumberTokenVisitor(BaseTokenVisitor):
    """Visits number tokens to find incorrect usages."""

    _leading_zero_pattern: ClassVar[re.Pattern[str]] = re.compile(
        r'^[0-9\.]+([box]|e\+?\-?)0.+',
        re.IGNORECASE | re.ASCII,
    )
    _leading_zero_float_pattern: ClassVar[re.Pattern[str]] = re.compile(
        r'^[0-9]*\.[0-9]+0+$',
    )

    _float_zero: ClassVar[re.Pattern[str]] = re.compile(
        r'^0\.0$',
    )

    def visit_number(self, token: tokenize.TokenInfo) -> None:
        """
        Checks number declarations.

        Regressions:
        https://github.com/wemake-services/wemake-python-styleguide/issues/557
        """
        self._check_underscored_number(token)
        self._check_bad_number_suffixes(token)
        self._check_float_zeros(token)

    def _check_underscored_number(self, token: tokenize.TokenInfo) -> None:
        if '_' in token.string and not has_correct_underscores(token.string):
            self.add_violation(
                consistency.UnderscoredNumberViolation(
                    token,
                    text=token.string,
                ),
            )

    def _check_bad_number_suffixes(self, token: tokenize.TokenInfo) -> None:
        float_zeros = self._leading_zero_float_pattern.match(token.string)
        other_zeros = self._leading_zero_pattern.match(token.string)
        if float_zeros or other_zeros:
            self.add_violation(
                consistency.NumberWithMeaninglessZeroViolation(
                    token,
                    text=token.string,
                ),
            )

    def _check_float_zeros(self, token: tokenize.TokenInfo) -> None:
        if self._float_zero.match(token.string):
            self.add_violation(
                consistency.FloatZeroViolation(token),
            )


@final
class _StringTokenChecker:
    _bad_string_modifiers: ClassVar[frozenset[str]] = frozenset(
        (
            'R',
            'F',
            'B',
            'U',
        ),
    )

    _unicode_escapes: ClassVar[frozenset[str]] = frozenset(
        (
            'u',
            'U',
            'N',
        ),
    )

    _implicit_raw_strings: ClassVar[re.Pattern[str]] = re.compile(r'\\{2}.+')

    def __init__(
        self,
        file_tokens: Sequence[tokenize.TokenInfo],
        add_violation: Callable[[TokenizeViolation], None],
    ) -> None:
        self._add_violation = add_violation

    def check_string_modifiers(
        self,
        token: tokenize.TokenInfo,
        modifiers: str,
    ) -> None:
        for modifier in modifiers:
            if modifier in self._bad_string_modifiers:
                self._add_violation(
                    consistency.UppercaseStringModifierViolation(
                        token,
                        text=modifier,
                    ),
                )

    def check_implicit_raw_string(
        self,
        token: tokenize.TokenInfo,
        modifiers: str,
        string_def: str,
    ) -> None:
        if 'r' in modifiers.lower():
            return

        if self._implicit_raw_strings.search(_replace_braces(string_def)):
            self._add_violation(
                consistency.ImplicitRawStringViolation(
                    token,
                    text=token.string,
                ),
            )

    def check_wrong_unicode_escape(
        self,
        token: tokenize.TokenInfo,
        modifiers: str,
        string_def: str,
    ) -> None:
        # See: http://docs.python.org/reference/lexical_analysis.html
        index = 0
        while True:
            index = string_def.find('\\', index)
            if index == -1:
                break

            next_char = string_def[index + 1]
            if 'b' in modifiers.lower() and next_char in self._unicode_escapes:
                self._add_violation(
                    WrongUnicodeEscapeViolation(token, text=token.string),
                )

            # Whether it was a valid escape or not, backslash followed by
            # another character can always be consumed whole: the second
            # character can never be the start of a new backslash escape.
            index += 2


@final
class WrongStringTokenVisitor(BaseTokenVisitor):
    """Checks incorrect string tokens usages."""

    def __init__(self, *args, **kwargs) -> None:
        """Check string definitions."""
        super().__init__(*args, **kwargs)
        self._checker = _StringTokenChecker(
            self.file_tokens,
            self.add_violation,
        )

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Finds incorrect string usages.

        ``u`` can only be the only prefix.
        You cannot combine it with ``r``, ``b``, or ``f``.
        Since it will raise a ``SyntaxError`` while parsing.
        """
        modifiers, string_def = split_prefixes(token.string)
        self._checker.check_string_modifiers(token, modifiers)
        self._checker.check_implicit_raw_string(token, modifiers, string_def)
        self._checker.check_wrong_unicode_escape(token, modifiers, string_def)

    def visit_fstring_start(  # pragma: >3.12 cover
        self,
        token: tokenize.TokenInfo,
    ) -> None:
        """
        In python3.12 fstring parser was changed.

        Now, instead of `STRING` token it produces a series of:
        - `FSTRING_START`
        - `FSTRING_MIDDLE`
        - `FSTRING_END`
        tokens.

        Compare, before 3.12::

            TokenInfo(
                type=3 (STRING), string="RF'abc'",
                start=(1, 0), end=(1, 7), line="RF'abc'",
            )

        3.12 and later versions::

            TokenInfo(
                type=61 (FSTRING_START), string="RF'",
                start=(1, 0), end=(1, 3), line="RF'abc'",
            )
            TokenInfo(
                type=62 (FSTRING_MIDDLE), string='abc',
                start=(1, 3), end=(1, 6), line="RF'abc'",
            )
            TokenInfo(
                type=63 (FSTRING_END), string="'",
                start=(1, 6), end=(1, 7), line="RF'abc'",
            )

        """
        # TODO: parse all string contents and report them
        # but, since we don't recommend `f`-string, this is a low-priority
        modifiers = token.string[:-1]
        self._checker.check_string_modifiers(token, modifiers)


@final
class MultilineFormattedStringTokenVisitor(
    BaseTokenVisitor
):  # pragma: >=3.12 cover
    """Checks incorrect formatted string usages."""

    _multiline_fstring_pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"""
        .*                  # (1) anything before the f-string
        fr?(['"])           # (2) `f` or `fr`prefix + a single or double quote
        (?!\1\1)            # (3) not triple quote
        .*                  # (4) any characters up to…
        (\{.*\}.)*          # (5) any fully closed {…} expressions, if present
        .*                  # (6) then more arbitrary chars
        \{                  # (7) an opening brace of an f-expr
        [^}]*\n             # (8) chars up to a newline (i.e. multiline)
        """,
        re.VERBOSE,
    )

    def visit_fstring_start(self, token: tokenize.TokenInfo) -> None:
        """Performs check."""
        self._check_fstring_is_multi_lined(token)

    def _check_fstring_is_multi_lined(self, token: tokenize.TokenInfo) -> None:
        """Finds if f-string is multi-line."""
        if self._multiline_fstring_pattern.match(token.line):
            self.add_violation(MultilineFormattedStringViolation(token))
