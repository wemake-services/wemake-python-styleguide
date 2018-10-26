# -*- coding: utf-8 -*-

import ast
from typing import List, Tuple, Union

from wemake_python_styleguide.constants import (
    MODULE_METADATA_VARIABLES_BLACKLIST,
    VARIABLE_NAMES_BLACKLIST,
)
from wemake_python_styleguide.logics.variables import access
from wemake_python_styleguide.logics.variables.name_nodes import (
    get_assigned_name,
)
from wemake_python_styleguide.logics.variables.naming import (
    is_too_short_variable_name,
    is_upper_case_name,
    is_variable_name_contains_consecutive_underscores,
    is_variable_name_with_underscored_number,
    is_wrong_variable_name,
)
from wemake_python_styleguide.types import AnyFunctionDef, AnyImport, final
from wemake_python_styleguide.violations.best_practices import (
    ReassigningVariableToItselfViolation,
    WrongModuleMetadataViolation,
)
from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
    PrivateNameViolation,
    TooShortVariableNameViolation,
    UnderScoredNumberNameViolation,
    UpperCaseAttributeViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

VariableDef = Union[ast.Name, ast.Attribute, ast.ExceptHandler]
AssignTargets = List[ast.expr]
AssignTargetsNameList = List[Union[str, Tuple[str]]]


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

    def _check_name(self, node: ast.AST, name: str) -> None:

        if is_wrong_variable_name(name, VARIABLE_NAMES_BLACKLIST):
            self.add_violation(WrongVariableNameViolation(node, text=name))

        min_length = self.options.min_variable_length
        if is_too_short_variable_name(name, min_length=min_length):
            self.add_violation(TooShortVariableNameViolation(node, text=name))

        if access.is_private_variable(name):
            self.add_violation(PrivateNameViolation(node, text=name))

        if is_variable_name_with_underscored_number(name):
            self.add_violation(UnderScoredNumberNameViolation())
        if is_variable_name_contains_consecutive_underscores(name):
            self.add_violation(
                ConsecutiveUnderscoresInNameViolation(node, text=name),
            )

    def _check_function_signature(self, node: AnyFunctionDef) -> None:
        for arg in node.args.args:
            self._check_name(node, arg.arg)

        for arg in node.args.kwonlyargs:
            self._check_name(node, arg.arg)

        if node.args.vararg:
            self._check_name(node, node.args.vararg.arg)

        if node.args.kwarg:
            self._check_name(node, node.args.kwarg.arg)

    def _check_attribute_name(self, node: ast.ClassDef) -> None:
        top_level_assigns = [
            sub_node
            for sub_node in node.body
            if isinstance(sub_node, ast.Assign)
        ]

        for assignment in top_level_assigns:
            for target in assignment.targets:
                name = getattr(target, 'id', None)
                if is_upper_case_name(name):
                    self.add_violation(
                        UpperCaseAttributeViolation(target, text=name),
                    )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Used to find upper attribute declarations.

        Raises:
            UpperCaseAttributeViolation

        """
        self._check_attribute_name(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Used to find wrong function and method parameters.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        self._check_name(node, node.name)
        self._check_function_signature(node)
        self.generic_visit(node)

    def visit_any_import(self, node: AnyImport) -> None:
        """
        Used to check wrong import alias names.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        for alias_node in node.names:
            if alias_node.asname:
                self._check_name(node, alias_node.asname)

        self.generic_visit(node)

    def visit_variable(self, node: VariableDef) -> None:
        """
        Used to check wrong names of assigned.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        variable_name = get_assigned_name(node)

        if variable_name is not None:
            self._check_name(node, variable_name)
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
            self, target: AssignTargets,
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
