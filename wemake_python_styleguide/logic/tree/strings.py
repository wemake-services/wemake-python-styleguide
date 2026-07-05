import ast

from wemake_python_styleguide.compat import nodes
from wemake_python_styleguide.logic.walk import get_closest_parent


def is_doc_string(node: ast.AST) -> bool:
    """
    Tells whether or not the given node is a docstring.

    We call docstrings any string nodes that are placed right after
    function, class, or module definition.
    """
    if not isinstance(node, ast.Expr):
        return False
    return isinstance(node.value, ast.Constant) and isinstance(
        node.value.value,
        str,
    )


def has_fstring_conversion(component: ast.AST) -> bool:
    """Checks whether f/t-string with the component has a conversion specifier."""
    formatted_component = (
        get_closest_parent(component, (ast.FormattedValue, nodes.Interpolation))
        or component
    )
    return (
        isinstance(
            formatted_component, (ast.FormattedValue, nodes.Interpolation)
        )
        and formatted_component.conversion != -1
    )
