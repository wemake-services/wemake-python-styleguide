# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)

TOKENS_PRESET = (
    WrongCommentVisitor,
    WrongPrimitivesVisitor,
)
