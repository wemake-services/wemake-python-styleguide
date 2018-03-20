# -*- coding: utf-8 -*-

import ast
from typing import Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.errors import WrongFunctionCallViolation
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
    'help',

    # Attribute access:
    'hasattr',
    'delattr',
))


class _WrongFunctionCallVisitor(BaseNodeVisitor):
    def visit_Call(self, node: ast.Call):
        """Used to find `BAD_FUNCTIONS` calls."""
        function_name = given_function_called(node, BAD_FUNCTIONS)
        if function_name:
            self.add_error(WrongFunctionCallViolation(
                node, text=function_name,
            ))
        self.generic_visit(node)


class WrongFunctionCallChecker(BaseChecker):
    """
    This class is responsible for restricting some dangerous function calls.

    All these functions are defined in `BAD_FUNCTIONS`.
    """

    name = 'wms-wrong-function-call'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _WrongFunctionCallVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
