# -*- coding: utf-8 -*-

import tokenize
from typing import Container, Iterable, Tuple


def split_prefixes(token: tokenize.TokenInfo) -> Tuple[str, str]:
    """Splits string token by prefixes and the quoted content."""
    split = token.string.split(token.string[-1])
    return split[0], token.string.replace(split[0], '', 1)


def has_triple_string_quotes(string_contents: str) -> bool:
    """Tells whether string token is written as inside triple quotes."""
    if string_contents.startswith('"""') and string_contents.endswith('"""'):
        return True
    elif string_contents.startswith("'''") and string_contents.endswith("'''"):
        return True
    return False


def only_contains(
    tokens: Iterable[tokenize.TokenInfo],
    container: Container[int],
) -> bool:
    """Determins that only tokens from the given list are contained."""
    for token in tokens:
        if token.exact_type not in container:
            return False
    return True


def get_comment_text(token: tokenize.TokenInfo) -> str:
    """Returns comment without `#` char from comment tokens."""
    return token.string[1:].strip()
