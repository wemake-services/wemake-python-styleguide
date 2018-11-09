# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, List, Union

from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    UnreachableCodeViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

StatementWithBody = Union[
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.ExceptHandler,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Module,
]


@final
@alias('visit_statement_with_body', (
    'visit_If',
    'visit_For',
    'visit_AsyncFor',
    'visit_While',
    'visit_With',
    'visit_AsyncWith',
    'visit_Try',
    'visit_ExceptHandler',
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
    'visit_ClassDef',
    'visit_Module',
))
class StatementsWithBodiesVisitor(BaseNodeVisitor):
    """
    Responsible for restricting incorrect patterns and members inside bodies.

    This visitor checks all statements that have multiline bodies.
    """

    _closing_nodes: ClassVar[AnyNodes] = (
        ast.Raise,
        ast.Return,
        ast.Break,
        ast.Continue,
    )

    # Not typed, since `mypy` will complain about `isinstance` calls.
    _nodes_with_orelse = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
    )

    def _check_internals(self, body: List[ast.stmt]) -> None:
        after_closing_node = False
        for statement in body:
            if after_closing_node:
                self.add_violation(UnreachableCodeViolation(statement))

            if isinstance(statement, self._closing_nodes):
                after_closing_node = True

    def visit_statement_with_body(self, node: StatementWithBody) -> None:
        """
        Visits statement's body internals.

        Raises:
            UnreachableCodeViolation

        """
        self._check_internals(node.body)
        if isinstance(node, self._nodes_with_orelse):
            self._check_internals(node.orelse)
        if isinstance(node, ast.Try):
            self._check_internals(node.finalbody)

        self.generic_visit(node)
