import math
import tokenize

from typing_extensions import final

from wemake_python_styleguide.violations import best_practices
from wemake_python_styleguide.visitors import base


@final
class WrongEmptyLinesCountVisitor(base.BaseTokenVisitor):
    """Restricts empty lines in function or method body."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes a counter."""
        super().__init__(*args, **kwargs)
        self._empty_lines_count = 0
        self._function_start_line = 0

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Find empty lines count."""
        self._try_mark_function_start(token)
        if self._function_start_line:
            if token.type == tokenize.NL and token.line == '\n':
                self._empty_lines_count += 1
            self._check_empty_lines(token)

    def _check_empty_lines(self, token: tokenize.TokenInfo):
        if token.type == tokenize.DEDENT and token.line == '':
            func_lines = token.start[0] - self._function_start_line - 1
            if self._empty_lines_count:
                available_empty_lines = self._available_empty_lines(
                    func_lines,
                    self._empty_lines_count,
                )
                if self._empty_lines_count > available_empty_lines:
                    self.add_violation(
                        best_practices.WrongEmptyLinesCountViolation(
                            token,
                            text=str(self._empty_lines_count),
                            baseline=available_empty_lines,
                        ),
                    )
                self._function_start_line = 0

    def _try_mark_function_start(self, token: tokenize.TokenInfo):
        if token.string == 'def':
            self._empty_lines_count = 0
            self._function_start_line = token.start[0]

    def _available_empty_lines(
        self,
        function_len: int,
        empty_lines: int,
    ) -> int:
        option = self.options.exps_for_one_empty_line
        if option == 0:
            return 0
        lines_with_expressions = function_len - empty_lines
        return math.floor(lines_with_expressions / option)
