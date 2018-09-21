# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import BAD_FUNCTIONS
from wemake_python_styleguide.errors.general import WrongFunctionCallViolation
from wemake_python_styleguide.logics.functions import given_function_called
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongFunctionCallVisitor(BaseNodeVisitor):
    """
    Responsible for restricting some dangerous function calls.

    All these functions are defined in ``BAD_FUNCTIONS``.
    """

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``BAD_FUNCTIONS`` calls.

        Raises:
            WrongFunctionCallViolation

        """
        function_name = given_function_called(node, BAD_FUNCTIONS)
        if function_name:
            self.add_error(WrongFunctionCallViolation(
                node, text=function_name,
            ))

        self.generic_visit(node)
