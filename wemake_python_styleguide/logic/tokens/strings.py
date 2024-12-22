import tokenize
from typing import Final

#: All tokens that don't really mean anything for user.
_UTILITY_TOKENS: Final = frozenset((
    tokenize.NEWLINE,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.NL,
    tokenize.COMMENT,
))


def split_prefixes(string: str) -> tuple[str, str]:
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
    _mods, string_contents = split_prefixes(string_contents)
    return bool(
        (string_contents.startswith('"""') and string_contents.endswith('"""'))
        or (
            string_contents.startswith("'''")
            and string_contents.endswith("'''")
        ),
    )


def get_comment_text(token: tokenize.TokenInfo) -> str:
    """Returns comment without `#` char from comment tokens."""
    return token.string[1:].strip()


def is_meaningful_token(token: tokenize.TokenInfo) -> bool:
    """Returns `True` if some token is a real, not utility token."""
    return token.exact_type not in _UTILITY_TOKENS
