# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics import functions
from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
    IncorrectSuperCallViolation,
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

    def _check_boolean_arguments(self, node: ast.Call) -> None:
        for arg in node.args:
            if isinstance(arg, ast.NameConstant):
                # We do not check for `None` values here:
                if arg.value is True or arg.value is False:
                    self.add_violation(
                        BooleanPositionalArgumentViolation(
                            arg, text=str(arg.value),
                        ),
                    )

    def _ensure_super_context(self, node: ast.Call) -> None:
        parent_context = getattr(node, 'wps_context', None)
        if isinstance(parent_context, (ast.FunctionDef, ast.AsyncFunctionDef)):
            grand_context = getattr(parent_context, 'wps_context', None)
            if isinstance(grand_context, ast.ClassDef):
                return
        self.add_violation(
            IncorrectSuperCallViolation(node, text='not inside method'),
        )

    def _ensure_super_arguments(self, node: ast.Call) -> None:
        if len(node.args) > 0 or len(node.keywords) > 0:
            self.add_violation(
                IncorrectSuperCallViolation(node, text='remove arguments'),
            )

    def _check_super_call(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, ['super'])
        if function_name:
            self._ensure_super_context(node)
            self._ensure_super_arguments(node)

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``FUNCTIONS_BLACKLIST`` calls.

        Raises:
            BooleanPositionalArgumentViolation
            WrongFunctionCallViolation
            IncorrectSuperCallViolation

        """
        self._check_wrong_function_called(node)
        self._check_boolean_arguments(node)
        self._check_super_call(node)
        self.generic_visit(node)
