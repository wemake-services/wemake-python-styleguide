import tokenize
from typing import ClassVar, Final, TypedDict, final

from wemake_python_styleguide.violations import consistency
from wemake_python_styleguide.visitors.base import BaseTokenVisitor

_INSIGNIFICANT_TYPES: Final = frozenset((
    tokenize.NL,
    tokenize.NEWLINE,
    tokenize.COMMENT,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.ENCODING,
    tokenize.ENDMARKER,
))


_COLON_COUNT: Final = 'colon_count'
_LAST_WAS_COLON: Final = 'last_was_colon'
_LAST_COLON: Final = 'last_colon'
_HAS_NON_COLON: Final = 'has_non_colon'


class _SliceBracketState(TypedDict):
    """Mutable state tracker for a single ``[...]`` bracket level."""

    colon_count: int
    last_was_colon: bool
    last_colon: tokenize.TokenInfo | None
    has_non_colon: bool


@final
class RedundantTrailingSliceVisitor(BaseTokenVisitor):
    """Check for redundant trailing colon in subscript slices."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize state for bracket tracking."""
        super().__init__(*args, **kwargs)
        self._bracket_stack: list[_SliceBracketState] = []

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Track brackets and colons to detect trailing colon."""
        self._maybe_push_bracket(token)
        self._maybe_pop_bracket(token)
        self._maybe_track_colon(token)
        self._maybe_track_other(token)
        super().visit(token)

    def _maybe_push_bracket(self, token: tokenize.TokenInfo) -> None:
        if token.exact_type == tokenize.OP and token.string == '[':
            self._bracket_stack.append({
                _COLON_COUNT: 0,
                _LAST_WAS_COLON: False,
                _LAST_COLON: None,
                _HAS_NON_COLON: False,
            })

    def _maybe_pop_bracket(self, token: tokenize.TokenInfo) -> None:
        if not (token.exact_type == tokenize.OP and token.string == ']'):
            return
        if not self._bracket_stack:
            return
        entry = self._bracket_stack.pop()
        if (
            entry[_LAST_WAS_COLON]
            and entry[_COLON_COUNT] >= 2
            and entry[_HAS_NON_COLON]
        ):
            self.add_violation(
                consistency.RedundantTrailingSliceViolation(
                    entry[_LAST_COLON],
                ),
            )

    def _maybe_track_colon(self, token: tokenize.TokenInfo) -> None:
        if not (
            token.exact_type == tokenize.OP
            and token.string == ':'
            and self._bracket_stack
        ):
            return
        entry = self._bracket_stack[-1]
        entry[_COLON_COUNT] += 1
        entry[_LAST_WAS_COLON] = True
        entry[_LAST_COLON] = token

    def _maybe_track_other(self, token: tokenize.TokenInfo) -> None:
        if token.type in _INSIGNIFICANT_TYPES or not self._bracket_stack:
            return
        entry = self._bracket_stack[-1]
        entry[_LAST_WAS_COLON] = False
        if token.string != ':':
            entry[_HAS_NON_COLON] = True
