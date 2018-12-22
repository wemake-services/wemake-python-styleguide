# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, FrozenSet

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.logics.nodes import is_contained
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
    BaseExceptionSubclassViolation,
    IncorrectClassBodyContentViolation,
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

    _allowed_body_nodes: ClassVar[types.AnyNodes] = (
        ast.FunctionDef,  # methods
        ast.AsyncFunctionDef,

        ast.ClassDef,  # we allow some nested classes

        ast.Assign,  # attributes
        ast.AnnAssign,  # type annotations
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
        """Check ``object`` class in parent classes list."""
        if len(node.bases) == 0:
            self.add_violation(
                RequiredBaseClassViolation(node, text=node.name),
            )

        for base_name in node.bases:
            id_attr = getattr(base_name, 'id', None)
            if id_attr == 'BaseException':
                self.add_violation(BaseExceptionSubclassViolation(node))
            elif id_attr == 'object' and len(node.bases) >= 2:
                self.add_violation(
                    ObjectInBaseClassesListViolation(node, text=id_attr),
                )

    def _check_method_contents(self, node: types.AnyFunctionDef) -> None:
        if node.name == constants.INIT:
            if is_contained(node, self._not_appropriate_for_init):
                self.add_violation(YieldInsideInitViolation(node))

    def _check_wrong_body_nodes(self, node: ast.ClassDef) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, self._allowed_body_nodes):
                continue
            if isinstance(sub_node, ast.Expr):
                if isinstance(sub_node.value, ast.Str):
                    # This means it is a docsting, we can ignore this node:
                    continue
            self.add_violation(IncorrectClassBodyContentViolation(sub_node))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            RequiredBaseClassViolation
            ObjectInBaseClassesListViolation
            IncorrectClassBodyContentViolation

        """
        self._check_base_classes(node)
        self._check_wrong_body_nodes(node)
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
