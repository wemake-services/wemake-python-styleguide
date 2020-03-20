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
from typing import ClassVar
from typing.re import Pattern

from typing_extensions import final

from wemake_python_styleguide.constants import MAX_NO_COVER_COMMENTS, STDIN
from wemake_python_styleguide.logic.system import (
    is_executable_file,
    is_windows,
)
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
        if not declared_type.startswith('ignore'):
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
    """
    Checks the first shebang in the file.

    Code is insipired by https://github.com/xuhdev/flake8-executable
    """

    _shebang: ClassVar[Pattern] = re.compile(r'(\s*)#!')
    _python_executable: ClassVar[str] = 'python'

    def visit_comment(self, token: tokenize.TokenInfo) -> None:
        """
        Checks if there is an executable mismatch.

        Raises:
            ShebangViolation

        """
        if not self._is_first_comment(token):
            return  # this is a regular comment, not a shebang

        is_shebang = self._is_valid_shebang_line(token)
        self._check_executable_mismatch(token, is_shebang=is_shebang)
        if is_shebang:
            self._check_valid_shebang(token)

    def _check_executable_mismatch(
        self,
        token: tokenize.TokenInfo,
        *,
        is_shebang: bool,
    ) -> None:
        if is_windows() or self.filename == STDIN:
            # Windows does not have this concept of "executable" file.
            # The same for STDIN inputs.
            return

        is_executable = is_executable_file(self.filename)
        if is_executable and not is_shebang:
            self.add_violation(
                ShebangViolation(
                    text='file is executable but no shebang is present',
                ),
            )
        elif not is_executable and is_shebang:
            self.add_violation(
                ShebangViolation(
                    text='shebang is present but the file is not executable',
                ),
            )

    def _check_valid_shebang(self, token: tokenize.TokenInfo) -> None:
        if self._python_executable not in token.line:
            self.add_violation(
                ShebangViolation(
                    text='shebang is present but does not contain `python`',
                ),
            )

        if token.start[1] != 0:
            self.add_violation(
                ShebangViolation(
                    text='there is a whitespace before shebang',
                ),
            )

        if token.start[0] != 1:
            self.add_violation(
                ShebangViolation(
                    text='there are blank or comment lines before shebang',
                ),
            )

    def _is_first_comment(self, token: tokenize.TokenInfo) -> bool:
        all_tokens = iter(self.file_tokens)
        current_token = next(all_tokens)

        while True:
            if current_token == token:
                return True
            elif current_token.exact_type not in NEWLINES:
                break
            current_token = next(all_tokens)
        return False

    def _is_valid_shebang_line(self, token: tokenize.TokenInfo) -> bool:
        return self._shebang.match(token.line) is not None
