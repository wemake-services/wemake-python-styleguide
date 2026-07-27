import ast
import re
import tokenize
from collections.abc import Sequence


def _is_token_in_span(node: ast.Subscript, token: tokenize.TokenInfo) -> bool:

    if not isinstance(node.end_col_offset, int):  # pragma: no cover
        return False

    return bool(
        token.start[0] == node.lineno
        and node.col_offset <= token.start[1]
        and node.end_col_offset >= token.end[1],
    )


def has_redundant_step(
    node: ast.Subscript,
    tokens: Sequence[tokenize.TokenInfo],
) -> bool:
    """
    Find patterns like ``[start:stop:]`` or ``[start::]``.

    Return ``True`` if pattern is found, ``False`` otherwise.
    """
    pattern = r'\[\d+:\d+:\]'  # [<start>:<stop>:]

    sub_tokens: list[str] = [
        token.string for token in tokens if _is_token_in_span(node, token)
    ]

    sub_tokens_str = ''.join(sub_tokens)

    return '::]' in sub_tokens_str or bool(re.search(pattern, sub_tokens_str))
