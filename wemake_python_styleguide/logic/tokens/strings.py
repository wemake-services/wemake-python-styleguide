import tokenize
from typing import Tuple

from flake8_quotes.docstring_detection import (  # noqa: WPS113, F401
    get_docstring_tokens as get_docstring_tokens,
)


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


def get_comment_text(token: tokenize.TokenInfo) -> str:
    """Returns comment without `#` char from comment tokens."""
    return token.string[1:].strip()
