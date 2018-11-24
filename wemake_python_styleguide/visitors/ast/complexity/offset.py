# -*- coding: utf-8 -*-

import ast
from typing import ClassVar

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.complexity import (
    TooDeepNestingViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias('visit_line_expression', (
    'visit_Try',
    'visit_ExceptHandler',
    'visit_For',
    'visit_With',
    'visit_While',
    'visit_If',
    'visit_Raise',
    'visit_Return',
    'visit_Continue',
    'visit_Break',
    'visit_Assign',
    'visit_Expr',
    'visit_Pass',
    'visit_ClassDef',
    'visit_FunctionDef',
    'visit_AsyncFor',
    'visit_AsyncWith',
    'visit_AsyncFunctionDef',
))
class OffsetVisitor(BaseNodeVisitor):
    """Checks offset values for several nodes."""

    #: Maximum number of blocks to nest different structures:
    _max_offset_blocks: ClassVar[int] = 5

    def _check_offset(self, node: ast.AST) -> None:
        offset = getattr(node, 'col_offset', 0)
        if offset > self._max_offset_blocks * 4:
            self.add_violation(TooDeepNestingViolation(node, text=str(offset)))

    def visit_line_expression(self, node: ast.AST) -> None:
        """
        Checks statement's offset.

        We check only several nodes, because other nodes might have
        different offsets, which is fine.
        For example, ``ast.Name`` node has inline offset,
        which can take values from ``0`` to ``~80``.
        But ``Name`` node is allowed to behave like so.

        So, we only check nodes that represent "all liners".

        Raises:
            TooDeepNestingViolation

        """
        self._check_offset(node)
        self.generic_visit(node)
