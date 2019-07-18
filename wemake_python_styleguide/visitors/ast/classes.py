# -*- coding: utf-8 -*-

import ast
from collections import Counter
from typing import ClassVar, Container, FrozenSet, List, Tuple

from typing_extensions import final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import classes, functions
from wemake_python_styleguide.logic.nodes import (
    get_context,
    is_contained,
    is_doc_string,
)
from wemake_python_styleguide.violations import best_practices as bp
from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.violations.consistency import (
    ObjectInBaseClassesListViolation,
    RequiredBaseClassViolation,
)
from wemake_python_styleguide.visitors import base, decorators


@final
class WrongClassVisitor(base.BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` anti-patterns.

    Here we check for stylistic issues and design patterns.
    """

    _allowed_body_nodes: ClassVar[types.AnyNodes] = (
        *FunctionNodes,

        ast.ClassDef,  # we allow some nested classes

        ast.Assign,  # attributes
        ast.AnnAssign,  # type annotations
    )

    _allowed_base_classes_nodes: ClassVar[types.AnyNodes] = (
        ast.Name,
        ast.Attribute,
        ast.Subscript,
    )

    def _check_base_classes_count(self, node: ast.ClassDef) -> None:
        if not node.bases:
            self.add_violation(
                RequiredBaseClassViolation(node, text=node.name),
            )

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        for base_name in node.bases:
            if not isinstance(base_name, self._allowed_base_classes_nodes):
                self.add_violation(oop.WrongBaseClassViolation(node))
                continue

            id_attr = getattr(base_name, 'id', None)
            if id_attr == 'BaseException':
                self.add_violation(bp.BaseExceptionSubclassViolation(node))
            elif id_attr == 'object' and len(node.bases) >= 2:
                self.add_violation(
                    ObjectInBaseClassesListViolation(node, text=id_attr),
                )
            elif classes.is_forbidden_super_class(id_attr):
                self.add_violation(
                    oop.BuiltinSubclassViolation(node, text=id_attr),
                )

    def _check_wrong_body_nodes(self, node: ast.ClassDef) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, self._allowed_body_nodes):
                continue
            if is_doc_string(sub_node):
                continue
            self.add_violation(oop.WrongClassBodyContentViolation(sub_node))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            RequiredBaseClassViolation
            ObjectInBaseClassesListViolation
            WrongClassBodyContentViolation
            BuiltinSubclassViolation

        """
        self._check_base_classes_count(node)
        self._check_base_classes(node)
        self._check_wrong_body_nodes(node)
        self.generic_visit(node)


@final
@decorators.alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongMethodVisitor(base.BaseNodeVisitor):
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
                self.add_violation(oop.StaticMethodViolation(node))

    def _check_bound_methods(self, node: types.AnyFunctionDef) -> None:
        node_context = get_context(node)
        if not isinstance(node_context, ast.ClassDef):
            return

        if not functions.get_all_arguments(node):
            self.add_violation(
                oop.MethodWithoutArgumentsViolation(node, text=node.name),
            )

        if node.name in constants.MAGIC_METHODS_BLACKLIST:
            self.add_violation(
                oop.BadMagicMethodViolation(node, text=node.name),
            )

    def _check_method_contents(self, node: types.AnyFunctionDef) -> None:
        if node.name == constants.INIT:
            if is_contained(node, self._not_appropriate_for_init):
                self.add_violation(bp.YieldInsideInitViolation(node))


@final
@decorators.alias('visit_any_assign', (
    'visit_Assign',
    'visit_AnnAssign',
))
class WrongSlotsVisitor(base.BaseNodeVisitor):
    """Visits class attributes."""

    _blacklisted_slots_nodes: ClassVar[types.AnyNodes] = (
        ast.Dict,
        ast.List,
        ast.Set,
    )

    def visit_any_assign(self, node: types.AnyAssign) -> None:
        """
        Checks all assigns that have correct context.

        Raises:
            WrongSlotsViolation

        """
        self._check_slots(node)
        self.generic_visit(node)

    def _contains_slots_assign(self, node: types.AnyAssign) -> bool:
        targets = get_assign_targets(node)

        for target in targets:
            if isinstance(target, ast.Name) and target.id == '__slots__':
                return True
        return False

    def _count_slots_items(
        self,
        node: types.AnyAssign,
        elements: ast.Tuple,
    ) -> None:
        fields: List[str] = []
        for tuple_item in elements.elts:
            if not isinstance(tuple_item, ast.Str):
                self.add_violation(oop.WrongSlotsViolation(node))
                return
            fields.append(tuple_item.s)

        for _, counter in Counter(fields).items():
            if counter > 1:
                self.add_violation(oop.WrongSlotsViolation(node))
                return

    def _check_slots(self, node: types.AnyAssign) -> None:
        if not isinstance(get_context(node), ast.ClassDef):
            return

        if not self._contains_slots_assign(node):
            return

        if isinstance(node.value, self._blacklisted_slots_nodes):
            self.add_violation(oop.WrongSlotsViolation(node))
            return

        if isinstance(node.value, ast.Tuple):
            self._count_slots_items(node, node.value)


@final
class ClassAttributeVisitor(base.BaseNodeVisitor):
    """Finds incorrect class attributes."""

    # TODO: can be moved to logic, if is used anywhere else
    def _flat_assign_names(
        self,
        nodes: List[types.AnyAssign],
    ) -> Container[str]:
        flat_assigns = []
        for attribute in nodes:
            targets = get_assign_targets(attribute)
            flat_assigns.extend([
                at.id for at in targets
                if isinstance(at, ast.Name)
            ])
        return set(flat_assigns)

    def _get_attributes(
        self,
        node: ast.ClassDef,
    ) -> Tuple[List[types.AnyAssign], List[ast.Attribute]]:
        class_attributes = []
        instance_attributes = []

        for child in ast.walk(node):
            if isinstance(child, ast.Attribute):
                if isinstance(child.ctx, ast.Store):
                    instance_attributes.append(child)
            if isinstance(child, AssignNodes) and get_context(child) == node:
                if child.value is not None:  # Not: `a: int`
                    class_attributes.append(child)
        return class_attributes, instance_attributes

    def _check_attributes_shadowing(self, node: ast.ClassDef) -> None:
        class_attributes, instance_attributes = self._get_attributes(node)
        class_attribute_names = self._flat_assign_names(class_attributes)

        for instance_attr in instance_attributes:
            if instance_attr.attr in class_attribute_names:
                self.add_violation(
                    oop.ShadowedClassAttributeViolation(
                        instance_attr, text=instance_attr.attr,
                    ),
                )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checks that class attributes are correct.

        Raises:
            ShadowedClassAttributeViolation

        """
        self._check_attributes_shadowing(node)
        self.generic_visit(node)
