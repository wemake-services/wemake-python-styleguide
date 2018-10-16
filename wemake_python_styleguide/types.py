# -*- coding: utf-8 -*-

"""
This module contains custom ``mypy`` types that we commonly use.

Policy
------

If any of the following statements is true, move the type to this file:

- if type is used in multiple files
- if type is complex enough it has to be documented
- if type is very important for the public API

"""

import ast
from typing import TYPE_CHECKING, Tuple, Type, Union

if TYPE_CHECKING:  # pragma: no cover
    # TODO: use Final types to annotate all constants
    from typing_extensions import Protocol  # noqa: Z435

    # This solves cycle imports problem:
    from .visitors import base  # noqa: F401,Z300,Z435
else:
    # We do not need to do anything if type checker is not working:
    Protocol = object

#: Visitor type definition:
VisitorClass = Type['base.BaseVisitor']

#: In cases we need to work with both import types:
AnyImport = Union[ast.Import, ast.ImportFrom]

#: In cases we need to work with both function definitions:
AnyFunctionDef = Union[ast.FunctionDef, ast.AsyncFunctionDef]

#: In cases we need to work with all function definitions (including Lambda)
AnyFunctionDefAndLambda = Union[
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.Lambda,
]

#: In cases we need to work with both forms of if functions
AnyIf = Union[ast.If, ast.IfExp]


#: Flake8 API format to return error messages:
CheckResult = Tuple[int, int, str, type]

#: Tuple of AST node types for declarative syntax:
AnyNodes = Tuple[Type[ast.AST], ...]


class ConfigurationOptions(Protocol):
    """
    Provides structure for the options we use in our checker.

    Then this protocol is passed to each individual visitor and used there.
    It uses structural sub-typing, and does not represent any kind of a real
    class or structure.

    This class actually works only when running type check.
    At other cases it is just an ``object``.

    See also:
        https://mypy.readthedocs.io/en/latest/protocols.html

    """

    # General:
    min_variable_length: int
    i_control_code: bool

    # Complexity:
    max_arguments: int
    max_local_variables: int
    max_returns: int
    max_expressions: int
    max_offset_blocks: int
    max_elifs: int
    max_module_members: int
    max_methods: int
    max_line_complexity: int
    max_jones_score: int
    max_imports: int
    max_conditions: int

    # File names:
    min_module_name_length: int
