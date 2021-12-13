import ast
from itertools import chain, product
from typing import Iterable, List

from typing_extensions import Final, final

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.tree import imports
from wemake_python_styleguide.types import AnyImport, ConfigurationOptions
from wemake_python_styleguide.violations.base import ErrorCallback
from wemake_python_styleguide.violations.best_practices import (
    FutureImportViolation,
    ImportCollisionViolation,
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

#: We use `.` to separate module names.
_MODULE_MEMBERS_SEPARATOR: Final = '.'


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
            if not imports.is_nested_typing_import(parent):
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
            if _MODULE_MEMBERS_SEPARATOR in alias.name:
                self._error_callback(
                    DottedRawImportViolation(node, text=alias.name),
                )

    def _check_protected_import(self, node: ast.Import) -> None:
        names: Iterable[str] = chain.from_iterable([
            alias.name.split(_MODULE_MEMBERS_SEPARATOR)
            for alias in node.names
        ])
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
class _ImportCollisionValidator(object):
    """
    Validator of ``AnyImport`` nodes collisions.

    All imported names that are aliased (by using ``as`` keyword) are
    considered valid.
    """

    def __init__(self, error_callback: ErrorCallback) -> None:
        self._error_callback = error_callback
        self._imported_names: List[imports.ImportedObjectInfo] = []

    def validate(self) -> None:
        """Validates that there are no intersecting imported modules."""
        for first, second in product(self._imported_names, repeat=2):
            if first.module == second.module:
                continue

            if len(first.module) < len(second.module):
                continue

            if self._does_collide(first, second):
                self._error_callback(ImportCollisionViolation(
                    first.node,
                    second.module,
                ))

    def add_import(self, node: ast.Import) -> None:
        """Extract info needed for validation from ``ast.Import``."""
        for alias in node.names:
            if not alias.asname:
                self._imported_names.append(imports.ImportedObjectInfo(
                    alias.name,
                    node,
                ))

    def add_import_from(self, node: ast.ImportFrom) -> None:
        """Extract info needed for validation from ``ast.ImportFrom``."""
        for alias in node.names:
            if not alias.asname:
                self._imported_names.append(imports.ImportedObjectInfo(
                    _MODULE_MEMBERS_SEPARATOR.join(
                        # ignoring `from . import some` case:
                        filter(None, (node.module, alias.name)),
                    ),
                    node,
                ))

    def _does_collide(
        self,
        first: imports.ImportedObjectInfo,
        second: imports.ImportedObjectInfo,
    ) -> bool:
        first_path = first.module.split('.')[:-1]
        second_path = second.module.split('.')
        return first_path == second_path


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
        self._import_collision_validator = _ImportCollisionValidator(
            self.add_violation,
        )

    def visit_Import(self, node: ast.Import) -> None:
        """Used to find wrong ``import`` statements."""
        self._import_validator.validate(node)
        self._import_collision_validator.add_import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Used to find wrong ``from ... import ...`` statements."""
        self._import_from_validator.validate(node)
        self._import_collision_validator.add_import_from(node)
        self.generic_visit(node)

    def _post_visit(self) -> None:
        """Used to find imports collisions."""
        self._import_collision_validator.validate()
