# -*- coding: utf-8 -*-

import ast
from typing import Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.errors import WrongKeywordViolation


class _WrongKeywordVisitor(BaseNodeVisitor):
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


class WrongKeywordChecker(BaseChecker):
    """This class is responsible for finding wrong keywords."""

    name = 'wms-wrong-keyword'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _WrongKeywordVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
