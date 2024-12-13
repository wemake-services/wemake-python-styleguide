import tokenize
from typing import Final

#: Constant for several types of new lines in Python's grammar.
NEWLINES: Final = frozenset(
    (
        tokenize.NL,
        tokenize.NEWLINE,
    ),
)
