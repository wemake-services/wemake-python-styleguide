import ast
from typing import Final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import ContextNodes

_CONTEXTS: Final = (
    ast.Module,
    ast.ClassDef,
    *FunctionNodes,
)


def set_node_context(tree: ast.AST) -> ast.AST:
    """
    Used to set proper context to all nodes.

    What we call "a context"?
    Context is where exactly this node belongs on a global level.

    Example:
    .. code:: python

        if some_value > 2:
            test = 'passed'

    Despite the fact ``test`` variable has ``Assign`` as it parent
    it will have ``Module`` as a context.

    What contexts do we respect?

    - :py:class:`ast.Module`
    - :py:class:`ast.ClassDef`
    - :py:class:`ast.FunctionDef` and :py:class:`ast.AsyncFunctionDef`

    .. versionchanged:: 0.8.1

    """
    for statement in ast.walk(tree):
        current_context = _find_context(statement, _CONTEXTS)
        setattr(statement, 'wps_context', current_context)  # noqa: B010
    return tree


def _find_context(
    node: ast.AST,
    contexts: tuple[type[ContextNodes], ...],
) -> ast.AST | None:
    """
    We changed how we find and assign contexts in 0.8.1 version.

    It happened because of the bug #520
    See: https://github.com/wemake-services/wemake-python-styleguide/issues/520
    """
    parent = get_parent(node)
    if parent is None:
        return None
    if isinstance(parent, contexts):
        return parent
    return _find_context(parent, contexts)
