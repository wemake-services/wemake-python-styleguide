import tokenize
from collections import defaultdict
from operator import attrgetter
from typing import TypeAlias, final

from wemake_python_styleguide.logic.tokens import strings
from wemake_python_styleguide.violations import best_practices, consistency
from wemake_python_styleguide.visitors.base import BaseTokenVisitor

TokenLines: TypeAlias = defaultdict[int, list[tokenize.TokenInfo]]


@final
class MultilineStringVisitor(BaseTokenVisitor):
    """Checks if multiline strings are used only in assignment or docstrings."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates line tracking for tokens."""
        super().__init__(*args, **kwargs)
        self._lines: TokenLines = defaultdict(list)

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Goes through all tokens to separate them by line numbers."""
        self._lines[token.start[0]].append(token)

    def _check_multiline_usage(
        self,
        index: int,
        tokens: list[tokenize.TokenInfo],
        meaningful_tokens: list[tokenize.TokenInfo],
        previous_token: tokenize.TokenInfo | None,
        next_token: tokenize.TokenInfo | None,
    ) -> None:
        if index != 0:
            previous_token = tokens[index - 1]
        if index + 1 < len(tokens):
            next_token = tokens[index + 1]

        if len(meaningful_tokens) == 1:
            # We allow simple string tokens to be present anywhere, for example:
            # ```python
            # class Example:
            #     """Docstring."""  # <- this should be allowed
            #     x: int  # noqa: ERA001
            #     """Attr docs."""  # <- this should be allowed
            # ```
            return

        if previous_token and previous_token.exact_type != tokenize.EQUAL:
            self.add_violation(
                best_practices.WrongMultilineStringUseViolation(previous_token)
            )

        if next_token and next_token.exact_type == tokenize.DOT:
            self.add_violation(
                best_practices.WrongMultilineStringUseViolation(next_token)
            )

    def _check_useless_multiline(
        self,
        token: tokenize.TokenInfo,
        meaningful_tokens: list[tokenize.TokenInfo],
    ) -> None:
        if len(meaningful_tokens) == 1:
            return  # We always allow just multiline strings on a single line.
        _modifiers, string_def = strings.split_prefixes(token.string)
        if '\n' in string_def:
            return  # Strings with newlines are fine
        self.add_violation(
            consistency.UselessMultilineStringViolation(token),
        )

    def _check_individual_line(
        self,
        tokens: list[tokenize.TokenInfo],
        previous_token: tokenize.TokenInfo | None,
        next_token: tokenize.TokenInfo | None,
    ) -> None:
        for index, token in enumerate(tokens):
            if (
                token.exact_type != tokenize.STRING
                or not strings.has_triple_string_quotes(token.string)
            ):
                continue
            meaningful_tokens = list(
                filter(strings.is_meaningful_token, tokens),
            )
            self._check_useless_multiline(token, meaningful_tokens)
            self._check_multiline_usage(
                index,
                tokens,
                meaningful_tokens,
                previous_token,
                next_token,
            )

    def _post_visit(self) -> None:
        linenos = sorted(self._lines.keys())
        for index, _ in enumerate(linenos):
            line_tokens = sorted(
                self._lines[linenos[index]],
                key=attrgetter('start'),
            )
            previous_line_token = None
            next_line_token = None
            if index != 0:
                previous_line_token = max(
                    self._lines[linenos[index - 1]],
                    key=attrgetter('start'),
                )
            if index + 1 < len(linenos):
                next_line_token = min(
                    self._lines[linenos[index + 1]],
                    key=attrgetter('start'),
                )
            self._check_individual_line(
                line_tokens,
                previous_line_token,
                next_line_token,
            )
