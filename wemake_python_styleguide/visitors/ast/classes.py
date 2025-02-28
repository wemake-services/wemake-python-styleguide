import ast
from collections import defaultdict
from typing import ClassVar, final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.logic.arguments import function_args, super_args
from wemake_python_styleguide.logic.naming import access, enums, name_nodes
from wemake_python_styleguide.logic.tree import (
    attributes,
    classes,
    functions,
    getters_setters,
    strings,
)
from wemake_python_styleguide.violations import best_practices as bp
from wemake_python_styleguide.violations import consistency, oop
from wemake_python_styleguide.visitors import base, decorators


@final
class WrongClassDefVisitor(base.BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` def anti-patterns.

    Here we check for stylistic issues and design patterns.
    """

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Checking class definitions."""
        self._check_base_classes(node)
        self._check_kwargs_unpacking(node)
        self.generic_visit(node)

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        for base_name in node.bases:
            if not self._is_correct_base_class(base_name):
                self.add_violation(oop.WrongBaseClassViolation(base_name))
                continue

            self._check_base_classes_rules(node, base_name)

    def _is_correct_base_class(self, base_class: ast.AST) -> bool:
        if isinstance(base_class, ast.Name):
            return True
        if isinstance(base_class, ast.Attribute):
            return all(
                isinstance(sub_node, ast.Name | ast.Attribute)
                for sub_node in attributes.parts(base_class)
            )
        if isinstance(base_class, ast.Subscript):
            parts = list(attributes.parts(base_class))
            subscripts = list(
                filter(
                    lambda part: isinstance(part, ast.Subscript),
                    parts,
                ),
            )
            correct_items = all(
                isinstance(sub_node, ast.Name | ast.Attribute | ast.Subscript)
                for sub_node in parts
            )

            return len(subscripts) == 1 and correct_items
        return False

    def _check_base_classes_rules(
        self,
        node: ast.ClassDef,
        base_name: ast.expr,
    ) -> None:
        id_attr = getattr(base_name, 'id', None)

        if id_attr == 'BaseException':
            self.add_violation(bp.BaseExceptionSubclassViolation(node))
        elif classes.is_forbidden_super_class(
            id_attr,
        ) and not enums.has_enum_base(node):
            self.add_violation(
                oop.BuiltinSubclassViolation(node, text=id_attr),
            )

    def _check_kwargs_unpacking(self, node: ast.ClassDef) -> None:
        for keyword in node.keywords:
            if keyword.arg is None:
                self.add_violation(
                    bp.KwargsUnpackingInClassDefinitionViolation(node),
                )


@final
class WrongClassBodyVisitor(base.BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` body anti-patterns.

    Here we check for stylistic issues and design patterns.
    """

    _allowed_body_nodes: ClassVar[types.AnyNodes] = (
        *FunctionNodes,
        ast.ClassDef,  # we allow some nested classes
        *AssignNodes,  # fields and annotations
    )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Checking class definitions."""
        self._check_wrong_body_nodes(node)
        self._check_getters_setters_methods(node)
        self.generic_visit(node)

    def _check_wrong_body_nodes(self, node: ast.ClassDef) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, self._allowed_body_nodes):
                continue
            if strings.is_doc_string(sub_node):
                continue
            self.add_violation(oop.WrongClassBodyContentViolation(sub_node))

    def _check_getters_setters_methods(self, node: ast.ClassDef) -> None:
        getters_and_setters = set(
            getters_setters.find_paired_getters_and_setters(node),
        ).union(
            set(  # To delete duplicated violations
                getters_setters.find_attributed_getters_and_setters(node),
            ),
        )
        for method in getters_and_setters:
            self.add_violation(
                oop.UnpythonicGetterSetterViolation(
                    method,
                    text=method.name,
                ),
            )


@final
@decorators.alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class WrongMethodVisitor(base.BaseNodeVisitor):
    """Visits functions, but treats them as methods."""

    _special_async_iter: ClassVar[frozenset[str]] = frozenset(('__aiter__',))

    def visit_any_function(self, node: types.AnyFunctionDef) -> None:
        """Checking class methods: async and regular."""
        node_context = nodes.get_context(node)
        if isinstance(node_context, ast.ClassDef):
            self._check_bound_methods(node)
            self._check_yield_magic_methods(node)
            self._check_async_magic_methods(node)
            self._check_useless_overwritten_methods(
                node,
                class_name=node_context.name,
            )
        self.generic_visit(node)

    def _check_bound_methods(self, node: types.AnyFunctionDef) -> None:
        if functions.is_staticmethod(node):
            self.add_violation(oop.StaticMethodViolation(node))
        elif not functions.get_all_arguments(node):
            self.add_violation(
                oop.MethodWithoutArgumentsViolation(node, text=node.name),
            )

        if node.name in constants.MAGIC_METHODS_BLACKLIST:
            self.add_violation(
                oop.BadMagicMethodViolation(node, text=node.name),
            )

    def _check_yield_magic_methods(self, node: types.AnyFunctionDef) -> None:
        if isinstance(node, ast.AsyncFunctionDef):
            return

        if (
            node.name in constants.YIELD_MAGIC_METHODS_BLACKLIST
            and walk.is_contained(node, (ast.Yield, ast.YieldFrom))
        ):
            self.add_violation(
                oop.YieldMagicMethodViolation(node, text=node.name),
            )

    def _check_async_magic_methods(self, node: types.AnyFunctionDef) -> None:
        if not isinstance(node, ast.AsyncFunctionDef):
            return

        if node.name in self._special_async_iter:
            if not walk.is_contained(node, ast.Yield):  # YieldFrom not async
                self.add_violation(
                    oop.AsyncMagicMethodViolation(node, text=node.name),
                )
        elif node.name in constants.ASYNC_MAGIC_METHODS_BLACKLIST:
            self.add_violation(
                oop.AsyncMagicMethodViolation(node, text=node.name),
            )

    def _check_useless_overwritten_methods(
        self,
        node: types.AnyFunctionDef,
        class_name: str,
    ) -> None:
        if node.decorator_list:
            # Any decorator can change logic and make this overwrite useful.
            return

        if node.args.defaults or list(filter(None, node.args.kw_defaults)):
            # It means that function / method has defaults in args,
            # we cannot be sure that these defaults are the same
            # as in the call def, ignoring it.
            return

        call_stmt = self._get_call_stmt_of_useless_method(node)
        if call_stmt is None or not isinstance(call_stmt.func, ast.Attribute):
            return

        attribute = call_stmt.func
        defined_method_name = node.name
        if defined_method_name != attribute.attr:
            return

        if not super_args.is_ordinary_super_call(
            attribute.value, class_name
        ) or not function_args.is_call_matched_by_arguments(node, call_stmt):
            return

        self.add_violation(
            oop.UselessOverwrittenMethodViolation(
                node,
                text=defined_method_name,
            ),
        )

    def _get_call_stmt_of_useless_method(
        self,
        node: types.AnyFunctionDef,
    ) -> ast.Call | None:
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

        if statements_number == 2 and not strings.is_doc_string(node.body[0]):
            return None

        stmt = node.body[-1]
        if isinstance(stmt, ast.Return):
            call_stmt = stmt.value
            return call_stmt if isinstance(call_stmt, ast.Call) else None
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            return stmt.value
        return None


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
class ClassMethodOrderVisitor(base.BaseNodeVisitor):
    """Checks that all methods inside the class are ordered correctly."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Ensures that class has correct methods order."""
        self._check_method_order(node)
        self.generic_visit(node)

    def _check_method_order(self, node: ast.ClassDef) -> None:
        method_nodes = [
            subnode.name
            for subnode in ast.walk(node)
            if (
                isinstance(subnode, FunctionNodes)
                and nodes.get_context(subnode) is node
            )
        ]

        ideal = sorted(method_nodes, key=self._ideal_order, reverse=True)
        for existing_order, ideal_order in zip(
            method_nodes,
            ideal,
            strict=False,
        ):
            if existing_order != ideal_order:
                self.add_violation(consistency.WrongMethodOrderViolation(node))
                return

    def _ideal_order(self, first: str) -> int:
        base_methods_order = {
            '__init_subclass__': 7,  # highest priority
            '__new__': 6,
            '__init__': 5,
            '__call__': 4,
            '__await__': 3,
        }
        public_and_magic_methods_priority = 2

        if access.is_protected(first):
            return 1
        if access.is_private(first):
            return 0  # lowest priority
        return base_methods_order.get(first, public_and_magic_methods_priority)


@final
class BuggySuperCallVisitor(base.BaseNodeVisitor):
    """
    Responsible for finding wrong form of `super()` call for certain contexts.

    Call to `super()` without arguments will cause unexpected `TypeError` in a
    number of specific contexts. Read more: https://bugs.python.org/issue46175
    """

    _buggy_super_contexts: ClassVar[types.AnyNodes] = (
        ast.GeneratorExp,
        ast.SetComp,
        ast.ListComp,
        ast.DictComp,
    )

    def visit_Call(self, node: ast.Call) -> None:
        """Checks if this is a `super()` call in a specific context."""
        self._check_buggy_super_context(node)
        self.generic_visit(node)

    def _check_buggy_super_context(self, node: ast.Call):
        if not isinstance(node.func, ast.Name):
            return

        if node.func.id != 'super' or node.args:
            return

        # Check for being in a nested function
        ctx = nodes.get_context(node)
        if isinstance(ctx, FunctionNodes):
            outer_ctx = nodes.get_context(ctx)
            if isinstance(outer_ctx, FunctionNodes):
                self.add_violation(oop.BuggySuperContextViolation(node))
                return

        if walk.get_closest_parent(node, self._buggy_super_contexts):
            self.add_violation(oop.BuggySuperContextViolation(node))
