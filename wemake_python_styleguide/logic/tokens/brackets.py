import tokenize
from typing import List

from wemake_python_styleguide.logic.tokens.constants import (
    MATCHING_BRACKETS,
    NEWLINES,
)
from wemake_python_styleguide.logic.tokens.queries import only_contains


def get_reverse_bracket(bracket: tokenize.TokenInfo) -> int:
    """
    Returns the reverse closing bracket for an opening token.

    >>> import tokenize
    >>> import token
    >>> bracket = tokenize.TokenInfo(token.RPAR, ")", 6, 7, "(a, b)")
    >>> get_reverse_bracket(bracket) == token.LPAR
    True

    """
    index = list(MATCHING_BRACKETS.values()).index(bracket.exact_type)
    return list(MATCHING_BRACKETS.keys())[index]


def last_bracket(tokens: List[tokenize.TokenInfo], index: int) -> bool:
    """Tells whether the given index is the last bracket token in line."""
    return only_contains(
        tokens[index + 1:],
        NEWLINES.union({tokenize.COMMENT}),
    )
