import ast

from wemake_python_styleguide.compat.aliases import ForNodes
from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.types import AnyLoop


def _is_nested_loop(node: AnyLoop, sub: ast.AST) -> bool:
    return isinstance(sub, (*ForNodes, ast.While)) and sub is not node


def has_break(node: AnyLoop) -> bool:
    """Tells whether or not given loop has ``break`` keyword in its body."""
    closest_loop = None

    for sub in ast.walk(node):
        if _is_nested_loop(node, sub):
            closest_loop = sub

        if isinstance(sub, ast.Break):
            if not closest_loop or not walk.is_contained_by(sub, closest_loop):
                return True
    return False
