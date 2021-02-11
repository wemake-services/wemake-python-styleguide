import tokenize
from typing import Sequence

from wemake_python_styleguide.logic.tokens.constants import NEWLINES


def next_meaningful_token(
    tokens: Sequence[tokenize.TokenInfo],
    token_position: int,
) -> tokenize.TokenInfo:
    """
    Returns the next meaningful (non-newline) token.

    Please, make sure that `tokens` are non empty.
    We don't want to make this return `Optional`.

    Get ready for some `IndexError` if `tokens` is messed up.
    """
    # This looks like a bug in coverage.py!
    # Because we test all the possibilities here.
    return next(  # pragma: no cover
        tokens[index]
        for index in range(token_position + 1, len(tokens))  # noqa: WPS518
        if tokens[index].exact_type not in NEWLINES
    )
