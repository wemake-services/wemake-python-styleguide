import ast
from typing import List, Tuple, Union

from wemake_python_styleguide.compat.types import NodeWithTypeParams
from wemake_python_styleguide.types import AnyAssignWithWalrus


def get_assign_targets(
    node: Union[AnyAssignWithWalrus, ast.AugAssign],
) -> List[ast.expr]:
    """Returns list of assign targets without knowing the type of assign."""
    if isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
        return [node.target]
    return node.targets


def get_type_param_names(  # pragma: py-lt-312
    node: NodeWithTypeParams,
) -> List[Tuple[ast.AST, str]]:
    """Return list of type parameters' names."""
    type_params = []
    for type_param_node in getattr(node, 'type_params', []):
        type_param_name = type_param_node.name
        type_params.append((type_param_node, type_param_name))
    return type_params
