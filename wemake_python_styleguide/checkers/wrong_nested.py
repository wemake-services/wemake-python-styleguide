# -*- coding: utf-8 -*-

import ast
from typing import Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.errors import (
    NestedClassViolation,
    NestedFunctionViolation,
)

NESTED_CLASSES_WHITELIST = frozenset((
    'Meta',
))


class _WrongNestedVisitor(BaseNodeVisitor):
    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Used to find nested classes in other classes and functions.

        Uses `NESTED_CLASSES_WHITELIST` to respect some nested classes.
        """
        parent = getattr(node, 'parent', None)
        is_inside_class = isinstance(parent, ast.ClassDef)
        is_inside_function = isinstance(parent, ast.FunctionDef)

        if is_inside_class and node.name not in NESTED_CLASSES_WHITELIST:
            self.add_error(NestedClassViolation(node, text=node.name))
        elif is_inside_function:
            self.add_error(NestedClassViolation(node, text=node.name))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Used to find nested functions."""
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.FunctionDef):
            self.add_error(NestedFunctionViolation(node, text=node.name))
        self.generic_visit(node)


class WrongNestedChecker(BaseChecker):
    """
    This class is responsible for finding nested structures.

    It finds nested functions, nested classes, and classes in functions.
    It all respects some whitelist classes such as `Meta.
    """

    name = 'wms-wrong-nested'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _WrongNestedVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
