# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors.general import (
    BareRiseViolation,
    RaiseNotImplementedViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongRaiseVisitor(BaseNodeVisitor):
    """This class finds wrong `raise` keywords."""

    def _check_exception_type(self, node: ast.Raise, exception) -> None:
        exception_func = getattr(exception, 'func', None)
        if exception_func:
            exception = exception_func

        exception_name = getattr(exception, 'id', None)
        if exception_name == 'NotImplemented':
            self.add_error(
                RaiseNotImplementedViolation(node, text=exception_name),
            )

    def _check_bare_raise(self, node: ast.Raise) -> None:
        parent = getattr(node, 'parent', None)
        if not isinstance(parent, ast.ExceptHandler):
            self.add_error(BareRiseViolation(node))

    def visit_Raise(self, node: ast.Raise) -> None:
        """
        Checks how `raise` keyword is used.

        Raises:
            - RaiseNotImplementedViolation
            - BareRiseViolation

        """
        exception = getattr(node, 'exc', None)
        if not exception:
            self._check_bare_raise(node)
        else:
            self._check_exception_type(node, exception)

        self.generic_visit(node)


class WrongKeywordVisitor(BaseNodeVisitor):
    """This class is responsible for finding wrong keywords."""

    def visit_Global(self, node: ast.Global):
        """
        Used to find `global` keyword.

        Raises:
            - WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        """
        Used to find `nonlocal` keyword.

        Raises:
            - WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete):
        """
        Used to find `del` keyword.

        Raises:
            - WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node, text='del'))
        self.generic_visit(node)

    def visit_Pass(self, node: ast.Pass):
        """
        Used to find `pass` keyword.

        Raises:
            - WrongKeywordViolation

        """
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)
