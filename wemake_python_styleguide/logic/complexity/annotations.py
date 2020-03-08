"""
Counts annotation complexity by getting the nesting level of nodes.

So ``List[int]`` complexity is 2
and ``Tuple[List[Optional[str]], int]`` is 4.

Adapted from: https://github.com/best-doctor/flake8-annotations-complexity
"""

import ast
from typing import Union

_Annotation = Union[
    ast.expr,
    ast.Str,
]


def get_annotation_compexity(annotation_node: _Annotation) -> int:
    """
    Recursevly counts complexity of annotation nodes.

    When annotations are written as strings,
    we additionally parse them to ``ast`` nodes.
    """
    if isinstance(annotation_node, ast.Str):
        try:
            annotation_node = ast.parse(  # type: ignore
                annotation_node.s,
            ).body[0].value
        except SyntaxError:
            return 1

    if isinstance(annotation_node, ast.Subscript):
        return 1 + get_annotation_compexity(
            annotation_node.slice.value,  # type: ignore
        )
    elif isinstance(annotation_node, (ast.Tuple, ast.List)):
        return max(
            (get_annotation_compexity(node) for node in annotation_node.elts),
            default=1,
        )
    return 1
