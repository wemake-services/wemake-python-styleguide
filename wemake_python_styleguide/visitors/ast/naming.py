# -*- coding: utf-8 -*-

import ast
from typing import Callable, List, Tuple, Union

from wemake_python_styleguide.constants import (
    MODULE_METADATA_VARIABLES_BLACKLIST,
    SPECIAL_ARGUMENT_NAMES_WHITELIST,
    VARIABLE_NAMES_BLACKLIST,
)
from wemake_python_styleguide.logics import functions
from wemake_python_styleguide.logics.naming import access, logical, name_nodes
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
    AnyImport,
    ConfigurationOptions,
    final,
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


class _NameValidator(object):
    """Utility class to separate logic from the visitor."""

    def __init__(
        self,
        error_callback: Callable[[base.BaseViolation], None],  # TODO: alias
        options: ConfigurationOptions,
    ) -> None:
        """Creates new instance of a name validator."""
        self._error_callback = error_callback
        self._options = options

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

    def _ensure_length(self, node: ast.AST, name: str) -> None:
        min_length = self._options.min_name_length
        if logical.is_too_short_name(name, min_length=min_length):
            self._error_callback(naming.TooShortNameViolation(node, text=name))

        max_length = self._options.max_name_length
        if logical.is_too_long_name(name, max_length=max_length):
            self._error_callback(naming.TooLongNameViolation(node, text=name))

    def check_name(
        self,
        node: ast.AST,
        name: str,
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
            if isinstance(sub_node, ast.Assign)
        ]

        for assignment in top_level_assigns:
            for target in assignment.targets:
                name = getattr(target, 'id', None)
                if logical.is_upper_case_name(name):
                    self._error_callback(
                        naming.UpperCaseAttributeViolation(target, text=name),
                    )


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

        """
        variable_name = name_nodes.get_assigned_name(node)

        if variable_name is not None:
            self._validator.check_name(node, variable_name)
        self.generic_visit(node)


@final
class WrongModuleMetadataVisitor(BaseNodeVisitor):
    """Finds wrong metadata information of a module."""

    def _check_metadata(self, node: ast.Assign) -> None:
        node_parent = getattr(node, 'parent', None)
        if not isinstance(node_parent, ast.Module):
            return

        for target_node in node.targets:
            target_node_id = getattr(target_node, 'id', None)
            if target_node_id in MODULE_METADATA_VARIABLES_BLACKLIST:
                self.add_violation(
                    WrongModuleMetadataViolation(node, text=target_node_id),
                )

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Used to find the bad metadata variable names.

        Raises:
            WrongModuleMetadataViolation

        """
        self._check_metadata(node)
        self.generic_visit(node)


@final
class WrongVariableAssignmentVisitor(BaseNodeVisitor):
    """Finds wrong variables assignments."""

    def _create_target_names(
        self,
        target: AssignTargets,
    ) -> AssignTargetsNameList:
        """Creates list with names of targets of assignment."""
        target_names = []
        for ast_object in target:
            if isinstance(ast_object, ast.Name):
                target_names.append(getattr(ast_object, 'id', None))
            if isinstance(ast_object, ast.Tuple):
                target_names.append(getattr(ast_object, 'elts', None))
                for index, _ in enumerate(target_names):
                    target_names[index] = tuple(
                        name.id for name in target_names[index]
                        if isinstance(name, ast.Name)
                    )
        return target_names

    def _check_assignment(self, node: ast.Assign) -> None:
        target_names = self._create_target_names(node.targets)

        if isinstance(node.value, ast.Tuple):
            node_values = node.value.elts
            values_names = tuple(
                getattr(node_value, 'id', None) for node_value in node_values
            )

        else:
            values_names = getattr(node.value, 'id', None)
        has_repeatable_values = len(target_names) != len(set(target_names))
        if values_names in target_names or has_repeatable_values:
            self.add_violation(ReassigningVariableToItselfViolation(node))

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Used to check assignment variable to itself.

        Raises:
            ReassigningVariableToItselfViolation

        """
        self._check_assignment(node)
        self.generic_visit(node)
