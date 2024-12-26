import math
import tokenize
from collections.abc import Iterable
from typing import final

from wemake_python_styleguide.violations import best_practices
from wemake_python_styleguide.visitors import base


@final
class _Function:
    def __init__(self, file_tokens: list[tokenize.TokenInfo]) -> None:
        self._tokens = file_tokens

    def name_token(self) -> tokenize.TokenInfo:
        return self._tokens[1]

    def body(self) -> str:
        target_tokens = []
        for token in self._tokens:
            if self._is_target_line(token):
                continue
            target_tokens.append(token)
        return ''.join([target_token.string for target_token in target_tokens])

    def _is_target_line(self, token: tokenize.TokenInfo) -> bool:
        stripped_token_line = token.line.strip()
        is_comment = False
        if stripped_token_line:
            is_comment = stripped_token_line.startswith('#')
        is_multistring_end = '"""' in token.line
        return is_comment or is_multistring_end


@final
class _FileFunctions:
    def __init__(self, file_tokens: list[tokenize.TokenInfo]) -> None:
        self._file_tokens = file_tokens

    def search_functions(self) -> Iterable[_Function]:  # noqa: WPS210
        function_tokens: list[tokenize.TokenInfo] = []
        in_function = False
        function_start_token = (0, 0)
        for token_index, token in enumerate(self._file_tokens):
            function_ended = self._is_function_end(
                token,
                token_index,
                function_start_token,
                function_tokens_exists=bool(function_tokens),
            )
            if not in_function and self._is_function_start(token):
                in_function = True
                function_start_token = token.start
            elif function_ended:
                in_function = False
                function_start_token = (function_start_token[0], 0)
                yield _Function(function_tokens)
                function_tokens = []
            if in_function:
                function_tokens.append(token)

    def _is_function_start(self, token: tokenize.TokenInfo) -> bool:
        return token.type == tokenize.NAME and token.string in {'def', 'async'}

    def _is_function_end(
        self,
        token: tokenize.TokenInfo,
        token_index: int,
        function_start: tuple[int, int],
        *,
        function_tokens_exists: bool,
    ) -> bool:
        next_token = self._next_token(token_index)
        is_elipsis_end = (
            next_token
            and next_token.exact_type == tokenize.NEWLINE
            and token.string == '...'
            and token.start[0] == function_start[0]
        )
        if is_elipsis_end:
            return True
        column_valid = token.start[1] in {0, function_start[1]}
        is_dedent_token = token.type == tokenize.DEDENT
        return is_dedent_token and function_tokens_exists and column_valid

    def _next_token(
        self,
        token_index: int,
    ) -> tokenize.TokenInfo | None:
        try:
            return self._file_tokens[token_index + 1]
        except IndexError:
            return None


@final
class _FileTokens:
    def __init__(
        self,
        file_functions: _FileFunctions,
        exps_for_one_empty_line: int,
    ) -> None:
        self._file_functions = file_functions
        self._exps_for_one_empty_line = exps_for_one_empty_line

    def analyze(self) -> Iterable[best_practices.WrongEmptyLinesCountViolation]:
        for function in self._file_functions.search_functions():
            splitted_function_body = function.body().strip().split('\n')
            empty_lines_count = len(
                [line for line in splitted_function_body if not line],
            )
            if not empty_lines_count:
                continue

            available_empty_lines = self._available_empty_lines(
                len(splitted_function_body),
                empty_lines_count,
            )
            if empty_lines_count > available_empty_lines:
                yield best_practices.WrongEmptyLinesCountViolation(
                    function.name_token(),
                    text=str(empty_lines_count),
                    baseline=available_empty_lines,
                )

    def _available_empty_lines(
        self,
        function_len: int,
        empty_lines: int,
    ) -> int:
        option = self._exps_for_one_empty_line
        if option == 0:
            return 0
        lines_with_expressions = function_len - empty_lines
        return math.floor(lines_with_expressions / option)


@final
class WrongEmptyLinesCountVisitor(base.BaseTokenVisitor):
    """Restricts empty lines in function or method body."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes a counter."""
        super().__init__(*args, **kwargs)
        self._file_tokens: list[tokenize.TokenInfo] = []

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Find empty lines count."""
        self._file_tokens.append(token)
        if token.type != tokenize.ENDMARKER:
            return
        violations = _FileTokens(
            _FileFunctions(self._file_tokens),
            self.options.exps_for_one_empty_line,
        ).analyze()
        for violation in violations:
            self.add_violation(violation)
