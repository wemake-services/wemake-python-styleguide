# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, FrozenSet

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.logics.nodes import is_contained
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
    StaticMethodViolation,
    YieldInsideInitViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ObjectInBaseClassesListViolation,
    RequiredBaseClassViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@types.final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongClassVisitor(BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` anti-patterns.

    Here we check for stylistic issues and design patterns.
    """

    _staticmethod_names: ClassVar[FrozenSet[str]] = frozenset((
        'staticmethod',
    ))

    _not_appropriate_for_init: ClassVar[types.AnyNodes] = (
        ast.Yield,
    )

    def _check_decorators(self, node: types.AnyFunctionDef) -> None:
        for decorator in node.decorator_list:
            decorator_name = getattr(decorator, 'id', None)
            if decorator_name in self._staticmethod_names:
                self.add_violation(StaticMethodViolation(node))

    def _check_magic_methods(self, node: types.AnyFunctionDef) -> None:
        if node.name in constants.MAGIC_METHODS_BLACKLIST:
            self.add_violation(BadMagicMethodViolation(node, text=node.name))

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        """Check 'object' class in parent list."""
        if len(node.bases) == 0:
            self.add_violation(
                RequiredBaseClassViolation(node, text=node.name),
            )

        if len(node.bases) >= 2:
            for base_name in node.bases:
                id_attr = getattr(base_name, 'id', None)
                if id_attr == 'object':
                    self.add_violation(
                        ObjectInBaseClassesListViolation(node, text=id_attr),
                    )

    def _check_method_contents(self, node: types.AnyFunctionDef) -> None:
        if node.name == constants.INIT:
            if is_contained(node, self._not_appropriate_for_init):
                self.add_violation(YieldInsideInitViolation(node))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            RequiredBaseClassViolation
            ObjectInBaseClassesListViolation

        """
        self._check_base_classes(node)
        self.generic_visit(node)

    def visit_any_function(self, node: types.AnyFunctionDef) -> None:
        """
        Checking class methods: async and regular.

        Raises:
            StaticMethodViolation
            BadMagicMethodViolation
            YieldInsideInitViolation

        """
        self._check_decorators(node)
        self._check_magic_methods(node)
        self._check_method_contents(node)
        self.generic_visit(node)
