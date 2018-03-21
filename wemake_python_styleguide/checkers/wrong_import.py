# -*- coding: utf-8 -*-

import ast
from typing import Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.constants import BAD_IMPORT_FUNCTIONS
from wemake_python_styleguide.errors import (
    DynamicImportViolation,
    LocalFolderImportViolation,
    NestedImportViolation,
)
from wemake_python_styleguide.helpers.functions import given_function_called


class _WrongImportVisitor(BaseNodeVisitor):
    def _get_error_text(self, node: ast.AST) -> str:
        module = getattr(node, 'module', None)
        if module is not None:
            return module

        if isinstance(node, ast.Import):
            return node.names[0].name
        return '.'

    def _check_nested_import(self, node: ast.AST, text: str):
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.FunctionDef):
            self.add_error(NestedImportViolation(node, text=text))

    def visit_Call(self, node: ast.Call):
        """Used to find `BAD_IMPORT_FUNCTIONS` function calls."""
        function_name = given_function_called(node, BAD_IMPORT_FUNCTIONS)
        if function_name:
            self.add_error(DynamicImportViolation(node, text=function_name))
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """Used to find nested `import` statements."""
        text = self._get_error_text(node)
        self._check_nested_import(node, text)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Used to find nested `from import` statements and local imports."""
        text = self._get_error_text(node)

        if node.level != 0:
            self.add_error(
                LocalFolderImportViolation(node, text=text),
            )

        if isinstance(getattr(node, 'parent', None), ast.FunctionDef):
            self.add_error(NestedImportViolation(node, text=text))
        self.generic_visit(node)


class WrongImportChecker(BaseChecker):
    """This class is responsible for finding wrong imports."""

    name = 'wms-wrong-import'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _WrongImportVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
