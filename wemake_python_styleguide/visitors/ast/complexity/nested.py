# -*- coding: utf-8 -*-

import ast

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import (
    NESTED_CLASSES_WHITELIST,
    NESTED_FUNCTIONS_WHITELIST,
)
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.best_practices import (
    NestedClassViolation,
    NestedFunctionViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class NestedComplexityVisitor(BaseNodeVisitor):
    """
    Checks that structures are not nested.

    We disallow to use nested functions and nested classes.
    Because flat is better than nested.

    We allow to nest function inside classes, that's called methods.
    """

    def _check_nested_function(self, node: AnyFunctionDef) -> None:
        is_inside_function = isinstance(get_parent(node), FunctionNodes)

        if is_inside_function and node.name not in NESTED_FUNCTIONS_WHITELIST:
            self.add_violation(NestedFunctionViolation(node, text=node.name))

    def _check_nested_classes(self, node: ast.ClassDef) -> None:
        parent = get_parent(node)
        is_inside_class = isinstance(parent, ast.ClassDef)
        is_inside_function = isinstance(parent, FunctionNodes)

        if is_inside_class and node.name not in NESTED_CLASSES_WHITELIST:
            self.add_violation(NestedClassViolation(node, text=node.name))
        elif is_inside_function:
            self.add_violation(NestedClassViolation(node, text=node.name))

    def _check_nested_lambdas(self, node: ast.Lambda) -> None:
        if isinstance(get_parent(node), ast.Lambda):
            self.add_violation(NestedFunctionViolation(node, text='lambda'))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Used to find nested classes in other classes and functions.

        Uses ``NESTED_CLASSES_WHITELIST`` to respect some nested classes.

        Raises:
            NestedClassViolation

        """
        self._check_nested_classes(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Used to find nested functions.

        Uses ``NESTED_FUNCTIONS_WHITELIST`` to respect some nested functions.

        Raises:
            NestedFunctionViolation

        """
        self._check_nested_function(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """
        Used to find nested ``lambda`` functions.

        Raises:
            NestedFunctionViolation

        """
        self._check_nested_lambdas(node)
        self.generic_visit(node)
