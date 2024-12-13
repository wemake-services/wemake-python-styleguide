import tokenize


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
    if string_contents.startswith('"""') and string_contents.endswith('"""'):
        return True
    elif string_contents.startswith("'''") and string_contents.endswith("'''"):
        return True
    return False


def get_comment_text(token: tokenize.TokenInfo) -> str:
    """Returns comment without `#` char from comment tokens."""
    return token.string[1:].strip()


def is_wrongly_underscored_number(string: str) -> bool:
    """Checks if the number in the string is incorrectly formatted.

    The number uses underscores for thousands separators.

    """
    parts = string.split('_')
    if '.' in parts[-1]:
        parts[-1] = parts[-1].split('.')[0]
    is_correct_first_part = 1 <= len(parts[0]) <= 3
    wrong_parts = [part for part in parts[1:] if len(part) != 3]
    return not (is_correct_first_part and not wrong_parts)
