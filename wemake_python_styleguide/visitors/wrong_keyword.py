# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors import (
    BareRiseViolation,
    RiseNotImplementedViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongRaiseVisitor(BaseNodeVisitor):
    """This class finds wrong `raise` keywords."""

    def visit_Raise(self, node: ast.Raise):
        """Checks how `raise` keyword is used."""
        exception = getattr(node, 'exc', None)
        if not exception:
            parent = getattr(node, 'parent')
            if not isinstance(parent, ast.ExceptHandler):
                self.add_error(BareRiseViolation(node))
        else:
            exception_func = getattr(exception, 'func', None)
            if exception_func:
                exception = exception_func

            exception_name = getattr(exception, 'id', None)
            if exception_name == 'NotImplemented':
                self.add_error(
                    RiseNotImplementedViolation(node, text=exception_name),
                )

        self.generic_visit(node)


class WrongKeywordVisitor(BaseNodeVisitor):
    """This class is responsible for finding wrong keywords."""

    def visit_Global(self, node: ast.Global):
        """Used to find `global` keyword."""
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        """Used to find `nonlocal` keyword."""
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete):
        """Used to find `del` keyword."""
        self.add_error(WrongKeywordViolation(node, text='del'))
        self.generic_visit(node)

    def visit_Pass(self, node: ast.Pass):
        """Used to find `pass` keyword."""
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)
