import ast
from typing import Final, TypeAlias

from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.constants import ALLOWED_BUILTIN_CLASSES
from wemake_python_styleguide.logic import nodes, source
from wemake_python_styleguide.logic.naming.builtins import is_builtin_name
from wemake_python_styleguide.types import AnyAssign

#: Type alias for the attributes we return from class inspection.
_AllAttributes: TypeAlias = tuple[list[AnyAssign], list[ast.Attribute]]

#: Names that can define a dataclass.
_DATACLASS_NAMES: Final = frozenset((
    # stdlib:
    'dataclasses.dataclass',
    # attrs:
    'attrs.define',
    'attrs.frozen',
    'attrs.mutable',
    'attr.s',
    'attr.attrs',
    'attr.attributes',
    'attr.frozen',
    'attr.mutable',
    'attr.dataclass',
    # pydantic also has `dataclass` and `dataclasses.dataclass`
))

#: Short form of dataclass decorators without module names.
_SHORT_DATACLASS_NAMES: Final = frozenset(
    dataclass_name.split('.')[1] for dataclass_name in _DATACLASS_NAMES
)


def is_forbidden_super_class(class_name: str | None) -> bool:
    """
    Tells whether or not the base class is forbidden to be subclassed.

    >>> is_forbidden_super_class('str')
    True

    >>> is_forbidden_super_class('Exception')
    False

    >>> is_forbidden_super_class('object')
    False

    >>> is_forbidden_super_class('type')
    False

    >>> is_forbidden_super_class('CustomName')
    False

    >>> is_forbidden_super_class(None)
    False

    """
    if not class_name or not class_name.islower():
        return False
    if class_name in ALLOWED_BUILTIN_CLASSES:
        return False
    return is_builtin_name(class_name)


def is_dataclass(node: ast.ClassDef) -> bool:
    """Checks if some class is defined as a dataclass using popular libs."""
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call):
            decorator = decorator.func  # noqa: PLW2901

        if not isinstance(decorator, ast.Name | ast.Attribute):
            continue

        decorator_code = source.node_to_string(decorator)
        if (
            decorator_code in _DATACLASS_NAMES
            or decorator_code in _SHORT_DATACLASS_NAMES
        ):
            return True
    return False


def get_attributes(
    node: ast.ClassDef,
    *,
    include_annotated: bool,
) -> _AllAttributes:
    """
    Helper to get all attributes from class nod definitions.

    There are limitations.
    First of all, we cannot get inherited attributes.
    Secondly, ones that are set via ``setattr`` or similar.
    Thirdly, we return all attributes and there might be duplicates.

    Args:
        node: class node definition.
        include_annotated: whether or not to include AnnAssign attributes.

    Returns:
        A tuple of lists for both class and instance level variables.

    """
    class_attributes = []
    instance_attributes = []

    for subnode in ast.walk(node):
        instance_attr = get_instance_attribute(subnode)
        if instance_attr is not None:
            instance_attributes.append(instance_attr)
            continue

        if include_annotated:
            class_attr = _get_annotated_class_attribute(node, subnode)
        else:
            class_attr = _get_class_attribute(node, subnode)
        if class_attr is not None:
            class_attributes.append(class_attr)

    return class_attributes, instance_attributes


def get_instance_attribute(node: ast.AST) -> ast.Attribute | None:
    """Returns node if this is an instance attribute or `None` if not."""
    return (
        node
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.ctx, ast.Store)
            and isinstance(node.value, ast.Name)
            and node.value.id == 'self'
        )
        else None
    )


def _get_class_attribute(
    node: ast.ClassDef,
    subnode: ast.AST,
) -> AnyAssign | None:
    return (
        subnode
        if (
            nodes.get_context(subnode) is node
            and getattr(subnode, 'value', None)
            and isinstance(subnode, AssignNodes)
        )
        else None
    )


def _get_annotated_class_attribute(
    node: ast.ClassDef,
    subnode: ast.AST,
) -> AnyAssign | None:
    return (
        subnode
        if (
            (
                nodes.get_context(subnode) is node
                and (
                    getattr(subnode, 'value', None)
                    and isinstance(subnode, AssignNodes)
                )
            )
            or isinstance(subnode, ast.AnnAssign)
        )
        else None
    )
