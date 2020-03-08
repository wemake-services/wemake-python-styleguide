import ast
from typing import List, Union

from wemake_python_styleguide.compat.nodes import NamedExpr
from wemake_python_styleguide.compat.types import AnyAssignWithWalrus
from wemake_python_styleguide.types import AnyFunctionDefAndLambda


def get_assign_targets(
    node: Union[AnyAssignWithWalrus, ast.AugAssign],
) -> List[ast.expr]:
    """Returns list of assign targets without knowing the type of assign."""
    if isinstance(node, (ast.AnnAssign, ast.AugAssign, NamedExpr)):
        return [node.target]
    return node.targets


def get_posonlyargs(node: AnyFunctionDefAndLambda) -> List[ast.arg]:
    """
    Helper function to get posonlyargs in all version of python.

    This field was added in ``python3.8+``. And it was not present before.

    mypy also gives an error on this on older version of python::

        error: "arguments" has no attribute "posonlyargs"; maybe "kwonlyargs"?

    """
    return getattr(node.args, 'posonlyargs', [])
