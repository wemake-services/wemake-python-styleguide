# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, List, Optional, Sequence, Union

from wemake_python_styleguide.logics.functions import get_all_arguments
from wemake_python_styleguide.logics.nodes import is_doc_string
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    StatementHasNoEffectViolation,
    UnreachableCodeViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ParametersIndentationViolation,
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

AnyCollection = Union[
    ast.List,
    ast.Set,
    ast.Dict,
    ast.Tuple,
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


@final
@alias('visit_collection', (
    'visit_List',
    'visit_Set',
    'visit_Dict',
    'visit_Tuple',
))
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongParametersIndentationVisitor(BaseNodeVisitor):
    """Ensures that all parameters indentation follow our rules."""

    def _check_first_element(
        self,
        node: ast.AST,
        statement: ast.AST,
        extra_lines: int,
    ) -> Optional[bool]:
        if statement.lineno == node.lineno and not extra_lines:
            return False
        return None

    def _check_rest_elements(
        self,
        node: ast.AST,
        statement: ast.AST,
        previous_line: int,
        multi_line_mode: Optional[bool],
    ) -> Optional[bool]:
        previous_has_break = previous_line != statement.lineno
        if not previous_has_break and multi_line_mode:
            self.add_violation(ParametersIndentationViolation(node))
            return None
        elif previous_has_break and multi_line_mode is False:
            self.add_violation(ParametersIndentationViolation(node))
            return None
        return previous_has_break

    def _check_indentation(
        self,
        node: ast.AST,
        elements: Sequence[ast.AST],
        extra_lines: int = 0,  # we need it due to wrong lineno in collections
    ) -> None:
        multi_line_mode: Optional[bool] = None
        for index, statement in enumerate(elements):
            if index == 0:
                # We treat first element differently,
                # since it is impossible to say what kind of multi-line
                # parameters styles will be used at this moment.
                multi_line_mode = self._check_first_element(
                    node,
                    statement,
                    extra_lines,
                )
            else:
                multi_line_mode = self._check_rest_elements(
                    node,
                    statement,
                    elements[index - 1].lineno,
                    multi_line_mode,
                )

    def visit_collection(self, node: AnyCollection) -> None:
        """Checks how collection items indentation."""
        elements = node.keys if isinstance(node, ast.Dict) else node.elts
        self._check_indentation(node, elements, extra_lines=1)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Checks call arguments indentation."""
        all_args = [*node.args, *[kw.value for kw in node.keywords]]
        self._check_indentation(node, all_args)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks function parameters indentation."""
        self._check_indentation(node, get_all_arguments(node))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Checks base classes indentation."""
        all_args = [*node.bases, *[kw.value for kw in node.keywords]]
        self._check_indentation(node, all_args)
        self.generic_visit(node)
