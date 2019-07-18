# -*- coding: utf-8 -*-

r"""
Disallows to use incorrect magic comments.

That's how a basic ``comment`` type token looks like:

.. code:: python

    TokenInfo(
        type=57 (COMMENT),
        string='# noqa: WPS100',
        start=(1, 4),
        end=(1, 16),
        line="u'' # noqa: WPS100\n",
    )

All comments have the same type.
"""

import re
import tokenize
from typing import ClassVar, FrozenSet
from typing.re import Pattern

from typing_extensions import final

from wemake_python_styleguide.constants import (
    MAX_NO_COVER_COMMENTS,
    MAX_NOQA_COMMENTS,
)
from wemake_python_styleguide.logic.tokens import get_comment_text
from wemake_python_styleguide.violations.best_practices import (
    OveruseOfNoCoverCommentViolation,
    OveruseOfNoqaCommentViolation,
    WrongDocCommentViolation,
    WrongMagicCommentViolation,
)
from wemake_python_styleguide.violations.consistency import (
    EmptyLineAfterCodingViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongCommentVisitor(BaseTokenVisitor):
    """Checks comment tokens."""

    _no_cover: ClassVar[Pattern] = re.compile(r'^pragma:\s+no\s+cover')
    _noqa_check: ClassVar[Pattern] = re.compile(r'^noqa:?($|[A-WPS\d\,\s]+)')
    _type_check: ClassVar[Pattern] = re.compile(
        r'^type:\s?([\w\d\[\]\'\"\.]+)$',
    )

    def __init__(self, *args, **kwargs) -> None:
        """Initializes a counter."""
        super().__init__(*args, **kwargs)
        self._noqa_count = 0
        self._no_cover_count = 0

    def _check_noqa(self, token: tokenize.TokenInfo) -> None:
        comment_text = get_comment_text(token)
        match = self._noqa_check.match(comment_text)
        if not match:
            return

        self._noqa_count += 1
        excludes = match.groups()[0].strip()
        if not excludes:
            # We can not pass the actual line here,
            # since it will be ignored due to `# noqa` comment:
            self.add_violation(WrongMagicCommentViolation(text=comment_text))

    def _check_typed_ast(self, token: tokenize.TokenInfo) -> None:
        comment_text = get_comment_text(token)
        match = self._type_check.match(comment_text)
        if not match:
            return

        declared_type = match.groups()[0].strip()
        if declared_type != 'ignore':
            self.add_violation(
                WrongMagicCommentViolation(token, text=comment_text),
            )

    def _check_empty_doc_comment(self, token: tokenize.TokenInfo) -> None:
        if get_comment_text(token) == ':':
            self.add_violation(WrongDocCommentViolation(token))

    def _check_cover_comments(self, token: tokenize.TokenInfo) -> None:
        comment_text = get_comment_text(token)
        match = self._no_cover.match(comment_text)
        if not match:
            return

        self._no_cover_count += 1

    def _post_visit(self) -> None:
        if self._noqa_count > MAX_NOQA_COMMENTS:
            self.add_violation(
                OveruseOfNoqaCommentViolation(text=str(self._noqa_count)),
            )
        if self._no_cover_count > MAX_NO_COVER_COMMENTS:
            self.add_violation(
                OveruseOfNoCoverCommentViolation(
                    text=str(self._no_cover_count),
                ),
            )

    def visit_comment(self, token: tokenize.TokenInfo) -> None:
        """
        Performs comment checks.

        Raises:
            OveruseOfNoqaCommentViolation
            WrongDocCommentViolation
            WrongMagicCommentViolation

        """
        self._check_noqa(token)
        self._check_typed_ast(token)
        self._check_empty_doc_comment(token)
        self._check_cover_comments(token)


@final
class FileMagicCommentsVisitor(BaseTokenVisitor):
    """Checks comments for the whole file."""

    _allowed_newlines: ClassVar[FrozenSet[int]] = frozenset((
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.ENDMARKER,
    ))

    def _offset_for_comment_line(self, token: tokenize.TokenInfo) -> int:
        if token.exact_type == tokenize.COMMENT:
            return 2
        return 0

    def _check_empty_line_after_codding(
        self,
        token: tokenize.TokenInfo,
    ) -> None:
        """
        Checks that we have a blank line after the magic comments.

        PEP-263 says: a magic comment must be placed into the source
        files either as first or second line in the file

        See also:
            https://www.python.org/dev/peps/pep-0263/

        """
        if token.start == (1, 0):
            tokens = iter(self.file_tokens[self.file_tokens.index(token):])
            available_offset = 2  # comment + newline
            while True:
                next_token = next(tokens)
                if not available_offset:
                    available_offset = self._offset_for_comment_line(
                        next_token,
                    )

                if available_offset > 0:
                    available_offset -= 1
                    continue

                if next_token.exact_type not in self._allowed_newlines:
                    self.add_violation(EmptyLineAfterCodingViolation(token))
                break

    def visit_comment(self, token: tokenize.TokenInfo) -> None:
        """
        Checks special comments that are magic per each file.

        Raises:
            EmptyLineAfterCoddingViolation

        """
        self._check_empty_line_after_codding(token)
