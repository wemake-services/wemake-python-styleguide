# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import (
    BAD_MODULE_METADATA_VARIABLES,
    BAD_VARIABLE_NAMES,
)
from wemake_python_styleguide.errors.general import (
    PrivateNameViolation,
    TooShortVariableNameViolation,
    WrongModuleMetadataViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.logics.variables import (
    is_private_variable,
    is_too_short_variable_name,
    is_wrong_variable_name,
)
from wemake_python_styleguide.types import AnyImport
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongNameVisitor(BaseNodeVisitor):
    """
    Performs checks based on variable names.

    It is responsible for finding short and blacklisted variables,
    functions, and arguments.
    """

    def _check_name(self, node: ast.AST, name: str) -> None:
        if is_wrong_variable_name(name, BAD_VARIABLE_NAMES):
            self.add_error(WrongVariableNameViolation(node, text=name))

        min_length = self.options.min_variable_length
        if is_too_short_variable_name(name, min_length=min_length):
            self.add_error(TooShortVariableNameViolation(node, text=name))

        if is_private_variable(name):
            self.add_error(PrivateNameViolation(node, text=name))

    def _check_function_signature(self, node: ast.FunctionDef) -> None:
        for arg in node.args.args:
            self._check_name(node, arg.arg)

        for arg in node.args.kwonlyargs:
            self._check_name(node, arg.arg)

        if node.args.vararg:
            self._check_name(node, node.args.vararg.arg)

        if node.args.kwarg:
            self._check_name(node, node.args.kwarg.arg)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """
        Used to find wrong attribute names inside classes.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        if isinstance(node.ctx, ast.Store):
            self._check_name(node, node.attr)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
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

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Used to find wrong exception instances in ``try``/``except``.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        self._check_name(node, getattr(node, 'name', None))
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        """
        Used to find wrong regular variables.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        if isinstance(node.ctx, ast.Store):
            self._check_name(node, node.id)

        self.generic_visit(node)

    def visit_Import(self, node: AnyImport) -> None:
        """
        Used to check wrong import alias names.

        Raises:
            WrongVariableNameViolation
            TooShortVariableNameViolation
            PrivateNameViolation

        """
        for alias in node.names:
            if alias.asname:
                self._check_name(node, alias.asname)

        self.generic_visit(node)

    visit_ImportFrom = visit_Import


class WrongModuleMetadataVisitor(BaseNodeVisitor):
    """Finds wrong metadata information of a module."""

    def _check_metadata(self, node: ast.Assign) -> None:
        node_parent = getattr(node, 'parent', None)
        if not isinstance(node_parent, ast.Module):
            return

        for target_node in node.targets:
            target_node_id = getattr(target_node, 'id', None)
            if target_node_id in BAD_MODULE_METADATA_VARIABLES:
                self.add_error(
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
