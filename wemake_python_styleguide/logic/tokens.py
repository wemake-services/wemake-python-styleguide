import tokenize
import types
from typing import Container, FrozenSet, Iterable, List, Mapping, Tuple

MATCHING: Mapping[int, int] = types.MappingProxyType({
    tokenize.LBRACE: tokenize.RBRACE,
    tokenize.LSQB: tokenize.RSQB,
    tokenize.LPAR: tokenize.RPAR,
})

NEWLINES: FrozenSet[int] = frozenset((
    tokenize.NL,
    tokenize.NEWLINE,
))

ALLOWED_EMPTY_LINE_TOKENS: FrozenSet[int] = frozenset((
    *NEWLINES,
    *MATCHING.values(),
))


def split_prefixes(string: str) -> Tuple[str, str]:
    """
    Splits string repr by prefixes and the quoted content.

    Returns the tuple of modifiers and untouched internal string contents.

    >>> split_prefixes("Br'test'")
    ('Br', "'test'")

    >>> split_prefixes("'test'")
    ('', "'test'")

    """
    split = string.split(string[-1])
    return split[0], string.replace(split[0], '', 1)


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


def get_reverse_bracket(bracket: tokenize.TokenInfo) -> int:
    """
    Returns the reverse closing bracket for an openning token.

    >>> import tokenize
    >>> import token
    >>> bracket = tokenize.TokenInfo(token.RPAR, ")", 6, 7, "(a, b)")
    >>> get_reverse_bracket(bracket) == token.LPAR
    True

    """
    index = list(MATCHING.values()).index(bracket.exact_type)
    return list(MATCHING.keys())[index]


def last_bracket(tokens: List[tokenize.TokenInfo], index: int) -> bool:
    """Tells whether the given index is the last bracket token in line."""
    return only_contains(
        tokens[index + 1:],
        NEWLINES.union({tokenize.COMMENT}),
    )
