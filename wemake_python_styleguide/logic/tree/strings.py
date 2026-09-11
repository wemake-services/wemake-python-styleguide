import ast
import itertools
from typing import Final

from wemake_python_styleguide.compat import nodes
from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.logic.walk import get_closest_parent

#: Nodes that a docstring can document by being placed right after them.
_DocumentedNodes: Final = (*AssignNodes, nodes.TypeAlias)


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

    Attribute docstrings count as well: PEP 258 documents
    an assignment with a string placed right after it.
    Type aliases are documented the same way, see
    https://discuss.python.org/t/docstrings-for-type-aliases/108901
    """
    statement = get_parent(node)
    if statement is None or not is_doc_string(statement):
        return False
    context = get_context(statement)
    return context is not None and _is_doc_string_place(
        context.body,
        statement,
    )


def _is_doc_string_place(
    body: list[ast.stmt],
    statement: ast.AST,
) -> bool:
    """Docstrings open a definition's body or follow what they document."""
    if body[0] is statement:
        return True
    return any(
        current is statement and isinstance(previous, _DocumentedNodes)
        for previous, current in itertools.pairwise(body)
    )


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
