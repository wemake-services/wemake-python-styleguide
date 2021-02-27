import ast

from wemake_python_styleguide.types import AnyFunctionDef


def has_overload_decorator(function: AnyFunctionDef) -> bool:
    """
    Detects if a function has ``@overload`` or ``@typing.overload`` decorators.

    It is useful, because ``@overload`` function defs
    have slightly different rules: for example, they do not count as real defs
    in complexity rules.
    """
    for decorator in function.decorator_list:
        is_partial_name = (
            isinstance(decorator, ast.Name) and
            decorator.id == 'overload'
        )
        is_full_name = (
            isinstance(decorator, ast.Attribute) and
            decorator.attr == 'overload' and
            isinstance(decorator.value, ast.Name) and
            decorator.value.id == 'typing'
        )
        if is_partial_name or is_full_name:
            return True
    return False
