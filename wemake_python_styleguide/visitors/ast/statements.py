import ast
from collections.abc import Mapping, Sequence
from typing import ClassVar, TypeAlias, final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.compat.aliases import (
    ForNodes,
    TextNodes,
)
from wemake_python_styleguide.compat.nodes import TryStar
from wemake_python_styleguide.logic.arguments import call_args
from wemake_python_styleguide.logic.naming import name_nodes
from wemake_python_styleguide.logic.tree.collections import (
    first,
    sequence_of_node,
)
from wemake_python_styleguide.violations.best_practices import (
    UnreachableCodeViolation,
    WrongNamedKeywordViolation,
)
from wemake_python_styleguide.violations.consistency import (
    AugmentedAssignPatternViolation,
    UselessNodeViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    AlmostSwappedViolation,
    MisrefactoredAssignmentViolation,
    NotATupleArgumentViolation,
    PointlessStarredViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

#: Statements that do have `.body` attribute.
_StatementWithBody: TypeAlias = (
    ast.If
    | types.AnyFor
    | ast.While
    | types.AnyWith
    | ast.Try
    | TryStar
    | ast.ExceptHandler
    | types.AnyFunctionDef
    | ast.ClassDef
    | ast.Module
    | ast.match_case
)


@final
@alias(
    'visit_statement_with_body',
    (
        'visit_If',
        'visit_For',
        'visit_AsyncFor',
        'visit_While',
        'visit_With',
        'visit_AsyncWith',
        'visit_Try',
        'visit_TryStar',
        'visit_ExceptHandler',
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
        'visit_ClassDef',
        'visit_Module',
        'visit_match_case',
    ),
)
class StatementsWithBodiesVisitor(BaseNodeVisitor):
    """
    Responsible for restricting incorrect patterns and members inside bodies.

    This visitor checks all statements that have multiline bodies.
    """

    _closing_nodes: ClassVar[types.AnyNodes] = (
        ast.Raise,
        ast.Return,
        ast.Break,
        ast.Continue,
    )

    _blocked_self_assignment: ClassVar[types.AnyNodes] = (ast.BinOp,)

    _nodes_with_orelse = (
        ast.If,
        *ForNodes,
        ast.While,
        ast.Try,
        TryStar,
    )

    # Useless nodes:
    _generally_useless_body: ClassVar[types.AnyNodes] = (
        ast.Break,
        ast.Continue,
        ast.Pass,
        ast.Constant,
        ast.Dict,
        ast.List,
        ast.Tuple,
        ast.Set,
    )
    _loop_useless_body: ClassVar[types.AnyNodes] = (
        ast.Return,
        ast.Raise,
    )

    _useless_combination: ClassVar[Mapping[str, types.AnyNodes]] = {
        'For': _generally_useless_body + _loop_useless_body,
        'AsyncFor': _generally_useless_body + _loop_useless_body,
        'While': _generally_useless_body + _loop_useless_body,
        'Try': (*_generally_useless_body, ast.Raise),
        'TryStar': (*_generally_useless_body, ast.Raise),
        'With': _generally_useless_body,
        'AsyncWith': _generally_useless_body,
    }

    def visit_statement_with_body(self, node: _StatementWithBody) -> None:
        """Visits statement's body internals."""
        self._check_internals(node.body)
        if isinstance(node, self._nodes_with_orelse):
            self._check_internals(node.orelse)
        if isinstance(node, ast.Try):
            self._check_internals(node.finalbody)

        self._check_swapped_variables(node.body)
        self._check_useless_node(node, node.body)
        self.generic_visit(node)

    def _check_swapped_variables(
        self,
        body: Sequence[ast.stmt],
    ) -> None:
        for assigns in sequence_of_node((ast.Assign,), body):
            self._almost_swapped(assigns)

    def _almost_swapped(self, assigns: Sequence[ast.Assign]) -> None:
        previous_var: set[str | None] = set()

        for assign in assigns:
            current_var = {
                first(name_nodes.flat_variable_names([assign])),
                first(name_nodes.get_variables_from_node(assign.value)),
            }

            if not all(map(bool, current_var)):
                previous_var.clear()
                continue

            if current_var == previous_var:
                self.add_violation(AlmostSwappedViolation(assign))

            if len(previous_var & current_var) == 1:
                current_var ^= previous_var
            previous_var = current_var

    def _check_useless_node(
        self,
        node: _StatementWithBody,
        body: Sequence[ast.stmt],
    ) -> None:
        if len(body) != 1:
            return

        forbidden = self._useless_combination.get(
            node.__class__.__qualname__,
            None,
        )

        if not forbidden or not isinstance(body[0], forbidden):
            return

        self.add_violation(
            UselessNodeViolation(
                node,
                text=node.__class__.__qualname__.lower(),
            ),
        )

    def _check_self_misrefactored_assignment(
        self,
        node: ast.AugAssign,
    ) -> None:
        node_value: ast.expr
        if isinstance(node.value, ast.BinOp):
            node_value = node.value.left

        if isinstance(
            node.value,
            self._blocked_self_assignment,
        ) and name_nodes.is_same_variable(node.target, node_value):
            self.add_violation(MisrefactoredAssignmentViolation(node))

    def _check_internals(self, body: Sequence[ast.stmt]) -> None:
        after_closing_node = False
        for statement in body:
            if after_closing_node:
                self.add_violation(UnreachableCodeViolation(statement))

            if isinstance(statement, self._closing_nodes):
                after_closing_node = True
            elif isinstance(statement, ast.AugAssign):
                self._check_self_misrefactored_assignment(statement)


@final
class PointlessStarredVisitor(BaseNodeVisitor):
    """Responsible for absence of useless starred expressions."""

    _pointless_star_nodes: ClassVar[types.AnyNodes] = (
        ast.Dict,
        ast.List,
        ast.Set,
        ast.Tuple,
        TextNodes,
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
            if isinstance(node, ast.Starred) and self._is_pointless_star(
                node.value,
            ):
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
            if not (
                isinstance(key_node, ast.Constant)
                and isinstance(key_node.value, str)
            ):
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
            if (
                isinstance(key_node, ast.Constant)
                and isinstance(key_node.value, str)
                and not str.isidentifier(key_node.value)
            ):
                return True
        return False


@final
class AssignmentPatternsVisitor(BaseNodeVisitor):
    """Responsible for checking assignment patterns."""

    def visit_Assign(self, node: ast.Assign) -> None:
        """Checks assignment patterns."""
        self._check_augmented_assign_pattern(node)
        self.generic_visit(node)

    def _check_augmented_assign_pattern(
        self,
        node: ast.Assign,
    ) -> None:
        if not isinstance(node.value, ast.BinOp):
            return

        is_checkable = (
            len(node.targets) == 1
            and isinstance(node.value.right, ast.Name)
            and isinstance(node.value.left, ast.Name)
        )

        if not is_checkable:
            return

        if name_nodes.is_same_variable(node.targets[0], node.value.left):
            self.add_violation(AugmentedAssignPatternViolation(node))


@final
class WrongMethodArgumentsVisitor(BaseNodeVisitor):
    """Ensures that all arguments follow our rules."""

    _no_tuples_collections: ClassVar[types.AnyNodes] = (
        ast.List,
        ast.ListComp,
        ast.Set,
        ast.SetComp,
    )

    def visit_Call(self, node: ast.Call) -> None:
        """Checks call arguments."""
        self._check_tuple_arguments_types(node)
        self.generic_visit(node)

    def _check_tuple_arguments_types(
        self,
        node: ast.Call,
    ) -> None:
        is_checkable = (
            isinstance(node.func, ast.Name)
            and node.func.id in constants.TUPLE_ARGUMENTS_METHODS
        )

        if not is_checkable:
            return

        all_args = call_args.get_all_args(node)
        for arg in all_args:
            if isinstance(arg, self._no_tuples_collections):
                self.add_violation(NotATupleArgumentViolation(node))
                break
