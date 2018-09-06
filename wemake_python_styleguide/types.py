# -*- coding: utf-8 -*-

"""
This module contains custom `mypy` types that we commonly use.

General rule is: if there's a complex type, put it here.
"""

import ast
from typing import TYPE_CHECKING, Sequence, Tuple, Type, Union

from typing_extensions import Protocol

if TYPE_CHECKING:  # pragma: no cover
    # This solves cycle imports problem:
    from .visitors.base import visitor  # noqa: Z100,Z101,F401

#: Visitors container, that has all enable visitors' classes:
VisitorSequence = Sequence[Type['visitor.BaseNodeVisitor']]

#: In cases we need to work with both import types:
AnyImport = Union[ast.Import, ast.ImportFrom]

#: Flake8 API format to return error messages:
CheckResult = Tuple[int, int, str, type]

#: Code members that we count in a module:
ModuleMembers = Union[ast.FunctionDef, ast.ClassDef]


class ConfigurationOptions(Protocol):
    """
    This class provides structure for the options we use in our checker.

    It uses structural subtyping, and does not represent any kind of a real
    class or structure.

    See: https://mypy.readthedocs.io/en/latest/protocols.html
    """

    max_arguments: int
    max_local_variables: int
    max_returns: int
    max_expressions: int
    min_variable_length: int
    max_offset_blocks: int
    max_elifs: int
    max_module_members: int
    max_methods: int
