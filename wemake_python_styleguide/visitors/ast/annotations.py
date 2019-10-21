# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, FrozenSet, Optional

from typing_extensions import final

from wemake_python_styleguide.logic import source
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.annotations import (
    LiteralNoneViolation,
    NestedAnnotationsViolation,
    UnionNestedInOptionalViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultilineFunctionAnnotationViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class _GenericAnnotationVisitor(BaseNodeVisitor):
    """Base class for all annotations visitors."""

    _possible_prefixes: ClassVar[FrozenSet[str]] = frozenset((
        'typing.',
        'typing_extensions.',
    ))

    @final
    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """
        Checks for assigned value annotation.

        Raises:
            LiteralNoneAnnotation

        """
        self._check_annotation(node.annotation)
        self.generic_visit(node)

    @final
    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks return type annotations.

        Raises:
            LiteralNoneAnnotation

        """
        self._check_annotation(node.returns)
        self.generic_visit(node)

    @final
    def visit_arg(self, node: ast.arg) -> None:
        """
        Checks arguments annotations.

        Raises:
            LiteralNoneAnnotation

        """
        self._check_annotation(node.annotation)
        self.generic_visit(node)

    @final
    def _get_annotation(self, node: ast.AST) -> str:
        """Smartly turns annotation node to string."""
        full_annotation = source.node_to_string(node)
        for prefix in self._possible_prefixes:
            full_annotation = full_annotation.replace(prefix, '')
        return full_annotation

    def _check_annotation(self, annotation: Optional[ast.expr]) -> None:
        """The only method that need to me implemented in child visitors."""


@final
class SemanticAnnotationVisitor(_GenericAnnotationVisitor):
    """Ensures that nested annotations are used correctly."""

    _flat_types: ClassVar[FrozenSet[str]] = frozenset((
        'Literal',
        'Union',
        'Annotated',
    ))

    def _check_annotation(self, annotation: Optional[ast.expr]) -> None:
        if not annotation:
            return

        self._check_nested_annotations(annotation)
        self._check_literal_none(annotation)
        self._check_union_nested_in_optional(annotation)

    def _check_nested_annotations(self, annotation: ast.expr) -> None:
        annotation_string = self._get_annotation(annotation)
        for flat_type in self._flat_types:
            if annotation_string.count(flat_type) > 1:
                self.add_violation(NestedAnnotationsViolation(annotation))

    def _check_literal_none(self, annotation: ast.expr) -> None:
        annotation_string = self._get_annotation(annotation)
        if 'Literal[None]' in annotation_string:
            self.add_violation(LiteralNoneViolation(annotation))

    def _check_union_nested_in_optional(self, annotation: ast.expr) -> None:
        annotation_string = self._get_annotation(annotation)
        if 'Optional[Union[' in annotation_string:
            self.add_violation(UnionNestedInOptionalViolation(annotation))


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

    def _check_arg_annotation(self, node: ast.arg) -> None:
        for sub_node in ast.walk(node):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

    def _check_return_annotation(self, node: AnyFunctionDef) -> None:
        if not node.returns:
            return

        for sub_node in ast.walk(node.returns):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.returns.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return
