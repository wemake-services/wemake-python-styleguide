import ast
from typing import Iterable, List, Optional, Tuple

from typing_extensions import Final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming.builtins import is_builtin_name
from wemake_python_styleguide.logic.naming.name_nodes import flat_tuples
from wemake_python_styleguide.types import AnyAssign, AnyFunctionDef

#: Type alias for the assignments we return from class inspection.
_AllAssignments = Tuple[List[AnyAssign], List[AnyAssign]]

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
    if class_name in constants.ALLOWED_BUILTIN_CLASSES:
        return False
    return is_builtin_name(class_name)


def get_assignments(
    node: ast.ClassDef,
    *,
    include_annotated: bool,
) -> _AllAssignments:
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
    class_assignments = []
    instance_assignments = []

    for subnode in ast.walk(node):
        instance_assign = _get_instance_assignment(subnode)
        if instance_assign is not None:
            instance_assignments.append(instance_assign)
            continue

        if include_annotated:
            class_assign = _get_annotated_class_attribute(node, subnode)
        else:
            class_assign = _get_class_assignment(node, subnode)
        if class_assign is not None:
            class_assignments.append(class_assign)

    return class_assignments, instance_assignments


def _get_instance_assignment(subnode: ast.AST) -> Optional[AnyAssign]:
    return subnode if (
        isinstance(subnode, AssignNodes) and
        any(
            isinstance(target, ast.Attribute) and
            isinstance(target.ctx, ast.Store) and
            isinstance(target.value, ast.Name) and
            target.value.id in constants.SPECIAL_ARGUMENT_NAMES_WHITELIST
            for targets in get_assign_targets(subnode)
            for target in flat_tuples(targets)
        )
    ) else None


def _get_class_assignment(
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
