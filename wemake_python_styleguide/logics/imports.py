# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import PROTECTED_MODULE_PATTERN
from wemake_python_styleguide.types import AnyImport


def get_error_text(node: AnyImport) -> str:
    """Returns correct error text for import nodes."""
    module = getattr(node, 'module', None)
    if module is not None:
        return module

    if isinstance(node, ast.Import):
        return node.names[0].name
    return '.'


def is_contain_protected_module(module_name: str) -> bool:
    """Returns whether the module contains protected module."""
    return PROTECTED_MODULE_PATTERN.match(module_name) is not None
