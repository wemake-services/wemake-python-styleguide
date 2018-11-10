# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, List

from wemake_python_styleguide.constants import UNUSED_VARIABLE
from wemake_python_styleguide.logics import functions
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
    AnyNodes,
    final,
)
from wemake_python_styleguide.violations.complexity import (
    TooManyArgumentsViolation,
    TooManyExpressionsViolation,
    TooManyLocalsViolation,
    TooManyReturnsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

FunctionCounter = DefaultDict[AnyFunctionDef, int]
FunctionCounterWithLambda = DefaultDict[AnyFunctionDefAndLambda, int]


@final
class _ComplexityCounter(object):
    """Helper class to encapsulate logic from the visitor."""

    _not_contain_locals: ClassVar[AnyNodes] = (
        ast.comprehension,
    )

    def __init__(self) -> None:
        self.arguments: FunctionCounterWithLambda = defaultdict(int)
        self.returns: FunctionCounter = defaultdict(int)
        self.expressions: FunctionCounter = defaultdict(int)
        self.variables: DefaultDict[
            AnyFunctionDef, List[str],
        ] = defaultdict(list)

    def _update_variables(
        self,
        function: AnyFunctionDef,
        variable_def: ast.Name,
    ) -> None:
        """
        Increases the counter of local variables.

        What is treated as a local variable?
        Check ``TooManyLocalsViolation`` documentation.
        """
        function_variables = self.variables[function]
        if variable_def.id not in function_variables:
            if variable_def.id == UNUSED_VARIABLE:
                return

            parent = getattr(variable_def, 'parent', None)
            if isinstance(parent, self._not_contain_locals):
                return

            function_variables.append(variable_def.id)

    def _check_sub_node(self, node: AnyFunctionDef, sub_node) -> None:
        is_variable = isinstance(sub_node, ast.Name)
        context = getattr(sub_node, 'ctx', None)

        if is_variable and isinstance(context, ast.Store):
            self._update_variables(node, sub_node)
        elif isinstance(sub_node, ast.Return):
            self.returns[node] += 1
        elif isinstance(sub_node, ast.Expr):
            self.expressions[node] += 1

    def check_arguments_count(self, node: AnyFunctionDefAndLambda) -> None:
        """Checks the number of the arguments in a function."""
        has_extra_arg = 0
        if functions.is_method(getattr(node, 'function_type', None)):
            has_extra_arg = 1

        arguments = functions.get_all_arguments(node)
        self.arguments[node] = len(arguments) - has_extra_arg

    def check_function_complexity(self, node: AnyFunctionDef) -> None:
        """
        In this function we iterate all the internal body's node.

        We check different complexity metrics based on these internals.
        """
        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                self._check_sub_node(node, sub_node)


@final
@alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class FunctionComplexityVisitor(BaseNodeVisitor):
    """
    This class checks for complexity inside functions.

    This includes:

    1. Number of arguments
    2. Number of `return` statements
    3. Number of expressions
    4. Number of local variables

    """

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._counter = _ComplexityCounter()

    def _check_function_internals(self) -> None:
        for node, variables in self._counter.variables.items():
            if len(variables) > self.options.max_local_variables:
                self.add_violation(
                    TooManyLocalsViolation(node, text=str(len(variables))),
                )

        for node, expressions in self._counter.expressions.items():
            if expressions > self.options.max_expressions:
                self.add_violation(
                    TooManyExpressionsViolation(node, text=str(expressions)),
                )

    def _check_function_signature(self) -> None:
        for node, arguments in self._counter.arguments.items():
            if arguments > self.options.max_arguments:
                self.add_violation(
                    TooManyArgumentsViolation(node, text=str(arguments)),
                )

        for node, returns in self._counter.returns.items():
            if returns > self.options.max_returns:
                self.add_violation(
                    TooManyReturnsViolation(node, text=str(returns)),
                )

    def _post_visit(self) -> None:
        self._check_function_signature()
        self._check_function_internals()

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks function's internal complexity.

        Raises:
            TooManyExpressionsViolation
            TooManyReturnsViolation
            TooManyLocalsViolation
            TooManyArgumentsViolation

        """
        self._counter.check_arguments_count(node)
        self._counter.check_function_complexity(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """
        Checks lambda function's internal complexity.

        Raises:
            TooManyArgumentsViolation

        """
        self._counter.check_arguments_count(node)
        self.generic_visit(node)
