import ast
from typing import List, Union

from typing_extensions import TypeAlias

from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming import access

_VarDefinition: TypeAlias = Union[ast.AST, ast.expr]
_LocalVariable: TypeAlias = Union[ast.Name, ast.ExceptHandler]


def get_variable_name(node: _LocalVariable) -> str:
    """Used to get variable names from all definitions."""
    if isinstance(node, ast.Name):
        return node.id
    return getattr(node, 'name', '')


def does_shadow_builtin(node: ast.AST) -> bool:
    """
    We allow attributes and class-level builtin overrides.

    Like: ``self.list = []`` or ``def map(self, function):``

    Why?
    Because they cannot harm you since they do not shadow the real builtin.
    """
    return (
        not isinstance(node, ast.Attribute) and
        not isinstance(nodes.get_context(node), ast.ClassDef)
    )


def is_valid_block_variable_definition(node: _VarDefinition) -> bool:
    """Is used to check either block variables are correctly defined."""
    if isinstance(node, ast.Tuple):
        return all(
            is_valid_block_variable_definition(var_definition)
            for var_definition in node.elts
        )
    return _is_valid_single(node)


def is_valid_unpacking_target(target: ast.expr) -> bool:
    """Checks if unpacking target is correct."""
    if isinstance(target, ast.Tuple):
        return all(
            _is_valid_single(element)
            for element in target.elts
        )
    return _is_valid_single(target)


def _is_valid_single(node: _VarDefinition) -> bool:
    return (
        isinstance(node, ast.Name) or
        isinstance(node, ast.Starred) and isinstance(node.value, ast.Name)
    )


def is_getting_element_by_unpacking(targets: List[ast.expr]) -> bool:
    """Checks if unpacking targets used to get first or last element."""
    if len(targets) != 2:
        return False
    first_item = (
        isinstance(targets[1], ast.Starred) and
        _is_unused_variable_name(targets[1].value)
    )
    last_item = (
        isinstance(targets[0], ast.Starred) and
        _is_unused_variable_name(targets[0].value)
    )
    return first_item or last_item


def _is_unused_variable_name(node: ast.expr) -> bool:
    return isinstance(node, ast.Name) and access.looks_like_unused(node.id)
