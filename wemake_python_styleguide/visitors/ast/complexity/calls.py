import ast
from itertools import takewhile
from typing import Set

from typing_extensions import final

from wemake_python_styleguide.logic.tree.calls import parts
from wemake_python_styleguide.violations.complexity import (
    TooLongCallChainViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class CallChainsVisitor(BaseNodeVisitor):
    """Counts number of consecutive calls."""

    def __init__(self, *args, **kwargs) -> None:
        """Keeps visited calls to not visit them again."""
        super().__init__(*args, **kwargs)
        self._visited_calls: Set[ast.Call] = set()

    def visit_Call(self, node: ast.Call) -> None:
        """
        Checks number of function calls.

        Raises:
            TooLongCallChainViolation

        """
        self._check_consecutive_call_number(node)
        self.generic_visit(node)

    def _is_call(self, node: ast.AST) -> bool:
        return isinstance(node, ast.Call)

    def _check_consecutive_call_number(self, node: ast.Call) -> None:
        if node in self._visited_calls:
            return

        consecutive_calls = set(takewhile(
            self._is_call, parts(node),
        ))

        self._visited_calls.update(consecutive_calls)
        num_of_calls = len(consecutive_calls)

        if num_of_calls > self.options.max_call_level:
            self.add_violation(
                TooLongCallChainViolation(
                    node,
                    text=str(num_of_calls),
                    baseline=self.options.max_call_level,
                ),
            )
