import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, FrozenSet, List, Optional

from typing_extensions import final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.logic.arguments import function_args, super_args
from wemake_python_styleguide.logic.naming import access, name_nodes
from wemake_python_styleguide.logic.tree import (
    attributes,
    classes,
    functions,
    strings,
)
from wemake_python_styleguide.violations import best_practices as bp
from wemake_python_styleguide.violations import consistency, oop
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
        *AssignNodes,  # fields and annotations
    )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Raises:
            RequiredBaseClassViolation
            ObjectInBaseClassesListViolation
            WrongBaseClassViolation
            WrongClassBodyContentViolation
            BuiltinSubclassViolation

        """
        self._check_base_classes_count(node)
        self._check_base_classes(node)
        self._check_wrong_body_nodes(node)
        self.generic_visit(node)

    def _check_base_classes_count(self, node: ast.ClassDef) -> None:
        if not node.bases:
            self.add_violation(
                consistency.RequiredBaseClassViolation(node, text=node.name),
            )

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        for base_name in node.bases:
            if not self._is_correct_base_class(base_name):
                self.add_violation(oop.WrongBaseClassViolation(base_name))
                continue

            self._check_base_classes_rules(node, base_name)

    def _check_base_classes_rules(
        self,
        node: ast.ClassDef,
        base_name: ast.expr,
    ) -> None:
        id_attr = getattr(base_name, 'id', None)

        if id_attr == 'BaseException':
            self.add_violation(bp.BaseExceptionSubclassViolation(node))
        elif id_attr == 'object' and len(node.bases) >= 2:
            self.add_violation(
                consistency.ObjectInBaseClassesListViolation(
                    node, text=id_attr,
                ),
            )
        elif classes.is_forbidden_super_class(id_attr):
            self.add_violation(
                oop.BuiltinSubclassViolation(node, text=id_attr),
            )

    def _check_wrong_body_nodes(self, node: ast.ClassDef) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, self._allowed_body_nodes):
                continue
            if strings.is_doc_string(sub_node):
                continue
            self.add_violation(oop.WrongClassBodyContentViolation(sub_node))

    def _is_correct_base_class(self, base_class: ast.AST) -> bool:
        if isinstance(base_class, ast.Name):
            return True
        elif isinstance(base_class, ast.Attribute):
            return all(
                isinstance(sub_node, (ast.Name, ast.Attribute))
                for sub_node in attributes.parts(base_class)
            )
        elif isinstance(base_class, ast.Subscript):
            parts = list(attributes.parts(base_class))
            subscripts = list(filter(
                lambda part: isinstance(part, ast.Subscript), parts,
            ))
            correct_items = all(
                isinstance(sub_node, (ast.Name, ast.Attribute, ast.Subscript))
                for sub_node in parts
            )

            return len(subscripts) == 1 and correct_items
        return False


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

    def visit_any_function(self, node: types.AnyFunctionDef) -> None:
        """
        Checking class methods: async and regular.

        Raises:
            StaticMethodViolation
            BadMagicMethodViolation
            YieldMagicMethodViolation
            MethodWithoutArgumentsViolation
            AsyncMagicMethodViolation
            UselessOverwrittenMethodViolation

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
        node_context = nodes.get_context(node)
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

        is_async = isinstance(node, ast.AsyncFunctionDef)
        if is_async and access.is_magic(node.name):
            if node.name in constants.ASYNC_MAGIC_METHODS_BLACKLIST:
                self.add_violation(
                    oop.AsyncMagicMethodViolation(node, text=node.name),
                )

        self._check_useless_overwritten_methods(
            node,
            class_name=node_context.name,
        )

    def _check_method_contents(self, node: types.AnyFunctionDef) -> None:
        if node.name in constants.YIELD_MAGIC_METHODS_BLACKLIST:
            if walk.is_contained(node, (ast.Yield, ast.YieldFrom)):
                self.add_violation(oop.YieldMagicMethodViolation(node))

    def _get_call_stmt_of_useless_method(
        self,
        node: types.AnyFunctionDef,
    ) -> Optional[ast.Call]:
        """
        Fetches ``super`` call statement from function definition.

        Consider next body as possible candidate of useless method:

        1. Optional[docstring]
        2. single return statement with call
        3. single statement with call, but without return

        Related:
        https://github.com/wemake-services/wemake-python-styleguide/issues/1168

        """
        statements_number = len(node.body)
        if statements_number > 2 or statements_number == 0:
            return None

        if statements_number == 2:
            if not strings.is_doc_string(node.body[0]):
                return None

        stmt = node.body[-1]
        if isinstance(stmt, ast.Return):
            call_stmt = stmt.value
            return call_stmt if isinstance(call_stmt, ast.Call) else None
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            return stmt.value
        return None

    def _check_useless_overwritten_methods(
        self,
        node: types.AnyFunctionDef,
        class_name: str,
    ) -> None:
        if node.decorator_list:
            # Any decorator can change logic and make this overwrite useful.
            return

        call_stmt = self._get_call_stmt_of_useless_method(node)
        if call_stmt is None or not isinstance(call_stmt.func, ast.Attribute):
            return

        attribute = call_stmt.func
        defined_method_name = node.name
        if defined_method_name != attribute.attr:
            return

        if not super_args.is_ordinary_super_call(attribute.value, class_name):
            return

        if not function_args.is_call_matched_by_arguments(node, call_stmt):
            return

        self.add_violation(
            oop.UselessOverwrittenMethodViolation(
                node, text=defined_method_name,
            ),
        )


@final
@decorators.alias('visit_any_assign', (
    'visit_Assign',
    'visit_AnnAssign',
))
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
        """
        Checks all assigns that have correct context.

        Raises:
            WrongSlotsViolation

        """
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
        fields: DefaultDict[str, List[ast.AST]] = defaultdict(list)

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

    def _slot_item_name(self, node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Str):
            return node.s
        if isinstance(node, ast.Starred):
            return source.node_to_string(node)
        return None

    def _are_correct_slots(self, slots: List[ast.AST]) -> bool:
        return all(
            slot.s.isidentifier()
            for slot in slots
            if isinstance(slot, ast.Str)
        )


@final
class ClassAttributeVisitor(base.BaseNodeVisitor):
    """Finds incorrect class attributes."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checks that class attributes are correct.

        Raises:
            ShadowedClassAttributeViolation

        """
        self._check_attributes_shadowing(node)
        self.generic_visit(node)

    def _check_attributes_shadowing(self, node: ast.ClassDef) -> None:
        class_attributes, instance_attributes = classes.get_attributes(node)
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


@final
class ClassMethodOrderVisitor(base.BaseNodeVisitor):
    """Checks that all methods inside the class are ordered correctly."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Ensures that class has correct method order.

        Raises:
            WrongMethodOrderViolation

        """
        self._check_method_order(node)
        self.generic_visit(node)

    def _check_method_order(self, node: ast.ClassDef) -> None:
        method_nodes: List[str] = []

        for subnode in ast.walk(node):
            if isinstance(subnode, FunctionNodes):
                if nodes.get_context(subnode) == node:
                    method_nodes.append(subnode.name)

        ideal = sorted(method_nodes, key=self._ideal_order, reverse=True)
        for existing_order, ideal_order in zip(method_nodes, ideal):
            if existing_order != ideal_order:
                self.add_violation(consistency.WrongMethodOrderViolation(node))
                return

    def _ideal_order(self, first: str) -> int:
        base_methods_order = {
            '__new__': 5,  # highest priority
            '__init__': 4,
            '__call__': 3,
        }
        public_and_magic_methods_priority = 2

        if access.is_protected(first):
            return 1
        if access.is_private(first):
            return 0  # lowest priority
        return base_methods_order.get(first, public_and_magic_methods_priority)
