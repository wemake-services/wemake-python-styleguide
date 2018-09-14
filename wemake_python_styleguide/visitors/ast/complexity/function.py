# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict, List, Type

from wemake_python_styleguide.errors.base import BaseStyleViolation
from wemake_python_styleguide.errors.complexity import (
    TooManyArgumentsViolation,
    TooManyElifsViolation,
    TooManyExpressionsViolation,
    TooManyLocalsViolation,
    TooManyReturnsViolation,
)
from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.logics.limits import has_just_exceeded_limit
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class _ComplexityCounter(object):
    """Helper class to encapsulate logic from the visitor."""

    def __init__(self, delegate: 'FunctionComplexityVisitor') -> None:
        self.delegate = delegate

        self.expressions: DefaultDict[str, int] = defaultdict(int)
        self.variables: DefaultDict[str, List[str]] = defaultdict(list)
        self.returns: DefaultDict[str, int] = defaultdict(int)

    def _update_variables(
        self,
        function: ast.FunctionDef,
        variable_name: str,
    ) -> None:
        """
        Increases the counter of local variables.

        What is treated as a local variable?
        Check ``TooManyLocalsViolation`` documentation.
        """
        function_variables = self.variables[function.name]
        if variable_name not in function_variables and variable_name != '_':
            function_variables.append(variable_name)

            limit_exceeded = has_just_exceeded_limit(
                len(function_variables),
                self.delegate.options.max_local_variables,
            )
            if limit_exceeded:
                self.delegate.add_error(
                    TooManyLocalsViolation(function, text=function.name),
                )

    def _update_counter(
        self,
        function: ast.FunctionDef,
        counter: DefaultDict[str, int],
        max_value: int,
        exception: Type[BaseStyleViolation],
    ) -> None:
        counter[function.name] += 1
        limit_exceeded = has_just_exceeded_limit(
            counter[function.name], max_value,
        )
        if limit_exceeded:
            self.delegate.add_error(exception(function, text=function.name))

    def _update_elifs(self, node: ast.If, count: int = 0) -> None:
        if node.orelse and isinstance(node.orelse[0], ast.If):
            self._update_elifs(node.orelse[0], count=count + 1)
        else:
            if count > self.delegate.options.max_elifs:
                self.delegate.add_error(TooManyElifsViolation(node))

    def _check_sub_node(self, node: ast.FunctionDef, sub_node) -> None:
        is_variable = isinstance(sub_node, ast.Name)
        context = getattr(sub_node, 'ctx', None)

        if is_variable and isinstance(context, ast.Store):
            self._update_variables(node, getattr(sub_node, 'id'))
        if isinstance(sub_node, ast.Return):
            self._update_counter(
                node,
                self.returns,
                self.delegate.options.max_returns,
                TooManyReturnsViolation,
            )
        if isinstance(sub_node, ast.Expr):
            self._update_counter(
                node,
                self.expressions,
                self.delegate.options.max_expressions,
                TooManyExpressionsViolation,
            )
        if isinstance(sub_node, ast.If):
            self._update_elifs(sub_node)

    def check_arguments_count(self, node: ast.FunctionDef) -> None:
        """Checks the number of the arguments in a function."""
        counter = 0
        has_extra_arg = 0
        if is_method(getattr(node, 'function_type', None)):
            has_extra_arg = 1

        counter += len(node.args.args) + len(node.args.kwonlyargs)

        if node.args.vararg:
            counter += 1

        if node.args.kwarg:
            counter += 1

        if counter > self.delegate.options.max_arguments + has_extra_arg:
            self.delegate.add_error(
                TooManyArgumentsViolation(node, text=node.name),
            )

    def check_function_complexity(self, node: ast.FunctionDef) -> None:
        """
        In this function we iterate all the internal body's node.

        We check different complexity metrics based on these internals.
        """
        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                self._check_sub_node(node, sub_node)


class FunctionComplexityVisitor(BaseNodeVisitor):
    """
    This class checks for complexity inside functions.

    This includes:

    1. Number of arguments
    2. Number of `return` statements
    3. Number of expressions
    4. Number of local variables
    5. Number of `elif` branches

    """

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._counter = _ComplexityCounter(self)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Checks function's internal complexity.

        Raises:
            TooManyExpressionsViolation
            TooManyReturnsViolation
            TooManyLocalsViolation
            TooManyArgumentsViolation
            TooManyElifsViolation

        """
        self._counter.check_arguments_count(node)
        self._counter.check_function_complexity(node)
        self.generic_visit(node)
