# -*- coding: utf-8 -*-

import tokenize
import types
from collections import defaultdict
from typing import (
    ClassVar,
    DefaultDict,
    Dict,
    FrozenSet,
    List,
    Mapping,
    Sequence,
    Tuple,
)

from typing_extensions import final

from wemake_python_styleguide.logic.tokens import only_contains
from wemake_python_styleguide.violations.consistency import (
    ExtraIndentationViolation,
    UselessBlankLineViolation,
    WrongBracketPositionViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor

TokenLines = DefaultDict[int, List[tokenize.TokenInfo]]

MATCHING: Mapping[int, int] = types.MappingProxyType({
    tokenize.LBRACE: tokenize.RBRACE,
    tokenize.LSQB: tokenize.RSQB,
    tokenize.LPAR: tokenize.RPAR,
})

ALLOWED_EMPTY_LINE_TOKENS: FrozenSet[int] = frozenset((
    tokenize.NL,
    tokenize.NEWLINE,
    *MATCHING.values(),
))


def _get_reverse_bracket(bracket: tokenize.TokenInfo) -> int:
    index = list(MATCHING.values()).index(bracket.exact_type)
    return list(MATCHING.keys())[index]


@final
class ExtraIndentationVisitor(BaseTokenVisitor):
    """
    Is used to find extra indentation in nodes.

    Algorithm:
    1. goes through all nodes in a module
    2. remembers minimal indentation for each line
    3. compares each two closest lines: indentation should not be >4

    """

    _ignored_tokens: ClassVar[Tuple[int, ...]] = (
        tokenize.NEWLINE,
    )

    _ignored_previous_token: ClassVar[Tuple[int, ...]] = (
        tokenize.NL,
    )

    def __init__(self, *args, **kwargs) -> None:
        """Creates empty counter."""
        super().__init__(*args, **kwargs)
        self._offsets: Dict[int, tokenize.TokenInfo] = {}

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Goes through all tokens to find wrong indentation.

        Raises:
            ExtraIndentationViolation

        """
        self._check_extra_indentation(token)

    def _check_extra_indentation(self, token: tokenize.TokenInfo) -> None:
        lineno, _offset = token.start
        if lineno not in self._offsets:
            self._offsets[lineno] = token

    def _get_token_offset(self, token: tokenize.TokenInfo) -> int:
        if token.exact_type == tokenize.INDENT:
            return token.end[1]
        return token.start[1]

    def _check_individual_line(
        self,
        lines: Sequence[int],
        line: int,
        index: int,
    ) -> None:
        current_token = self._offsets[line]
        if current_token.exact_type in self._ignored_tokens:
            return

        previous_token = self._offsets[lines[index - 1]]
        if previous_token.exact_type in self._ignored_previous_token:
            return

        offset = self._get_token_offset(current_token)
        previous_offset = self._get_token_offset(previous_token)

        if offset > previous_offset + 4:
            self.add_violation(ExtraIndentationViolation(current_token))

    def _post_visit(self) -> None:
        lines = sorted(self._offsets.keys())

        for index, line in enumerate(lines):
            if index == 0 or line != lines[index - 1] + 1:
                continue
            self._check_individual_line(lines, line, index)


@final
class BlankLineVisitor(BaseTokenVisitor):
    """
    Finds blank lines location.

    We check that blank lines don't occur directly
    before or after a bracket (round, square, or curly).
    """

    def __init__(self, *arg, **kargs) -> None:
        """Creates line tracking for tokens."""
        super().__init__(*arg, **kargs)
        self._lines: TokenLines = defaultdict(list)

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Goes through all tokens to separate them by line numbers.

        Raises:
            UselessBlankLineViolation

        """
        self._lines[token.start[0]].append(token)

    def _check_if_line_is_blank(self, tokens: List[tokenize.TokenInfo]) -> None:
        if tokens is None:
            return
        if len(tokens) > 1:
            return
        if tokens[0].exact_type in ALLOWED_EMPTY_LINE_TOKENS:
            self.add_violation(UselessBlankLineViolation(tokens[0]))

    def _check_is_open_brace(self, token: tokenize.TokenInfo) -> None:
        return token.exact_type in MATCHING.keys()

    def _check_is_close_brace(self, token: tokenize.TokenInfo) -> None:
        return token.exact_type in MATCHING.values()

    def _check_individual_line(self, tokens: List[tokenize.TokenInfo]) -> None:
        if len(tokens) < 2:
            return
        if self._check_is_open_brace(tokens[-2]):
            my_line = tokens[-2].start[0]
            next_line_tokens = self._lines.get(my_line + 1)
            self._check_if_line_is_blank(next_line_tokens)

        if self._check_is_close_brace(tokens[0]):
            my_line = tokens[1].start[0]
            prev_line_tokens = self._lines.get(my_line - 1)
            self._check_if_line_is_blank(prev_line_tokens)

    def _post_visit(self) -> None:
        for _, tokens in self._lines.items():
            self._check_individual_line(tokens)


@final
class BracketLocationVisitor(BaseTokenVisitor):
    """
    Finds closing brackets location.

    We check that brackets can be on the same line or
    brackets can be the only tokens on the line.

    We track all kind of brackets: round, square, and curly.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Creates line tracking for tokens."""
        super().__init__(*args, **kwargs)
        self._lines: TokenLines = defaultdict(list)

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Goes trough all tokens to separate them by line numbers.

        Raises:
            WrongBracketPositionViolation

        """
        self._lines[token.start[0]].append(token)

    def _annotate_brackets(
        self,
        tokens: List[tokenize.TokenInfo],
    ) -> Dict[int, int]:
        """Annotates each opening bracket with the nested level index."""
        brackets = {bracket: 0 for bracket in MATCHING}
        for token in tokens:
            if token.exact_type in MATCHING.keys():
                brackets[token.exact_type] += 1
            if token.exact_type in MATCHING.values():
                reverse_bracket = _get_reverse_bracket(token)
                if brackets[reverse_bracket] > 0:
                    brackets[reverse_bracket] -= 1
        return brackets

    def _check_closing(
        self,
        token: tokenize.TokenInfo,
        index: int,
        tokens: List[tokenize.TokenInfo],
    ) -> None:
        tokens_before = tokens[:index]
        annotated = self._annotate_brackets(tokens_before)
        if annotated[_get_reverse_bracket(token)] == 0:
            if not only_contains(tokens_before, ALLOWED_EMPTY_LINE_TOKENS):
                self.add_violation(WrongBracketPositionViolation(token))

    def _check_individual_line(self, tokens: List[tokenize.TokenInfo]) -> None:
        for index, token in enumerate(tokens):
            if token.exact_type in MATCHING.values():
                self._check_closing(token, index, tokens)

    def _post_visit(self) -> None:
        for _, tokens in self._lines.items():
            self._check_individual_line(tokens)
