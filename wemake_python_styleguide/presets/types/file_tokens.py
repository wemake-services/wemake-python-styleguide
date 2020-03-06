from typing_extensions import Final

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

    syntax.WrongKeywordTokenVisitor,

    primitives.WrongNumberTokenVisitor,
    primitives.WrongStringTokenVisitor,
    primitives.WrongStringConcatenationVisitor,

    statements.ExtraIndentationVisitor,
    statements.BracketLocationVisitor,

    conditions.IfElseVisitor,
)
