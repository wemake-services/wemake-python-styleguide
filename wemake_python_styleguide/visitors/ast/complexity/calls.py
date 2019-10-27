# -*- coding: utf-8 -*-

import ast
from itertools import takewhile
from typing import cast, Set
from typing import Iterable, Optional

from typing_extensions import final

from wemake_python_styleguide.violations.complexity import (
    TooLongCallChainViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class CallChainsVisitor(BaseNodeVisitor):
    """Counts access number for expressions."""

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

    def _chained_item(self, iterator: ast.AST) -> Optional[ast.AST]:
        if isinstance(iterator, ast.Call):
            for child in ast.iter_child_nodes(iterator):
                if isinstance(child, ast.Call):
                    return iterator
        elif isinstance(iterator, ast.Expr) and isinstance(iterator.value, ast.Call):
            return iterator.value
        return None

    def _parts(self, node: ast.Call) -> Iterable[ast.AST]:
        iterator: ast.AST = node

        while True:
            yield iterator

            chained_item = self._chained_item(iterator)
            if chained_item is None:
                return
            iterator = chained_item

    def _check_consecutive_call_number(self, node: ast.Call) -> None:
        if node in self._visited_calls:
            return

        consecutive_calls = cast(Set[ast.Call], set(takewhile(
            self._is_call, self._parts(node),
        )))

        self._visited_calls.update(consecutive_calls)
        num_of_calls = len(self._visited_calls)

        if num_of_calls > self.options.max_call_level:
            self.add_violation(
                TooLongCallChainViolation(
                    node, text=str(num_of_calls),
                ),
            )
