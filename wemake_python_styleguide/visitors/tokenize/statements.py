import tokenize
from collections import defaultdict
from operator import attrgetter
from typing import (
    ClassVar,
    DefaultDict,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
)

from flake8_quotes.docstring_detection import get_docstring_tokens
from typing_extensions import final

from wemake_python_styleguide.logic.tokens import (
    ALLOWED_EMPTY_LINE_TOKENS,
    MATCHING,
    NEWLINES,
    get_reverse_bracket,
    has_triple_string_quotes,
    last_bracket,
    only_contains,
)
from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.violations.consistency import (
    BracketBlankLineViolation,
    ExtraIndentationViolation,
    WrongBracketPositionViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor

TokenLines = DefaultDict[int, List[tokenize.TokenInfo]]


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
    ) -> Mapping[int, int]:
        """Annotates each opening bracket with the nested level index."""
        brackets = {bracket: 0 for bracket in MATCHING}
        for token in tokens:
            if token.exact_type in MATCHING.keys():
                brackets[token.exact_type] += 1
            if token.exact_type in MATCHING.values():
                reverse_bracket = get_reverse_bracket(token)
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
        if annotated[get_reverse_bracket(token)] == 0:
            if not only_contains(tokens_before, ALLOWED_EMPTY_LINE_TOKENS):
                self.add_violation(WrongBracketPositionViolation(token))

    def _check_individual_line(self, tokens: List[tokenize.TokenInfo]) -> None:
        for index, token in enumerate(tokens):
            if token.exact_type in MATCHING.values():
                self._check_closing(token, index, tokens)
                if index == 0:
                    self._check_empty_line_wrap(token, delta=-1)
            elif token.exact_type in MATCHING and last_bracket(tokens, index):
                self._check_empty_line_wrap(token, delta=1)

    def _check_empty_line_wrap(
        self,
        token: tokenize.TokenInfo,
        *,
        delta: int,
    ) -> None:
        tokens = self._lines.get(token.start[0] + delta)
        if tokens is not None and only_contains(tokens, NEWLINES):
            self.add_violation(BracketBlankLineViolation(token))

    def _post_visit(self) -> None:
        for tokens in self._lines.values():
            self._check_individual_line(tokens)


@final
class MultilineStringVisitor(BaseTokenVisitor):
    """Checks if multiline strings are used only in assignment or docstrings."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates line tracking for tokens."""
        super().__init__(*args, **kwargs)
        self._lines: TokenLines = defaultdict(list)
        self._docstrings = get_docstring_tokens(self.file_tokens)

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Goes trough all tokens to separate them by line numbers.

        Raises:
            WrongMultilineStringUseViolation

        """
        self._lines[token.start[0]].append(token)

    def _check_token(
        self,
        index: int,
        tokens: List[tokenize.TokenInfo],
        previous_token: Optional[tokenize.TokenInfo],
        next_token: Optional[tokenize.TokenInfo],
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
        tokens: List[tokenize.TokenInfo],
        previous_token: Optional[tokenize.TokenInfo],
        next_token: Optional[tokenize.TokenInfo],
    ) -> None:
        for index, token in enumerate(tokens):
            if token.exact_type != tokenize.STRING or token in self._docstrings:
                continue
            if has_triple_string_quotes(token.string):
                self._check_token(index, tokens, previous_token, next_token)

    def _post_visit(self) -> None:
        linenos = sorted((self._lines.keys()))
        for index, _ in enumerate(linenos):
            line_tokens = sorted(
                self._lines[linenos[index]], key=attrgetter('start'),
            )
            previous_line_token = None
            next_line_token = None
            if index != 0:
                previous_line_token = sorted(
                    self._lines[linenos[index - 1]], key=attrgetter('start'),
                )[-1]
            if index + 1 < len(linenos):
                next_line_token = sorted(
                    self._lines[linenos[index + 1]], key=attrgetter('start'),
                )[0]
            self._check_individual_line(
                line_tokens, previous_line_token, next_line_token,
            )
