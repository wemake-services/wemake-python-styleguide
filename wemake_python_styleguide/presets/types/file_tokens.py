from typing import Final

from wemake_python_styleguide.visitors.tokenize import (
    comments,
    conditions,
    primitives,
    statements,
    syntax,
)

#: Used to store all token related visitors to be later passed to checker:
PRESET: Final = (
    comments.WrongCommentVisitor,
    comments.ShebangVisitor,
    comments.NoqaVisitor,
    comments.EmptyCommentVisitor,
    comments.CommentInFormattedStringVisitor,
    syntax.WrongKeywordTokenVisitor,
    primitives.WrongNumberTokenVisitor,
    primitives.WrongStringTokenVisitor,
    statements.MultilineStringVisitor,
    conditions.IfElseVisitor,
    primitives.MultilineFormattedStringTokenVisitor,
)
