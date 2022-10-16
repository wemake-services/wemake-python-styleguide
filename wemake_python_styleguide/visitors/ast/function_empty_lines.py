import math
import tokenize
from typing import List, Tuple

from typing_extensions import final

from wemake_python_styleguide.violations import best_practices
from wemake_python_styleguide.visitors import base


@final
class _Function(object):

    def __init__(self, file_tokens: Tuple[tokenize.TokenInfo, ...]):
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

    def _is_target_line(self, token) -> bool:
        is_comment = '#' in token.line
        is_string = token.type == tokenize.STRING
        is_multistring_end = '"""' in token.line
        return is_comment or is_string or is_multistring_end


@final
class _FileFunctions(object):

    def __init__(self, file_tokens: Tuple[tokenize.TokenInfo, ...]):
        self._file_tokens = file_tokens

    def as_list(self) -> List[_Function]:
        functions = []
        function_tokens: List[tokenize.TokenInfo] = []
        in_function = False
        for token in self._file_tokens:
            if self._is_definition_token(token):
                in_function = True
            elif self._is_function_end(token, function_tokens):
                in_function = False
                functions.append(_Function(tuple(function_tokens)))
                function_tokens = []
            if in_function:
                function_tokens.append(token)
        return functions

    def _is_definition_token(self, token) -> bool:
        return token.type == tokenize.NAME and token.string == 'def'

    def _is_function_end(self, token, function_tokens) -> bool:
        is_dedent_token = token.type == tokenize.DEDENT and token.start[1] == 0
        return is_dedent_token and function_tokens


@final
class _FileTokens(object):

    def __init__(
        self,
        file_functions: _FileFunctions,
        exps_for_one_empty_line: int,
    ) -> None:
        self._file_functions = file_functions
        self._exps_for_one_empty_line = exps_for_one_empty_line

    def analyze(self) -> List[best_practices.WrongEmptyLinesCountViolation]:
        violations = []
        for function in self._file_functions.as_list():
            splitted_function_body = function.body().strip().split('\n')
            empty_lines_count = len([
                line for line in splitted_function_body if line == ''
            ])
            if not empty_lines_count:
                return []
            available_empty_lines = self._available_empty_lines(
                len(splitted_function_body), empty_lines_count,
            )
            if empty_lines_count > available_empty_lines:
                violations.append(
                    best_practices.WrongEmptyLinesCountViolation(
                        function.name_token(),
                        text=str(empty_lines_count),
                        baseline=available_empty_lines,
                    ),
                )
        return violations

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
        self._file_tokens: List[tokenize.TokenInfo] = []

    def visit(self, token: tokenize.TokenInfo) -> None:
        """Find empty lines count."""
        self._file_tokens.append(token)
        if token.type != tokenize.ENDMARKER:
            return
        violations = _FileTokens(
            _FileFunctions(
                tuple(self._file_tokens),
            ),
            self.options.exps_for_one_empty_line,
        ).analyze()
        for violation in violations:
            self.add_violation(violation)
