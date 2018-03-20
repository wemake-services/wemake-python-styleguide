# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors import WrongKeywordViolation
from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor


class _WrongKeywordVisitor(BaseNodeVisitor):
    def visit_Global(self, node: ast.Global):
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete):
        self.add_error(WrongKeywordViolation(node, text='del'))
        self.generic_visit(node)

    def visit_Pass(self, node: ast.Pass):
        self.add_error(WrongKeywordViolation(node))
        self.generic_visit(node)


class WrongKeywordChecker(BaseChecker):
    name = 'wms-wrong-keyword'

    def run(self):
        visiter = _WrongKeywordVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
