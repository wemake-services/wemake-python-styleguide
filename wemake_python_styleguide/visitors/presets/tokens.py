# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor,
)
from wemake_python_styleguide.visitors.tokenize.keywords import (
    WrongKeywordTokenVisitor,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)

#: Used to store all token related visitors to be later passed to checker:
TOKENS_PRESET = (
    WrongCommentVisitor,
    WrongKeywordTokenVisitor,
    WrongPrimitivesVisitor,
)
