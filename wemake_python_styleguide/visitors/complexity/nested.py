# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import (
    NESTED_CLASSES_WHITELIST,
    NESTED_FUNCTIONS_WHITELIST,
)
from wemake_python_styleguide.errors.complexity import (
    NestedClassViolation,
    NestedFunctionViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class NestedComplexityVisitor(BaseNodeVisitor):
    """
    This class checks that structures are not nested.

    We disallow to use nested functions and nested classes.
    Because flat is better than nested.

    We allow to nest function inside classes, that's called methods.
    """

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Used to find nested classes in other classes and functions.

        Uses ``NESTED_CLASSES_WHITELIST`` to respect some nested classes.
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

        Uses ``NESTED_FUNCTIONS_WHITELIST`` to respect some nested functions.
        Respected usecases for nested functions:
        1. decorator
        2. factory function
        """
        parent = getattr(node, 'parent', None)
        is_inside_function = isinstance(parent, ast.FunctionDef)

        if is_inside_function and node.name not in NESTED_FUNCTIONS_WHITELIST:
            self.add_error(NestedFunctionViolation(node, text=node.name))
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda):
        """Used to find nested ``lambda``s."""
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.Lambda):
            self.add_error(NestedFunctionViolation(node))
        self.generic_visit(node)
