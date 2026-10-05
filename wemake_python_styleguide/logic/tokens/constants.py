import tokenize
from typing import Final

NEWLINES: Final = frozenset(
    (
        tokenize.NL,
        tokenize.NEWLINE,
    ),
)
"""Constant for several types of new lines in Python's grammar."""
