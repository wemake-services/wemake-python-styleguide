# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics import functions
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

    def _check_wrong_function_called(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(
            node, constants.FUNCTIONS_BLACKLIST,
        )
        if function_name:
            self.add_violation(
                WrongFunctionCallViolation(node, text=function_name),
            )

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``FUNCTIONS_BLACKLIST`` calls.

        Raises:
            WrongFunctionCallViolation

        """
        self._check_wrong_function_called(node)
        self.generic_visit(node)
