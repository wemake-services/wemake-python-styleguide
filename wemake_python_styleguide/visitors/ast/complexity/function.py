# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict, List

from wemake_python_styleguide.errors.complexity import (
    TooManyArgumentsViolation,
    TooManyElifsViolation,
    TooManyExpressionsViolation,
    TooManyLocalsViolation,
    TooManyReturnsViolation,
)
from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.visitors.base import BaseNodeVisitor

FunctionCounter = DefaultDict[ast.FunctionDef, int]


class _ComplexityCounter(object):
    """Helper class to encapsulate logic from the visitor."""

    def __init__(self) -> None:
        self.arguments: FunctionCounter = defaultdict(int)
        self.elifs: FunctionCounter = defaultdict(int)
        self.returns: FunctionCounter = defaultdict(int)
        self.expressions: FunctionCounter = defaultdict(int)
        self.variables: DefaultDict[
            ast.FunctionDef, List[str],
        ] = defaultdict(list)

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
        function_variables = self.variables[function]
        if variable_name not in function_variables and variable_name != '_':
            function_variables.append(variable_name)

    def _update_elifs(self, node: ast.FunctionDef, sub_node: ast.If) -> None:
        has_elif = any(
            isinstance(if_node, ast.If) for if_node in sub_node.orelse
        )

        if has_elif:
            self.elifs[node] += 1

    def _check_sub_node(self, node: ast.FunctionDef, sub_node) -> None:
        is_variable = isinstance(sub_node, ast.Name)
        context = getattr(sub_node, 'ctx', None)

        if is_variable and isinstance(context, ast.Store):
            self._update_variables(node, sub_node.id)
        elif isinstance(sub_node, ast.Return):
            self.returns[node] += 1
        elif isinstance(sub_node, ast.Expr):
            self.expressions[node] += 1
        elif isinstance(sub_node, ast.If):
            self._update_elifs(node, sub_node)

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

        self.arguments[node] = counter - has_extra_arg

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
        self._counter = _ComplexityCounter()

    def _check_possible_switch(self) -> None:
        for node, elifs in self._counter.elifs.items():
            if elifs > self.options.max_elifs:
                self.add_error(TooManyElifsViolation(node))

    def _check_function_internals(self) -> None:
        for node, variables in self._counter.variables.items():
            if len(variables) > self.options.max_local_variables:
                self.add_error(
                    TooManyLocalsViolation(node, text=node.name),
                )

        for node, expressions in self._counter.expressions.items():
            if expressions > self.options.max_expressions:
                self.add_error(
                    TooManyExpressionsViolation(node, text=node.name),
                )

    def _check_function_signature(self) -> None:
        for node, arguments in self._counter.arguments.items():
            if arguments > self.options.max_arguments:
                self.add_error(
                    TooManyArgumentsViolation(node, text=str(arguments)),
                )

        for node, returns in self._counter.returns.items():
            if returns > self.options.max_returns:
                self.add_error(TooManyReturnsViolation(node, text=node.name))

    def _post_visit(self) -> None:
        self._check_function_signature()
        self._check_function_internals()
        self._check_possible_switch()

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
