import ast
from itertools import chain
from typing import Iterable

from typing_extensions import final

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.tree import imports
from wemake_python_styleguide.types import AnyImport, ConfigurationOptions
from wemake_python_styleguide.violations.base import ErrorCallback
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


class _BaseImportValidator(object):
    """Base utility class to separate logic from the visitor."""

    def __init__(
        self,
        error_callback: ErrorCallback,
        options: ConfigurationOptions,
    ) -> None:
        self._error_callback = error_callback
        self._options = options

    def _validate_any_import(self, node: AnyImport) -> None:
        self._check_nested_import(node)
        self._check_same_alias(node)

    def _check_nested_import(self, node: AnyImport) -> None:
        parent = nodes.get_parent(node)
        if parent is not None and not isinstance(parent, ast.Module):
            self._error_callback(NestedImportViolation(node))

    def _check_same_alias(self, node: AnyImport) -> None:
        for alias in node.names:
            if alias.asname == alias.name and self._options.i_control_code:
                self._error_callback(
                    SameAliasImportViolation(node, text=alias.name),
                )


@final
class _ImportValidator(_BaseImportValidator):
    """Validator of ``ast.Import`` nodes."""

    def validate(self, node: ast.Import) -> None:
        self._validate_any_import(node)
        self._check_dotted_raw_import(node)
        self._check_protected_import(node)

    def _check_dotted_raw_import(self, node: ast.Import) -> None:
        for alias in node.names:
            if '.' in alias.name:
                self._error_callback(
                    DottedRawImportViolation(node, text=alias.name),
                )

    def _check_protected_import(self, node: ast.Import) -> None:
        names: Iterable[str] = chain.from_iterable(
            [alias.name.split('.') for alias in node.names],
        )
        for name in names:
            if access.is_protected(name):
                self._error_callback(ProtectedModuleViolation(node, text=name))


@final
class _ImportFromValidator(_BaseImportValidator):
    """Validator of ``ast.ImportFrom`` nodes."""

    def validate(self, node: ast.ImportFrom) -> None:
        self._validate_any_import(node)
        self._check_from_import(node)
        self._check_protected_import_from_module(node)
        self._check_protected_import_from_members(node)
        self._check_vague_alias(node)

    def _check_from_import(self, node: ast.ImportFrom) -> None:
        if node.level != 0:
            self._error_callback(LocalFolderImportViolation(node))

        if node.module == '__future__':
            for alias in node.names:
                if alias.name not in FUTURE_IMPORTS_WHITELIST:
                    self._error_callback(
                        FutureImportViolation(node, text=alias.name),
                    )

    def _check_protected_import_from_module(self, node: ast.ImportFrom) -> None:
        for name in imports.get_import_parts(node):
            if access.is_protected(name):
                self._error_callback(ProtectedModuleViolation(node, text=name))

    def _check_protected_import_from_members(
        self,
        node: ast.ImportFrom,
    ) -> None:
        for alias in node.names:
            if access.is_protected(alias.name):
                self._error_callback(
                    ProtectedModuleMemberViolation(node, text=alias.name),
                )

    def _check_vague_alias(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            for name in filter(None, (alias.name, alias.asname)):
                is_regular_import = (
                    (alias.asname and name != alias.asname) or
                    not imports.is_vague_import(name)
                )

                if not is_regular_import:
                    self._error_callback(VagueImportViolation(node, text=name))


@final
class WrongImportVisitor(BaseNodeVisitor):
    """Responsible for finding wrong imports."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a checker for tracked violations."""
        super().__init__(*args, **kwargs)
        self._import_validator = _ImportValidator(
            self.add_violation,
            self.options,
        )
        self._import_from_validator = _ImportFromValidator(
            self.add_violation,
            self.options,
        )

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
        self._import_validator.validate(node)
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
        self._import_from_validator.validate(node)
        self.generic_visit(node)
