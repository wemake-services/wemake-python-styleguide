# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import (
    BAD_MODULE_METADATA_VARIABLES,
    BAD_VARIABLE_NAMES,
)
from wemake_python_styleguide.errors import (
    TooShortArgumentNameViolation,
    TooShortAttributeNameViolation,
    TooShortFunctionNameViolation,
    TooShortVariableNameViolation,
    WrongArgumentNameViolation,
    WrongAttributeNameViolation,
    WrongFunctionNameViolation,
    WrongModuleMetadataViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.helpers.variables import (
    is_too_short_variable_name,
    is_wrong_variable_name,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongNameVisitor(BaseNodeVisitor):
    """
    This class performs checks based on variable names.

    It is responsible for finding short and blacklisted variables,
    functions, and arguments.
    """

    def _check_argument(self, node: ast.FunctionDef, arg: str) -> None:
        if is_wrong_variable_name(arg, BAD_VARIABLE_NAMES):
            self.add_error(WrongArgumentNameViolation(node, text=arg))

        if is_too_short_variable_name(arg):
            self.add_error(TooShortArgumentNameViolation(node, text=arg))

    def _check_function_signature(self, node: ast.FunctionDef) -> None:
        for arg in node.args.args:
            self._check_argument(node, arg.arg)

        for arg in node.args.kwonlyargs:
            self._check_argument(node, arg.arg)

        if node.args.vararg:
            self._check_argument(node, node.args.vararg.arg)

        if node.args.kwarg:
            self._check_argument(node, node.args.kwarg.arg)

    def visit_Attribute(self, node: ast.Attribute):
        """Used to find wrong attribute names inside classes."""
        context = getattr(node, 'ctx', None)

        if isinstance(context, ast.Store):
            if is_wrong_variable_name(node.attr, BAD_VARIABLE_NAMES):
                self.add_error(
                    WrongAttributeNameViolation(node, text=node.attr),
                )

            if is_too_short_variable_name(node.attr):
                self.add_error(
                    TooShortAttributeNameViolation(node, text=node.attr),
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Used to find wrong function and method parameters."""
        if is_too_short_variable_name(node.name):
            self.add_error(TooShortFunctionNameViolation(node, text=node.name))

        if is_wrong_variable_name(node.name, BAD_VARIABLE_NAMES):
            self.add_error(WrongFunctionNameViolation(node, text=node.name))

        self._check_function_signature(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        """Used to find wrong exception instances in `try/except`."""
        name = getattr(node, 'name', '_')
        if is_wrong_variable_name(name, BAD_VARIABLE_NAMES):
            self.add_error(
                WrongVariableNameViolation(node, text=name),
            )

        if is_too_short_variable_name(name):
            self.add_error(
                TooShortVariableNameViolation(node, text=name),
            )

    def visit_Name(self, node: ast.Name):
        """Used to find wrong regular variables."""
        context = getattr(node, 'ctx', None)

        if isinstance(context, ast.Store):
            if is_wrong_variable_name(node.id, BAD_VARIABLE_NAMES):
                self.add_error(
                    WrongVariableNameViolation(node, text=node.id),
                )

            if is_too_short_variable_name(node.id):
                self.add_error(
                    TooShortVariableNameViolation(node, text=node.id),
                )

        self.generic_visit(node)


class WrongModuleMetadataVisitor(BaseNodeVisitor):
    """This class finds wrong metadata information of a module."""

    def visit_Assign(self, node: ast.Assign):
        """Used to find the bad metadata variable names."""
        node_parent = getattr(node, 'parent')
        if not isinstance(node_parent, ast.Module):
            return

        for target_node in node.targets:
            target_node_id = getattr(target_node, 'id')
            if target_node_id in BAD_MODULE_METADATA_VARIABLES:
                self.add_error(
                    WrongModuleMetadataViolation(node, text=target_node_id),
                )
