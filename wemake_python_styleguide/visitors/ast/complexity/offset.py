# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors.complexity import TooDeepNestingViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class OffsetVisitor(BaseNodeVisitor):
    """This visitor checks offset values for some nodes."""

    def _check_offset(self, node: ast.AST) -> None:
        offset = getattr(node, 'col_offset', None)
        if offset is not None and offset > self.options.max_offset_blocks * 4:
            self.add_error(TooDeepNestingViolation(node))

    def visit_Expr(self, node: ast.AST) -> None:
        """
        Checks statement's offset.

        We check only several nodes, because other nodes might have
        different offsets, which is fine.
        For example, ``ast.Name`` node has inline offset,
        which can take values from ``0`` to ``~80``.
        But ``Name`` node is allowed to behave like so.

        Raises:
            TooDeepNestingViolation

        """
        self._check_offset(node)
        self.generic_visit(node)

    visit_Try = visit_ExceptHandler = visit_Expr
    visit_For = visit_With = visit_While = visit_If = visit_Expr
    visit_Raise = visit_Return = visit_Continue = visit_Break = visit_Expr
    visit_Assign = visit_Expr
