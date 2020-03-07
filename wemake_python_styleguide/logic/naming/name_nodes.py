import ast
import itertools
from typing import Iterable, List, Optional

from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.compat.types import AnyAssignWithWalrus


def is_same_variable(left: ast.AST, right: ast.AST) -> bool:
    """Ensures that nodes are the same variable."""
    if isinstance(left, ast.Name) and isinstance(right, ast.Name):
        return left.id == right.id
    return False


def get_assigned_name(node: ast.AST) -> Optional[str]:
    """
    Returns variable names for node that is just assigned.

    Returns ``None`` for nodes that are used in a different manner.
    """
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
        return node.id

    if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
        return node.attr

    if isinstance(node, ast.ExceptHandler):
        return node.name

    return None


def flat_variable_names(nodes: Iterable[AnyAssignWithWalrus]) -> Iterable[str]:
    """
    Returns flat variable names from several nodes.

    Use this function when you need to get list of string variable names
    from assign nodes.

    Here's an example:

    >>> import ast
    >>> tree = ast.parse('x: int = 0')
    >>> node = tree.body[0]
    >>> list(flat_variable_names([node]))
    ['x']

    >>> tree = ast.parse('z = y = 0')
    >>> node = tree.body[0]
    >>> list(flat_variable_names([node]))
    ['z', 'y']

    """
    return itertools.chain.from_iterable((
        get_variables_from_node(target)
        for node in nodes
        for target in get_assign_targets(node)
    ))


def get_variables_from_node(node: ast.AST) -> List[str]:
    """
    Gets the assigned names from the list of nodes.

    Can be used with any nodes that operate with ``ast.Name`` or ``ast.Tuple``
    as targets for the assignment.

    Can be used with nodes like ``ast.Assign``, ``ast.Tuple``, ``ast.For``,
    ``ast.With``, etc.
    """
    names: List[str] = []
    naive_attempt = extract_name(node)

    if naive_attempt:
        names.append(naive_attempt)
    elif isinstance(node, ast.Tuple):
        for subnode in node.elts:
            extracted_name = get_variables_from_node(subnode)
            if extracted_name:
                names.extend(extracted_name)
    return names


def extract_name(node: ast.AST) -> Optional[str]:
    """
    Utility to extract names for several types of nodes.

    Is used to get name from node in case it is ``ast.Name``.

    Should not be used direclty with assigns,
    use safer :py:`~get_assign_names` function.

    Example:
    >>> import ast
    >>> tree = ast.parse('a')
    >>> node = tree.body[0].value
    >>> extract_name(node)
    'a'

    """
    if isinstance(node, ast.Starred):
        node = node.value
    if isinstance(node, ast.Name):
        return node.id
    return None
