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
from typing import ClassVar, FrozenSet, Optional
from typing.re import Pattern

from typing_extensions import final

from wemake_python_styleguide.constants import MAX_NO_COVER_COMMENTS
from wemake_python_styleguide.logic.system import is_executable_file
from wemake_python_styleguide.logic.tokens import NEWLINES, get_comment_text
from wemake_python_styleguide.violations.best_practices import (
    OveruseOfNoCoverCommentViolation,
    OveruseOfNoqaCommentViolation,
    ShebangViolation,
    WrongDocCommentViolation,
    WrongMagicCommentViolation,
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
class ShebangVisitor(BaseTokenVisitor):
    """Checks the first shebang in the file."""

    _shebang: ClassVar[Pattern] = re.compile(r'(\s*)#!')
    _python_executable: ClassVar[str] = 'python'
    _comments_or_newlines: ClassVar[FrozenSet[int]] = NEWLINES.union(
        {tokenize.COMMENT},
    )

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Checks if there is an executable mismatch.

        Raises:
            ShebangViolation

        """
        is_first_token = token == self.file_tokens[0]

        if not is_first_token:  # TODO: test on windows
            return

        shebang_token = self._get_shebang_token()

        self._check_executable_mismatch(shebang_token)
        if shebang_token is not None:
            self._check_valid_shebang(shebang_token)

    def _check_executable_mismatch(self, shebang_token) -> None:
        is_executable = is_executable_file(self.filename)

        if is_executable and shebang_token is None:
            self.add_violation(
                ShebangViolation(
                    text='file is executable but no shebang is present',
                ),
            )

        if not is_executable and shebang_token is not None:
            self.add_violation(
                ShebangViolation(
                    text='shebang is present but the file is not executable',
                ),
            )

    def _check_valid_shebang(self, shebang_token: tokenize.TokenInfo) -> None:
        token_line = shebang_token.line
        on_first_line = shebang_token.start[0] == 1
        first_line_token = shebang_token.start[1] == 0
        if self._python_executable not in token_line:
            self.add_violation(
                ShebangViolation(
                    text='shebang is present but does not contain `python`',
                ),
            )

        if not first_line_token:
            self.add_violation(
                ShebangViolation(
                    text='there is whitespace before shebang',
                ),
            )

        if not on_first_line:
            self.add_violation(
                ShebangViolation(
                    text='there are blank or comment lines before shebang',
                ),
            )

    def _get_shebang_token(self) -> Optional[tokenize.TokenInfo]:
        all_tokens = iter(self.file_tokens)

        current_token = next(all_tokens)

        while current_token.exact_type in self._comments_or_newlines:
            if self._is_valid_shebang_line(current_token.line):
                return current_token

            current_token = next(all_tokens)

        return None

    def _is_valid_shebang_line(self, line) -> bool:
        return self._shebang.match(line) is not None
