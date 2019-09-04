# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Mapping, Optional, Sequence, Union

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import ForNodes, FunctionNodes
from wemake_python_styleguide.logic.collections import normalize_dict_elements
from wemake_python_styleguide.logic.functions import get_all_arguments
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.strings import is_doc_string
from wemake_python_styleguide.types import (
    AnyFor,
    AnyFunctionDef,
    AnyNodes,
    AnyWith,
)
from wemake_python_styleguide.violations.best_practices import (
    StatementHasNoEffectViolation,
    UnreachableCodeViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ParametersIndentationViolation,
    UselessNodeViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    PointlessStarredViolation,
    WrongNamedKeywordViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

StatementWithBody = Union[
    ast.If,
    AnyFor,
    ast.While,
    AnyWith,
    ast.Try,
    ast.ExceptHandler,
    AnyFunctionDef,
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
        *FunctionNodes,
        ast.ClassDef,
        ast.Module,
    )

    _nodes_with_orelse = (
        ast.If,
        *ForNodes,
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

    # Useless nodes:
    _generally_useless_body: ClassVar[AnyNodes] = (
        ast.Break,
        ast.Continue,
        ast.Pass,
        ast.Ellipsis,
    )
    _loop_useless_body: ClassVar[AnyNodes] = (
        ast.Return,
        ast.Raise,
    )

    _useless_combination: ClassVar[Mapping[str, AnyNodes]] = {
        'For': _generally_useless_body + _loop_useless_body,
        'AsyncFor': _generally_useless_body + _loop_useless_body,
        'While': _generally_useless_body + _loop_useless_body,
        'Try': _generally_useless_body + (ast.Raise,),
        'With': _generally_useless_body,
        'AsyncWith': _generally_useless_body,
    }

    def visit_statement_with_body(self, node: StatementWithBody) -> None:
        """
        Visits statement's body internals.

        Raises:
            UnreachableCodeViolation,
            UselessNodeViolation

        """
        self._check_internals(node.body)
        if isinstance(node, self._nodes_with_orelse):
            self._check_internals(node.orelse)
        if isinstance(node, ast.Try):
            self._check_internals(node.finalbody)

        self._check_useless_node(node, node.body)
        self.generic_visit(node)

    def _check_useless_node(
        self,
        node: StatementWithBody,
        body: Sequence[ast.stmt],
    ) -> None:
        if len(body) != 1:
            return

        forbiden = self._useless_combination.get(
            node.__class__.__qualname__, None,
        )

        if not forbiden or not isinstance(body[0], forbiden):
            return

        self.add_violation(
            UselessNodeViolation(
                node, text=node.__class__.__qualname__.lower(),
            ),
        )

    def _check_expression(
        self,
        node: ast.Expr,
        is_first: bool = False,
    ) -> None:
        if isinstance(node.value, self._have_effect):
            return

        if is_first and is_doc_string(node):
            if isinstance(get_parent(node), self._have_doc_strings):
                return

        self.add_violation(StatementHasNoEffectViolation(node))

    def _check_internals(self, body: Sequence[ast.stmt]) -> None:
        after_closing_node = False
        for index, statement in enumerate(body):
            if after_closing_node:
                self.add_violation(UnreachableCodeViolation(statement))

            if isinstance(statement, self._closing_nodes):
                after_closing_node = True

            if isinstance(statement, ast.Expr):
                self._check_expression(statement, is_first=index == 0)


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

    def visit_collection(self, node: AnyCollection) -> None:
        """Checks how collection items indentation."""
        if isinstance(node, ast.Dict):
            elements = normalize_dict_elements(node)
        else:
            elements = node.elts
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


@final
class PointlessStarredVisitor(BaseNodeVisitor):
    """Responsible for absence of useless starred expressions."""

    _pointless_star_nodes: ClassVar[AnyNodes] = (
        ast.Dict,
        ast.List,
        ast.Set,
        ast.Tuple,
    )

    def visit_Call(self, node: ast.Call) -> None:
        """Checks useless call arguments."""
        self._check_starred_args(node.args)
        self._check_double_starred_dict(node.keywords)
        self.generic_visit(node)

    def _check_starred_args(
        self,
        args: Sequence[ast.AST],
    ) -> None:
        for node in args:
            if isinstance(node, ast.Starred):
                if self._is_pointless_star(node.value):
                    self.add_violation(PointlessStarredViolation(node))

    def _check_double_starred_dict(
        self,
        keywords: Sequence[ast.keyword],
    ) -> None:
        for keyword in keywords:
            if keyword.arg is not None:
                continue

            complex_keys = self._has_non_string_keys(keyword)
            pointless_args = self._is_pointless_star(keyword.value)
            if not complex_keys and pointless_args:
                self.add_violation(PointlessStarredViolation(keyword.value))

    def _is_pointless_star(self, node: ast.AST) -> bool:
        return isinstance(node, self._pointless_star_nodes)

    def _has_non_string_keys(self, node: ast.keyword) -> bool:
        if not isinstance(node.value, ast.Dict):
            return True

        for key_node in node.value.keys:
            if not isinstance(key_node, ast.Str):
                return True
        return False


@final
class WrongNamedKeywordVisitor(BaseNodeVisitor):
    """Responsible for absence of wrong keywords."""

    def visit_Call(self, node: ast.Call) -> None:
        """Checks useless call arguments."""
        self._check_double_starred_dict(node.keywords)
        self.generic_visit(node)

    def _check_double_starred_dict(
        self,
        keywords: Sequence[ast.keyword],
    ) -> None:
        for keyword in keywords:
            if keyword.arg is not None:
                continue

            if self._has_wrong_keys(keyword):
                self.add_violation(WrongNamedKeywordViolation(keyword.value))

    def _has_wrong_keys(self, node: ast.keyword) -> bool:
        if not isinstance(node.value, ast.Dict):
            return False

        for key_node in node.value.keys:
            if isinstance(key_node, ast.Str) and not str.isidentifier(key_node.s):
                return True
        return False
