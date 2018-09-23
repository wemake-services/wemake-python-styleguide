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

import re
import tokenize
from typing.re import Match, Pattern

from wemake_python_styleguide.errors.tokens import WrongMagicCommentViolation
from wemake_python_styleguide.visitors.base import BaseTokenVisitor

NOQA_CHECK: Pattern = re.compile(r'^noqa:?($|[A-Z\d\,\s]+)')


class WrongCommentVisitor(BaseTokenVisitor):
    """Checks comment tokens."""

    def _check_noqa(self, token: tokenize.TokenInfo) -> None:
        comment_text = token.string[1:].strip()
        match: Match = NOQA_CHECK.match(comment_text)
        if not match:
            return

        excludes = match.groups()[0].strip()
        if not excludes:
            # We can not pass the actual line here,
            # since it will be ignored due to `noqa` comment:
            self.add_error(WrongMagicCommentViolation(text=comment_text))

    def visit_comment(self, token: tokenize.TokenInfo) -> None:
        """Performs comment checks."""
        self._check_noqa(token)
