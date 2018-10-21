# -*- coding: utf-8 -*-

import ast
from typing import List

from wemake_python_styleguide.types import AnyImport


def get_error_text(node: AnyImport) -> str:
    """Returns correct error text for import nodes."""
    module = getattr(node, 'module', None)
    if module is not None:
        return module

    if isinstance(node, ast.Import):
        return node.names[0].name
    return '.'


def get_import_parts(node: AnyImport) -> List[str]:
    """Returns list of import modules."""
    module_path = getattr(node, 'module', '') or ''
    return module_path.split('.')
