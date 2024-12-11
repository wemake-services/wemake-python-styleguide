import tokenize
from collections import defaultdict
from operator import attrgetter
from typing import DefaultDict, List, Optional

from typing_extensions import TypeAlias, final

from wemake_python_styleguide.logic.tokens.comprehensions import Compehension
from wemake_python_styleguide.logic.tokens.newlines import next_meaningful_token
from wemake_python_styleguide.logic.tokens.strings import (
    get_docstring_tokens,
    has_triple_string_quotes,
)
from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.violations.consistency import (
    InconsistentComprehensionViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor
from wemake_python_styleguide.visitors.decorators import alias

TokenLines: TypeAlias = DefaultDict[int, List[tokenize.TokenInfo]]


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

    def visit_name(self, token: tokenize.TokenInfo) -> None:
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
