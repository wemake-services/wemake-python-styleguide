import ast
import itertools
from typing import Final

from wemake_python_styleguide.compat import nodes
from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.logic.walk import get_closest_parent
from wemake_python_styleguide.types import ContextNodes

#: Targets that define an attribute a docstring can document.
_AttributeTargets: Final = (ast.Name, ast.Attribute)


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
    an attribute with a string placed right after it.
    Type aliases are documented the same way, see
    https://discuss.python.org/t/docstrings-for-type-aliases/108901
    """
    statement = get_parent(node)
    if statement is None or not is_doc_string(statement):
        return False
    context = get_context(statement)
    return context is not None and _is_doc_string_place(context, statement)


def _is_doc_string_place(
    context: ContextNodes,
    statement: ast.AST,
) -> bool:
    """Docstrings open a definition's body or follow what they document."""
    if context.body[0] is statement:
        return True
    return any(
        current is statement and _is_documented(previous, context)
        for previous, current in itertools.pairwise(context.body)
    )


def _is_documented(statement: ast.stmt, context: ContextNodes) -> bool:
    """Only type aliases and single attribute definitions are documented."""
    if not isinstance(statement, AssignNodes):
        return isinstance(statement, nodes.TypeAlias)  # `type X = int`
    targets = get_assign_targets(statement)
    if len(targets) != 1:  # `x = y = 1` defines no single attribute
        return False
    if isinstance(context, FunctionNodes):
        # Locals are not attributes, only `self.some = 1` is one.
        return isinstance(targets[0], ast.Attribute)
    return isinstance(targets[0], _AttributeTargets)


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
