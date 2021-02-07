import ast
from typing import Iterable, List, Optional, Tuple

from typing_extensions import Final

from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.constants import ALLOWED_BUILTIN_CLASSES
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming.builtins import is_builtin_name
from wemake_python_styleguide.types import AnyAssign, AnyFunctionDef

#: Type alias for the attributes we return from class inspection.
_AllAttributes = Tuple[List[AnyAssign], List[ast.Attribute]]

#: Prefixes that usually define getters and setters.
_GetterSetterPrefixes: Final = ('get_', 'set_')

#: Fixes length of a getter/setter.
GETTER_LENGTH: Final = 4


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
        instance_attr = _get_instance_attribute(subnode)
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


def _get_instance_attribute(node: ast.AST) -> Optional[ast.Attribute]:
    return node if (
        isinstance(node, ast.Attribute) and
        isinstance(node.ctx, ast.Store) and
        isinstance(node.value, ast.Name) and
        node.value.id == 'self'
    ) else None


def _get_class_attribute(
    node: ast.ClassDef,
    subnode: ast.AST,
) -> Optional[AnyAssign]:
    return subnode if (
        nodes.get_context(subnode) is node and
        getattr(subnode, 'value', None) and
        isinstance(subnode, AssignNodes)
    ) else None


def _get_annotated_class_attribute(
    node: ast.ClassDef,
    subnode: ast.AST,
) -> Optional[AnyAssign]:
    return subnode if (
        nodes.get_context(subnode) is node and
        (
            getattr(subnode, 'value', None) and
            isinstance(subnode, AssignNodes)
        ) or isinstance(subnode, ast.AnnAssign)
    ) else None


def find_getters_and_setters(node: ast.ClassDef) -> Iterable[AnyFunctionDef]:
    """Returns nodes of all getter or setter methods."""
    for sub in ast.walk(node):
        is_correct_context = nodes.get_context(sub) is node
        if isinstance(sub, FunctionNodes) and is_correct_context:
            if sub.name[:GETTER_LENGTH] in _GetterSetterPrefixes:
                yield sub
