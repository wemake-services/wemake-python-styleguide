# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict

from wemake_python_styleguide.errors import (
    TooManyArgumentsViolation,
    TooManyExpressionsViolation,
    TooManyLocalsViolation,
    TooManyReturnsViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor

# TODO: implement TooDeepNestingViolation, TooManyBranchesViolation


class ComplexityVisitor(BaseNodeVisitor):
    """This class checks for code with high complexity."""

    def __init__(self) -> None:
        """Creates counters for tracked metrics."""
        super().__init__()

        self.expressions: DefaultDict[str, int] = defaultdict(int)
        self.variables: DefaultDict[str, int] = defaultdict(int)
        self.returns: DefaultDict[str, int] = defaultdict(int)

    def _check_arguments_count(self, node: ast.FunctionDef):
        counter = 0
        has_extra_self_or_cls = 0
        if getattr(node, 'function_type', None) in ['method', 'classmethod']:
            has_extra_self_or_cls = 1

        counter += len(node.args.args)
        counter += len(node.args.kwonlyargs)

        if node.args.vararg:
            counter += 1

        if node.args.kwarg:
            counter += 1

        if counter > 5 + has_extra_self_or_cls:  # TODO: config
            self.add_error(
                TooManyArgumentsViolation(node, text=node.name),
            )

    def _update_variables(self, function: ast.FunctionDef):
        self.variables[function.name] += 1
        if self.variables[function.name] == 9 + 1:  # TODO: config
            self.add_error(
                TooManyLocalsViolation(function, text=function.name),
            )

    def _update_returns(self, function: ast.FunctionDef):
        self.returns[function.name] += 1
        if self.returns[function.name] == 5 + 1:  # TODO: config
            self.add_error(
                TooManyReturnsViolation(function, text=function.name),
            )

    def _update_expression(self, function: ast.FunctionDef):
        self.expressions[function.name] += 1
        if self.expressions[function.name] == 10:  # TODO: config
            self.add_error(
                TooManyExpressionsViolation(function, text=function.name),
            )

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Checks function internal complexity."""
        self._check_arguments_count(node)

        for body_item in node.body:
            for sub_node in ast.walk(body_item):  # TODO: iter_child
                is_variable = isinstance(sub_node, ast.Name)
                context = getattr(sub_node, 'ctx', None)

                if is_variable and isinstance(context, ast.Store):
                    self._update_variables(node)

                if isinstance(sub_node, ast.Return):
                    self._update_returns(node)

                if isinstance(sub_node, ast.Expr):
                    self._update_expression(node)

        self.generic_visit(node)


# class _BranchesVisitor(BaseNodeVisitor):
#     branches = frozenset((
#         ast.For,
#         ast.If,
#         ast.While,
#         ast.
#     ))

#     def visit_FunctionDef(self, node: ast.FunctionDef):
#         for body_item in node.body:
#             for sub_node in ast.walk(body_item):
