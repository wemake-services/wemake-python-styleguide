# -*- coding: utf-8 -*-

r"""
Disallows to use incorrect magic comments.

That's how a basic ``comment`` type token looks like:

TokenInfo(
    type=57 (COMMENT),
    string='# noqa: Z100',
    start=(1, 4),
    end=(1, 16),
    line="u'' # noqa: Z100\n",
)
"""

import tokenize

from wemake_python_styleguide.visitors.base import BaseTokenVisitor


class WrongCommentVisitor(BaseTokenVisitor):
    """Checks comment tokens."""

    def visit_comment(self, token: tokenize.TokenInfo) -> None:
        """Performs comment checks."""
