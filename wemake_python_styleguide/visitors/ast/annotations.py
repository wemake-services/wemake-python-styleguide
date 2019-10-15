# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, FrozenSet

from typing_extensions import final

from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.annotations import (
    LiteralNoneViolation,
    NestedAnnotationsViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultilineFunctionAnnotationViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongNestedAnnotationVisitor(BaseNodeVisitor):
    """Ensures that nested annotations are used correctly."""

    _flat_types: ClassVar[FrozenSet[str]] = frozenset((
        'Literal', 'Union', 'Annotated',
    ))

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks return type annotations.

        Raises:
            NestedAnnotationsViolation

        """
        self._check_return_nested_annotation(node)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        """
        Checks arguments annotations.

        Raises:
            NestedAnnotationsViolation

        """
        self._check_arg_nested_annotation(node)
        self.generic_visit(node)

    def _same_subscript(self, parent_node: ast.Subscript, child_node) -> bool:
        parent_annotation = self._get_annotation(parent_node)
        child_annotation = self._get_annotation(child_node)
        return parent_annotation == child_annotation

    def _get_annotation(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        if isinstance(node, ast.Subscript):
            return self._get_annotation(node.value)
        return ''

    def _check_nested_annotation(self, node: ast.Subscript) -> None:
        an = self._get_annotation(node)
        if an not in self._flat_types or not isinstance(node.slice, ast.Index):
            return

        if self._same_subscript(node, node.slice.value):
            self.add_violation(NestedAnnotationsViolation(node))
        elif isinstance(node.slice.value, ast.Tuple):
            for arg in node.slice.value.elts:
                if self._same_subscript(node, arg):
                    self.add_violation(NestedAnnotationsViolation(node))
                    return

    def _check_arg_nested_annotation(self, node: ast.arg) -> None:
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Subscript):
                self._check_nested_annotation(sub_node)

    def _check_return_nested_annotation(self, node: AnyFunctionDef) -> None:
        if not node.returns:
            return

        for sub_node in ast.walk(node.returns):
            if isinstance(sub_node, ast.Subscript):
                self._check_nested_annotation(sub_node)


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongAnnotationVisitor(BaseNodeVisitor):
    """Ensures that annotations are used correctly."""

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks return type annotations.

        Raises:
            MultilineFunctionAnnotationViolation
            LiteralNoneAnnotation

        """
        self._check_return_annotation(node)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        """
        Checks arguments annotations.

        Raises:
            MultilineFunctionAnnotationViolation
            LiteralNoneAnnotation

        """
        self._check_arg_annotation(node)
        self.generic_visit(node)

    def _check_for_literal_none(self, node: ast.Subscript) -> None:
        if not isinstance(node.value, ast.Name):
            return

        if not isinstance(node.slice, ast.Index):
            return

        if node.value.id != 'Literal':
            return

        if not isinstance(node.slice.value, ast.NameConstant):
            return

        if node.slice.value.value is None:
            self.add_violation(LiteralNoneViolation(node))

    def _check_arg_annotation(self, node: ast.arg) -> None:
        for sub_node in ast.walk(node):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

            if isinstance(sub_node, ast.Subscript):
                self._check_for_literal_none(sub_node)

    def _check_return_annotation(self, node: AnyFunctionDef) -> None:
        if not node.returns:
            return

        for sub_node in ast.walk(node.returns):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.returns.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

            if isinstance(sub_node, ast.Subscript):
                self._check_for_literal_none(sub_node)
