# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.complexity import UnusedElseViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongForElseVisitor(BaseNodeVisitor):
    """Responsible for restricting else in for loops without break."""

    def visit_For(self, node: ast.For) -> None:
        """Used for find else block in for loops without breaks."""
        break_in_for_loop = False

        for condition in ast.walk(node):
            if isinstance(condition, (ast.Break)):
                break_in_for_loop = True

        if node.orelse and not break_in_for_loop:
            self.add_violation(UnusedElseViolation(node=node))

        self.generic_visit(node)
