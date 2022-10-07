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
from typing import Tuple, Type, Union

from typing_extensions import Protocol, TypeAlias

#: We use this type to represent all string-like nodes.
AnyText: TypeAlias = Union[ast.Str, ast.Bytes]

#: In cases we need to work with both import types.
AnyImport: TypeAlias = Union[ast.Import, ast.ImportFrom]

#: In cases we need to work with both function definitions.
AnyFunctionDef: TypeAlias = Union[ast.FunctionDef, ast.AsyncFunctionDef]

#: In cases we need to work with all function definitions (including lambdas).
AnyFunctionDefAndLambda: TypeAlias = Union[AnyFunctionDef, ast.Lambda]

#: In cases we need to work with both forms of if functions.
AnyIf: TypeAlias = Union[ast.If, ast.IfExp]

#: In cases we need to work with both sync and async loops.
AnyFor: TypeAlias = Union[ast.For, ast.AsyncFor]

#: In case we need to work with any loop: sync, async, and while.
AnyLoop: TypeAlias = Union[AnyFor, ast.While]

#: This is how you can define a variable in Python.
AnyVariableDef: TypeAlias = Union[ast.Name, ast.Attribute, ast.ExceptHandler]

#: All different comprehension types in one place.
AnyComprehension: TypeAlias = Union[
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
]

#: In cases we need to work with both sync and async context managers.
AnyWith: TypeAlias = Union[ast.With, ast.AsyncWith]

#: When we search for assign elements, we also need typed assign.
AnyAssign: TypeAlias = Union[ast.Assign, ast.AnnAssign]

#: In cases we need to work with both access types.
AnyAccess: TypeAlias = Union[
    ast.Attribute,
    ast.Subscript,
]

#: In case we need to handle types that can be chained.
AnyChainable: TypeAlias = Union[
    ast.Attribute,
    ast.Subscript,
    ast.Call,
]

#: Tuple of AST node types for declarative syntax.
AnyNodes: TypeAlias = Tuple[Type[ast.AST], ...]

#: We use this type to work with any text-like values. Related to `AnyText`.
AnyTextPrimitive: TypeAlias = Union[str, bytes]

#: That's how we define context of operations.
ContextNodes: TypeAlias = Union[
    ast.Module,
    ast.ClassDef,
    AnyFunctionDef,
]

#: Flake8 API format to return error messages.
CheckResult: TypeAlias = Tuple[int, int, str, type]


class ConfigurationOptions(Protocol):
    """
    Provides structure for the options we use in our checker and visitors.

    Then this protocol is passed to each individual visitor.
    It uses structural sub-typing, and does not represent any kind of a real
    class or structure.

    We use ``@property`` decorator here instead of regular attributes,
    because we need to explicitly mark these atrtibutes as read-only.

    See also:
        https://mypy.readthedocs.io/en/latest/protocols.html

    """

    def __hash__(self) -> int:
        """We need these options to be hashable."""

    # General:
    @property
    def min_name_length(self) -> int:
        ...

    @property
    def i_control_code(self) -> bool:
        ...

    @property
    def max_name_length(self) -> int:
        ...

    @property
    def max_noqa_comments(self) -> int:
        ...

    @property
    def nested_classes_whitelist(self) -> Tuple[str, ...]:
        ...

    @property
    def forbidden_inline_ignore(self) -> Tuple[str, ...]:
        ...

    @property
    def allowed_domain_names(self) -> Tuple[str, ...]:
        ...

    @property
    def forbidden_domain_names(self) -> Tuple[str, ...]:
        ...

    # Complexity:
    @property
    def max_arguments(self) -> int:
        ...

    @property
    def max_local_variables(self) -> int:
        ...

    @property
    def max_returns(self) -> int:
        ...

    @property
    def max_expressions(self) -> int:
        ...

    @property
    def max_module_members(self) -> int:
        ...

    @property
    def max_methods(self) -> int:
        ...

    @property
    def max_line_complexity(self) -> int:
        ...

    @property
    def max_jones_score(self) -> int:
        ...

    @property
    def max_imports(self) -> int:
        ...

    @property
    def max_imported_names(self) -> int:
        ...

    @property
    def max_base_classes(self) -> int:
        ...

    @property
    def max_decorators(self) -> int:
        ...

    @property
    def max_string_usages(self) -> int:
        ...

    @property
    def max_awaits(self) -> int:
        ...

    @property
    def max_try_body_length(self) -> int:
        ...

    @property
    def max_module_expressions(self) -> int:
        ...

    @property
    def max_function_expressions(self) -> int:
        ...

    @property
    def max_asserts(self) -> int:
        ...

    @property
    def max_access_level(self) -> int:
        ...

    @property
    def max_attributes(self) -> int:
        ...

    @property
    def max_raises(self) -> int:
        ...

    @property
    def max_cognitive_score(self) -> int:
        ...

    @property
    def max_cognitive_average(self) -> int:
        ...

    @property
    def max_call_level(self) -> int:
        ...

    @property
    def max_annotation_complexity(self) -> int:
        ...

    @property
    def max_import_from_members(self) -> int:
        ...

    @property
    def max_tuple_unpack_length(self) -> int:
        ...

    @property
    def show_violation_links(self) -> bool:
        ...

    @property
    def exps_for_one_empty_line(self) -> int:
        ...
