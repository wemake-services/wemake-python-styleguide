# -*- coding: utf-8 -*-

import ast
from typing import Optional


def get_exception_name(node: ast.Raise) -> Optional[str]:
    """Returns the exception name or ``None`` if node has not it."""
    exception = node.exc
    if exception is None:
        return None

    exception_func = getattr(exception, 'func', None)
    if exception_func:
        exception = exception_func

    return getattr(exception, 'id', None)
