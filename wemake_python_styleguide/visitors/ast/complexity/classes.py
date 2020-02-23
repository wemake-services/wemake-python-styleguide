# -*- coding: utf-8 -*-

import ast

from typing_extensions import final

from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.violations.complexity import (
    TooManyBaseClassesViolation,
    TooManyPublicAttributesViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class ClassComplexityVisitor(BaseNodeVisitor):
    """Checks class complexity."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            TooManyBaseClassesViolation
            TooManyPublicAttributesViolation

        """
        self._check_base_classes(node)
        self._check_public_attributes(node)
        self.generic_visit(node)

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        if len(node.bases) > self.options.max_base_classes:
            self.add_violation(
                TooManyBaseClassesViolation(
                    node,
                    text=str(len(node.bases)),
                    baseline=self.options.max_base_classes,
                ),
            )

    def _check_public_attributes(self, node: ast.ClassDef) -> None:
        attributes = filter(
            self._is_public_instance_attr_def,
            walk.get_subnodes_by_type(node, ast.Attribute),
        )
        attrs_count = len({attr.attr for attr in attributes})
        if attrs_count > self.options.max_attributes:
            self.add_violation(
                TooManyPublicAttributesViolation(
                    node,
                    text=str(attrs_count),
                    baseline=self.options.max_attributes,
                ),
            )

    def _is_public_instance_attr_def(self, node: ast.Attribute) -> bool:
        return (
            isinstance(node.ctx, ast.Store) and
            access.is_public(node.attr) and
            isinstance(node.value, ast.Name) and
            node.value.id == 'self'
        )
