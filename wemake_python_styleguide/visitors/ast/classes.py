# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, FrozenSet

from wemake_python_styleguide.constants import MAGIC_METHODS_BLACKLIST
from wemake_python_styleguide.types import AnyFunctionDef, final
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
    StaticMethodViolation,
)
from wemake_python_styleguide.violations.complexity import (
    TooManyBaseClassesViolation,
)
from wemake_python_styleguide.violations.consistency import (
    RequiredBaseClassViolation,
    WrongParentClassListDef,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
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

    def _check_decorators(self, node: AnyFunctionDef) -> None:
        for decorator in node.decorator_list:
            decorator_name = getattr(decorator, 'id', None)
            if decorator_name in self._staticmethod_names:
                self.add_violation(StaticMethodViolation(node))

    def _check_magic_methods(self, node: AnyFunctionDef) -> None:
        if node.name in MAGIC_METHODS_BLACKLIST:
            self.add_violation(BadMagicMethodViolation(node, text=node.name))

    def _check_base_class(self, node: ast.ClassDef) -> None:
        if len(node.bases) == 0:
            self.add_violation(RequiredBaseClassViolation(node, text=node.name))

    def _check_extra_object(self, node: ast.ClassDef) -> None:
        """Check 'object' class in parent list."""
        if len(node.bases) >= 2:
            for base_name in node.bases:
                id_attr = getattr(base_name, 'id', None)
                if id_attr == 'object':
                    self.add_violation(
                        WrongParentClassListDef(node, text=id_attr),
                    )

    def _check_base_classes_number(self, node: ast.ClassDef) -> None:
        """Check number of base classes."""
        if len(node.bases) > self.options.max_base_classes:
            self.add_violation(TooManyBaseClassesViolation(node,
                                                           text=node.name))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            RequiredBaseClassViolation
            WrongParentClassListDef

        """
        self._check_base_class(node)
        self._check_extra_object(node)
        self._check_base_classes_number(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Checking class methods: async and regular.

        Raises:
            StaticMethodViolation
            BadMagicMethodViolation

        """
        self._check_decorators(node)
        self._check_magic_methods(node)
        self.generic_visit(node)
