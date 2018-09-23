# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.tokenize.wrong_comments import (
    WrongCommentVisitor,
)
from wemake_python_styleguide.visitors.tokenize.wrong_primitives import (
    WrongPrimitivesVisitor,
)

TOKENS_PRESET = (
    WrongCommentVisitor,
    WrongPrimitivesVisitor,
)
