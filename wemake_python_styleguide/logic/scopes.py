# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, Set, cast

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import AssignNodes, FunctionNodes
from wemake_python_styleguide.logic.naming import access, name_nodes
from wemake_python_styleguide.logic.nodes import get_context
from wemake_python_styleguide.logic.source import node_to_string
from wemake_python_styleguide.types import ContextNodes

#: That's how we represent scopes that are bound to contexts.
_ContextStore = DefaultDict[ContextNodes, Set[str]]

#: That's what we expect from `@overload` decorator:
_overload_exceptions = frozenset(('overload', 'typing.overload'))


class _BaseScope(object):
    """Base class for scope operations."""

    @final
    def __init__(self, node: ast.AST) -> None:
        """Saving current node and context."""
        self._node = node
        self._context = cast(ContextNodes, get_context(self._node))

    def add_to_scope(self, names: Set[str]) -> None:  # pragma: no cover
        """Adds a given set of names to some scope."""
        raise NotImplementedError()

    def shadowing(self, names: Set[str]) -> Set[str]:  # pragma: no cover
        """Tells either some shadowing exist between existing scopes."""
        raise NotImplementedError()

    @final
    def _exclude_unused(self, names: Set[str]) -> Set[str]:
        """Removes unused variables from set of names."""
        return {
            var_name  # we allow to reuse explicit `_` variables
            for var_name in names
            if not access.is_unused(var_name)
        }


@final
class BlockScope(_BaseScope):
    """Represents the visibility scope of a variable in a block."""

    #: Updated when we have a new block variable.
    _block_scopes: ClassVar[_ContextStore] = defaultdict(set)

    #: Updated when we have a new local variable.
    _local_scopes: ClassVar[_ContextStore] = defaultdict(set)

    def add_to_scope(
        self,
        names: Set[str],
        *,
        is_local: bool = False,
    ) -> None:
        """Adds a set of names to the specified scope."""
        scope = self._get_scope(is_local=is_local)
        scope[self._context] = scope[self._context].union(
            self._exclude_unused(names),
        )

    def shadowing(
        self,
        names: Set[str],
        *,
        is_local: bool = False,
    ) -> Set[str]:
        """Calculates the intersection for a set of names and a context."""
        if not names:
            return set()

        scope = self._get_scope(is_local=not is_local)
        current_names = scope[self._context]

        if not is_local:
            # Why do we care to update the scope for block variables?
            # Because, block variables cannot shadow each other.
            scope = self._get_scope(is_local=is_local)
            current_names = current_names.union(scope[self._context])

        return set(current_names).intersection(names)

    def _get_scope(self, *, is_local: bool = False) -> _ContextStore:
        return self._local_scopes if is_local else self._block_scopes


@final
class OuterScope(_BaseScope):
    """Represents scoping store to check name shadowing."""

    _scopes: ClassVar[_ContextStore] = defaultdict(set)

    def add_to_scope(self, names: Set[str]) -> None:
        """Adds a set of variables to the context scope."""
        if isinstance(self._context, ast.ClassDef):
            # Class names are not available to the caller directly.
            return

        self._scopes[self._context] = self._scopes[self._context].union(
            self._exclude_unused(names),
        )

    def shadowing(self, names: Set[str]) -> Set[str]:
        """Calculates the intersection for a set of names and a context."""
        if isinstance(self._context, ast.ClassDef):
            # Class names are not available to the caller directly.
            return set()

        current_names = self._build_outer_context()
        return set(current_names).intersection(names)

    def _build_outer_context(self) -> Set[str]:
        outer_names: Set[str] = set()
        context = self._context

        while True:
            context = cast(ContextNodes, get_context(context))
            outer_names = outer_names.union(self._scopes[context])
            if not context:
                break

        return outer_names


def extract_names(node: ast.AST) -> Set[str]:
    """Extracts unique set of names from a given node."""
    return set(name_nodes.get_variables_from_node(node))


def is_function_overload(node: ast.AST) -> bool:
    """Check that function decorated with `typing.overload`."""
    if isinstance(node, FunctionNodes):
        for decorator in node.decorator_list:
            if node_to_string(decorator) in _overload_exceptions:
                return True
    return False


def is_same_value_reuse(node: ast.AST, names: Set[str]) -> bool:
    """Checks if the given names are reused by the given node."""
    if isinstance(node, AssignNodes) and node.value:
        used_names = {
            name_node.id
            for name_node in ast.walk(node.value)
            if isinstance(name_node, ast.Name)
        }
        if not names.difference(used_names):
            return True
    return False
