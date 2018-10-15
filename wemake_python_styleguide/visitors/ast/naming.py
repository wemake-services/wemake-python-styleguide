# -*- coding: utf-8 -*-

import ast
from typing import Union

from wemake_python_styleguide.constants import (
    MODULE_METADATA_VARIABLES_BLACKLIST,
    VARIABLE_NAMES_BLACKLIST,
)
from wemake_python_styleguide.logics import variables
from wemake_python_styleguide.types import AnyFunctionDef, AnyImport
from wemake_python_styleguide.violations.best_practices import (
    ReassigningVariableToItselfViolation,
    WrongModuleMetadataViolation,
)
from wemake_python_styleguide.violations.naming import (
    PrivateNameViolation,
    TooShortVariableNameViolation,
    UnderScoredNumberNameViolation,
    UpperCaseAttributeViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

VariableDef = Union[ast.Name, ast.Attribute, ast.ExceptHandler]


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
        if variables.is_wrong_variable_name(name, VARIABLE_NAMES_BLACKLIST):
            self.add_violation(WrongVariableNameViolation(node, text=name))

        min_length = self.options.min_variable_length
        if variables.is_too_short_variable_name(name, min_length=min_length):
            self.add_violation(TooShortVariableNameViolation(node, text=name))

        if variables.is_private_variable(name):
            self.add_violation(PrivateNameViolation(node, text=name))

        if variables.is_variable_name_with_underscored_number(name):
            self.add_violation(UnderScoredNumberNameViolation())

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
                if variables.is_upper_case_name(name):
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
        Used to check wrong names of assigned variables.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        variable_name = variables.get_assigned_name(node)
        if variable_name is not None:
            self._check_name(node, variable_name)
        self.generic_visit(node)


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


class WrongVariableAssignmentVisitor(BaseNodeVisitor):
    """Finds wrong variables assignments."""

    def _check_assignment(self, node: ast.Assign) -> None:
        node_value_id = getattr(node.value, 'id', None)
        for target_node in node.targets:
            target_node_id = getattr(target_node, 'id', None)
            if target_node_id == node_value_id:
                self.add_violation(ReassigningVariableToItselfViolation(node))

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Used to check assignment variable to itself.

        Raises:
            ReassigningVariableToItselfViolation

        """
        self._check_assignment(node)
        self.generic_visit(node)
