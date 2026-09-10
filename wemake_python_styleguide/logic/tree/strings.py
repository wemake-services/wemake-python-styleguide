import ast

from wemake_python_styleguide.compat import nodes
from wemake_python_styleguide.logic.nodes import get_context, get_parent
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


def is_doc_string_value(node: ast.AST) -> bool:
    """
    Tells whether or not the given node is a docstring's own constant.

    While :func:`is_doc_string` works with statements,
    this one works with the string constant inside of them.
    """
    statement = get_parent(node)
    if statement is None or not is_doc_string(statement):
        return False
    context = get_context(statement)
    return context is not None and context.body[0] is statement


def has_format_string_conversion(component: ast.AST) -> bool:
    """Checks whether formatted string component has a conversion specifier."""
    formatted_component = (
        get_closest_parent(component, (ast.FormattedValue, nodes.Interpolation))
        or component
    )
    return (
        isinstance(
            formatted_component,
            (ast.FormattedValue, nodes.Interpolation),
        )
        and formatted_component.conversion != -1
    )
