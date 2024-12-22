import ast
from collections.abc import Mapping
from inspect import getmro
from typing import TypeAlias

from wemake_python_styleguide.compat.types import AnyTry
from wemake_python_styleguide.logic import source


def get_exception_name(node: ast.Raise) -> str | None:
    """Returns the exception name or ``None`` if node has not it."""
    exception = node.exc
    if exception is None:
        return None

    if isinstance(exception, ast.Call):
        exception = exception.func

    return getattr(exception, 'id', None)


def get_cause_name(node: ast.Raise) -> str | None:
    """Returns the cause name or ``None`` if node has not it."""
    return getattr(node.cause, 'id', None)


def get_all_exception_names(node: AnyTry) -> list[str]:
    """Returns a list of all exceptions names in try blocks."""
    exceptions: list[str] = []
    for exc_handler in node.handlers:
        # There might be complex things hidden inside an exception type,
        # so we want to get the string representation of it:
        if isinstance(exc_handler.type, ast.Name):
            exceptions.append(source.node_to_string(exc_handler.type))
        elif isinstance(exc_handler.type, ast.Tuple):
            exceptions.extend(
                [source.node_to_string(node) for node in exc_handler.type.elts],
            )
    return exceptions


_ExceptionMemo: TypeAlias = dict[str, tuple[str, ...]]


def traverse_exception(
    cls: type[BaseException],
    builtin_exceptions: _ExceptionMemo | None = None,
) -> Mapping[str, tuple[str, ...]]:
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
                issubclass(base, BaseException)
                and base.__name__ != exc.__name__
            )
        )
        traverse_exception(exc, builtin_exceptions)

    return builtin_exceptions
