# -*- coding: utf-8 -*-

import tokenize
from typing import Dict, Sequence

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.consistency import (
    ExtraIndentationViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class ExtraIndentationVisitor(BaseTokenVisitor):
    """
    Is used to find extra indentation in nodes.

    Algorithm:
    1. goes through all nodes in a module
    2. remembers minimal indentation for each line
    3. compares each two closest lines: indentation should not be >4

    """

    _ignored_tokens = (
        tokenize.NEWLINE,
    )

    _ignored_previous_token = (
        tokenize.NL,
    )

    def __init__(self, *args, **kwargs) -> None:
        """Creates empty counter."""
        super().__init__(*args, **kwargs)
        self._offsets: Dict[int, tokenize.TokenInfo] = {}

    def _check_extra_indentation(self, token: tokenize.TokenInfo) -> None:
        lineno, offset = token.start
        if lineno not in self._offsets:
            self._offsets[lineno] = token

    def _get_token_offset(self, token: tokenize.TokenInfo) -> int:
        if token.exact_type == tokenize.INDENT:
            offset = token.end[1]
        else:
            offset = token.start[1]
        return offset

    def _check_individual_line(
        self,
        lines: Sequence[int],
        line: int,
        index: int,
    ) -> None:
        current_token = self._offsets[line]
        if current_token.exact_type in self._ignored_tokens:
            return

        previous_token = self._offsets[lines[index - 1]]
        if previous_token.exact_type in self._ignored_previous_token:
            return

        offset = self._get_token_offset(current_token)
        previous_offset = self._get_token_offset(previous_token)

        if offset > previous_offset + 4:
            self.add_violation(ExtraIndentationViolation(current_token))

    def _post_visit(self) -> None:
        lines = sorted(self._offsets.keys())

        for index, line in enumerate(lines):
            if index == 0 or line != lines[index - 1] + 1:
                continue
            self._check_individual_line(lines, line, index)

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Goes through all nodes."""
        self._check_extra_indentation(token)
