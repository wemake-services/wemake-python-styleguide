# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import FUNCTIONS_BLACKLIST
from wemake_python_styleguide.logics.functions import given_function_called
from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.best_practices import (
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongFunctionCallVisitor(BaseNodeVisitor):
    """
    Responsible for restricting some dangerous function calls.

    All these functions are defined in ``FUNCTIONS_BLACKLIST``.
    """

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``FUNCTIONS_BLACKLIST`` calls.

        Raises:
            WrongFunctionCallViolation

        """
        function_name = given_function_called(node, FUNCTIONS_BLACKLIST)
        if function_name:
            self.add_violation(WrongFunctionCallViolation(
                node, text=function_name,
            ))

        self.generic_visit(node)
