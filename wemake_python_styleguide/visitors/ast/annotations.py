import ast
import sys
from typing import Optional, Union

from typing_extensions import final

from wemake_python_styleguide.compat.functions import get_slice_expr
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.best_practices import (
    DisallowUnionTypeViolation,
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
class WrongAnnotationVisitor(BaseNodeVisitor):
    """Ensures that annotations are used correctly."""
    _union_names = ('Union', 'Optional')

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks return type annotations."""
        self._check_return_annotation(node)
        self._check_prohibited_union_annotation(node, node.returns)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        """Checks arguments annotations."""
        self._check_arg_annotation(node)
        self._check_prohibited_union_annotation(node, node.annotation)
        self.generic_visit(node)

    def _check_return_annotation(self, node: AnyFunctionDef) -> None:
        if not node.returns:
            return

        for sub_node in ast.walk(node.returns):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.returns.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

    def _check_arg_annotation(self, node: ast.arg) -> None:
        for sub_node in ast.walk(node):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno and lineno != node.lineno:
                self.add_violation(MultilineFunctionAnnotationViolation(node))
                return

    def _check_prohibited_union_annotation(
        self,
        node: Union[AnyFunctionDef, ast.arg],
        annotation_node: Optional[ast.expr],
    ) -> None:
        should_skip_check = (
            sys.version_info < (3, 10) or
            annotation_node is None
        )
        if should_skip_check:
            return

        is_check_violated = self._has_union_annotation_been_used(node, annotation_node)
        if is_check_violated:  # pragma: py-lt-310
            self.add_violation(DisallowUnionTypeViolation(node))

    def _has_union_annotation_been_used(
        self,
        node: Union[AnyFunctionDef, ast.arg],
        annotation_node: Optional[ast.expr],
    ) -> bool:
        if not isinstance(annotation_node, ast.Subscript):
            return False

        union_used_in_node_name = (
            isinstance(annotation_node.value, ast.Name) and
            annotation_node.value.id in self._union_names
        )
        if union_used_in_node_name:
            return True

        union_used_in_node_attr = (
            isinstance(annotation_node.value, ast.Attribute) and
            annotation_node.value.attr in self._union_names
        )
        if union_used_in_node_attr:
            return True

        return self._has_union_annotation_been_used(
            node,
            get_slice_expr(annotation_node),
        )
