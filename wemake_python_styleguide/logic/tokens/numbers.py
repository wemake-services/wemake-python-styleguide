import re
from typing import Final

_UNDERSCORE_PATTERN: Final = re.compile(r'^\d{1,3}(_\d{3})*$')
_SPLIT_PATTERN: Final = re.compile(r'\.|e[\+-]?')


def has_correct_underscores(number: str) -> bool:
    """
    Formats a number as a string separated by thousands with support floating.

    >>> has_correct_underscores('1_234.157_000e-1_123')
    True

    >>> has_correct_underscores('0b1_001')
    True

    >>> has_correct_underscores('12_345.987_654_321')
    True

    >>> has_correct_underscores('10000_000_00')
    False
    """
    assert '_' in number  # noqa: S101
    number_cleared = (
        number.strip()
        .lower()
        .removeprefix('0b')
        .removeprefix('0x')
        .removeprefix('0o')
        .removesuffix('j')
    )
    return all(
        _UNDERSCORE_PATTERN.match(number_part)
        for number_part in _SPLIT_PATTERN.split(number_cleared)
    )
