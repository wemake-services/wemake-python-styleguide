"""
Counts annotation complexity by getting the nesting level of nodes.

So ``List[int]`` complexity is 2
and ``Tuple[List[Optional[str]], int]`` is 4.

Adapted from: https://github.com/best-doctor/flake8-annotations-complexity
"""

import ast
from collections.abc import Container
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


def check_is_node_in_specific_annotation(
    node: ast.AST | None,
    annotation_name: str,
    annotation_modules: Container[str],
) -> bool:
    """
    Check is node inside specific annotation.

    Checks is ast node in annotation with name `annotation_name`
    and is annotation module in `annotation_modules`.
    """
    if isinstance(node, ast.Subscript):
        if (
            isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id in annotation_modules
            and node.value.attr == annotation_name
        ):
            return True
        if (
            isinstance(node.value, ast.Name)
            and node.value.id in annotation_name
        ):
            return True
    return False
