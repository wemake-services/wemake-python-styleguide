# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.complexity import (
    TooManyBaseClassesViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class ClassComplexityVisitor(BaseNodeVisitor):
    """Checks class complexity."""

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        if len(node.bases) > self.options.max_base_classes:
            self.add_violation(
                TooManyBaseClassesViolation(node, text=str(len(node.bases))),
            )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            TooManyBaseClassesViolation

        """
        self._check_base_classes(node)
        self.generic_visit(node)
