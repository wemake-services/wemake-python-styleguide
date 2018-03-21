# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict, Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.errors import (
    TooManyArgumentsViolation,
    TooManyLocalsViolation,
    TooManyReturnsViolation,
)

# TODO: implement TooDeepNestingViolation, TooManyStatementsViolation,
# and TooManyBranchesViolation


class _LocalsVisitor(BaseNodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.variables: DefaultDict[str, int] = defaultdict(int)
        self.returns: DefaultDict[str, int] = defaultdict(int)

    def _check_arguments_count(self, node: ast.FunctionDef):
        counter = 0  # TODO: check for `self` and `cls`
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

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_arguments_count(node)

        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                is_variable = isinstance(sub_node, ast.Name)
                context = getattr(sub_node, 'ctx', None)
                if is_variable and isinstance(context, ast.Store):
                    self._update_variables(node)

                if isinstance(sub_node, ast.Return):
                    self._update_returns(node)

        self.generic_visit(node)


class HighComplexityChecker(BaseChecker):
    """This class is responsible for checking for code with high complexity."""

    name = 'wms-high-comlexity'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _LocalsVisitor()
        visiter.visit(self.tree)

        # for node in ast.walk(self.tree):
        #     if isinstance(node, ast.arguments):
        #         print(node, vars(node))

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
