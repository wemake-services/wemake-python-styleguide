import tokenize
from collections import defaultdict
from dataclasses import dataclass
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
        Goes through all tokens to separate them by line numbers.

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
        Goes through all tokens to separate them by line numbers.

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


@final
@dataclass
class InconsistentComprehensionContext(object):
    r"""Context for individual bracket enclosures (i.e. [],\{\}, or ())."""

    def __init__(self) -> None:
        r"""
        Initializes context for a given bracket enclosure (i.e. [],\{\}, or ()).

        Helper class for InconsistentComprehensionVisitor which stores context
        for the current (potential) comprehension we are in. Combined with a
        stack to enable support for nested comprehensions.

        _is_comprehension:
        Flag is set if current clause is identified as a list comprehension.

        seen_clause_in_line:
        Flag is set when the current line already contains a clause, which
        is either the action, each for loop, or the conditional. Starts off
        as True to account for the action, which we don't actually visit.

        _seen_for:
        Flag tracks whether we've seen a for statement within these brackets.
        Effectively determines whether we are looking at some kind of
        comprehension or not.

        _seen_for_in_line:
        Flag tracks whether we've seen a for statement on this line. Used to
        determine if a for...in statement has been split across multiple lines.

        _seen_if_in_line:
        Flag tracks whether we've seen an if statement on this line. Used to
        determine whether an in statement is from a for...in statement or
        is a logical in.

        _seen_nl:
        Flag for if we've seen any logical newlines, indicating this is a
        multiline comprehension

        _potential_violation:
        Flag for when we see multiple clauses in one line. Only a violation
        if this is a multiline comprehension

        _reported:
        Flag tracks whether we've already reported this violation.
        """
        self.seen_clause_in_line = False
        self._is_comprehension = False
        self._seen_for = False
        self._seen_for_in_line = False
        self._seen_if_in_line = False
        self._seen_nl = False
        self._potential_violation = False
        self._reported = False

    def check_nl(self, token: tokenize.TokenInfo) -> None:
        """
        Handles logical newline character depending on context.

        Sets appropriate flags to True if nl encountered inside brackets after
        some clause, so that a single line comprehension with brackets on
        multiple lines is still accepted.
        """
        self._seen_nl = self.seen_clause_in_line
        self.seen_clause_in_line = False
        self._seen_for_in_line = False
        self._seen_if_in_line = False

    def check_for(self, token: tokenize.TokenInfo) -> bool:
        """Handles 'for' tokens inside brackets."""
        self._is_comprehension = True
        self._seen_for = True
        self._seen_for_in_line = True

        self._potential_violation = (
            self._potential_violation or
            self.seen_clause_in_line
        )
        return self._check_violation(token)

    def check_if(self, token: tokenize.TokenInfo) -> bool:
        """
        Handles 'if' tokens inside brackets.

        In order to rule out this if statement being part of a ternary operator
        in the action statement of a comprehension, we ensure that we've already
        passed the action statement, as once a for statement appears any
        following if statements will be the conditional statement of the
        comprehension.
        """
        if self._seen_for:
            self._seen_if_in_line = True

            self._potential_violation = (
                self._potential_violation or
                self.seen_clause_in_line
            )
            return self._check_violation(token)
        return True

    def check_in(self, token: tokenize.TokenInfo) -> bool:
        """
        Adds a violation when a for...in statement is split across lines.

        Because of the overloaded nature of 'in', we have to rule
        out several edge cases before we can say that this is a violation:
        First, we only want to consider this split for...in statement
        in the case that we've seen a for statement but not on this line.
        Second, we don't want to catch an 'in' in the conditional clause of the
        comprehension, so we make sure we haven't seen an if statement on
        this line.
        """
        if self._seen_for:
            if not self._seen_for_in_line:
                if not self._seen_if_in_line:
                    self._reported = True
                    return False
        return True

    def _check_violation(self, token: tokenize.TokenInfo) -> bool:
        """Checks if current environment state implies a violation."""
        if self._seen_nl:
            if self._potential_violation and not self._reported:
                self._reported = True
                return False
        return True


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
        self._bracket_stack: List[InconsistentComprehensionContext] = []
        self._current_ctx: Optional[InconsistentComprehensionContext] = None

    def visit_any_left_bracket(self, token: tokenize.TokenInfo) -> None:
        """Sets self._inside_brackets to True if left bracket found."""
        self._bracket_stack.append(InconsistentComprehensionContext())
        self._current_ctx = self._bracket_stack[-1]

    def visit_any_right_bracket(self, token: tokenize.TokenInfo) -> None:
        """Resets environment if right bracket is encountered."""
        self._bracket_stack.pop()
        if self._bracket_stack:
            self._current_ctx = self._bracket_stack[-1]
        else:
            self._current_ctx = None

    def visit_nl(self, token: tokenize.TokenInfo) -> None:
        """Handles logical newline character depending on context."""
        if self._current_ctx:
            self._current_ctx.check_nl(token)

    def visit_name(self, token: tokenize.TokenInfo) -> None:
        """Sets flags for comprehension keywords."""
        if self._current_ctx:
            well_formed = True
            if token.string == 'for':
                well_formed = self._current_ctx.check_for(token)
            elif token.string == 'if':
                well_formed = self._current_ctx.check_if(token)
            elif token.string == 'in':
                well_formed = self._current_ctx.check_in(token)

            self._current_ctx.seen_clause_in_line = True
            if not well_formed:
                self.add_violation(
                    InconsistentComprehensionViolation(token),
                )
