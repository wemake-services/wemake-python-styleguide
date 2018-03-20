# -*- coding: utf-8 -*-

import ast
from typing import Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.errors import (
    TooShortArgumentNameViolation,
    TooShortAttributeNameViolation,
    TooShortVariableNameViolation,
    WrongArgumentNameViolation,
    WrongAttributeNameViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.helpers.variables import (
    is_too_short_variable_name,
    is_wrong_variable_name,
)

BAD_VARIABLE_NAMES = frozenset((
    'data',
    'result',
    'results',
    'item',
    'items',
    'value',
    'values',
    'val',
    'vals',
    'var',
    'vars',
    'content',
    'contents',
))


class _WrongVariableVisitor(BaseNodeVisitor):
    def _check_argument(self, node: ast.FunctionDef, arg: str) -> None:
        if is_wrong_variable_name(arg, BAD_VARIABLE_NAMES):
            self.add_error(WrongArgumentNameViolation(node, text=arg))

        if is_too_short_variable_name(arg):
            self.add_error(TooShortArgumentNameViolation(node, text=arg))

    def visit_Attribute(self, node: ast.Attribute):
        """Used to find wrong attribute names inside classes."""
        context = getattr(node, 'ctx', None)

        if isinstance(context, ast.Store):
            if is_wrong_variable_name(node.attr, BAD_VARIABLE_NAMES):
                self.add_error(
                    WrongAttributeNameViolation(node, text=node.attr),
                )

            if is_too_short_variable_name(node.attr):
                self.add_error(
                    TooShortAttributeNameViolation(node, text=node.attr),
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Used to find wrong function and method parameters."""
        for arg in node.args.args:
            self._check_argument(node, arg.arg)

        for arg in node.args.kwonlyargs:
            self._check_argument(node, arg.arg)

        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        """Used to find wrong regular variables."""
        context = getattr(node, 'ctx', None)

        if isinstance(context, ast.Store):
            if is_wrong_variable_name(node.id, BAD_VARIABLE_NAMES):
                self.add_error(
                    WrongVariableNameViolation(node, text=node.id),
                )

            if is_too_short_variable_name(node.id):
                self.add_error(
                    TooShortVariableNameViolation(node, text=node.id),
                )

        self.generic_visit(node)


class WrongVariableChecker(BaseChecker):
    """
    This class performs checks based on variable names.

    It is responsible for finding short and blacklisted variables.
    """

    name = 'wms-wrong-variable'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _WrongVariableVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
