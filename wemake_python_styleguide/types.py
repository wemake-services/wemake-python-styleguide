# -*- coding: utf-8 -*-

"""
This module contains custom `mypy` types that we commonly use.

General rule is: if there's a complex type, put it here.
"""

import ast
from typing import Tuple, Union

from typing_extensions import Protocol

#: In cases we need to work with both import types:
AnyImport = Union[ast.Import, ast.ImportFrom]

#: Flake8 API format to return error messages:
CheckResult = Tuple[int, int, str, type]


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
