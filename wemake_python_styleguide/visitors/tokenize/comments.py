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

import os
import re
import tokenize
from typing import ClassVar, FrozenSet
from typing.re import Pattern

from typing_extensions import final

from wemake_python_styleguide.constants import MAX_NO_COVER_COMMENTS
from wemake_python_styleguide.logic.tokens import get_comment_text
from wemake_python_styleguide.violations.best_practices import (
    ExecutableMismatchViolation,
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
    _noqa_check: ClassVar[Pattern] = re.compile(r'^(noqa:?)($|[A-Z\d\,\s]+)')
    _type_check: ClassVar[Pattern] = re.compile(
        r'^type:\s?([\w\d\[\]\'\"\.]+)$',
    )

    def __init__(self, *args, **kwargs) -> None:
        """Initializes a counter."""
        super().__init__(*args, **kwargs)
        self._noqa_count = 0
        self._no_cover_count = 0

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

    def _check_noqa(self, token: tokenize.TokenInfo) -> None:
        comment_text = get_comment_text(token)
        match = self._noqa_check.match(comment_text)
        if not match:
            return

        self._noqa_count += 1
        excludes = match.groups()[1].strip()
        prefix = match.groups()[0].strip()

        if not excludes or prefix[-1] != ':':
            # We cannot pass the actual line here,
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
        if self._noqa_count > self.options.max_noqa_comments:
            self.add_violation(
                OveruseOfNoqaCommentViolation(text=str(self._noqa_count)),
            )
        if self._no_cover_count > MAX_NO_COVER_COMMENTS:
            self.add_violation(
                OveruseOfNoCoverCommentViolation(
                    text=str(self._no_cover_count),
                    baseline=MAX_NO_COVER_COMMENTS,
                ),
            )


@final
class FileMagicCommentsVisitor(BaseTokenVisitor):
    """Checks comments for the whole file."""

    _newlines: ClassVar[FrozenSet[int]] = frozenset((
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.ENDMARKER,
    ))

    def visit_comment(self, token: tokenize.TokenInfo) -> None:
        """
        Checks special comments that are magic per each file.

        Raises:
            EmptyLineAfterCoddingViolation

        """
        self._check_empty_line_after_codding(token)
        self._check_valid_shebang(token)

    def _offset_for_comment_line(self, token: tokenize.TokenInfo) -> int:
        return 2 if token.exact_type == tokenize.COMMENT else 0

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
        if token.start != (1, 0):
            return

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

            # We have a coverage error here.
            # It reports, that this line is not covered.
            # While we do have test cases for both correct and wrong cases.
            if next_token.exact_type not in self._newlines:  # pragma: no cover
                self.add_violation(EmptyLineAfterCodingViolation(token))
            break

    def _check_valid_shebang(self, token: tokenize.TokenInfo) -> None:
        shebang_string = token.string
        is_shebang_present = re.match(r'(\s*)#!', shebang_string)
        is_first_line = token.start[0] == 1
        is_executable = os.access(self.filename, os.X_OK)

        if is_first_line and is_executable and not is_shebang_present:
            self.add_violation(
                ExecutableMismatchViolation(
                    node=token,
                    text='The file is executable but no shebang is present',
                ),
            )

        if not is_shebang_present:
            return

        if not is_executable:
            self.add_violation(
                ExecutableMismatchViolation(
                    node=token,
                    text='Shebang is present but the file is not executable',
                ),
            )

        if 'python' not in shebang_string:
            self.add_violation(
                ExecutableMismatchViolation(
                    node=token,
                    text='Shebang is present but does not contain \"python\"',
                ),
            )

        if is_first_line and shebang_string.startswith((' ', '\t')):
            self.add_violation(
                ExecutableMismatchViolation(
                    node=token,
                    text='There is whitespace before shebang',
                ),
            )

        if not is_first_line:
            self.add_violation(
                ExecutableMismatchViolation(
                    node=token,
                    text='Shebang is not on first line',
                ),
            )
