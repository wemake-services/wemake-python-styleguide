# -*- coding: utf-8 -*-

import ast
from typing import Callable, ClassVar, FrozenSet, cast

from typing_extensions import final

from wemake_python_styleguide.types import AnyFunctionDef, ConfigurationOptions
from wemake_python_styleguide.violations import base
from wemake_python_styleguide.violations.annotations import (
    LiteralNoneViolation,
    NestedAnnotationsViolation,
    UnionNoneViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultilineFunctionAnnotationViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
class _AnnotationValidator(object):
    """Utility class to separate logic from the annotation visitor."""

    def __init__(
        self,
        error_callback: Callable[[base.BaseViolation], None],
        options: ConfigurationOptions,
    ) -> None:
        """Creates new instance of a annotation validator."""
        self._error_callback = error_callback
        self._options = options

    def check_for_literal_none(self, node: ast.Subscript) -> None:
        annotation_name = cast(ast.Name, node.value)
        slice_index = cast(ast.Index, node.slice)

        if annotation_name.id != 'Literal':
            return

        if self._check_slice_for_none(slice_index.value):
            self._error_callback(LiteralNoneViolation(node))

    def check_for_union_none(self, node: ast.Subscript) -> None:
        if node.value.id != 'Union':
            return

        slice_args = node.slice.value

        if not isinstance(slice_args, ast.Tuple):
            return

        if len(slice_args.elts) != 2:
            return

        for slice_arg in slice_args.elts:
            if self._check_slice_for_none(slice_arg):
                self._error_callback(UnionNoneViolation(node))
                return

    def _check_slice_for_none(self, slice_arg) -> bool:
        if isinstance(slice_arg, ast.NameConstant):
            return slice_arg.value is None
        return False


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
        node_annotation = self._get_annotation(node)

        if node_annotation not in self._flat_types:
            return

        slice_index = cast(ast.Index, node.slice)
        slice_args = slice_index.value

        if self._same_subscript(node, slice_args):
            self.add_violation(NestedAnnotationsViolation(node))
            return
        if isinstance(slice_args, ast.Tuple):
            for arg in slice_args.elts:
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
@alias('visit_variable', (
    'visit_AnnAssign',
))
class WrongAnnotationVisitor(BaseNodeVisitor):
    """Ensures that annotations are used correctly."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new annotation validator for this visitor."""
        super().__init__(*args, **kwargs)
        self._validator = _AnnotationValidator(self.add_violation, self.options)

    def visit_variable(self, node: ast.AnnAssign) -> None:
        """
        Checks wrong annotations of assigned.

        Raises:
            UnionNoneViolation

        """
        self._check_variable_annotation(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks return type annotations.

        Raises:
            MultilineFunctionAnnotationViolation
            LiteralNoneAnnotation
            UnionNoneViolation

        """
        self._check_return_annotation(node)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        """
        Checks arguments annotations.

        Raises:
            MultilineFunctionAnnotationViolation
            LiteralNoneAnnotation
            UnionNoneViolation

        """
        self._check_arg_annotation(node)
        self.generic_visit(node)

    def _check_arg_annotation(self, node: ast.arg) -> None:
        for sub_node in ast.walk(node):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

            if isinstance(sub_node, ast.Subscript):
                self._validator.check_for_literal_none(sub_node)
                self._validator.check_for_union_none(sub_node)

    def _check_return_annotation(self, node: AnyFunctionDef) -> None:
        if not node.returns:
            return

        for sub_node in ast.walk(node.returns):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.returns.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

            if isinstance(sub_node, ast.Subscript):
                self._validator.check_for_literal_none(sub_node)
                self._validator.check_for_union_none(sub_node)

    def _check_variable_annotation(self, node: ast.AnnAssign) -> None:
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Subscript):
                self._validator.check_for_union_none(sub_node)
