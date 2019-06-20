# -*- coding: utf-8 -*-

import ast
from collections import Counter
from typing import ClassVar, FrozenSet, List

from typing_extensions import final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.logics.functions import get_all_arguments
from wemake_python_styleguide.logics.nodes import is_contained, is_doc_string
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
    BaseExceptionSubclassViolation,
    IncorrectBaseClassViolation,
    IncorrectClassBodyContentViolation,
    IncorrectSlotsViolation,
    MethodWithoutArgumentsViolation,
    StaticMethodViolation,
    YieldInsideInitViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ObjectInBaseClassesListViolation,
    RequiredBaseClassViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
class WrongClassVisitor(BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` anti-patterns.

    Here we check for stylistic issues and design patterns.
    """

    _allowed_body_nodes: ClassVar[types.AnyNodes] = (
        ast.FunctionDef,  # methods
        ast.AsyncFunctionDef,

        ast.ClassDef,  # we allow some nested classes

        ast.Assign,  # attributes
        ast.AnnAssign,  # type annotations
    )

    _allowed_base_classes_nodes: ClassVar[types.AnyNodes] = (
        ast.Name,
        ast.Attribute,
        ast.Subscript,
    )

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        if len(node.bases) == 0:
            self.add_violation(
                RequiredBaseClassViolation(node, text=node.name),
            )

        for base_name in node.bases:
            if not isinstance(base_name, self._allowed_base_classes_nodes):
                self.add_violation(IncorrectBaseClassViolation(node))
                continue

            id_attr = getattr(base_name, 'id', None)
            if id_attr == 'BaseException':
                self.add_violation(BaseExceptionSubclassViolation(node))
            elif id_attr == 'object' and len(node.bases) >= 2:
                self.add_violation(
                    ObjectInBaseClassesListViolation(node, text=id_attr),
                )

    def _check_wrong_body_nodes(self, node: ast.ClassDef) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, self._allowed_body_nodes):
                continue
            if is_doc_string(sub_node):
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


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongMethodVisitor(BaseNodeVisitor):
    """Visits functions, but treats them as methods."""

    _staticmethod_names: ClassVar[FrozenSet[str]] = frozenset((
        'staticmethod',
    ))

    _not_appropriate_for_init: ClassVar[types.AnyNodes] = (
        ast.Yield,
    )

    def visit_any_function(self, node: types.AnyFunctionDef) -> None:
        """
        Checking class methods: async and regular.

        Raises:
            StaticMethodViolation
            BadMagicMethodViolation
            YieldInsideInitViolation
            MethodWithoutArgumentsViolation

        """
        self._check_decorators(node)
        self._check_bound_methods(node)
        self._check_method_contents(node)
        self.generic_visit(node)

    def _check_decorators(self, node: types.AnyFunctionDef) -> None:
        for decorator in node.decorator_list:
            decorator_name = getattr(decorator, 'id', None)
            if decorator_name in self._staticmethod_names:
                self.add_violation(StaticMethodViolation(node))

    def _check_bound_methods(self, node: types.AnyFunctionDef) -> None:
        node_context = getattr(node, 'wps_context', None)
        if not isinstance(node_context, ast.ClassDef):
            return

        if len(get_all_arguments(node)) == 0:
            self.add_violation(
                MethodWithoutArgumentsViolation(node, text=node.name),
            )

        if node.name in constants.MAGIC_METHODS_BLACKLIST:
            self.add_violation(BadMagicMethodViolation(node, text=node.name))

    def _check_method_contents(self, node: types.AnyFunctionDef) -> None:
        if node.name == constants.INIT:
            if is_contained(node, self._not_appropriate_for_init):
                self.add_violation(YieldInsideInitViolation(node))


@final
class WrongSlotsVisitor(BaseNodeVisitor):
    """Visits class attributes."""

    _blacklisted_slots_nodes: ClassVar[types.AnyNodes] = (
        ast.Dict,
        ast.List,
        ast.Set,
    )

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Checks all assigns that have correct context.

        Raises:
            IncorrectSlotsViolation

        """
        context = getattr(node, 'wps_context', None)
        if isinstance(context, ast.ClassDef):
            self._check_slots(node)
        self.generic_visit(node)

    def _contains_slots_assign(self, node: ast.Assign) -> bool:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == '__slots__':
                return True
        return False

    def _count_slots_items(
        self,
        node: ast.Assign,
        elements: ast.Tuple,
    ) -> None:
        fields: List[str] = []
        for tuple_item in elements.elts:
            if not isinstance(tuple_item, ast.Str):
                self.add_violation(IncorrectSlotsViolation(node))
                return
            fields.append(tuple_item.s)

        for _, counter in Counter(fields).items():
            if counter > 1:
                self.add_violation(IncorrectSlotsViolation(node))
                return

    def _check_slots(self, node: ast.Assign) -> None:
        if not self._contains_slots_assign(node):
            return

        if isinstance(node.value, self._blacklisted_slots_nodes):
            self.add_violation(IncorrectSlotsViolation(node))
            return

        if isinstance(node.value, ast.Tuple):
            self._count_slots_items(node, node.value)
