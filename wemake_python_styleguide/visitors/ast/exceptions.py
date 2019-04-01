# -*- coding: utf-8 -*-

import ast
from collections import Counter
from typing import ClassVar, List

import astor
from typing_extensions import final

from wemake_python_styleguide.logics.nodes import is_contained
from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
    DuplicateExceptionViolation,
    NestedTryViolation,
    RedundantFinallyViolation,
    TryExceptMultipleReturnPathViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UselessExceptCaseViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


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

    def _check_useless_except(self, node: ast.ExceptHandler) -> None:
        if len(node.body) != 1:
            return

        body = node.body[0]
        if not isinstance(body, ast.Raise):
            return

        if isinstance(body.exc, ast.Call):
            return

        if isinstance(body.exc, ast.Name) and node.name:
            if body.exc.id != node.name:
                return

        self.add_violation(UselessExceptCaseViolation(node))

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
            UselessExceptCaseViolation

        """
        self._check_useless_except(node)
        self._check_exception_type(node)
        self.generic_visit(node)


@final
class NestedTryBlocksVisitor(BaseNodeVisitor):
    """Ensures that there are no nested ``try`` blocks."""

    def visit_Try(self, node: ast.Try) -> None:
        """
        Visits all try nodes in the tree.

        Raises:
            NestedTryViolation

        """
        self._check_nested_try(node)
        self.generic_visit(node)

    def _check_nested_try(self, node: ast.Try) -> None:
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Try) and sub_node is not node:
                self.add_violation(NestedTryViolation(sub_node))
