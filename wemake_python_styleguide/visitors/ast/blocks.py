import ast
from collections import defaultdict
from typing import TypeAlias, cast, final

from wemake_python_styleguide.compat.aliases import ForNodes, WithNodes
from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.naming import name_nodes
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.types import (
    AnyFor,
    AnyWith,
)
from wemake_python_styleguide.violations.best_practices import (
    ControlVarUsedAfterBlockViolation,
)
from wemake_python_styleguide.visitors import base, decorators

#: That's how we represent contexts for control variables.
_BlockVariables: TypeAlias = defaultdict[
    ast.AST,
    defaultdict[str, list[ast.AST]],
]


@final
@decorators.alias(
    'visit_any_for',
    (
        'visit_For',
        'visit_AsyncFor',
    ),
)
class AfterBlockVariablesVisitor(base.BaseNodeVisitor):
    """Visitor that ensures that block variables are not used after block."""

    def __init__(self, *args, **kwargs) -> None:
        """We need to store complex data about variable usages."""
        super().__init__(*args, **kwargs)
        self._block_variables: _BlockVariables = defaultdict(
            lambda: defaultdict(list),
        )

    # Blocks:

    def visit_any_for(self, node: AnyFor) -> None:
        """Visit loops."""
        self._add_to_scope(
            node,
            set(name_nodes.get_variables_from_node(node.target)),
        )
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        """Visits ``with`` and ``async with`` declarations."""
        if node.optional_vars:
            self._add_to_scope(
                cast(AnyWith, get_parent(node)),
                set(name_nodes.get_variables_from_node(node.optional_vars)),
            )
        self.generic_visit(node)

    # Variable usages:

    def visit_Name(self, node: ast.Name) -> None:
        """Check variable usages."""
        if isinstance(node.ctx, ast.Load):
            self._check_variable_usage(node)
        self.generic_visit(node)

    # Utils:

    def _add_to_scope(self, node: ast.AST, names: set[str]) -> None:
        context = cast(ast.AST, get_context(node))
        for var_name in names:
            self._block_variables[context][var_name].append(node)

    def _check_variable_usage(self, node: ast.Name) -> None:
        if walk.get_closest_parent(node, ast.Assert):
            return  # Allow any names to be used in `assert` statements

        context = cast(ast.AST, get_context(node))
        blocks = self._block_variables[context][node.id]
        is_contained_block_var = any(
            walk.is_contained_by(node, block) for block in blocks
        )
        # Restrict the use of block variables with the same name to
        # the same type of block - either `for` or `with`.
        is_same_type_block = all(
            isinstance(block, ForNodes) for block in blocks
        ) or all(isinstance(block, WithNodes) for block in blocks)
        # Return if not a block variable or a contained block variable.
        if not blocks or (is_contained_block_var and is_same_type_block):
            return

        self.add_violation(
            ControlVarUsedAfterBlockViolation(node, text=node.id),
        )
