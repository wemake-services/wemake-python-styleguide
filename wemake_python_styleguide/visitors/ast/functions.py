# -*- coding: utf-8 -*-

import ast
from typing import Dict

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics import functions
from wemake_python_styleguide.logics.naming import access
from wemake_python_styleguide.types import AnyFunctionDefAndLambda, final
from wemake_python_styleguide.violations.best_practices import (
    UnusedArgumentIsUsedViolation,
    UnusedArgumentViolation,
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


def _filter_args(argument: ast.arg) -> bool:
    """Only keeps regular arguments for functions and methods."""
    if argument.arg in constants.SPECIAL_ARGUMENT_NAMES_WHITELIST:
        return False
    return True


@final
@alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
    'visit_Lambda',
))
class FunctionDefinitionVisitor(BaseNodeVisitor):
    """Responsible for checking function definitions and arguments."""

    def _maybe_raise_for_arguments(
        self,
        node: AnyFunctionDefAndLambda,
        used_arguments: Dict[str, bool],
    ) -> None:
        for name, is_used in used_arguments.items():
            is_marked_as_unused = access.is_protected(name)
            if not is_marked_as_unused and not is_used:
                self.add_violation(UnusedArgumentViolation(node, text=name))
            elif is_marked_as_unused and is_used:
                self.add_violation(
                    UnusedArgumentIsUsedViolation(node, text=name),
                )

    def _check_unused_arguments(self, node: AnyFunctionDefAndLambda) -> None:
        arguments = filter(_filter_args, functions.get_all_arguments(node))
        used_arguments = {arg.arg: False for arg in arguments}
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id in used_arguments:
                if not isinstance(child.ctx, ast.Store):
                    used_arguments[child.id] = True

        self._maybe_raise_for_arguments(node, used_arguments)

    def visit_any_function(self, node: AnyFunctionDefAndLambda) -> None:
        """
        Checks regular, lambda, and async functions.

        Raises:
            UnusedArgumentViolation

        """
        self._check_unused_arguments(node)
        self.generic_visit(node)


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
