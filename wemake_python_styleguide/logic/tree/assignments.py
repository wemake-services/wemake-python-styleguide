import ast
import itertools
from typing import Iterable, List, Optional, Tuple

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.types import AnyAssign

#: Type alias for the assignments we return from class inspection.
_AllAssignments = Tuple[List[AnyAssign], List[AnyAssign]]


def flat_assignment_values(assigns: Iterable[AnyAssign]) -> Iterable[ast.AST]:
    """
    Returns flat values from assignment.

    Use this function when you need to get list of values
    from assign nodes.
    """
    return itertools.chain.from_iterable((
        _flat_nodes(assign.value)
        for assign in assigns
        if isinstance(assign.value, ast.AST)
    ))


def _flat_nodes(node: ast.AST) -> List[ast.AST]:
    flatten_nodes: List[ast.AST] = []

    if isinstance(node, ast.Tuple):
        for subnode in node.elts:
            flatten_nodes.extend(_flat_nodes(subnode))
    else:
        flatten_nodes.append(node)
    return flatten_nodes


def get_assignments(node: ast.ClassDef) -> _AllAssignments:
    """
    Helper to get all assignments from class nod definitions.

    Args:
        node: class node definition.

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

        class_assign = _get_class_assignment(node, subnode)
        if class_assign is not None:
            class_assignments.append(class_assign)

    return class_assignments, instance_assignments


def _get_instance_assignment(subnode: ast.AST) -> Optional[AnyAssign]:
    return subnode if (
        isinstance(subnode, AssignNodes) and
        any(
            isinstance(target, ast.Attribute) and
            isinstance(target.value, ast.Name) and
            target.value.id in constants.SPECIAL_ARGUMENT_NAMES_WHITELIST
            for targets in get_assign_targets(subnode)
            for target in _flat_nodes(targets)
        )
    ) else None


def _get_class_assignment(
    node: ast.ClassDef,
    subnode: ast.AST,
) -> Optional[AnyAssign]:
    return subnode if (
        isinstance(subnode, AssignNodes) and
        nodes.get_context(subnode) is node and
        getattr(subnode, 'value', None)
    ) else None
