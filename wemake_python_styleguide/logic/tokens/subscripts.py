import ast
import re
import tokenize
from collections.abc import Sequence


def has_redundant_step(
    node: ast.Subscript,
    tokens: Sequence[tokenize.TokenInfo],
) -> bool:
    """
    Find patterns like ``[start:stop:]`` or ``[start::]``.

    Return ``True`` if pattern is found, ``False`` otherwise.
    """
    if not isinstance(node.end_col_offset, int):  # pragma: no cover
        return False

    pattern = r'\[\d+:\d+:\]'  # [<start>:<stop>:]

    sub_tokens: list[str] = [
        token.string
        for token in tokens
        if node.col_offset <= token.start[1]
        and node.end_col_offset >= token.end[1]
    ]

    sub_tokens_str = ''.join(sub_tokens)

    return '::]' in sub_tokens_str or bool(re.search(pattern, sub_tokens_str))
