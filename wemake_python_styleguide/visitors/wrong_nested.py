# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import (
    NESTED_CLASSES_WHITELIST,
    NESTED_FUNCTIONS_WHITELIST,
)
from wemake_python_styleguide.errors import (
    NestedClassViolation,
    NestedFunctionViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongNestedVisitor(BaseNodeVisitor):
    """This class checks that structures are not nested."""

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
        """
        Used to find nested functions.

        Uses `NESTED_FUNCTIONS_WHITELIST` to respect some nested functions.
        """
        parent = getattr(node, 'parent', None)
        is_inside_function = isinstance(parent, ast.FunctionDef)

        if is_inside_function and node.name not in NESTED_FUNCTIONS_WHITELIST:
            self.add_error(NestedFunctionViolation(node, text=node.name))
        self.generic_visit(node)
