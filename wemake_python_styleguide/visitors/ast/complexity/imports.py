import ast
from typing import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.filenames import get_stem
from wemake_python_styleguide.logic.tree.strings import is_doc_string
from wemake_python_styleguide.options.validation import ValidatedOptions
from wemake_python_styleguide.types import AnyImport
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.violations.base import ErrorCallback
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class _ImportFromMembersValidator:
    """Validator of ``ast.ImportFrom`` nodes names."""

    def __init__(
        self,
        error_callback: ErrorCallback,
        options: ValidatedOptions,
    ) -> None:
        self._error_callback = error_callback
        self._options = options

    def validate(self, node: ast.ImportFrom) -> None:
        self._check_import_from_names_count(node)

    def _check_import_from_names_count(self, node: ast.ImportFrom) -> None:
        imported_names_number = len(node.names)
        if imported_names_number > self._options.max_import_from_members:
            self._error_callback(
                complexity.TooManyImportedModuleMembersViolation(
                    node,
                    text=str(imported_names_number),
                    baseline=self._options.max_import_from_members,
                ),
            )


@final
class ImportMembersVisitor(BaseNodeVisitor):
    """Counts imports in a module."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._imports_count = 0
        self._imported_names_count = 0
        self._import_from_members_validator = _ImportFromMembersValidator(
            self.add_violation,
            self.options,
        )

    def visit_Import(self, node: ast.Import) -> None:
        """Counts the number of ``import`` nodes."""
        self._visit_any_import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Counts the number of ``from ... import ...``."""
        self._import_from_members_validator.validate(node)
        self._visit_any_import(node)
        self.generic_visit(node)

    def _visit_any_import(self, node: AnyImport) -> None:
        self._imports_count += 1
        self._imported_names_count += len(node.names)
        self.generic_visit(node)

    def _check_imports_count(self) -> None:
        if _is_reexport_module(self.tree, self.filename):
            return
        if self._imports_count > self.options.max_imports:
            self.add_violation(
                complexity.TooManyImportsViolation(
                    text=str(self._imports_count),
                    baseline=self.options.max_imports,
                ),
            )

    def _check_imported_names_count(self) -> None:
        if self._imported_names_count > self.options.max_imported_names:
            self.add_violation(
                complexity.TooManyImportedNamesViolation(
                    text=str(self._imported_names_count),
                    baseline=self.options.max_imported_names,
                ),
            )

    def _post_visit(self) -> None:
        self._check_imports_count()
        self._check_imported_names_count()


def _is_reexport_module(tree: ast.AST, filename: str) -> bool:
    is_init = get_stem(filename) == constants.INIT
    if not is_init or not isinstance(tree, ast.Module):
        return False

    body = tree.body
    if not body:
        return False

    if is_doc_string(body[0]):
        body = body[1:]

    return bool(body) and all(
        isinstance(statement, (ast.Import, ast.ImportFrom))
        for statement in body
    )
