import ast

from wemake_python_styleguide.logic.nodes import get_context
from wemake_python_styleguide.logic.tree.functions import given_function_called
from wemake_python_styleguide.types import AnyFunctionDef


def _is_self_call(func: AnyFunctionDef, node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and bool(given_function_called(node, {f'self.{func.name}'}))
    )


def _check_method_recursion(func: AnyFunctionDef) -> bool:
    return bool([node for node in ast.walk(func) if _is_self_call(func, node)])


def _check_function_recursion(func: AnyFunctionDef) -> bool:
    return bool(
        [
            node
            for node in ast.walk(func)
            if isinstance(node, ast.Call)
            and given_function_called(node, {func.name})
        ],
    )


def has_recursive_calls(func: AnyFunctionDef) -> bool:
    """
    Determines whether function has recursive calls or not.

    Does not work for methods.
    """
    if isinstance(get_context(func), ast.ClassDef):
        return _check_method_recursion(func)
    return _check_function_recursion(func)
