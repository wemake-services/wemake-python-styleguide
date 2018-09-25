# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors.general import (
    MultipleIfsInComprehensionViolation,
    RaiseNotImplementedViolation,
    WrongKeywordViolation,
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
            self.add_error(RaiseNotImplementedViolation(node))

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

    def visit_Global(self, node: ast.Global) -> None:
        """
        Used to find ``global`` keyword.

        Raises:
            WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        """
        Used to find ``nonlocal`` keyword.

        Raises:
            WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete) -> None:
        """
        Used to find ``del`` keyword.

        Raises:
            WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node, text='del'))
        self.generic_visit(node)

    def visit_Pass(self, node: ast.Pass) -> None:
        """
        Used to find ``pass`` keyword.

        Raises:
            WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)


class WrongListComprehensionVisitor(BaseNodeVisitor):
    """Checks list comprehensions."""

    def _check_ifs(self, node: ast.comprehension) -> None:
        if len(node.ifs) > 1:
            self.add_error(MultipleIfsInComprehensionViolation(node))

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation,

        """
        self._check_ifs(node)
        self.generic_visit(node)
