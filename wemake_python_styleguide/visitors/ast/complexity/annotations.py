import ast
from typing import List

from typing_extensions import final

from wemake_python_styleguide.logic.complexity.annotations import (
    get_annotation_compexity,
)
from wemake_python_styleguide.logic.tree.functions import get_all_arguments
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.complexity import (
    TooComplexAnnotationViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class AnnotationComplexityVisitor(BaseNodeVisitor):
    """Ensures that annotations are used correctly."""

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checks return type annotations.

        Raises:
            TooComplexAnnotationViolation

        """
        self._check_function_annotations_complexity(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """
        Check assignment annotation.

        Raises:
            TooComplexAnnotationViolation

        """
        self._check_annotations_complexity(node, [node.annotation])
        self.generic_visit(node)

    def _check_function_annotations_complexity(
        self, node: AnyFunctionDef,
    ) -> None:
        annotations = [
            arg.annotation
            for arg in get_all_arguments(node)
            if arg.annotation is not None
        ]
        if node.returns is not None:
            annotations.append(node.returns)
        self._check_annotations_complexity(node, annotations)

    def _check_annotations_complexity(
        self,
        node: ast.AST,
        annotations: List[ast.expr],
    ) -> None:
        max_complexity = self.options.max_annotation_complexity
        for annotation in annotations:
            complexity = get_annotation_compexity(annotation)
            if complexity > max_complexity:
                self.add_violation(
                    TooComplexAnnotationViolation(
                        node,
                        text=str(complexity),
                        baseline=max_complexity,
                    ),
                )
