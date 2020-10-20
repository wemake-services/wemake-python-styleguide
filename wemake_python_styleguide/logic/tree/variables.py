import ast
from typing import Union

_VarDefinition = Union[ast.AST, ast.expr]
_LocalVariable = Union[ast.Name, ast.ExceptHandler]


def get_variable_name(node: _LocalVariable) -> str:
    """Used to get variable names from all definitions."""
    if isinstance(node, ast.Name):
        return node.id
    return getattr(node, 'name', '')


def is_valid_block_variable_definition(node: _VarDefinition) -> bool:
    """Is used to check either block variables are correctly defined."""
    if isinstance(node, ast.Tuple):
        return all(
            _is_valid_single(var_definition)
            for var_definition in node.elts
        )
    return _is_valid_single(node)


def _is_valid_single(node: _VarDefinition) -> bool:
    return (
        isinstance(node, ast.Name) or
        isinstance(node, ast.Starred) and isinstance(node.value, ast.Name)
    )
