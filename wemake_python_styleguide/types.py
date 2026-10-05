"""
This module contains knowledge about the most important types that we use.

There are also different :term:`visitor` specific types
that are defined and use exclusively in that file.

Policy
~~~~~~

If any of the following statements is true, move the type to this file:

- if type is used in multiple files
- if type is complex enough it has to be documented
- if type is very important for the public API

final
~~~~~

As you can see in the source code almost everything
is marked as ``@final`` or ``Final``.

It means that this value cannot be subclassed or reassigned.
This it only a ``mypy`` feature, it does not affect ``python`` runtime.

We do this, because we value composition over inheritance.
And this ``@final`` decorators help you to define readable and clear APIs
for cases when inheritance is used.

See also:
    My guide about ``@final`` type in ``python``:
    https://sobolevn.me/2018/07/real-python-contants

Reference
~~~~~~~~~

"""

import ast
from typing import TypeAlias

AnyImport: TypeAlias = ast.Import | ast.ImportFrom
"""In cases we need to work with both import types."""

AnyFunctionDef: TypeAlias = ast.FunctionDef | ast.AsyncFunctionDef
"""In cases we need to work with both function definitions."""

AnyFunctionDefAndLambda: TypeAlias = AnyFunctionDef | ast.Lambda
"""In cases we need to work with all
 function definitions (including lambdas)."""

AnyIf: TypeAlias = ast.If | ast.IfExp
"""In cases we need to work with both forms of if functions."""

AnyFor: TypeAlias = ast.For | ast.AsyncFor
"""In cases we need to work with both sync and async loops."""

AnyLoop: TypeAlias = AnyFor | ast.While
"""In case we need to work with any loop: sync, async, and while."""

AnyVariableDef: TypeAlias = ast.Name | ast.Attribute | ast.ExceptHandler
"""This is how you can define a variable in Python."""

AnyComprehension: TypeAlias = (
    ast.ListComp | ast.DictComp | ast.SetComp | ast.GeneratorExp
)
"""All different comprehension types in one place."""

AnyWith: TypeAlias = ast.With | ast.AsyncWith
"""In cases we need to work with both sync and async context managers."""

AnyAssign: TypeAlias = ast.Assign | ast.AnnAssign
"""When we search for assign elements, we also need typed assign."""

AnyAssignWithWalrus: TypeAlias = AnyAssign | ast.NamedExpr
"""When we search for assign elements, we also need typed assign."""

AnyAccess: TypeAlias = ast.Attribute | ast.Subscript
"""In cases we need to work with both access types."""

AnyChainable: TypeAlias = ast.Attribute | ast.Subscript | ast.Call
"""In case we need to handle types that can be chained."""

AnyNodes: TypeAlias = tuple[type[ast.AST], ...]
"""Tuple of AST node types for declarative syntax."""

AnyTextPrimitive: TypeAlias = str | bytes
"""We use this type to work with any text-like values. Related to `AnyText`."""

ContextNodes: TypeAlias = ast.Module | ast.ClassDef | AnyFunctionDef
"""That's how we define context of operations."""

CheckResult: TypeAlias = tuple[int, int, str, type]
"""Flake8 API format to return error messages."""
