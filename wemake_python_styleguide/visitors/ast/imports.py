# -*- coding: utf-8 -*-

import ast
from itertools import chain
from typing import Callable, Iterable

from typing_extensions import final

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.logic import imports, nodes
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.types import AnyImport, ConfigurationOptions
from wemake_python_styleguide.violations.base import BaseViolation
from wemake_python_styleguide.violations.best_practices import (
    FutureImportViolation,
    NestedImportViolation,
    ProtectedModuleMemberViolation,
    ProtectedModuleViolation,
)
from wemake_python_styleguide.violations.consistency import (
    DottedRawImportViolation,
    LocalFolderImportViolation,
    VagueImportViolation,
)
from wemake_python_styleguide.violations.naming import SameAliasImportViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor

ErrorCallback = Callable[[BaseViolation], None]  # TODO: alias and move


@final  # noqa: WPS214
class _ImportsValidator(object):
    """Utility class to separate logic from the visitor."""

    def __init__(
        self,
        error_callback: ErrorCallback,
        options: ConfigurationOptions,
    ) -> None:
        self._error_callback = error_callback
        self._options = options

    def check_nested_import(self, node: AnyImport) -> None:
        parent = nodes.get_parent(node)
        if parent is not None and not isinstance(parent, ast.Module):
            self._error_callback(NestedImportViolation(node))

    def check_from_import(self, node: ast.ImportFrom) -> None:
        if node.level != 0:
            self._error_callback(LocalFolderImportViolation(node))

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
            for name in (alias.name, alias.asname):
                if name is None:
                    continue

                if imports.is_vague_import(name):
                    self._error_callback(
                        VagueImportViolation(node, text=alias.name),
                    )

    def check_same_alias(self, node: AnyImport) -> None:
        for alias in node.names:
            if alias.asname == alias.name and not self._options.i_control_code:
                self._error_callback(
                    SameAliasImportViolation(node, text=alias.name),
                )

    def check_protected_import(self, node: ast.Import) -> None:
        self._check_protected_names(
            chain.from_iterable(
                [alias.name.split('.') for alias in node.names],
            ),
            ProtectedModuleViolation(node),
        )

    def check_protected_import_from(self, node: ast.ImportFrom) -> None:
        self._check_protected_names(
            imports.get_import_parts(node),
            ProtectedModuleViolation(node),
        )
        self._check_protected_names(
            [alias.name for alias in node.names],
            ProtectedModuleMemberViolation(node),
        )

    def _check_protected_names(
        self,
        names: Iterable[str],
        violation: BaseViolation,
    ) -> None:
        for name in names:
            if access.is_protected(name):
                self._error_callback(violation)


@final
class WrongImportVisitor(BaseNodeVisitor):
    """Responsible for finding wrong imports."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a checker for tracked violations."""
        super().__init__(*args, **kwargs)
        self._validator = _ImportsValidator(self.add_violation, self.options)

    def visit_Import(self, node: ast.Import) -> None:
        """
        Used to find wrong ``import`` statements.

        Raises:
            DottedRawImportViolation
            NestedImportViolation
            ProtectedModuleViolation
            SameAliasImportViolation
            VagueImportViolation

        """
        self._validator.check_nested_import(node)
        self._validator.check_dotted_raw_import(node)
        self._validator.check_alias(node)
        self._validator.check_same_alias(node)
        self._validator.check_protected_import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Used to find wrong ``from ... import ...`` statements.

        Raises:
            FutureImportViolation
            LocalFolderImportViolation
            NestedImportViolation
            ProtectedModuleMemberViolation
            ProtectedModuleViolation
            SameAliasImportViolation
            VagueImportViolation

        """
        self._validator.check_from_import(node)
        self._validator.check_nested_import(node)
        self._validator.check_alias(node)
        self._validator.check_same_alias(node)
        self._validator.check_protected_import_from(node)
        self.generic_visit(node)
