import ast
from typing import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import NESTED_FUNCTIONS_WHITELIST
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.logic.walk import get_closest_parent
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.best_practices import (
    NestedClassViolation,
    NestedFunctionViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class NestedComplexityVisitor(BaseNodeVisitor):
    """
    Checks that structures are not nested.

    We disallow to use nested functions and nested classes.
    Because flat is better than nested.

    We allow to nest function inside classes, that's called methods.
    """

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Used to find nested classes in other classes and functions.

        Uses ``NESTED_CLASSES_WHITELIST`` to respect some nested classes.
        """
        self._check_nested_classes(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Used to find nested functions.

        Uses ``NESTED_FUNCTIONS_WHITELIST`` to respect some nested functions.
        Only whitelisted functions are allowed, either directly inside
        a function or inside a single function-level ``if`` / ``if-else``.
        All other nesting is forbidden.
        """
        self._check_nested_function(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """Used to find nested ``lambda`` functions."""
        self._check_nested_lambdas(node)
        self.generic_visit(node)

    def _check_nested_function(self, node: AnyFunctionDef) -> None:
        context = get_context(node)
        if not isinstance(context, FunctionNodes):
            return

        parent = get_parent(node)

        is_direct = isinstance(parent, FunctionNodes)

        is_single_if = (
            isinstance(parent, ast.If) and get_parent(parent) is context
        )

        if node.name in NESTED_FUNCTIONS_WHITELIST and (
            is_direct or is_single_if
        ):
            return

        self.add_violation(
            NestedFunctionViolation(node, text=node.name),
        )

    def _check_nested_classes(self, node: ast.ClassDef) -> None:
        parent_context = get_context(node)

        is_inside_class = isinstance(parent_context, ast.ClassDef)
        is_whitelisted = node.name in self.options.nested_classes_whitelist

        is_bad = is_inside_class and not is_whitelisted

        is_inside_function = isinstance(parent_context, FunctionNodes)

        if is_bad or is_inside_function:
            self.add_violation(NestedClassViolation(node, text=node.name))

    def _check_nested_lambdas(self, node: ast.Lambda) -> None:
        is_direct = isinstance(get_context(node), ast.Lambda)
        is_deep = get_closest_parent(node, ast.Lambda)

        if is_direct or is_deep:
            self.add_violation(NestedFunctionViolation(node, text='lambda'))
