# -*- coding: utf-8 -*-

import ast
from collections import Counter
from typing import ClassVar, List, Type, Union

import astor

from wemake_python_styleguide.logics.nodes import get_parent, is_contained
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
    DuplicateExceptionViolation,
    RaiseNotImplementedViolation,
    RedundantFinallyViolation,
    TryExceptMultipleReturnPathViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.violations.consistency import (
    InconsistentReturnViolation,
    InconsistentYieldViolation,
    MultipleContextManagerAssignmentsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

AnyWith = Union[ast.With, ast.AsyncWith]
ReturningViolations = Union[
    Type[InconsistentReturnViolation],
    Type[InconsistentYieldViolation],
]


@final
class WrongRaiseVisitor(BaseNodeVisitor):
    """Finds wrong ``raise`` keywords."""

    def _check_exception_type(self, node: ast.Raise) -> None:
        exception = getattr(node, 'exc', None)
        if exception is None:
            return

        exception_func = getattr(exception, 'func', None)
        if exception_func:
            exception = exception_func

        exception_name = getattr(exception, 'id', None)
        if exception_name == 'NotImplemented':
            self.add_violation(RaiseNotImplementedViolation(node))

    def visit_Raise(self, node: ast.Raise) -> None:
        """
        Checks how ``raise`` keyword is used.

        Raises:
            RaiseNotImplementedViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class ConsistentReturningVisitor(BaseNodeVisitor):
    """Finds incorrect and inconsistent ``return`` and ``yield`` nodes."""

    def _check_last_return_in_function(self, node: ast.Return) -> None:
        parent = get_parent(node)
        if not isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return

        if node is parent.body[-1] and node.value is None:
            self.add_violation(InconsistentReturnViolation(node))

    def _iterate_returning_values(
        self,
        node: AnyFunctionDef,
        returning_type,  # mypy is not ok with this type declaration
        violation: ReturningViolations,
    ):
        returns: List[ast.Return] = []
        has_values = False
        for sub_node in ast.walk(node):
            if isinstance(sub_node, returning_type):
                if sub_node.value:
                    has_values = True
                returns.append(sub_node)

        for sub_node in returns:
            if not sub_node.value and has_values:
                self.add_violation(violation(sub_node))

    def _check_return_values(self, node: AnyFunctionDef) -> None:
        self._iterate_returning_values(
            node, ast.Return, InconsistentReturnViolation,
        )

    def _check_yield_values(self, node: AnyFunctionDef) -> None:
        self._iterate_returning_values(
            node, ast.Yield, InconsistentYieldViolation,
        )

    def visit_Return(self, node: ast.Return) -> None:
        """
        Checks ``return`` statements for consistency.

        Raises:
            InconsistentReturnViolation

        """
        self._check_last_return_in_function(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Helper to get all ``return`` and ``yield`` nodes in a function at once.

        Raises:
            InconsistentReturnViolation
            InconsistentYieldViolation

        """
        self._check_return_values(node)
        self._check_yield_values(node)
        self.generic_visit(node)


@final
class WrongKeywordVisitor(BaseNodeVisitor):
    """Finds wrong keywords."""

    _forbidden_keywords: ClassVar[AnyNodes] = (
        ast.Pass,
        ast.Delete,
        ast.Global,
        ast.Nonlocal,
    )

    def _check_keyword(self, node: ast.AST) -> None:
        if isinstance(node, self._forbidden_keywords):
            self.add_violation(
                WrongKeywordViolation(
                    node, text=node.__class__.__qualname__.lower(),
                ),
            )

    def visit(self, node: ast.AST) -> None:
        """
        Used to find wrong keywords.

        Raises:
            WrongKeywordViolation

        """
        self._check_keyword(node)
        self.generic_visit(node)


@final
class WrongTryExceptVisitor(BaseNodeVisitor):
    """Responsible for examining ``try`` and friends."""

    _base_exception: ClassVar[str] = 'BaseException'

    def _check_if_needs_except(self, node: ast.Try) -> None:
        if node.finalbody and not node.handlers:
            self.add_violation(RedundantFinallyViolation(node))

    def _check_exception_type(self, node: ast.ExceptHandler) -> None:
        exception_name = getattr(node, 'type', None)
        if exception_name is None:
            return

        exception_id = getattr(exception_name, 'id', None)
        if exception_id == self._base_exception:
            self.add_violation(BaseExceptionViolation(node))

    def _check_duplicate_exceptions(self, node: ast.Try) -> None:
        exceptions: List[str] = []
        for exc_handler in node.handlers:
            # There might be complex things hidden inside an exception type,
            # so we want to get the string representation of it:
            if isinstance(exc_handler.type, ast.Name):
                exceptions.append(astor.to_source(exc_handler.type).strip())
            elif isinstance(exc_handler.type, ast.Tuple):
                exceptions.extend([
                    astor.to_source(node).strip()
                    for node in exc_handler.type.elts
                ])

        counts = Counter(exceptions)
        for exc_name, count in counts.items():
            if count > 1:
                self.add_violation(
                    DuplicateExceptionViolation(node, text=exc_name),
                )

    def _check_return_path(self, node: ast.Try) -> None:
        try_has = any(
            is_contained(line, ast.Return) for line in node.body
        )
        except_has = any(
            is_contained(except_handler, ast.Return)
            for except_handler in node.handlers
        )
        else_has = any(
            is_contained(line, ast.Return) for line in node.orelse
        )
        finally_has = any(
            is_contained(line, ast.Return) for line in node.finalbody
        )

        if finally_has and (try_has or except_has):
            self.add_violation(TryExceptMultipleReturnPathViolation(node))
        if else_has and try_has:
            self.add_violation(TryExceptMultipleReturnPathViolation(node))

    def visit_Try(self, node: ast.Try) -> None:
        """
        Used for find finally in try blocks without except.

        Raises:
            RedundantFinallyViolation
            DuplicateExceptionViolation
            TryExceptMultipleReturnPathViolation

        """
        self._check_if_needs_except(node)
        self._check_duplicate_exceptions(node)
        self._check_return_path(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Checks all ``ExceptionHandler`` nodes.

        Raises:
            BaseExceptionViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)


@final
@alias('visit_any_with', (
    'visit_With',
    'visit_AsyncWith',
))
class WrongContextManagerVisitor(BaseNodeVisitor):
    """Checks context managers."""

    def _check_target_assignment(self, node: AnyWith):
        if len(node.items) > 1:
            self.add_violation(
                MultipleContextManagerAssignmentsViolation(node),
            )

    def visit_any_with(self, node: AnyWith) -> None:
        """
        Checks the number of assignments for context managers.

        Raises:
            MultipleContextManagerAssignmentsViolation

        """
        self._check_target_assignment(node)
        self.generic_visit(node)
