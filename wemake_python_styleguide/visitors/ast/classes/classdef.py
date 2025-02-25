import ast
from collections.abc import Sequence
from typing import ClassVar, final

from attrs import frozen

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
from wemake_python_styleguide.options.validation import ValidatedOptions
from wemake_python_styleguide.violations import best_practices as bp
from wemake_python_styleguide.violations import oop
from wemake_python_styleguide.violations.best_practices import (
    SneakyTypeVarWithDefaultViolation,
)
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


@frozen
class TypeVarInfo:
    """Contains all the needed info of TypeVar."""

    name: str
    has_default: bool


@final
@decorators.alias(
    'visit_any_assign',
    (
        'visit_Assign',
        'visit_AnnAssign',
    ),
)
class ConsecutiveDefaultTypeVarsVisitor(base.BaseNodeVisitor):
    """Responsible for finding TypeVarTuple after a TypeVar with default."""

    def __init__(
        self, options: ValidatedOptions, tree: ast.AST, **kwargs
    ) -> None:
        """Create visitor and typevars namespace."""
        super().__init__(options, tree, **kwargs)
        self._defaulted_typevars: set[str] = set()

    def visit_any_assign(self, node: types.AnyAssign) -> None:
        """Register a TypeVar if needed."""
        typevar = self._assume_typevar_creation(node)
        if not typevar or not typevar.has_default:
            return
        self._defaulted_typevars.add(typevar.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Check class definition for violation."""
        if hasattr(node, 'type_params'):  # pragma: no cover
            self._check_new_style_generics(node.type_params)
        self._check_old_style_generics(node.bases)
        self.generic_visit(node)

    def _assume_typevar_creation(
        self, node: types.AnyAssign
    ) -> TypeVarInfo | None:
        target = _get_target_of_assign(node)
        if (
            not isinstance(node.value, ast.Call)
            or not isinstance(node.value.func, ast.Name)
            or not isinstance(target, ast.Name)
            or node.value.func.id != 'TypeVar'
        ):
            return None
        return TypeVarInfo(
            name=target.id,
            has_default=any(kw.arg == 'default' for kw in node.value.keywords),
        )

    def _check_new_style_generics(self, type_params: Sequence[ast.AST]) -> None:
        had_default = False
        for type_param in type_params:
            had_default = had_default or (
                isinstance(type_param, TypeVar)
                and type_param.name in self._defaulted_typevars
            )
            if isinstance(type_param, TypeVarTuple) and had_default:
                self.add_violation(
                    SneakyTypeVarWithDefaultViolation(type_param)
                )

    def _check_old_style_generics(self, bases: Sequence[ast.expr]) -> None:
        for cls_base in bases:
            if (
                isinstance(cls_base, ast.Subscript)
                and isinstance(cls_base.value, ast.Name)
                and cls_base.value.id == 'Generic'
                and isinstance(cls_base.slice, ast.Tuple)
            ):
                self._check_generic_tuple(cls_base.slice.elts)

    def _check_generic_tuple(self, elts: Sequence[ast.expr]) -> None:
        had_default = False
        for expr in elts:
            had_default = had_default or (
                isinstance(expr, ast.Name)
                and expr.id in self._defaulted_typevars
            )
            if isinstance(expr, ast.Starred) and had_default:
                self.add_violation(SneakyTypeVarWithDefaultViolation(expr))


def _get_target_of_assign(assign: types.AnyAssign) -> ast.AST:
    if isinstance(assign, ast.Assign):
        return assign.targets[0]
    return assign.target
