from collections.abc import Sequence
from tokenize import COMMENT, TokenInfo


def count_comments_in_range(
    file_tokens: Sequence[TokenInfo],
    start_line: int,
    end_line: int,
) -> int:
    """Counts comment tokens within a given line range."""
    return sum(
        1
        for token in file_tokens
        if token.type == COMMENT and start_line <= token.start[0] <= end_line
    )
