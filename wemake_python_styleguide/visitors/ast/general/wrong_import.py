# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.errors.imports import (
    DottedRawImportViolation,
    FutureImportViolation,
    LocalFolderImportViolation,
    NestedImportViolation,
    SameAliasImportViolation,
)
from wemake_python_styleguide.logics.imports import get_error_text
from wemake_python_styleguide.types import AnyImport
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class _ImportsChecker(object):

    def __init__(self, delegate: 'WrongImportVisitor') -> None:
        self.delegate = delegate

    def check_nested_import(self, node: AnyImport) -> None:
        text = get_error_text(node)
        parent = getattr(node, 'parent', None)
        if parent is not None and not isinstance(parent, ast.Module):
            self.delegate.add_error(NestedImportViolation(node, text=text))

    def check_local_import(self, node: ast.ImportFrom) -> None:
        text = get_error_text(node)
        if node.level != 0:
            self.delegate.add_error(
                LocalFolderImportViolation(node, text=text),
            )

    def check_future_import(self, node: ast.ImportFrom) -> None:
        if node.module == '__future__':
            for alias in node.names:
                if alias.name not in FUTURE_IMPORTS_WHITELIST:
                    self.delegate.add_error(
                        FutureImportViolation(node, text=alias.name),
                    )

    def check_dotted_raw_import(self, node: ast.Import) -> None:
        for alias in node.names:
            if '.' in alias.name:
                self.delegate.add_error(
                    DottedRawImportViolation(node, text=alias.name),
                )

    def check_alias(self, node: AnyImport) -> None:
        for alias in node.names:
            if alias.asname == alias.name:
                self.delegate.add_error(
                    SameAliasImportViolation(node, text=alias.name),
                )


class WrongImportVisitor(BaseNodeVisitor):
    """Responsible for finding wrong imports."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a checker for tracked violations."""
        super().__init__(*args, **kwargs)
        self._checker = _ImportsChecker(self)

    def visit_Import(self, node: ast.Import) -> None:
        """
        Used to find wrong ``import`` statements.

        Raises:
            SameAliasImportViolation
            DottedRawImportViolation
            NestedImportViolation

        """
        self._checker.check_nested_import(node)
        self._checker.check_dotted_raw_import(node)
        self._checker.check_alias(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Used to find wrong ``from ... import ...`` statements.

        Raises:
            SameAliasImportViolation
            NestedImportViolation
            LocalFolderImportViolation
            FutureImportViolation

        """
        self._checker.check_local_import(node)
        self._checker.check_nested_import(node)
        self._checker.check_future_import(node)
        self._checker.check_alias(node)
        self.generic_visit(node)
