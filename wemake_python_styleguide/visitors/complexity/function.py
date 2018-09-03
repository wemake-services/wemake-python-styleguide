# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict, List

from wemake_python_styleguide.errors.complexity import (
    TooManyArgumentsViolation,
    TooManyExpressionsViolation,
    TooManyLocalsViolation,
    TooManyReturnsViolation,
)
from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.logics.limits import has_just_exceeded_limit
from wemake_python_styleguide.types import ConfigurationOptions
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class FunctionComplexityVisitor(BaseNodeVisitor):
    """
    This class checks for complexity inside functions.

    This includes:
    1. Number of arguments
    2. Number of `return`s
    3. Number of expressions
    4. Number of local variables
    """

    def __init__(self, options: ConfigurationOptions) -> None:
        """Creates config parser instance and counters for tracked metrics."""
        super().__init__(options)

        self.expressions: DefaultDict[str, int] = defaultdict(int)
        self.variables: DefaultDict[str, List[str]] = defaultdict(list)
        self.returns: DefaultDict[str, int] = defaultdict(int)

    def _check_arguments_count(self, node: ast.FunctionDef):
        counter = 0
        has_extra_self_or_cls = 0
        max_arguments_count = self.options.max_arguments
        if is_method(getattr(node, 'function_type', None)):
            has_extra_self_or_cls = 1

        counter += len(node.args.args)
        counter += len(node.args.kwonlyargs)

        if node.args.vararg:
            counter += 1

        if node.args.kwarg:
            counter += 1

        if counter > max_arguments_count + has_extra_self_or_cls:
            self.add_error(
                TooManyArgumentsViolation(node, text=node.name),
            )

    # TODO: move this logics inside into another place:
    def _update_variables(self, function: ast.FunctionDef, variable_name: str):
        """
        Increases the counter of local variables.

        What is treated as local variable?
        Check ``TooManyLocalsViolation`` documentation.
        """
        max_local_variables_count = self.options.max_local_variables
        function_variables = self.variables[function.name]
        if variable_name not in function_variables and variable_name != '_':
            function_variables.append(variable_name)

            limit_exceeded = has_just_exceeded_limit(
                len(function_variables),
                max_local_variables_count,
            )
            if limit_exceeded:
                self.add_error(
                    TooManyLocalsViolation(function, text=function.name),
                )

    # TODO: move this logics inside into another place:
    def _update_returns(self, function: ast.FunctionDef):
        max_returns_count = self.options.max_returns
        self.returns[function.name] += 1
        limit_exceeded = has_just_exceeded_limit(
            self.returns[function.name],
            max_returns_count,
        )
        if limit_exceeded:
            self.add_error(
                TooManyReturnsViolation(function, text=function.name),
            )

    # TODO: move this logics inside into another place:
    def _update_expression(self, function: ast.FunctionDef):
        max_expressions_count = self.options.max_expressions
        self.expressions[function.name] += 1
        limit_exceeded = has_just_exceeded_limit(
            self.expressions[function.name],
            max_expressions_count,
        )
        if limit_exceeded:
            self.add_error(
                TooManyExpressionsViolation(function, text=function.name),
            )

    def _check_function_complexity(self, node: ast.FunctionDef):
        """
        In this function we iterate all the internal body's node.

        We check different complexity metrics based on these internals.
        """
        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                is_variable = isinstance(sub_node, ast.Name)
                context = getattr(sub_node, 'ctx', None)

                if is_variable and isinstance(context, ast.Store):
                    self._update_variables(node, getattr(sub_node, 'id'))

                if isinstance(sub_node, ast.Return):
                    self._update_returns(node)

                if isinstance(sub_node, ast.Expr):
                    self._update_expression(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Checks function's internal complexity.

        Raises:
            - TooManyExpressionsViolation
            - TooManyReturnsViolation
            - TooManyLocalsViolation
            - TooManyArgumentsViolation

        """
        self._check_arguments_count(node)
        self._check_function_complexity(node)
        self.generic_visit(node)
