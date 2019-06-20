# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Dict, List, Optional, Union

from typing_extensions import final

from wemake_python_styleguide.constants import (
    FUNCTIONS_BLACKLIST,
    UNUSED_VARIABLE,
)
from wemake_python_styleguide.logics import functions, operators
from wemake_python_styleguide.logics.naming import access
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
    ComplexDefaultValuesViolation,
    IncorrectSuperCallViolation,
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.violations.naming import (
    UnusedVariableIsUsedViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

LocalVariable = Union[ast.Name, ast.ExceptHandler]


@final
class WrongFunctionCallVisitor(BaseNodeVisitor):
    """
    Responsible for restricting some dangerous function calls.

    All these functions are defined in ``FUNCTIONS_BLACKLIST``.
    """

    def _check_wrong_function_called(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(
            node, FUNCTIONS_BLACKLIST,
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


@final
@alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class FunctionDefinitionVisitor(BaseNodeVisitor):
    """Responsible for checking function internals."""

    _allowed_default_value_types: ClassVar[AnyNodes] = (
        ast.Name,
        ast.Attribute,
        ast.Str,
        ast.NameConstant,
        ast.Tuple,
        ast.Bytes,
        ast.Num,
        ast.Ellipsis,
    )

    def _check_used_variables(
        self,
        local_variables: Dict[str, List[LocalVariable]],
    ) -> None:
        for varname, usages in local_variables.items():
            for node in usages:
                if access.is_protected(varname) or varname == UNUSED_VARIABLE:
                    self.add_violation(
                        UnusedVariableIsUsedViolation(node, text=varname),
                    )

    def _maybe_update_variable(
        self,
        sub_node: LocalVariable,
        var_name: str,
        local_variables: Dict[str, List[LocalVariable]],
    ) -> None:
        if var_name in local_variables:
            if var_name == UNUSED_VARIABLE:
                if isinstance(getattr(sub_node, 'ctx', None), ast.Store):
                    return
            local_variables[var_name].append(sub_node)
            return

        is_name_def = isinstance(
            sub_node, ast.Name,
        ) and isinstance(
            sub_node.ctx, ast.Store,
        )

        if is_name_def or isinstance(sub_node, ast.ExceptHandler):
            local_variables[var_name] = []

    def _get_variable_name(self, node: LocalVariable) -> Optional[str]:
        if isinstance(node, ast.Name):
            return node.id
        return getattr(node, 'name', None)

    def _check_unused_variables(self, node: AnyFunctionDef) -> None:
        local_variables: Dict[str, List[LocalVariable]] = {}
        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                if not isinstance(sub_node, (ast.Name, ast.ExceptHandler)):
                    continue

                var_name = self._get_variable_name(sub_node)
                if not var_name:
                    continue

                self._maybe_update_variable(
                    sub_node, var_name, local_variables,
                )
        self._check_used_variables(local_variables)

    def _check_argument_default_values(self, node: AnyFunctionDef) -> None:
        for arg in node.args.defaults:
            real_arg = operators.unwrap_unary_node(arg)
            if not isinstance(real_arg, self._allowed_default_value_types):
                self.add_violation(ComplexDefaultValuesViolation(node))

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks regular, lambda, and async functions.

        Raises:
            UnusedVariableIsUsedViolation
            ComplexDefaultValuesViolation

        """
        self._check_argument_default_values(node)
        self._check_unused_variables(node)
        self.generic_visit(node)
