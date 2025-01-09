import ast
from collections import defaultdict
from itertools import product
from typing import Final, TypeAlias, final

from attrs import frozen

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.tree import imports
from wemake_python_styleguide.options.validation import ValidatedOptions
from wemake_python_styleguide.violations.base import ErrorCallback
from wemake_python_styleguide.violations.best_practices import (
    FutureImportViolation,
    ImportCollisionViolation,
    ImportObjectCollisionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    DottedRawImportViolation,
    LocalFolderImportViolation,
    VagueImportViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor

#: We use `.` to separate module names.
_MODULE_MEMBERS_SEPARATOR: Final = '.'

_NameAndContext: TypeAlias = tuple[str, ast.AST | None]


@frozen
class _BaseImportValidator:
    """Base utility class to separate logic from the visitor."""

    _error_callback: ErrorCallback
    _options: ValidatedOptions


@final
class _ImportValidator(_BaseImportValidator):
    """Validator of ``ast.Import`` nodes."""

    def validate(self, node: ast.Import) -> None:
        self._check_dotted_raw_import(node)

    def _check_dotted_raw_import(self, node: ast.Import) -> None:
        for alias in node.names:
            if _MODULE_MEMBERS_SEPARATOR in alias.name:
                self._error_callback(
                    DottedRawImportViolation(node, text=alias.name),
                )


@final
class _ImportFromValidator(_BaseImportValidator):
    """Validator of ``ast.ImportFrom`` nodes."""

    def validate(self, node: ast.ImportFrom) -> None:
        self._check_from_import(node)
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

    def _check_vague_alias(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            for name in filter(None, (alias.name, alias.asname)):
                is_regular_import = (
                    alias.asname and name != alias.asname
                ) or not imports.is_vague_import(name)

                if not is_regular_import:
                    self._error_callback(VagueImportViolation(node, text=name))


@final
class _ImportCollisionValidator:
    """
    Validator of ``AnyImport`` nodes collisions.

    All imported names that are aliased (by using ``as`` keyword) are
    considered valid.
    """

    def __init__(self, error_callback: ErrorCallback) -> None:
        self._error_callback = error_callback
        self._imported_names: list[imports.ImportedObjectInfo] = []
        # This helps us to detect cases like:
        # `from x import y, y as z`
        self._imported_objects: defaultdict[_NameAndContext, set[str]] = (
            defaultdict(set)
        )

    def validate(self) -> None:
        """Validates that there are no intersecting imported modules."""
        for first, second in product(self._imported_names, repeat=2):
            if first.module == second.module:
                continue

            if len(first.module) < len(second.module):
                continue

            if self._does_collide(first, second):
                self._error_callback(
                    ImportCollisionViolation(
                        first.node,
                        second.module,
                    ),
                )

    def add_import(self, node: ast.Import) -> None:
        """Extract info needed for validation from ``ast.Import``."""
        for alias in node.names:
            if not alias.asname:
                self._imported_names.append(
                    imports.ImportedObjectInfo(
                        alias.name,
                        node,
                    ),
                )

    def add_import_from(self, node: ast.ImportFrom) -> None:
        """Extract info needed for validation from ``ast.ImportFrom``."""
        for alias in node.names:
            identifier = imports.get_module_name(node)
            context = nodes.get_context(node)
            if alias.name in self._imported_objects[identifier, context]:
                self._error_callback(
                    ImportObjectCollisionViolation(node, alias.name),
                )
            self._imported_objects[identifier, context].add(alias.name)

            if not alias.asname:
                self._imported_names.append(
                    imports.ImportedObjectInfo(
                        _MODULE_MEMBERS_SEPARATOR.join(
                            # ignoring `from . import some` case:
                            filter(None, (node.module, alias.name)),
                        ),
                        node,
                    ),
                )

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
