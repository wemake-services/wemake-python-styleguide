# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.types import AnyImport


def get_error_text(node: AnyImport) -> str:
    """Returns correct error text for import nodes."""
    module = getattr(node, 'module', None)
    if module is not None:
        return module

    if isinstance(node, ast.Import):
        return node.names[0].name
    return '.'


def get_input_parts(node: ast.ImportFrom):
    """Returns list of import module"""
    module_path = getattr(node, 'module', '')
    return module_path.split('.')
