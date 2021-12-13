import ast
from inspect import getmro
from typing import List, Mapping, Optional, Tuple

from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.walk import is_contained
from wemake_python_styleguide.types import AnyNodes


def get_exception_name(node: ast.Raise) -> Optional[str]:
    """Returns the exception name or ``None`` if node has not it."""
    exception = node.exc
    if exception is None:
        return None

    exception_func = getattr(exception, 'func', None)
    if exception_func:
        exception = exception_func

    return getattr(exception, 'id', None)


def get_cause_name(node: ast.Raise) -> Optional[str]:
    """Returns the cause name or ``None`` if node has not it."""
    return getattr(node.cause, 'id', None)


def get_all_exception_names(node: ast.Try) -> List[str]:
    """Returns a list of all exceptions names in ``ast.Try``."""
    exceptions: List[str] = []
    for exc_handler in node.handlers:
        # There might be complex things hidden inside an exception type,
        # so we want to get the string representation of it:
        if isinstance(exc_handler.type, ast.Name):
            exceptions.append(source.node_to_string(exc_handler.type))
        elif isinstance(exc_handler.type, ast.Tuple):
            exceptions.extend([
                source.node_to_string(node)
                for node in exc_handler.type.elts
            ])
    return exceptions


def traverse_exception(
    cls,
    builtin_exceptions=None,
) -> Mapping[str, Tuple[str]]:
    """
    Returns a dictionary of built-in exceptions hierarchy.

    The return dictionary has exception name as the key and
    all its subclasses as the value.

    Original code: https://bit.ly/36HVPk2
    """
    builtin_exceptions = builtin_exceptions or {}

    if cls.__name__ not in builtin_exceptions:
        builtin_exceptions[cls.__name__] = ()

    for exc in cls.__subclasses__():
        builtin_exceptions[exc.__name__] = tuple(
            base.__name__
            for base in getmro(exc)
            if (
                issubclass(base, BaseException) and
                base.__name__ != exc.__name__
            )
        )
        traverse_exception(exc, builtin_exceptions)

    return builtin_exceptions


def find_returning_nodes(
    node: ast.Try,
    bad_returning_nodes: AnyNodes,
) -> Tuple[bool, bool, bool, bool]:
    """Find nodes that return value and are inside try/except/else/finally."""
    try_has = any(
        is_contained(line, bad_returning_nodes)
        for line in node.body
    )
    except_has = any(
        is_contained(except_handler, bad_returning_nodes)
        for except_handler in node.handlers
    )
    else_has = any(
        is_contained(line, bad_returning_nodes)
        for line in node.orelse
    )
    finally_has = any(
        is_contained(line, bad_returning_nodes)
        for line in node.finalbody
    )
    return try_has, except_has, else_has, finally_has
