import ast

from typing_extensions import Final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import walk

#: Nodes that can be directly annotated.
_AnnNodes: Final = (ast.AnnAssign, ast.arg)

#: Nodes that can be a part of an annotation.
_AnnParts: Final = (
    ast.Name,
    ast.Attribute,
    ast.Str,
    ast.List,
    ast.Tuple,
    ast.Subscript,
    ast.BinOp,  # new styled unions, like: `str | int`
)


def is_annotation(node: ast.AST) -> bool:
    """
    Detects if node is an annotation. Or a part of it.

    We use this predicate to allow all types of repetetive
    function and instance annotations.
    """
    if not isinstance(node, _AnnParts):
        return False

    annotated = walk.get_closest_parent(node, (*_AnnNodes, *FunctionNodes))
    if isinstance(annotated, FunctionNodes):
        contains_node = bool(
            annotated.returns and
            walk.is_contained_by(node, annotated.returns),
        )
        return node == annotated.returns or contains_node
    elif isinstance(annotated, _AnnNodes):
        contains_node = bool(
            annotated.annotation and
            walk.is_contained_by(node, annotated.annotation),
        )
        return node == annotated.annotation or contains_node
    return False
