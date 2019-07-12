# -*- coding: utf-8 -*-

from typing import List

from wemake_python_styleguide.types import AnyImport


def get_import_parts(node: AnyImport) -> List[str]:
    """Returns list of import modules."""
    module_path = getattr(node, 'module', '') or ''
    return module_path.split('.')
