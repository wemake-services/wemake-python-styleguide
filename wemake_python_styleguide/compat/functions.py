import ast
from typing import List, Union

from wemake_python_styleguide.compat.types import AnyAssignWithWalrus


def get_assign_targets(
    node: Union[AnyAssignWithWalrus, ast.AugAssign],
) -> List[ast.expr]:
    """Returns list of assign targets without knowing the type of assign."""
    if isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
        return [node.target]
    return node.targets


def get_slice_expr(node: ast.Subscript) -> ast.expr:
    """
    Get slice expression from the subscript in all versions of python.

    It was changed in ``python3.9``.

    Before: ``ast.Subscript`` -> ``ast.Index`` -> ``ast.expr``
    After: ``ast.Subscript`` -> ``ast.expr``
    """
    return (
        node.slice.value  # type: ignore
        if isinstance(node.slice, ast.Index)
        else node.slice
    )
