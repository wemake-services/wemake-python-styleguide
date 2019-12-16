# -*- coding: utf-8 -*-

import ast
from contextlib import suppress
from typing import ClassVar, Dict, List, Optional, Union

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import (
    FUNCTIONS_BLACKLIST,
    LITERALS_BLACKLIST,
)
from wemake_python_styleguide.logic import (
    exceptions,
    functions,
    nodes,
    operators,
    prop_access,
    walk,
)
from wemake_python_styleguide.logic.arguments import function_args
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes
from wemake_python_styleguide.violations import consistency, naming
from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
    ComplexDefaultValueViolation,
    StopIterationInsideGeneratorViolation,
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.violations.oop import (
    WrongSuperCallAccessViolation,
    WrongSuperCallViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    ImplicitEnumerateViolation,
    ImplicitPrimitiveViolation,
    OpenWithoutContextManagerViolation,
    TypeCompareViolation,
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

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``FUNCTIONS_BLACKLIST`` calls.

        Raises:
            BooleanPositionalArgumentViolation
            WrongFunctionCallViolation
            WrongIsinstanceWithTupleViolation
            WrongSuperCallAccessViolation
            WrongSuperCallViolation

        """
        self._check_wrong_function_called(node)
        self._check_boolean_arguments(node)
        self._check_super_call(node)
        self._check_isinstance_call(node)
        self.generic_visit(node)

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
        parent_node = nodes.get_parent(node)

        attr = getattr(parent_node, 'attr', None)
        parent_name = getattr(parent_context, 'name', None)

        if attr and parent_name and attr != parent_name:
            self.add_violation(
                WrongSuperCallAccessViolation(
                    node,
                    text='super call with incorrect method or property access',
                ),
            )

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


@final
class WrongFunctionCallContextVisitior(base.BaseNodeVisitor):
    """Ensure that we call several functions in the correct context."""

    def visit_Call(self, node: ast.Call) -> None:
        """
        Visits function calls to find wrong contexts.

        Raises:
            OpenWithoutContextManagerViolation
            TypeCompareViolation
            ImplicitEnumerateViolation

        """
        self._check_open_call_context(node)
        self._check_type_compare(node)
        self._check_range_len(node)
        self.generic_visit(node)

    def _check_open_call_context(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'open'})
        if not function_name:
            return

        if isinstance(nodes.get_parent(node), ast.withitem):
            # We do not care about `with` or `async with` - both are fine.
            return

        self.add_violation(OpenWithoutContextManagerViolation(node))

    def _check_type_compare(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'type'})
        if not function_name:
            return

        if isinstance(nodes.get_parent(node), ast.Compare):
            self.add_violation(TypeCompareViolation(node))

    def _check_range_len(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'range'})
        if not function_name:
            return

        is_one_argument_range = (
            len(node.args) == 1 and
            isinstance(node.args[0], ast.Call) and
            functions.given_function_called(node.args[0], {'len'})
        )
        is_two_arguments_range = (
            len(node.args) in {2, 3} and
            isinstance(node.args[1], ast.Call) and
            functions.given_function_called(node.args[1], {'len'})
        )
        if is_one_argument_range or is_two_arguments_range:
            self.add_violation(ImplicitEnumerateViolation(node))


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

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks regular, lambda, and async functions.

        Raises:
            UnusedVariableIsUsedViolation
            ComplexDefaultValueViolation
            StopIterationInsideGeneratorViolation

        """
        self._check_argument_default_values(node)
        self._check_unused_variables(node)
        self._check_generator(node)
        self.generic_visit(node)

    def _check_used_variables(
        self,
        local_variables: Dict[str, List[LocalVariable]],
    ) -> None:
        for varname, usages in local_variables.items():
            for node in usages:
                if access.is_protected(varname):
                    self.add_violation(
                        naming.UnusedVariableIsUsedViolation(
                            node,
                            text=varname,
                        ),
                    )

    def _maybe_update_variable(
        self,
        sub_node: LocalVariable,
        var_name: str,
        local_variables: Dict[str, List[LocalVariable]],
    ) -> None:
        defs = local_variables.get(var_name)
        if defs is not None:
            if access.is_unused(var_name):
                # We check unused variable usage in a different place:
                # see `visitors/ast/naming.py`
                return
            defs.append(sub_node)
            return

        is_name_def = (
            isinstance(sub_node, ast.Name) and
            isinstance(sub_node.ctx, ast.Store)
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
            parts = prop_access.parts(real_arg) if isinstance(
                real_arg, ast.Attribute,
            ) else [real_arg]

            for part in parts:
                if not isinstance(part, self._allowed_default_value_types):
                    self.add_violation(ComplexDefaultValueViolation(arg))
                    return

    def _check_generator(self, node: AnyFunctionDef) -> None:
        if not functions.is_generator(node):
            return

        for sub_node in walk.get_subnodes_by_type(node, ast.Raise):
            if exceptions.get_exception_name(sub_node) == 'StopIteration':
                self.add_violation(
                    StopIterationInsideGeneratorViolation(sub_node),
                )


@final
class UselessLambdaDefinitionVisitor(base.BaseNodeVisitor):
    """This visitor is used specifically for ``lambda`` functions."""

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """
        Checks if ``lambda`` functions are defined correctly.

        Raises:
            UselessLambdaViolation
            ImplicitPrimitiveViolation

        """
        self._check_useless_lambda(node)
        self._check_implicit_primitive(node)
        self.generic_visit(node)

    def _check_implicit_primitive(self, node: ast.Lambda) -> None:
        arguments = functions.get_all_arguments(node)
        if arguments:
            # We return from this check, since `lambda` has some arguments.
            return

        with suppress(ValueError):
            return_value = ast.literal_eval(node.body)
            if return_value is not None and not return_value:
                self.add_violation(ImplicitPrimitiveViolation(node))

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

        if not function_args.is_call_matched_by_arguments(node, node.body):
            return

        self.add_violation(UselessLambdaViolation(node))


@final
class UnnecessaryLiteralsVisitor(base.BaseNodeVisitor):
    """
    Responsible for restricting some literals.

    All these literals are defined in ``LITERALS_BLACKLIST``.
    """

    def visit_Call(self, node: ast.Call) -> None:
        """
        Used to find ``LITERALS_BLACKLIST`` without args calls.

        Raises:
            UnnecessaryLiteralsViolation

        """
        self._check_unnecessary_literals(node)
        self.generic_visit(node)

    def _check_unnecessary_literals(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(
            node, LITERALS_BLACKLIST,
        )
        if function_name and not node.args:
            self.add_violation(consistency.UnnecessaryLiteralsViolation(node))
