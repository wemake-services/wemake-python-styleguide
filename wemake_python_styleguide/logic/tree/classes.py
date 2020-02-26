# -*- coding: utf-8 -*-

import ast
from typing import List, Optional, Set, Tuple

from wemake_python_styleguide import types
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.constants import ALLOWED_BUILTIN_CLASSES
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming.builtins import is_builtin_name


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

    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and isinstance(sub.ctx, ast.Store):
            instance_attributes.append(sub)
            continue

        has_assign = (
            nodes.get_context(sub) == node and
            getattr(sub, 'value', None)
        )
        if isinstance(sub, AssignNodes) and has_assign:
            class_attributes.append(sub)

    return class_attributes, instance_attributes


def getter_setter_postfixes(node: ast.ClassDef) -> Set[str]:
    """
    Return postfixes of all getter or setter methods.

    get_class_attribute becomes class_attribute

    set_instance_attribute becomes instance_attribute

    """
    method_postfixes = set()
    for sub in ast.walk(node):
        correct_context = nodes.get_context(sub) == node
        if isinstance(sub, FunctionNodes) and correct_context:
            if any(sub.name.startswith(prefix) for prefix in ('get_', 'set_')):
                method_postfixes.add(sub.name.partition('get_')[2])
                method_postfixes.add(sub.name.partition('set_')[2])
    return method_postfixes
