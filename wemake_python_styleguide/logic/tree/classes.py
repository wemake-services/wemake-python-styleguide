# -*- coding: utf-8 -*-

import ast
from typing import List, Optional, Set, Tuple

from wemake_python_styleguide import types
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.constants import ALLOWED_BUILTIN_CLASSES
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming.builtins import is_builtin_name
from wemake_python_styleguide.logic.tree import functions


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
) -> Tuple[List[types.AnyAssign], List[ast.Attribute]]:
    """Returns all class and instance attributes of a class."""
    class_attributes = []
    instance_attributes = []

    for nd in ast.walk(node):
        if isinstance(nd, ast.Attribute) and isinstance(nd.ctx, ast.Store):
            instance_attributes.append(nd)
            continue

        has_assign = (
            nodes.get_context(nd) == node and
            getattr(nd, 'value', None)
        )
        if isinstance(nd, AssignNodes) and has_assign:
            class_attributes.append(nd)

    return class_attributes, instance_attributes


def getter_setter_postfixes(node: ast.ClassDef) -> Set[str]:
    """
    Return postfixes of all getter or setter methods.

    get_class_attribute becomes class_attribute

    set_instance_attribute becomes instance_attribute

    """
    method_postfixes = set()
    for subnode in ast.walk(node):
        correct_context = nodes.get_context(subnode) == node
        if isinstance(subnode, FunctionNodes) and correct_context:
            if is_getter_or_setter(subnode):
                method_postfixes.add(subnode.name.partition('get_')[2])
                method_postfixes.add(subnode.name.partition('set_')[2])
    return method_postfixes


def is_getter_or_setter(node: types.AnyFunctionDef) -> bool:
    """Checks if non property decorated function contains get or set prefix."""
    if any(node.name.startswith(prefix) for prefix in ('get_', 'set_')):
        is_property = functions.check_decorators(node, 'property')
        is_property_setter = functions.check_decorators(node, '.setter')
        if not (is_property or is_property_setter):
            return True
    return False
