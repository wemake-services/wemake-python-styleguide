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
