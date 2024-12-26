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

#: In cases we need to work with both import types.
AnyImport: TypeAlias = ast.Import | ast.ImportFrom

#: In cases we need to work with both function definitions.
AnyFunctionDef: TypeAlias = ast.FunctionDef | ast.AsyncFunctionDef

#: In cases we need to work with all function definitions (including lambdas).
AnyFunctionDefAndLambda: TypeAlias = AnyFunctionDef | ast.Lambda

#: In cases we need to work with both forms of if functions.
AnyIf: TypeAlias = ast.If | ast.IfExp

#: In cases we need to work with both sync and async loops.
AnyFor: TypeAlias = ast.For | ast.AsyncFor

#: In case we need to work with any loop: sync, async, and while.
AnyLoop: TypeAlias = AnyFor | ast.While

#: This is how you can define a variable in Python.
AnyVariableDef: TypeAlias = ast.Name | ast.Attribute | ast.ExceptHandler

#: All different comprehension types in one place.
AnyComprehension: TypeAlias = (
    ast.ListComp | ast.DictComp | ast.SetComp | ast.GeneratorExp
)

#: In cases we need to work with both sync and async context managers.
AnyWith: TypeAlias = ast.With | ast.AsyncWith

#: When we search for assign elements, we also need typed assign.
AnyAssign: TypeAlias = ast.Assign | ast.AnnAssign

#: When we search for assign elements, we also need typed assign.
AnyAssignWithWalrus: TypeAlias = AnyAssign | ast.NamedExpr

#: In cases we need to work with both access types.
AnyAccess: TypeAlias = ast.Attribute | ast.Subscript

#: In case we need to handle types that can be chained.
AnyChainable: TypeAlias = ast.Attribute | ast.Subscript | ast.Call

#: Tuple of AST node types for declarative syntax.
AnyNodes: TypeAlias = tuple[type[ast.AST], ...]

#: We use this type to work with any text-like values. Related to `AnyText`.
AnyTextPrimitive: TypeAlias = str | bytes

#: That's how we define context of operations.
ContextNodes: TypeAlias = ast.Module | ast.ClassDef | AnyFunctionDef

#: Flake8 API format to return error messages.
CheckResult: TypeAlias = tuple[int, int, str, type]
