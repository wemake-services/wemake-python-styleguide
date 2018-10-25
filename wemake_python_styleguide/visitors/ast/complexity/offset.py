# -*- coding: utf-8 -*-

import ast
from typing import Union

from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.complexity import (
    TooDeepNestingViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

AsyncNodes = Union[ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith]


@final
@alias('visit_line_expression', (
    'visit_Try',
    'visit_ExceptHandler',
    'visit_Expr',
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
    'visit_Await',
    'visit_Pass',
))
@alias('visit_async_statement', (
    'visit_AsyncFor',
    'visit_AsyncWith',
    'visit_AsyncFunctionDef',
))
class OffsetVisitor(BaseNodeVisitor):
    """Checks offset values for several nodes."""

    def _check_offset(self, node: ast.AST, error: int = 0) -> None:
        offset = getattr(node, 'col_offset', 0) - error
        if offset > self.options.max_offset_blocks * 4:
            self.add_violation(TooDeepNestingViolation(node))

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

    def visit_async_statement(self, node: AsyncNodes):
        """
        Checks async definitions offset.

        This is a temporary check for async-based expressions, because offset
        for them isn't calculated properly. We can calculate right version
        of offset with subscripting ``6`` (length of "async " part).

        Read more:
            https://bugs.python.org/issue29205
            github.com/wemake-services/wemake-python-styleguide/issues/282

        Raises:
            TooDeepNestingViolation

        """
        error = 6 if node.col_offset % 4 != 0 else 0
        self._check_offset(node, error=error)
        self.generic_visit(node)
