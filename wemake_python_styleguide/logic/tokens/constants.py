import tokenize
import types

from typing_extensions import Final

MATCHING: Final = types.MappingProxyType({
    tokenize.LBRACE: tokenize.RBRACE,
    tokenize.LSQB: tokenize.RSQB,
    tokenize.LPAR: tokenize.RPAR,
})

NEWLINES: Final = frozenset((
    tokenize.NL,
    tokenize.NEWLINE,
))

ALLOWED_EMPTY_LINE_TOKENS: Final = frozenset((
    *NEWLINES,
    *MATCHING.values(),
))
