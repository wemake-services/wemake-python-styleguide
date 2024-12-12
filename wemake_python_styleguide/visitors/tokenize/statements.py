import tokenize
from collections import defaultdict
from operator import attrgetter
from typing import DefaultDict, TypeAlias

from typing_extensions import final

from wemake_python_styleguide.logic.tokens.strings import (
    get_docstring_tokens,
    has_triple_string_quotes,
)
from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor

TokenLines: TypeAlias = DefaultDict[int, list[tokenize.TokenInfo]]


@final
class MultilineStringVisitor(BaseTokenVisitor):
    """Checks if multiline strings are used only in assignment or docstrings."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates line tracking for tokens."""
        super().__init__(*args, **kwargs)
        self._lines: TokenLines = defaultdict(list)
        self._docstrings = get_docstring_tokens(self.file_tokens)

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Goes through all tokens to separate them by line numbers."""
        self._lines[token.start[0]].append(token)

    def _check_token(
        self,
        index: int,
        tokens: list[tokenize.TokenInfo],
        previous_token: tokenize.TokenInfo | None,
        next_token: tokenize.TokenInfo | None,
    ) -> None:
        if index != 0:
            previous_token = tokens[index - 1]
        if previous_token and previous_token.exact_type != tokenize.EQUAL:
            self.add_violation(WrongMultilineStringUseViolation(previous_token))

        if index + 1 < len(tokens):
            next_token = tokens[index + 1]
        if next_token and next_token.exact_type == tokenize.DOT:
            self.add_violation(WrongMultilineStringUseViolation(next_token))

    def _check_individual_line(
        self,
        tokens: list[tokenize.TokenInfo],
        previous_token: tokenize.TokenInfo | None,
        next_token: tokenize.TokenInfo | None,
    ) -> None:
        for index, token in enumerate(tokens):
            if token.exact_type != tokenize.STRING or token in self._docstrings:
                continue
            if has_triple_string_quotes(token.string):
                self._check_token(index, tokens, previous_token, next_token)

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
                previous_line_token = sorted(
                    self._lines[linenos[index - 1]],
                    key=attrgetter('start'),
                )[-1]
            if index + 1 < len(linenos):
                next_line_token = sorted(
                    self._lines[linenos[index + 1]],
                    key=attrgetter('start'),
                )[0]
            self._check_individual_line(
                line_tokens,
                previous_line_token,
                next_line_token,
            )
