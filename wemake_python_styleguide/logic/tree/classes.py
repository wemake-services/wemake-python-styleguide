# -*- coding: utf-8 -*-

import ast
from typing import List, Optional, Set, Tuple, Union

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
    include_annotations: bool,
) -> Tuple[List[types.AnyAssign], List[ast.Attribute]]:
    """Returns all non annotated class and instance attributes of a class."""
    instance_attributes = get_instance_attributes(node)
    class_attributes = []
    if include_annotations:
        class_attributes = get_annotated_class_attributes(node)
    else:
        class_attributes = get_class_attributes(node)
    return class_attributes, instance_attributes


def get_class_attributes(
    node: ast.ClassDef,
) -> List[Union[ast.Assign, ast.AnnAssign]]:
    """Returns all non annotated class attributes of a class."""
    class_attributes = []
    for sub in ast.walk(node):
        is_correct_context = nodes.get_context(sub) == node
        has_value = getattr(sub, 'value', None)
        if isinstance(sub, AssignNodes) and has_value and is_correct_context:
            class_attributes.append(sub)

    return class_attributes


def get_annotated_class_attributes(
    node: ast.ClassDef,
) -> List[Union[ast.Assign, ast.AnnAssign]]:
    """Returns all class attributes of a class."""
    class_attributes = []
    for sub in ast.walk(node):
        is_correct_context = nodes.get_context(sub) == node
        has_value = getattr(sub, 'value', None)
        if isinstance(sub, AssignNodes) and has_value and is_correct_context:
            class_attributes.append(sub)
            continue
        if isinstance(sub, ast.AnnAssign) and is_correct_context:
            class_attributes.append(sub)

    return class_attributes


def get_instance_attributes(node: ast.ClassDef) -> List[ast.Attribute]:
    """Returns all instance attributes of a class."""
    instance_attributes = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and isinstance(sub.ctx, ast.Store):
            instance_attributes.append(sub)
    return instance_attributes


def getter_setter_postfixes(node: ast.ClassDef) -> Set[str]:
    """
    Return postfixes of all getter or setter methods.

    get_class_attribute becomes class_attribute

    set_instance_attribute becomes instance_attribute

    """
    method_postfixes = set()
    for sub in ast.walk(node):
        is_correct_context = nodes.get_context(sub) == node
        if isinstance(sub, FunctionNodes) and is_correct_context:
            if any(sub.name.startswith(prefix) for prefix in ('get_', 'set_')):
                method_postfixes.add(sub.name.partition('get_')[2])
                method_postfixes.add(sub.name.partition('set_')[2])
    return method_postfixes
