import ast

from wemake_python_styleguide.compat.functions import get_slice_expr
from wemake_python_styleguide.logic import source


def is_same_slice(
    iterable: str,
    target: str,
    node: ast.Subscript,
) -> bool:
    """Used to tell when slice is identical to some pair of name/index."""
    return (
        source.node_to_string(node.value) == iterable and
        source.node_to_string(get_slice_expr(node)) == target
    )
