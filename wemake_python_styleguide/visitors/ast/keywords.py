# -*- coding: utf-8 -*-

import ast
from typing import ClassVar

from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
    RaiseNotImplementedViolation,
    RedundantFinallyViolation,
    RedundantForElseViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultipleIfsInComprehensionViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


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
            self.add_violation(WrongKeywordViolation(node))

    def visit(self, node: ast.AST) -> None:
        """
        Used to find wrong keywords.

        Raises:
            WrongKeywordViolation

        """
        self._check_keyword(node)
        self.generic_visit(node)


class WrongListComprehensionVisitor(BaseNodeVisitor):
    """Checks list comprehensions."""

    def _check_ifs(self, node: ast.comprehension) -> None:
        if len(node.ifs) > 1:
            # We are trying to fix line number in the report,
            # since `comprehension` does not have this property.
            parent = getattr(node, 'parent', node)
            self.add_violation(MultipleIfsInComprehensionViolation(parent))

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation,

        """
        self._check_ifs(node)
        self.generic_visit(node)


class WrongForElseVisitor(BaseNodeVisitor):
    """Responsible for restricting else in for loops with break."""

    def _check_for_needs_else(self, node: ast.For) -> None:
        break_in_for_loop = False

        for condition in ast.walk(node):
            if isinstance(condition, ast.Break):
                break_in_for_loop = True

        if node.orelse and break_in_for_loop:
            self.add_violation(RedundantForElseViolation(node=node))

    def visit_For(self, node: ast.For) -> None:
        """Used for find else block in for loops with break."""
        self._check_for_needs_else(node)
        self.generic_visit(node)


class WrongTryFinallyVisitor(BaseNodeVisitor):
    """Responsible for restricting finally in try blocks without except."""

    def _check_for_needs_except(self, node: ast.Try) -> None:
        if node.finalbody and not node.handlers:
            self.add_violation(RedundantFinallyViolation(node=node))

    def visit_Try(self, node: ast.Try) -> None:
        """Used for find finally in try blocks without except."""
        self._check_for_needs_except(node)
        self.generic_visit(node)


class WrongExceptionTypeVisitor(BaseNodeVisitor):
    """Finds use of ``BaseException`` exception."""

    def _check_exception_type(self, node: ast.ExceptHandler) -> None:
        exception_name = getattr(node, 'type', None)
        if exception_name is None:
            return
        exception_id = getattr(exception_name, 'id', None)
        if exception_id == 'BaseException':
            self.add_violation(BaseExceptionViolation(node))

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Checks if ``BaseException`` exception is used.

        Raises:
            BaseExceptionViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)
