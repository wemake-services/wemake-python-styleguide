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
    return bool(
        (string_contents.startswith('"""') and string_contents.endswith('"""'))
        or (
            string_contents.startswith("'''")
            and string_contents.endswith("'''")
        )
    )


def get_comment_text(token: tokenize.TokenInfo) -> str:
    """Returns comment without `#` char from comment tokens."""
    return token.string[1:].strip()


def format_with_thousands(
    number_str: str,
    thousands_separator: str = '_',
    decimal_separator: str = '.',
) -> str:
    """
    Formats a number as a string separated by thousands with support floating.

    >>> format_with_thousands('123456789')
    '123_456_789'

    >>> format_with_thousands('123456789.987654321')
    '123_456_789.987_654_321'

    >>> format_with_thousands('1000.00001')
    '1_000.00_001'

    >>> format_with_thousands('10000_000_00')
    '1_000_000_000'
    """
    number_cleared = number_str.strip().replace(thousands_separator, '')
    number_formated = ''
    digit_counter = 1
    for char in reversed(number_cleared):
        if char == decimal_separator:
            number_formated = '{0}{1}'.format(char, number_formated)
            digit_counter = 1
            continue
        if digit_counter > 3:
            number_formated = '{0}{1}'.format(
                thousands_separator, number_formated,
            )
            digit_counter = 1
        number_formated = '{0}{1}'.format(char, number_formated)
        digit_counter += 1
    return number_formated
