# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.tokenize import (
    comments,
    keywords,
    primitives,
    statements,
)

#: Used to store all token related visitors to be later passed to checker:
TOKENS_PRESET = (
    comments.WrongCommentVisitor,
    keywords.WrongKeywordTokenVisitor,
    primitives.WrongPrimitivesVisitor,
    statements.ExtraIndentationVisitor,
    statements.BracketLocationVisitor,
)
