# -*- coding: utf-8 -*-

from cognitive_complexity.api import get_cognitive_complexity

from wemake_python_styleguide.types import AnyFunctionDef


def cognitive_score(node: AnyFunctionDef) -> int:
    """
    A thin wrapper around 3rd party dependency.

    We only need to be sure that our visitors API does not directly
    related to some 3rd party code.
    """
    return get_cognitive_complexity(node)
