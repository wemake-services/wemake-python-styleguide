# -*- coding: utf-8 -*-

import ast
from typing import ClassVar

from wemake_python_styleguide.constants import (
    NESTED_CLASSES_WHITELIST,
    NESTED_FUNCTIONS_WHITELIST,
)
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes, final
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

    _function_nodes: ClassVar[AnyNodes] = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
    )

    def _check_nested_function(self, node: AnyFunctionDef) -> None:
        parent = getattr(node, 'parent', None)
        is_inside_function = isinstance(parent, self._function_nodes)

        if is_inside_function and node.name not in NESTED_FUNCTIONS_WHITELIST:
            self.add_violation(NestedFunctionViolation(node, text=node.name))

    def _check_nested_classes(self, node: ast.ClassDef) -> None:
        parent = getattr(node, 'parent', None)
        is_inside_class = isinstance(parent, ast.ClassDef)
        is_inside_function = isinstance(parent, self._function_nodes)

        if is_inside_class and node.name not in NESTED_CLASSES_WHITELIST:
            self.add_violation(NestedClassViolation(node, text=node.name))
        elif is_inside_function:
            self.add_violation(NestedClassViolation(node, text=node.name))

    def _check_nested_lambdas(self, node: ast.Lambda) -> None:
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.Lambda):
            self.add_violation(NestedFunctionViolation(node))

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
