# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors import (
    WrongArgumentNameViolation,
    WrongAttributeNameViolation,
    WrongVariableNameViolation,
    TooShortArgumentNameViolation,
    TooShortAttributeNameViolation,
    TooShortVariableNameViolation,
)
from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.helpers.functions import given_function_called

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
    def visit_Attribute(self, node: ast.Attribute):
        context = getattr(node, 'ctx', None)

        if isinstance(context, ast.Store):
            if node.attr in BAD_VARIABLE_NAMES:
                self.add_error(
                    WrongAttributeNameViolation(node, text=node.attr),
                )

            if len(node.attr) < 2:  # TODO: configuration option
                self.add_error(
                    TooShortAttributeNameViolation(node, text=node.attr),
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for arg in node.args.args:
            if arg.arg in BAD_VARIABLE_NAMES:
                self.add_error(
                    WrongArgumentNameViolation(node, text=arg.arg),
                )

            if len(arg.arg) < 2:  # TODO: configuration option
                self.add_error(
                    TooShortArgumentNameViolation(node, text=arg.arg),
                )

        for arg in node.args.kwonlyargs:
            if arg.arg in BAD_VARIABLE_NAMES:
                self.add_error(
                    WrongArgumentNameViolation(node, text=arg.arg),
                )

            if len(arg.arg) < 2:  # TODO: configuration option
                self.add_error(
                    TooShortArgumentNameViolation(node, text=arg.arg),
                )

        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        context = getattr(node, 'ctx', None)

        if isinstance(context, ast.Store):
            if node.id in BAD_VARIABLE_NAMES:
                self.add_error(
                    WrongVariableNameViolation(node, text=node.id),
                )

            if len(node.id) < 2:  # TODO: configuration option
                self.add_error(
                    TooShortVariableNameViolation(node, text=node.id),
                )

        self.generic_visit(node)


class WrongVariableChecker(BaseChecker):
    name = 'wms-wrong-variable'

    def run(self):
        visiter = _WrongVariableVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
