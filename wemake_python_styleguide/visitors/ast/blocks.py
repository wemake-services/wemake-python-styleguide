# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import (
    Callable,
    ClassVar,
    DefaultDict,
    List,
    Set,
    Tuple,
    Union,
    cast,
)

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import ForNodes, WithNodes
from wemake_python_styleguide.logic.naming.name_nodes import (
    flat_variable_names,
)
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.logic.scope_predicates import (
    is_function_overload,
    is_no_value_annotation,
    is_property_setter,
    is_same_value_reuse,
)
from wemake_python_styleguide.logic.scopes import (
    BlockScope,
    OuterScope,
    extract_names,
)
from wemake_python_styleguide.logic.walk import is_contained_by
from wemake_python_styleguide.types import (
    AnyAssign,
    AnyFor,
    AnyFunctionDef,
    AnyImport,
    AnyNodes,
    AnyWith,
)
from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
    ControlVarUsedAfterBlockViolation,
    OuterScopeShadowingViolation,
)
from wemake_python_styleguide.visitors import base, decorators

#: That's how we represent contexts for control variables.
_BlockVariables = DefaultDict[
    ast.AST,
    DefaultDict[str, List[ast.AST]],
]

#: That's how we filter some overlaps that do happen in Python:
_ScopePredicate = Callable[[ast.AST, Set[str]], bool]
_NamePredicate = Callable[[ast.AST], bool]


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

    _naming_predicates: Tuple[_NamePredicate, ...] = (
        is_function_overload,
        is_property_setter,
        is_no_value_annotation,
    )

    _scope_predicates: Tuple[_ScopePredicate, ...] = (
        is_same_value_reuse,
        is_property_setter,
    )

    # Blocks:

    def visit_named_nodes(self, node: AnyFunctionDef) -> None:
        """
        Visits block nodes that have ``.name`` property.

        Raises:
            BlockAndLocalOverlapViolation

        """
        names = {node.name} if node.name else set()
        self._scope(node, names, is_local=False)
        self._outer_scope(node, names)
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """
        Collects block nodes from loop definitions.

        Raises:
            BlockAndLocalOverlapViolation

        """
        names = extract_names(node.target)
        self._scope(node, names, is_local=False)
        self._outer_scope(node, names)
        self.generic_visit(node)

    def visit_alias(self, node: ast.alias) -> None:
        """
        Visits aliases from ``import`` and ``from ... import`` block nodes.

        Raises:
            BlockAndLocalOverlapViolation

        """
        parent = cast(AnyImport, get_parent(node))
        import_name = {node.asname} if node.asname else {node.name}
        self._scope(parent, import_name, is_local=False)
        self._outer_scope(parent, import_name)
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        """
        Visits ``with`` and ``async with`` declarations.

        Raises:
            BlockAndLocalOverlapViolation

        """
        if node.optional_vars:
            parent = cast(AnyWith, get_parent(node))
            names = extract_names(node.optional_vars)
            self._scope(parent, names, is_local=False)
            self._outer_scope(parent, names)
        self.generic_visit(node)

    # Locals:

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
        self._outer_scope(node, names)
        self.generic_visit(node)

    # Utils:

    def _scope(
        self,
        node: ast.AST,
        names: Set[str],
        *,
        is_local: bool,
    ) -> None:
        scope = BlockScope(node)
        shadow = scope.shadowing(names, is_local=is_local)

        ignored_scope = any(
            predicate(node, names)
            for predicate in self._scope_predicates
        )
        ignored_name = any(
            predicate(node)
            for predicate in self._naming_predicates
        )

        if shadow and not ignored_scope:
            self.add_violation(
                BlockAndLocalOverlapViolation(node, text=', '.join(shadow)),
            )

        if not ignored_name:
            scope.add_to_scope(names, is_local=is_local)

    def _outer_scope(self, node: ast.AST, names: Set[str]) -> None:
        scope = OuterScope(node)
        shadow = scope.shadowing(names)

        if shadow:
            self.add_violation(
                OuterScopeShadowingViolation(node, text=', '.join(shadow)),
            )

        scope.add_to_scope(names)


@final
@decorators.alias('visit_any_for', (
    'visit_For',
    'visit_AsyncFor',
))
class AfterBlockVariablesVisitor(base.BaseNodeVisitor):
    """Visitor that ensures that block variables are not used after block."""

    _block_nodes: ClassVar[AnyNodes] = (
        ast.ExceptHandler,
        *ForNodes,
        *WithNodes,
    )

    def __init__(self, *args, **kwargs) -> None:
        """We need to store complex data about variable usages."""
        super().__init__(*args, **kwargs)
        self._block_variables: _BlockVariables = defaultdict(
            lambda: defaultdict(list),
        )

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Visit exception names definition."""
        if node.name:
            self._add_to_scope(node, {node.name})
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """Visit loops."""
        self._add_to_scope(node, extract_names(node.target))
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        """Visits ``with`` and ``async with`` declarations."""
        if node.optional_vars:
            self._add_to_scope(
                cast(AnyWith, get_parent(node)),
                extract_names(node.optional_vars),
            )
        self.generic_visit(node)

    # Variable usages:

    def visit_Name(self, node: ast.Name) -> None:
        """
        Check variable usages.

        Raises:
            ControlVarUsedAfterBlockViolation

        """
        if isinstance(node.ctx, ast.Load):
            self._check_variable_usage(node)
        self.generic_visit(node)

    # Utils:

    def _add_to_scope(self, node: ast.AST, names: Set[str]) -> None:
        context = cast(ast.AST, get_context(node))
        for var_name in names:
            self._block_variables[context][var_name].append(node)

    def _check_variable_usage(self, node: ast.Name) -> None:
        context = cast(ast.AST, get_context(node))
        blocks = self._block_variables[context][node.id]
        if all(is_contained_by(node, block) for block in blocks):
            return

        self.add_violation(
            ControlVarUsedAfterBlockViolation(node, text=node.id),
        )
