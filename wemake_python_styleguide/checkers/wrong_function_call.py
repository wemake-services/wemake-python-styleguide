# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors import WrongFunctionCallViolation
from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.helpers.functions import given_function_called

BAD_FUNCTIONS = frozenset((
    # Code generation:
    'eval',
    'exec',
    'compile',

    # Magic:
    'globals',
    'locals',
    'vars',
    'dir',

    # IO:
    'input',
))


class _WrongFunctionCallVisitor(BaseNodeVisitor):
    def visit_Call(self, node: ast.Call):
        function_name = given_function_called(node, BAD_FUNCTIONS)
        if function_name:
            self.add_error(WrongFunctionCallViolation(
                node, text=function_name,
            ))
        self.generic_visit(node)


class WrongFunctionCallChecker(BaseChecker):
    name = 'wms-wrong-function-call'

    def run(self):
        visiter = _WrongFunctionCallVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
