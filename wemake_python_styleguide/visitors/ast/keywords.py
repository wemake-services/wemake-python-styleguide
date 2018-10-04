# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.best_practices import (
    RaiseNotImplementedViolation,
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

    _forbidden_keywords = (
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
            self.add_violation(MultipleIfsInComprehensionViolation(node))

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation,

        """
        self._check_ifs(node)
        self.generic_visit(node)
