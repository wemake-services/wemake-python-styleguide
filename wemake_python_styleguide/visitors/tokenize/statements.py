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

from typing_extensions import final

from wemake_python_styleguide.logic.tokens.brackets import (
    get_reverse_bracket,
    last_bracket,
)
from wemake_python_styleguide.logic.tokens.comprehensions import Compehension
from wemake_python_styleguide.logic.tokens.constants import (
    ALLOWED_EMPTY_LINE_TOKENS,
)
from wemake_python_styleguide.logic.tokens.constants import (
    MATCHING_BRACKETS as MATCHING,
)
from wemake_python_styleguide.logic.tokens.constants import NEWLINES
from wemake_python_styleguide.logic.tokens.newlines import next_meaningful_token
from wemake_python_styleguide.logic.tokens.queries import only_contains
from wemake_python_styleguide.logic.tokens.strings import (
    get_docstring_tokens,
    has_triple_string_quotes,
)
from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.violations.consistency import (
    BracketBlankLineViolation,
    ExtraIndentationViolation,
    InconsistentComprehensionViolation,
    WrongBracketPositionViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor
from wemake_python_styleguide.visitors.decorators import alias

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
        """Goes through all tokens to find wrong indentation."""
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
        """Goes through all tokens to separate them by line numbers."""
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
        """Goes through all tokens to separate them by line numbers."""
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


@final
@alias('visit_any_left_bracket', (
    'visit_lsqb',
    'visit_lbrace',
    'visit_lpar',
))
@alias('visit_any_right_bracket', (
    'visit_rsqb',
    'visit_rbrace',
    'visit_rpar',
))
@alias('visit_compat_name', (
    'visit_name',
    'visit_async',  # python3.6 has this token type for `async` keyword
))
class InconsistentComprehensionVisitor(BaseTokenVisitor):
    """
    Visitor for checking inconsistent comprehension syntax.

    Checks if comprehensions either use only one line or inserts a newline
    for each clause (i.e. bracket, action, for loop(s), and conditional)
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes stack of bracket contexts.

        Creates an empty stack for bracket contexts to accommodate for nested
        comprehensions.
        """
        super().__init__(*args, **kwargs)
        self._bracket_stack: List[Compehension] = []
        self._current_ctx: Optional[Compehension] = None

    def visit_any_left_bracket(self, token: tokenize.TokenInfo) -> None:
        """Sets self._inside_brackets to True if left bracket found."""
        self._current_ctx = Compehension(left_bracket=token)
        self._bracket_stack.append(self._current_ctx)

    def visit_any_right_bracket(self, token: tokenize.TokenInfo) -> None:
        """Resets environment if right bracket is encountered."""
        previous_ctx = self._bracket_stack.pop()
        if previous_ctx.is_ready() and not previous_ctx.is_valid():
            self.add_violation(
                InconsistentComprehensionViolation(previous_ctx.fors[-1]),
            )

        self._current_ctx = (
            self._bracket_stack[-1] if self._bracket_stack else None
        )

    def visit_compat_name(self, token: tokenize.TokenInfo) -> None:
        """Builds the comprehension."""
        if not self._current_ctx:
            return

        if token.string == 'async':
            self._apply_async(token)
        elif token.string == 'for':
            self._apply_expr(token)
            self._current_ctx.fors.append(token)
        elif token.string == 'in':
            self._apply_in_expr(token)
            self._current_ctx.ins.append(token)
        elif token.string == 'if':
            self._current_ctx.append_if(token)

    def _apply_async(self, token: tokenize.TokenInfo) -> None:
        assert self._current_ctx  # noqa: S101

        # `for` is always next due to grammar rules,
        # you can try to add a comment there, but we don't allow it
        for_token = self.file_tokens[self.file_tokens.index(token) + 1]
        is_broken = (
            for_token.string != 'for' or
            token.start[0] != for_token.start[0]
        )
        if is_broken:
            self._current_ctx.async_broken = True

    def _apply_expr(self, token: tokenize.TokenInfo) -> None:
        assert self._current_ctx  # noqa: S101

        if self._current_ctx.expr:
            return  # we set this value only once

        # What we do here:
        # 1. We find an opening bracket
        # 2. Then we find the next meaningful (non-NL) token
        #    that represents the actual expr of a comprehension
        # 3. We assign it to the current comprehension structure
        token_index = self.file_tokens.index(self._current_ctx.left_bracket)
        self._current_ctx.expr = next_meaningful_token(
            self.file_tokens,
            token_index,
        )

    def _apply_in_expr(self, token: tokenize.TokenInfo) -> None:
        assert self._current_ctx  # noqa: S101

        # This is not the whole expression, but we only need where it starts:
        token_index = self.file_tokens.index(token)
        self._current_ctx.in_exprs.append(next_meaningful_token(
            self.file_tokens,
            token_index,
        ))
