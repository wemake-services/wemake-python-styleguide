import ast
from typing import Union

from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.types import AnyVariableDef

_VarDefinition = Union[ast.AST, ast.expr]
_LocalVariable = Union[ast.Name, ast.ExceptHandler]


def get_variable_name(node: _LocalVariable) -> str:
    """Used to get variable names from all definitions."""
    if isinstance(node, ast.Name):
        return node.id
    return getattr(node, 'name', '')


def looks_like_builtin(node: AnyVariableDef) -> bool:
    """
    We allow attributes and class-level builtin overrides.

    Like: ``self.map = {}`` or ``def map(self, function):``
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
            _is_valid_single(element) is not None
            for element in target.elts
        )
    return _is_valid_single(target)


def _is_valid_single(node: _VarDefinition) -> bool:
    return (
        isinstance(node, ast.Name) or
        isinstance(node, ast.Starred) and isinstance(node.value, ast.Name)
    )
