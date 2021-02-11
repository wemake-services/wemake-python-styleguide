import tokenize
import types

from typing_extensions import Final

#: Pairs of matching bracket types.
MATCHING_BRACKETS: Final = types.MappingProxyType({
    tokenize.LBRACE: tokenize.RBRACE,
    tokenize.LSQB: tokenize.RSQB,
    tokenize.LPAR: tokenize.RPAR,
})

#: Constant for several types of new lines in Python's grammar.
NEWLINES: Final = frozenset((
    tokenize.NL,
    tokenize.NEWLINE,
))

#: We do allow some tokens on empty lines.
ALLOWED_EMPTY_LINE_TOKENS: Final = frozenset((
    *NEWLINES,
    *MATCHING_BRACKETS.values(),
))
