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


@final
class InconsistentComprehensionContext(object):
    """
    Context for individual bracket contexts (i.e. within a set of brackets).

    Helper class for InconsistentComprehensionVisitor which stores context
    for the current (potential) comprehension we are in. Combined with a
    stack to enable support for nested comprehensions.
    """

    def __init__(self) -> None:
        """
        Sets all flags tracked by this visitor.

        self._inside_brackets:
        Flag is set if a left bracket has been encountered, and a right
        bracket has not yet been encountered.
        self._is_comprehension:
        Flag is set if current clause is identified as a list comprehension.
        self._seen_clause_in_line:
        Flag is set when the current line already contains a clause, which
        is either the action, each for loop, or the conditional. Starts off
        as True to account for the action, which we don't actually visit.
        self._seen_nl:
        Flag for if we've seen any logical newlines, indicating this is a
        multiline comprehension
        self._potential_violation = False
        Flag for when we see multiple clauses in one line. Only a violation
        if this is a multiline comprehension
        self._reported:
        Flag tracks whether we've already reported this violation.
        """
        self.is_comprehension = False
        self.seen_clause_in_line = False
        self.seen_nl = False
        self.potential_violation = False
        self.reported = False


@final
@alias('visit_any_left_bracket', (
    'visit_lsqb',
    'visit_lbrace',
))
@alias('visit_any_right_bracket', (
    'visit_rsqb',
    'visit_rbrace',
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

        Creates an empty stack for bracket contexts to accomodate for nested
        comprehensions.
        """
        super().__init__(*args, **kwargs)
        self._bracket_stack = []
        self._ctxt = None

    def visit_any_left_bracket(self, token: tokenize.TokenInfo) -> None:
        """Sets self._inside_brackets to True if left bracket found."""
        self._bracket_stack.append(InconsistentComprehensionContext())
        self._ctxt = self._bracket_stack[-1]

    def visit_any_right_bracket(self, token: tokenize.TokenInfo) -> None:
        """Resets environment if right bracket is encountered."""
        self._bracket_stack.pop()
        self._ctxt = self._bracket_stack[-1] if self._bracket_stack else None

    def visit_nl(self, token: tokenize.TokenInfo) -> None:
        """Sets appropriate flags to True if nl encountered inside brackets."""
        if self._ctxt:
            self._ctxt.seen_nl = True
            self._ctxt.seen_clause_in_line = False
            self._check_violation(token)

    def visit_name(self, token: tokenize.TokenInfo) -> None:
        """
        Sets flags for comprehension and potential violation as appropriate.

        Conditionally dependent on the flag signifying inside brackets.
        """
        if self._ctxt:
            if token.string in {'for', 'if'}:
                self._ctxt.is_comprehension = True
                self._ctxt.potential_violation = (
                    self._ctxt.potential_violation or
                    self._ctxt.seen_clause_in_line
                )
                self._check_violation(token)
            self._ctxt.seen_clause_in_line = True

    def _check_violation(self, token: tokenize.TokenInfo) -> None:
        """Checks if current environment state implies a violation."""
        if self._ctxt and self._ctxt.seen_nl:
            if self._ctxt.potential_violation and not self._ctxt.reported:
                self._ctxt.reported = True
                self.add_violation(InconsistentComprehensionViolation(token))
