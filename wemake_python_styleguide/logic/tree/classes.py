import ast
from typing import List, Optional, Tuple

from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.constants import ALLOWED_BUILTIN_CLASSES
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming.builtins import is_builtin_name
from wemake_python_styleguide.types import AnyAssign

#: Type alias for the attributes we return from class inspection.
_AllAttributes = Tuple[List[AnyAssign], List[ast.Attribute]]


def is_forbidden_super_class(class_name: Optional[str]) -> bool:
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


def get_attributes(node: ast.ClassDef) -> _AllAttributes:
    """
    Helper to get all attributes from class nod definitions.

    There are limitations.
    First of all, we cannot get inherited attributes.
    Secondly, ones that are set via ``setattr`` or similar.
    Thirdly, we return all attributes and there might be duplicates.

    Args:
        node: class node definition.

    Returns:
        A tuple of lists for both class and instance level variables.

    """
    class_attributes = []
    instance_attributes = []

    for subnode in ast.walk(node):
        instance_attr = _get_instance_attribute(subnode)
        if instance_attr is not None:
            instance_attributes.append(instance_attr)
            continue

        class_attr = _get_class_attribute(node, subnode)
        if class_attr is not None:
            class_attributes.append(class_attr)

    return class_attributes, instance_attributes


def _get_instance_attribute(node: ast.AST) -> Optional[ast.Attribute]:
    return node if (
        isinstance(node, ast.Attribute) and
        isinstance(node.ctx, ast.Store) and
        isinstance(node.value, ast.Name) and
        node.value.id == 'self'
    ) else None


def _get_class_attribute(
    node: ast.ClassDef, subnode: ast.AST,
) -> Optional[AnyAssign]:
    return subnode if (
        isinstance(subnode, AssignNodes) and
        nodes.get_context(subnode) == node and
        getattr(subnode, 'value', None)
    ) else None
