"""
Counts annotation complexity by getting the nesting level of nodes.

So ``List[int]`` complexity is 2
and ``Tuple[List[Optional[str]], int]`` is 4.

Adapted from: https://github.com/best-doctor/flake8-annotations-complexity
"""

import ast
from typing import TypeAlias

_Annotation: TypeAlias = ast.expr | ast.Constant


def get_annotation_complexity(annotation_node: _Annotation) -> int:
    """
    Recursively counts complexity of annotation nodes.

    When annotations are written as strings,
    we additionally parse them to ``ast`` nodes.
    """
    if isinstance(annotation_node, ast.Constant) and isinstance(
        annotation_node.value,
        str,
    ):
        # try to parse string-wrapped annotations
        try:
            annotation_node = (
                ast.parse(  # type: ignore
                    annotation_node.value,
                )
                .body[0]
                .value
            )
        except Exception:
            return 1

    if isinstance(annotation_node, ast.Subscript):
        return 1 + get_annotation_complexity(annotation_node.slice)
    if isinstance(annotation_node, ast.Tuple | ast.List):
        return max(
            (get_annotation_complexity(node) for node in annotation_node.elts),
            default=1,
        )
    return 1
