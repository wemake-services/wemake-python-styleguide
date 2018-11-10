# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, List, Union

from wemake_python_styleguide.logics.nodes import is_doc_string
from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    StatementHasNoEffectViolation,
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

    _have_doc_strings: ClassVar[AnyNodes] = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Module,
    )

    # Not typed, since `mypy` will complain about `isinstance` calls.
    _nodes_with_orelse = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
    )

    _have_effect: ClassVar[AnyNodes] = (
        ast.Return,
        ast.YieldFrom,
        ast.Yield,

        ast.Raise,
        ast.Break,
        ast.Continue,

        ast.Call,
        ast.Await,

        ast.Nonlocal,
        ast.Global,
        ast.Delete,
        ast.Pass,

        ast.Assert,
    )

    def _check_expression(
        self,
        node: ast.Expr,
        is_first: bool = False,
    ) -> None:
        if isinstance(node.value, self._have_effect):
            return

        if is_first and is_doc_string(node):
            parent = getattr(node, 'parent', None)
            if isinstance(parent, self._have_doc_strings):
                return

        self.add_violation(StatementHasNoEffectViolation(node))

    def _check_internals(self, body: List[ast.stmt]) -> None:
        after_closing_node = False
        for index, statement in enumerate(body):
            if after_closing_node:
                self.add_violation(UnreachableCodeViolation(statement))

            if isinstance(statement, self._closing_nodes):
                after_closing_node = True

            if isinstance(statement, ast.Expr):
                self._check_expression(statement, is_first=index == 0)

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
