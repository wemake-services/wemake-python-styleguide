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
from typing import Tuple, Type, Union

from typing_extensions import Final, Protocol, final  # noqa: F401

#: In cases we need to work with both import types.
AnyImport = Union[ast.Import, ast.ImportFrom]

#: In cases we need to work with both function definitions.
AnyFunctionDef = Union[ast.FunctionDef, ast.AsyncFunctionDef]

#: In cases we need to work with all function definitions (including lambdas).
AnyFunctionDefAndLambda = Union[AnyFunctionDef, ast.Lambda]

#: In cases we need to work with both forms of if functions
AnyIf = Union[ast.If, ast.IfExp]

#: Flake8 API format to return error messages:
CheckResult = Tuple[int, int, str, type]

#: Tuple of AST node types for declarative syntax.
AnyNodes = Tuple[Type[ast.AST], ...]


class ConfigurationOptions(Protocol):
    """
    Provides structure for the options we use in our checker and visitors.

    Then this protocol is passed to each individual visitor.
    It uses structural sub-typing, and does not represent any kind of a real
    class or structure.

    See also:
        https://mypy.readthedocs.io/en/latest/protocols.html

    """

    # General:
    min_name_length: int
    i_control_code: bool
    max_name_length: int

    # Complexity:
    max_arguments: int
    max_local_variables: int
    max_returns: int
    max_expressions: int
    max_module_members: int
    max_methods: int
    max_line_complexity: int
    max_jones_score: int
    max_imports: int
    max_base_classes: int
    max_decorators: int
