import ast
from collections.abc import Iterable
from typing import cast, final

from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.constants import (
    UNUSED_PLACEHOLDER,
)
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming import access, blacklists, name_nodes
from wemake_python_styleguide.logic.tree import pattern_matching
from wemake_python_styleguide.types import (
    AnyAssign,
    AnyAssignWithWalrus,
    AnyFor,
)
from wemake_python_styleguide.violations import best_practices, naming
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias(
    'visit_any_assign',
    (
        'visit_Assign',
        'visit_AnnAssign',
    ),
)
class WrongModuleMetadataVisitor(BaseNodeVisitor):
    """Finds wrong metadata information of a module."""

    def visit_any_assign(self, node: AnyAssign) -> None:
        """Used to find the bad metadata variable names."""
        self._check_metadata(node)
        self.generic_visit(node)

    def _check_metadata(self, node: AnyAssign) -> None:
        if not isinstance(nodes.get_parent(node), ast.Module):
            return

        targets = get_assign_targets(node)
        for target_node in targets:
            if not isinstance(target_node, ast.Name):
                continue

            if target_node.id not in blacklists.module_metadata_blacklist(
                self.options,
            ):
                continue

            self.add_violation(
                best_practices.WrongModuleMetadataViolation(
                    node,
                    text=target_node.id,
                ),
            )


@final
@alias(
    'visit_any_assign',
    (
        'visit_Assign',
        'visit_AnnAssign',
        'visit_NamedExpr',
    ),
)
@alias(
    'visit_any_for',
    (
        'visit_For',
        'visit_AsyncFor',
    ),
)
class UnusedVariableDefinitionVisitor(BaseNodeVisitor):
    """Checks how variables are used."""

    def visit_any_assign(self, node: AnyAssignWithWalrus) -> None:
        """
        Checks that we cannot assign explicit unused variables.

        We do not check assigns inside modules and classes,
        since there ``_`` prefixed variable means
        that it is protected, not unused.
        """
        is_inside_class_or_module = isinstance(
            nodes.get_context(node),
            ast.ClassDef | ast.Module,
        )
        self._check_assign_unused(
            node,
            name_nodes.flat_variable_names([node]),
            is_local=not is_inside_class_or_module,
        )
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """Checks that we cannot create explicit unused loops."""
        target_names = name_nodes.get_variables_from_node(node.target)
        is_target_no_op_variable = len(target_names) == 1 and access.is_unused(
            target_names[0],
        )
        if not is_target_no_op_variable:  # see issue 1406
            self._check_assign_unused(
                node,
                target_names,
                is_local=True,
            )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Checks that we cannot create explicit unused exceptions."""
        if node.name:
            self._check_assign_unused(node, [node.name], is_local=True)
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        """Checks that we cannot create explicit unused context variables."""
        if node.optional_vars:
            self._check_assign_unused(
                cast(ast.AST, nodes.get_parent(node)),
                name_nodes.get_variables_from_node(node.optional_vars),
                is_local=True,
            )
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        """Check pattern matching in a form of `case ... as NAME`."""
        for match_as in pattern_matching.get_explicit_as_names(node):
            self._check_assign_unused(
                match_as,
                [cast(str, match_as.name)],  # We check for it in getter
                is_local=True,
            )
        self.generic_visit(node)

    def _check_assign_unused(
        self,
        node: ast.AST,
        all_names: Iterable[str],
        *,
        is_local: bool,
    ) -> None:
        all_names = list(all_names)  # we are using it twice
        all_unused = all(
            is_local if access.is_protected(vn) else access.is_unused(vn)
            for vn in all_names
        )

        if all_names and all_unused:
            self.add_violation(
                naming.UnusedVariableIsDefinedViolation(
                    node,
                    text=', '.join(all_names),
                ),
            )


@final
class UnusedVariableUsageVisitor(BaseNodeVisitor):
    """Checks how variables are used."""

    def visit_Name(self, node: ast.Name) -> None:
        """Checks that we cannot use unused variables anywhere."""
        self._check_variable_used(
            node,
            node.id,
            is_created=isinstance(node.ctx, ast.Store),
        )
        self.generic_visit(node)

    def _check_variable_used(
        self,
        node: ast.AST,
        assigned_name: str,
        *,
        is_created: bool,
    ) -> None:
        if not access.is_unused(assigned_name):
            return

        if assigned_name == UNUSED_PLACEHOLDER:
            # This is a special case for django's
            # gettext and similar tools.
            return

        if not is_created:
            self.add_violation(
                naming.UnusedVariableIsUsedViolation(node, text=assigned_name),
            )
