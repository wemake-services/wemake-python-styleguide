# -*- coding: utf-8 -*-

import ast
from itertools import zip_longest
from typing import ClassVar, Dict, List, Optional, Union

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import (
    FUNCTIONS_BLACKLIST,
    UNUSED_VARIABLE,
)
from wemake_python_styleguide.logic import functions, nodes, operators
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
    ComplexDefaultValueViolation,
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.violations.naming import (
    UnusedVariableIsUsedViolation,
)
from wemake_python_styleguide.violations.oop import WrongSuperCallViolation
from wemake_python_styleguide.violations.refactoring import (
    UselessLambdaViolation,
    WrongIsinstanceWithTupleViolation,
)
from wemake_python_styleguide.visitors import base, decorators

LocalVariable = Union[ast.Name, ast.ExceptHandler]


@final
class WrongFunctionCallVisitor(base.BaseNodeVisitor):
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
        parent_context = nodes.get_context(node)
        if isinstance(parent_context, FunctionNodes):
            grand_context = nodes.get_context(parent_context)
            if isinstance(grand_context, ast.ClassDef):
                return
        self.add_violation(
            WrongSuperCallViolation(node, text='not inside method'),
        )

    def _ensure_super_arguments(self, node: ast.Call) -> None:
        if node.args or node.keywords:
            self.add_violation(
                WrongSuperCallViolation(node, text='remove arguments'),
            )

    def _check_super_call(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'super'})
        if function_name:
            self._ensure_super_context(node)
            self._ensure_super_arguments(node)

    def _check_isinstance_call(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'isinstance'})
        if not function_name or len(node.args) != 2:
            return

        if isinstance(node.args[1], ast.Tuple):
            if len(node.args[1].elts) == 1:
                self.add_violation(WrongIsinstanceWithTupleViolation(node))

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``FUNCTIONS_BLACKLIST`` calls.

        Raises:
            BooleanPositionalArgumentViolation
            WrongFunctionCallViolation
            WrongSuperCallViolation
            WrongIsinstanceWithTupleViolation

        """
        self._check_wrong_function_called(node)
        self._check_boolean_arguments(node)
        self._check_super_call(node)
        self._check_isinstance_call(node)
        self.generic_visit(node)


@final
@decorators.alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class FunctionDefinitionVisitor(base.BaseNodeVisitor):
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
                self.add_violation(ComplexDefaultValueViolation(node))

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks regular, lambda, and async functions.

        Raises:
            UnusedVariableIsUsedViolation
            ComplexDefaultValueViolation

        """
        self._check_argument_default_values(node)
        self._check_unused_variables(node)
        self.generic_visit(node)


@final
class UselessLambdaDefinitionVisitor(base.BaseNodeVisitor):
    """This visitor is used specifically for ``lambda`` functions."""

    def _have_same_kwarg(self, node: ast.Lambda, call: ast.Call) -> bool:
        kwarg_name: Optional[str] = None
        for keyword in call.keywords:
            # `a=1` vs `**kwargs`:
            # {'arg': 'a', 'value': <_ast.Num object at 0x1027882b0>}
            # {'arg': None, 'value': <_ast.Name object at 0x102788320>}
            if keyword.arg is None:
                if isinstance(keyword.value, ast.Name):
                    kwarg_name = keyword.value.id
                else:  # We can judge on things like `**{}`
                    return False
        if node.args.kwarg and kwarg_name:
            return node.args.kwarg.arg == kwarg_name
        return node.args.kwarg == kwarg_name

    def _have_same_vararg(self, node: ast.Lambda, call: ast.Call) -> bool:
        vararg_name: Optional[str] = None
        for ar in call.args:
            # 'args': [<_ast.Starred object at 0x10d77a3c8>]
            if isinstance(ar, ast.Starred):
                if isinstance(ar.value, ast.Name):
                    vararg_name = ar.value.id
                else:  # We can judge on things like `*[]`
                    return False
        if vararg_name and node.args.vararg:
            return node.args.vararg.arg == vararg_name
        return node.args.vararg == vararg_name

    def _have_same_args(self, node: ast.Lambda, call: ast.Call) -> bool:
        paired_arguments = zip_longest(call.args, node.args.args)
        for call_arg, lambda_arg in paired_arguments:
            if isinstance(call_arg, ast.Starred):
                if isinstance(lambda_arg, ast.arg):
                    return False
            elif isinstance(call_arg, ast.Name):
                if not lambda_arg or call_arg.id != lambda_arg.arg:
                    return False
            else:
                return False
        return True

    def _have_same_kw_args(self, node: ast.Lambda, call: ast.Call) -> bool:
        prepared_kw_args = {
            kw.arg: kw
            for kw in call.keywords
            if isinstance(kw.value, ast.Name) and kw.arg == kw.value.id
        }

        real_kw_args = [
            # We need to remove ** args from here:
            kw for kw in call.keywords
            if not (isinstance(kw.value, ast.Name) and kw.arg is None)
        ]

        for lambda_arg in node.args.kwonlyargs:
            lambda_arg_name = getattr(lambda_arg, 'arg', None)
            call_arg = prepared_kw_args.get(lambda_arg_name)

            if lambda_arg and not call_arg:
                return False
        return len(real_kw_args) == len(node.args.kwonlyargs)

    def _check_useless_lambda(self, node: ast.Lambda) -> None:
        if not isinstance(node.body, ast.Call):
            return
        if not isinstance(node.body.func, ast.Name):
            # We do not track method (attr) calls, since it might me complex.
            return

        if node.args.defaults or list(filter(None, node.args.kw_defaults)):
            # It means that `lambda` has defaults in args,
            # we cannot be sure that these defaults are the same
            # as in the call def, ignoring it.
            # `kw_defaults` can have [None, ...] items.
            return

        same_vararg = self._have_same_vararg(node, node.body)
        same_kwarg = self._have_same_kwarg(node, node.body)
        if not same_vararg or not same_kwarg:
            return

        same_args = self._have_same_args(node, node.body)
        same_kw_args = self._have_same_kw_args(node, node.body)
        if not same_args or not same_kw_args:
            return

        self.add_violation(UselessLambdaViolation(node))

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """
        Checks if ``lambda`` functions are defined correctly.

        Raises:
            UselessLambdaViolation

        """
        self._check_useless_lambda(node)
        self.generic_visit(node)
