import ast
from collections import defaultdict
from typing import ClassVar, final

from wemake_python_styleguide import types
from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.logic.naming import name_nodes
from wemake_python_styleguide.logic.tree import (
    attributes,
    classes,
)
from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.visitors import base, decorators


@final
class ClassAttributeVisitor(base.BaseNodeVisitor):
    """Finds incorrectattributes."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Checks that assigned attributes are correct."""
        self._check_attributes_shadowing(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """Finds `lambda` assigns in attributes."""
        self._check_lambda_attribute(node)
        self.generic_visit(node)

    def _check_attributes_shadowing(self, node: ast.ClassDef) -> None:
        if classes.is_dataclass(node):
            # dataclasses by its nature allow class-level attributes
            # shadowing from instance level.
            return

        class_attributes, instance_attributes = classes.get_attributes(
            node,
            include_annotated=False,
        )
        class_attribute_names = set(
            name_nodes.flat_variable_names(class_attributes),
        )

        for instance_attr in instance_attributes:
            if instance_attr.attr in class_attribute_names:
                self.add_violation(
                    oop.ShadowedClassAttributeViolation(
                        instance_attr,
                        text=instance_attr.attr,
                    ),
                )

    def _check_lambda_attribute(self, node: ast.Lambda) -> None:
        assigned = walk.get_closest_parent(node, AssignNodes)
        if not assigned or not isinstance(assigned, ast.Assign):
            return  # just used, not assigned

        context = nodes.get_context(assigned)
        if not isinstance(context, types.AnyFunctionDef) or not isinstance(
            nodes.get_context(context),
            ast.ClassDef,
        ):
            return  # it is not assigned in a method of a class

        for attribute in assigned.targets:
            if isinstance(
                attribute, ast.Attribute
            ) and attributes.is_special_attr(attribute):
                self.add_violation(oop.LambdaAttributeAssignedViolation(node))


@final
@decorators.alias(
    'visit_any_assign',
    (
        'visit_Assign',
        'visit_AnnAssign',
    ),
)
class WrongSlotsVisitor(base.BaseNodeVisitor):
    """Visits class attributes."""

    _whitelisted_slots_nodes: ClassVar[types.AnyNodes] = (
        ast.Tuple,
        ast.Attribute,
        ast.Subscript,
        ast.Name,
        ast.Call,
    )

    def visit_any_assign(self, node: types.AnyAssign) -> None:
        """Checks all assigns that have correct context."""
        self._check_slots(node)
        self.generic_visit(node)

    def _contains_slots_assign(self, node: types.AnyAssign) -> bool:
        for target in get_assign_targets(node):
            if isinstance(target, ast.Name) and target.id == '__slots__':
                return True
        return False

    def _count_slots_items(
        self,
        node: types.AnyAssign,
        elements: ast.Tuple,
    ) -> None:
        fields: defaultdict[str, list[ast.AST]] = defaultdict(list)

        for tuple_item in elements.elts:
            slot_name = self._slot_item_name(tuple_item)
            if not slot_name:
                self.add_violation(oop.WrongSlotsViolation(tuple_item))
                return
            fields[slot_name].append(tuple_item)

        for slots in fields.values():
            if not self._are_correct_slots(slots) or len(slots) > 1:
                self.add_violation(oop.WrongSlotsViolation(node))
                return

    def _check_slots(self, node: types.AnyAssign) -> None:
        if not isinstance(nodes.get_context(node), ast.ClassDef):
            return

        if not self._contains_slots_assign(node):
            return

        if not isinstance(node.value, self._whitelisted_slots_nodes):
            self.add_violation(oop.WrongSlotsViolation(node))
            return

        if isinstance(node.value, ast.Tuple):
            self._count_slots_items(node, node.value)

    def _slot_item_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Starred):
            return source.node_to_string(node)
        return None

    def _are_correct_slots(self, slots: list[ast.AST]) -> bool:
        return all(
            slot.value.isidentifier()
            for slot in slots
            if isinstance(slot, ast.Constant) and isinstance(slot.value, str)
        )
