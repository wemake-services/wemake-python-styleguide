# -*- coding: utf-8 -*-

import ast
from typing import List

from wemake_python_styleguide.types import AnyAssign


def get_assign_targets(node: AnyAssign) -> List[ast.expr]:
    """Returns list of assign targets without knowing the type of assign."""
    if isinstance(node, ast.AnnAssign):
        return [node.target]
    return node.targets
