# -*- coding: utf-8 -*-

import ast
from itertools import chain
from typing import Callable

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.logics import imports
from wemake_python_styleguide.logics.naming import access
from wemake_python_styleguide.types import AnyImport, final
from wemake_python_styleguide.violations.base import BaseViolation
from wemake_python_styleguide.violations.best_practices import (
    FutureImportViolation,
    NestedImportViolation,
    ProtectedModuleViolation,
)
from wemake_python_styleguide.violations.consistency import (
    DottedRawImportViolation,
    LocalFolderImportViolation,
)
from wemake_python_styleguide.violations.naming import SameAliasImportViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor

ErrorCallback = Callable[[BaseViolation], None]  # TODO: alias and move


@final
class _ImportsValidator(object):
    """Utility class to separate logic from the visitor."""

    def __init__(self, error_callback: ErrorCallback) -> None:
        self._error_callback = error_callback

    def check_nested_import(self, node: AnyImport) -> None:
        parent = getattr(node, 'parent', None)
        if parent is not None and not isinstance(parent, ast.Module):
            self._error_callback(NestedImportViolation(node))

    def check_local_import(self, node: ast.ImportFrom) -> None:
        if node.level != 0:
            self._error_callback(LocalFolderImportViolation(node))

    def check_future_import(self, node: ast.ImportFrom) -> None:
        if node.module == '__future__':
            for alias in node.names:
                if alias.name not in FUTURE_IMPORTS_WHITELIST:
                    self._error_callback(
                        FutureImportViolation(node, text=alias.name),
                    )

    def check_dotted_raw_import(self, node: ast.Import) -> None:
        for alias in node.names:
            if '.' in alias.name:
                self._error_callback(
                    DottedRawImportViolation(node, text=alias.name),
                )

    def check_alias(self, node: AnyImport) -> None:
        for alias in node.names:
            if alias.asname == alias.name:
                self._error_callback(
                    SameAliasImportViolation(node, text=alias.name),
                )

    def check_protected_import(self, node: AnyImport) -> None:
        import_names = [alias.name for alias in node.names]
        for name in chain(imports.get_import_parts(node), import_names):
            if access.is_protected(name):
                self._error_callback(ProtectedModuleViolation(node))


@final
class WrongImportVisitor(BaseNodeVisitor):
    """Responsible for finding wrong imports."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a checker for tracked violations."""
        super().__init__(*args, **kwargs)
        self._validator = _ImportsValidator(self.add_violation)

    def visit_Import(self, node: ast.Import) -> None:
        """
        Used to find wrong ``import`` statements.

        Raises:
            SameAliasImportViolation
            DottedRawImportViolation
            NestedImportViolation

        """
        self._validator.check_nested_import(node)
        self._validator.check_dotted_raw_import(node)
        self._validator.check_alias(node)
        self._validator.check_protected_import(node)
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
        self._validator.check_local_import(node)
        self._validator.check_nested_import(node)
        self._validator.check_future_import(node)
        self._validator.check_alias(node)
        self._validator.check_protected_import(node)
        self.generic_visit(node)
