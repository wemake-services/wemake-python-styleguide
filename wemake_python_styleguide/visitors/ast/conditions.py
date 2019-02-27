# -*- coding: utf-8 -*-

import ast
from typing import ClassVar

from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    NegatedConditionsViolation,
    RedundantReturningElseViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class IfStatementVisitor(BaseNodeVisitor):
    """Checks single and consecutive ``if`` statement nodes."""

    #: Nodes that break or return the execution flow.
    _returning_nodes: ClassVar[AnyNodes] = (
        ast.Break,
        ast.Raise,
        ast.Return,
    )

    def _check_negated_conditions(self, node: ast.If) -> None:
        if not node.orelse:
            return

        if isinstance(node.test, ast.UnaryOp):
            if isinstance(node.test.op, ast.Not):
                self.add_violation(NegatedConditionsViolation(node))
        elif isinstance(node.test, ast.Compare):
            if any(isinstance(elem, ast.NotEq) for elem in node.test.ops):
                self.add_violation(NegatedConditionsViolation(node))

    def _check_redundant_else(self, node: ast.If) -> None:
        if not node.orelse:
            return

        next_chain = getattr(node, 'wps_chain', None)  # TODO: move into utils
        has_previous_chain = getattr(node, 'wps_chained', None)
        if next_chain or has_previous_chain:
            return

        if any(isinstance(line, self._returning_nodes) for line in node.body):
            self.add_violation(RedundantReturningElseViolation(node))

    def visit_If(self, node: ast.If) -> None:
        """
        Checks ``if`` nodes.

        Raises:
            RedundantReturningElseViolation
            NegatedConditionsViolation

        """
        self._check_negated_conditions(node)
        self._check_redundant_else(node)
        self.generic_visit(node)
