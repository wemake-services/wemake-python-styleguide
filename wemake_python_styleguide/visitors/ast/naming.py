# -*- coding: utf-8 -*-

import ast
import itertools
from collections import Counter
from typing import Callable, Iterable, List, Optional, Tuple, Union, cast

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.constants import (
    MODULE_METADATA_VARIABLES_BLACKLIST,
    SPECIAL_ARGUMENT_NAMES_WHITELIST,
    VARIABLE_NAMES_BLACKLIST,
)
from wemake_python_styleguide.logic import functions, nodes
from wemake_python_styleguide.logic.naming import (
    access,
    builtins,
    logical,
    name_nodes,
)
from wemake_python_styleguide.types import (
    AnyAssign,
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
    AnyImport,
    ConfigurationOptions,
)
from wemake_python_styleguide.violations import base, naming
from wemake_python_styleguide.violations.best_practices import (
    ReassigningVariableToItselfViolation,
    WrongModuleMetadataViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

VariableDef = Union[ast.Name, ast.Attribute, ast.ExceptHandler]
AssignTargets = List[ast.expr]
AssignTargetsNameList = List[Union[str, Tuple[str]]]


@final
class _NameValidator(object):
    """Utility class to separate logic from the naming visitor."""

    def __init__(
        self,
        error_callback: Callable[[base.BaseViolation], None],
        options: ConfigurationOptions,
    ) -> None:
        """Creates new instance of a name validator."""
        self._error_callback = error_callback
        self._options = options

    def check_name(
        self,
        node: ast.AST,
        name: str,
        *,
        is_first_argument: bool = False,
    ) -> None:
        if logical.is_wrong_name(name, VARIABLE_NAMES_BLACKLIST):
            self._error_callback(
                naming.WrongVariableNameViolation(node, text=name),
            )

        if not is_first_argument:
            if logical.is_wrong_name(name, SPECIAL_ARGUMENT_NAMES_WHITELIST):
                self._error_callback(
                    naming.ReservedArgumentNameViolation(node, text=name),
                )

        if logical.does_contain_unicode(name):
            self._error_callback(naming.UnicodeNameViolation(node, text=name))

        self._ensure_length(node, name)
        self._ensure_underscores(node, name)

    def check_function_signature(self, node: AnyFunctionDefAndLambda) -> None:
        arguments = functions.get_all_arguments(node)
        is_lambda = isinstance(node, ast.Lambda)
        for arg in arguments:
            should_check_argument = functions.is_first_argument(
                node, arg.arg,
            ) and not is_lambda

            self.check_name(
                arg, arg.arg, is_first_argument=should_check_argument,
            )

    def check_attribute_name(self, node: ast.ClassDef) -> None:
        top_level_assigns = [
            sub_node
            for sub_node in node.body
            if isinstance(sub_node, AssignNodes)
        ]

        for assignment in top_level_assigns:
            for target in get_assign_targets(assignment):
                if not isinstance(target, ast.Name):
                    continue

                if not target.id or not logical.is_upper_case_name(target.id):
                    continue

                self._error_callback(
                    naming.UpperCaseAttributeViolation(target, text=target.id),
                )

    def _ensure_underscores(self, node: ast.AST, name: str):
        if access.is_private(name):
            self._error_callback(
                naming.PrivateNameViolation(node, text=name),
            )

        if logical.does_contain_underscored_number(name):
            self._error_callback(
                naming.UnderscoredNumberNameViolation(node, text=name),
            )

        if logical.does_contain_consecutive_underscores(name):
            self._error_callback(
                naming.ConsecutiveUnderscoresInNameViolation(
                    node, text=name,
                ),
            )

        if builtins.is_wrong_alias(name):
            self._error_callback(
                naming.TrailingUnderscoreViolation(node, text=name),
            )

        if access.is_unused(name) and len(name) > 1:
            self._error_callback(
                naming.WrongUnusedVariableNameViolation(node, text=name),
            )

    def _ensure_length(self, node: ast.AST, name: str) -> None:
        min_length = self._options.min_name_length
        if logical.is_too_short_name(name, min_length=min_length):
            self._error_callback(naming.TooShortNameViolation(node, text=name))

        max_length = self._options.max_name_length
        if logical.is_too_long_name(name, max_length=max_length):
            self._error_callback(naming.TooLongNameViolation(node, text=name))


@final
@alias('visit_any_import', (
    'visit_ImportFrom',
    'visit_Import',
))
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
@alias('visit_variable', (
    'visit_Name',
    'visit_Attribute',
    'visit_ExceptHandler',
))
class WrongNameVisitor(BaseNodeVisitor):
    """Performs checks based on variable names."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new naming validator for this visitor."""
        super().__init__(*args, **kwargs)
        self._validator = _NameValidator(self.add_violation, self.options)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Used to find upper attribute declarations.

        Raises:
            UpperCaseAttributeViolation
            UnicodeNameViolation
            TrailingUnderscoreViolation

        """
        self._validator.check_attribute_name(node)
        self._validator.check_name(node, node.name)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Used to find wrong function and method parameters.

        Raises:
            WrongVariableNameViolation
            TooShortNameViolation
            PrivateNameViolation
            TooLongNameViolation
            UnicodeNameViolation
            TrailingUnderscoreViolation

        """
        self._validator.check_name(node, node.name)
        self._validator.check_function_signature(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """
        Used to find wrong parameters.

        Raises:
            WrongVariableNameViolation
            TooShortNameViolation
            PrivateNameViolation
            TooLongNameViolation
            TrailingUnderscoreViolation

        """
        self._validator.check_function_signature(node)
        self.generic_visit(node)

    def visit_any_import(self, node: AnyImport) -> None:
        """
        Used to check wrong import alias names.

        Raises:
            WrongVariableNameViolation
            TooShortNameViolation
            PrivateNameViolation
            TooLongNameViolation
            TrailingUnderscoreViolation

        """
        for alias_node in node.names:
            if alias_node.asname:
                self._validator.check_name(node, alias_node.asname)

        self.generic_visit(node)

    def visit_variable(self, node: VariableDef) -> None:
        """
        Used to check wrong names of assigned.

        Raises:
            WrongVariableNameViolation
            TooShortNameViolation
            PrivateNameViolation
            TooLongNameViolation
            UnicodeNameViolation
            TrailingUnderscoreViolation

        """
        variable_name = name_nodes.get_assigned_name(node)

        if variable_name is not None:
            self._validator.check_name(node, variable_name)
        self.generic_visit(node)


@final
@alias('visit_any_assign', (
    'visit_Assign',
    'visit_AnnAssign',
))
class WrongModuleMetadataVisitor(BaseNodeVisitor):
    """Finds wrong metadata information of a module."""

    def visit_any_assign(self, node: AnyAssign) -> None:
        """
        Used to find the bad metadata variable names.

        Raises:
            WrongModuleMetadataViolation

        """
        self._check_metadata(node)
        self.generic_visit(node)

    def _check_metadata(self, node: AnyAssign) -> None:
        if not isinstance(nodes.get_parent(node), ast.Module):
            return

        targets = get_assign_targets(node)
        for target_node in targets:
            if not isinstance(target_node, ast.Name):
                continue

            if target_node.id in MODULE_METADATA_VARIABLES_BLACKLIST:
                self.add_violation(
                    WrongModuleMetadataViolation(node, text=target_node.id),
                )


@final
@alias('visit_any_assign', (
    'visit_Assign',
    'visit_AnnAssign',
))
class WrongVariableAssignmentVisitor(BaseNodeVisitor):
    """Finds wrong variables assignments."""

    def visit_any_assign(self, node: AnyAssign) -> None:
        """
        Used to check assignment variable to itself.

        Raises:
            ReassigningVariableToItselfViolation

        """
        names = list(name_nodes.flat_variable_names([node]))

        self._check_reassignment(node, names)
        self._check_unique_assignment(node, names)
        self.generic_visit(node)

    def _check_reassignment(
        self,
        node: AnyAssign,
        names: List[str],
    ) -> None:
        if not node.value:
            return

        var_values = name_nodes.get_variables_from_node(node.value)
        for var_name, var_value in itertools.zip_longest(names, var_values):
            if var_name == var_value:
                self.add_violation(
                    ReassigningVariableToItselfViolation(node, text=var_name),
                )

    def _check_unique_assignment(
        self,
        node: AnyAssign,
        names: List[str],
    ) -> None:
        for used_name, count in Counter(names).items():
            if count > 1:
                self.add_violation(
                    ReassigningVariableToItselfViolation(node, text=used_name),
                )


@final
@alias('visit_any_assign', (
    'visit_Assign',
    'visit_AnnAssign',
))
class WrongVariableUsageVisitor(BaseNodeVisitor):
    """Checks how variables are used."""

    def visit_Name(self, node: ast.Name) -> None:
        """
        Checks that we cannot use ``_`` anywhere.

        Raises:
            UnusedVariableIsUsedViolation

        """
        self._check_variable_used(
            node,
            node.id,
            is_created=isinstance(node.ctx, ast.Store),
        )
        self.generic_visit(node)

    def visit_any_assign(self, node: AnyAssign) -> None:
        """
        Checks that we cannot assign explicit unused variables.

        We do not check assignes inside modules and classes,
        since there ``_`` prefixed variable means
        that it is protected, not unused.

        Raises:
            UnusedVariableIsDefinedViolation

        """
        is_inside_class_or_module = isinstance(
            nodes.get_context(node),
            (ast.ClassDef, ast.Module),
        )
        self._check_assign_unused(
            node,
            name_nodes.flat_variable_names([node]),
            is_local=not is_inside_class_or_module,
        )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Checks that we cannot create explicit unused exceptions.

        Raises:
            UnusedVariableIsDefinedViolation

        """
        if node.name:
            self._check_assign_unused(node, [node.name])
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        """
        Checks that we cannot create explicit unused context variables.

        Raises:
            UnusedVariableIsDefinedViolation

        """
        if node.optional_vars:
            self._check_assign_unused(
                cast(ast.AST, nodes.get_parent(node)),
                name_nodes.get_variables_from_node(node.optional_vars),
            )
        self.generic_visit(node)

    def _check_variable_used(
        self,
        node: ast.AST,
        assigned_name: Optional[str],
        *,
        is_created: bool,
    ) -> None:
        if not assigned_name or not access.is_unused(assigned_name):
            return

        if not is_created:
            self.add_violation(
                naming.UnusedVariableIsUsedViolation(node, text=assigned_name),
            )

    def _check_assign_unused(
        self,
        node: ast.AST,
        all_names: Iterable[str],
        *,
        is_local: bool = True,
    ) -> None:
        all_names = list(all_names)  # we are using it twice
        all_unused = all(
            is_local if access.is_protected(vn) else access.is_unused(vn)
            for vn in all_names
        )

        if all_names and all_unused:
            self.add_violation(
                naming.UnusedVariableIsDefinedViolation(
                    node, text=', '.join(all_names),
                ),
            )
