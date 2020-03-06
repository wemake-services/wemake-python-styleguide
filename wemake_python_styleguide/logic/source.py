import ast

import astor

from wemake_python_styleguide.types import AnyTextPrimitive


def node_to_string(node: ast.AST) -> str:
    """Returns the source code by doing ``ast`` to string convert."""
    return astor.to_source(node).strip()


def render_string(text_data: AnyTextPrimitive) -> str:
    """
    Method to render ``Str``, ``Bytes``, and f-string nodes to ``str``.

    Keep in mind, that bytes with wrong chars will be rendered incorrectly
    But, this is not important for the business logic.

    """
    if isinstance(text_data, bytes):
        # See https://docs.python.org/3/howto/unicode.html
        return text_data.decode('utf-8', errors='surrogateescape')
    return text_data  # it is a `str`
