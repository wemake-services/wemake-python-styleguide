import ast
from collections.abc import Sequence
from typing import ClassVar, final

from wemake_python_styleguide import types
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.nodes import TypeVar, TypeVarTuple
from wemake_python_styleguide.logic.naming import enums
from wemake_python_styleguide.logic.tree import (
    attributes,
    classes,
    getters_setters,
    strings,
)
from wemake_python_styleguide.violations import best_practices as bp
from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.violations.best_practices import (
    SneakyTypeVarWithDefaultViolation,
)
from wemake_python_styleguide.visitors import base


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
        ) and not enums.has_regular_enum_base(node):
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
class ConsecutiveDefaultTypeVarsVisitor(base.BaseNodeVisitor):
    """Responsible for finding TypeVarTuple after a TypeVar with default."""

    def visit_ClassDef(  # pragma: >=3.13 cover
        self, node: ast.ClassDef
    ) -> None:
        """Check class definition for violation."""
        if hasattr(node, 'type_params'):  # pragma: >=3.13 cover
            self._check_generics(node.type_params)
        self.generic_visit(node)

    def _check_generics(  # pragma: >=3.13 cover
        self, type_params: Sequence[ast.AST]
    ) -> None:
        had_default = False
        for type_param in type_params:
            had_default = had_default or (
                isinstance(type_param, TypeVar)
                and type_param.default_value is not None
            )
            if had_default and isinstance(type_param, TypeVarTuple):
                self.add_violation(
                    SneakyTypeVarWithDefaultViolation(type_param)
                )
