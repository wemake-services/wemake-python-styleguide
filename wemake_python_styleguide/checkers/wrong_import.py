# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors import (
    DynamicImportViolation,
    LocalFolderImportViolation,
    NestedImportViolation,
)
from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.helpers.functions import given_function_called

BAD_IMPORT_FUNCTIONS = frozenset((
    '__import__',
))


class _WrongImportVisitor(BaseNodeVisitor):
    def _get_error_text(self, node: ast.AST) -> str:
        module = getattr(node, 'module', None)
        if module is not None:
            return node.module

        if isinstance(node, ast.Import):
            return node.names[0].name
        return '.'

    def _check_nested_import(self, node: ast.AST, text: str):
        if isinstance(node.parent, ast.FunctionDef):
            self.add_error(NestedImportViolation(node, text=text))

    def visit_Call(self, node: ast.Call):
        function_name = given_function_called(node, BAD_IMPORT_FUNCTIONS)
        if function_name:
            self.add_error(DynamicImportViolation(node, text=function_name))
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        text = self._get_error_text(node)
        self._check_nested_import(node, text)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        text = self._get_error_text(node)

        if node.level != 0:
            self.add_error(
                LocalFolderImportViolation(node, text=text),
            )

        if isinstance(node.parent, ast.FunctionDef):
            self.add_error(NestedImportViolation(node, text=text))
        self.generic_visit(node)


class WrongImportChecker(BaseChecker):
    name = 'wms-wrong-import'

    def run(self):
        visiter = _WrongImportVisitor()
        visiter.visit(self.tree)

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
