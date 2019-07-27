# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, Set, Union, cast

from typing_extensions import final

from wemake_python_styleguide.logic.naming.name_nodes import (
    flat_variable_names,
    get_variables_from_node,
)
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.types import (
    AnyAssign,
    AnyFor,
    AnyFunctionDef,
    ContextNodes,
)
from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors import base, decorators

#: That's how we represent scopes that are bound to contexts.
_ContextStore = DefaultDict[ContextNodes, Set[str]]


@final
@decorators.alias('visit_named_nodes', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
    'visit_ClassDef',
    'visit_ExceptHandler',
))
@decorators.alias('visit_any_for', (
    'visit_For',
    'visit_AsyncFor',
))
@decorators.alias('visit_locals', (
    'visit_Assign',
    'visit_AnnAssign',
    'visit_arg',
))
class BlockVariableVisitor(base.BaseNodeVisitor):
    """
    This visitor is used to detect variables that are reused for blocks.

    Check out this example:

    .. code::

      exc = 7
      try:
          ...
      except Exception as exc:  # reusing existing variable
          ...

    Please, do not modify. This is fragile and complex.

    """

    def visit_named_nodes(self, node: AnyFunctionDef) -> None:
        """
        Visits block nodes that have ``.name`` property.

        Raises:
            BlockAndLocalOverlapViolation

        """
        names = {node.name} if node.name else set()
        self._scope(node, names, is_local=False)
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """
        Collects block nodes from loop definitions.

        Raises:
            BlockAndLocalOverlapViolation

        """
        self._scope(node, _extract_names(node.target), is_local=False)
        self.generic_visit(node)

    def visit_alias(self, node: ast.alias) -> None:
        """
        Visits aliases from ``import`` and ``from ... import`` block nodes.

        Raises:
            BlockAndLocalOverlapViolation

        """
        import_name = node.asname if node.asname else node.name
        self._scope(
            cast(ast.AST, get_parent(node)),
            {import_name},
            is_local=False,
        )
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        """
        Visits ``with`` and ``async with`` declarations.

        Raises:
            BlockAndLocalOverlapViolation

        """
        if node.optional_vars:
            self._scope(
                cast(ast.AST, get_parent(node)),
                _extract_names(node.optional_vars),
                is_local=False,
            )
        self.generic_visit(node)

    def visit_locals(self, node: Union[AnyAssign, ast.arg]) -> None:
        """
        Visits local variable definitions and function arguments.

        Raises:
            BlockAndLocalOverlapViolation

        """
        if isinstance(node, ast.arg):
            names = {node.arg}
        else:
            names = set(flat_variable_names([node]))

        self._scope(node, names, is_local=True)
        self.generic_visit(node)

    def _scope(
        self,
        node: ast.AST,
        names: Set[str],
        *,
        is_local: bool,
    ) -> None:
        scope = _Scope(node)
        shadow = scope.shadowing(names, is_local=is_local)

        if shadow:
            self.add_violation(
                BlockAndLocalOverlapViolation(node, text=', '.join(shadow)),
            )

        scope.add_to_scope(names, is_local=is_local)


class _Scope(object):
    """Represents the visibility scope of the variable."""

    #: Updated when we have a new block variable.
    _block_scopes: ClassVar[_ContextStore] = defaultdict(set)

    #: Updated when we have a new local variables.
    _local_scopes: ClassVar[_ContextStore] = defaultdict(set)

    def __init__(self, node: ast.AST) -> None:
        self._node = node
        self._context = cast(ContextNodes, get_context(self._node))

    def add_to_scope(
        self,
        names: Set[str],
        is_local: bool = False,
    ) -> None:
        """Adds a set of names to the specified scope."""
        scope = self._get_scope(is_local=is_local)
        scope[self._context] = scope[self._context].union(names)

    def shadowing(
        self,
        names: Set[str],
        is_local: bool = False,
    ) -> Set[str]:
        """Calculates the intersection for a set of names and a context."""
        if not names:
            return set()

        scope = self._get_scope(is_local=not is_local)
        current_names = scope[self._context]

        if not is_local:
            # Why do we care to update the scope for block variables?
            # Because, block variables cannot shadow
            scope = self._get_scope(is_local=is_local)
            current_names = current_names.union(scope[self._context])

        return set(current_names).intersection(names)

    def _get_scope(self, is_local: bool = False) -> _ContextStore:
        return self._local_scopes if is_local else self._block_scopes


def _extract_names(node: ast.AST) -> Set[str]:
    return set(get_variables_from_node(node))
