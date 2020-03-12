import ast
from collections import defaultdict
from typing import DefaultDict, List, Union

from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree.functions import is_method
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyImport,
    ConfigurationOptions,
)
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.violations.base import ErrorCallback
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

_ConditionNodes = Union[ast.If, ast.While, ast.IfExp]
_ModuleMembers = Union[AnyFunctionDef, ast.ClassDef]


@final
@alias('visit_module_members', (
    'visit_ClassDef',
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class ModuleMembersVisitor(BaseNodeVisitor):
    """Counts classes and functions in a module."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._public_items_count = 0

    def visit_module_members(self, node: _ModuleMembers) -> None:
        """
        Counts the number of _ModuleMembers in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._check_decorators_count(node)
        self._check_members_count(node)
        self.generic_visit(node)

    def _check_members_count(self, node: _ModuleMembers) -> None:
        """This method increases the number of module members."""
        is_real_method = is_method(getattr(node, 'function_type', None))

        if isinstance(get_parent(node), ast.Module) and not is_real_method:
            self._public_items_count += 1

    def _check_decorators_count(self, node: _ModuleMembers) -> None:
        number_of_decorators = len(node.decorator_list)
        if number_of_decorators > self.options.max_decorators:
            self.add_violation(
                complexity.TooManyDecoratorsViolation(
                    node,
                    text=str(number_of_decorators),
                    baseline=self.options.max_decorators,
                ),
            )

    def _post_visit(self) -> None:
        if self._public_items_count > self.options.max_module_members:
            self.add_violation(
                complexity.TooManyModuleMembersViolation(
                    text=str(self._public_items_count),
                    baseline=self.options.max_module_members,
                ),
            )


@final
class _ImportFromMembersValidator(object):
    """Validator of ``ast.ImportFrom`` nodes names."""

    def __init__(
        self,
        error_callback: ErrorCallback,
        options: ConfigurationOptions,
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
        """
        Counts the number of ``import``.

        Raises:
            TooManyImportedNamesViolation
            TooManyImportsViolation

        """
        self._visit_any_import(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Counts the number of ``from ... import ...``.

        Raises:
            TooManyImported_ModuleMembersViolation
            TooManyImportedNamesViolation
            TooManyImportsViolation

        """
        self._import_from_members_validator.validate(node)
        self._visit_any_import(node)

    def _visit_any_import(self, node: AnyImport) -> None:
        self._imports_count += 1
        self._imported_names_count += len(node.names)
        self.generic_visit(node)

    def _check_imports_count(self) -> None:
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


@final
class ConditionsVisitor(BaseNodeVisitor):
    """Checks booleans for condition counts."""

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """
        Counts the number of conditions.

        Raises:
            TooManyConditionsViolation

        """
        self._check_conditions(node)
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Counts the number of compare parts.

        Raises:
            TooLongCompareViolation

        """
        self._check_compares(node)
        self.generic_visit(node)

    def _count_conditions(self, node: ast.BoolOp) -> int:
        counter = 0
        for condition in node.values:
            if isinstance(condition, ast.BoolOp):
                counter += self._count_conditions(condition)
            else:
                counter += 1
        return counter

    def _check_conditions(self, node: ast.BoolOp) -> None:
        conditions_count = self._count_conditions(node)
        if conditions_count > constants.MAX_CONDITIONS:
            self.add_violation(
                complexity.TooManyConditionsViolation(
                    node,
                    text=str(conditions_count),
                    baseline=constants.MAX_CONDITIONS,
                ),
            )

    def _check_compares(self, node: ast.Compare) -> None:
        is_all_equals = all(isinstance(op, ast.Eq) for op in node.ops)
        is_all_notequals = all(isinstance(op, ast.NotEq) for op in node.ops)
        can_be_longer = is_all_notequals or is_all_equals

        threshold = constants.MAX_COMPARES
        if can_be_longer:
            threshold += 1

        if len(node.ops) > threshold:
            self.add_violation(
                complexity.TooLongCompareViolation(
                    node,
                    text=str(len(node.ops)),
                    baseline=threshold,
                ),
            )


@final
class ElifVisitor(BaseNodeVisitor):
    """Checks the number of ``elif`` cases inside conditions."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates internal ``elif`` counter."""
        super().__init__(*args, **kwargs)
        self._if_children: DefaultDict[ast.If, List[ast.If]] = defaultdict(
            list,
        )

    def visit_If(self, node: ast.If) -> None:
        """
        Checks condition not to reimplement switch.

        Raises:
            TooManyElifsViolation

        """
        self._check_elifs(node)
        self.generic_visit(node)

    def _get_root_if_node(self, node: ast.If) -> ast.If:
        for root, children in self._if_children.items():
            if node in children:
                return root
        return node

    def _update_if_child(self, root: ast.If, node: ast.If) -> None:
        if node is not root:
            self._if_children[root].append(node)
        self._if_children[root].extend(node.orelse)  # type: ignore

    def _check_elifs(self, node: ast.If) -> None:
        has_elif = all(
            isinstance(if_node, ast.If) for if_node in node.orelse
        )

        if has_elif:
            root = self._get_root_if_node(node)
            self._update_if_child(root, node)

    def _post_visit(self):
        for root, children in self._if_children.items():
            real_children_length = len(set(children))
            if real_children_length > constants.MAX_ELIFS:
                self.add_violation(
                    complexity.TooManyElifsViolation(
                        root,
                        text=str(real_children_length),
                        baseline=constants.MAX_ELIFS,
                    ),
                )


@final
class TryExceptVisitor(BaseNodeVisitor):
    """Visits all try/except nodes to ensure that they are not too complex."""

    def visit_Try(self, node: ast.Try) -> None:
        """
        Ensures that try/except is correct.

        Raises:
            TooManyExceptCasesViolation
            TooLongTryBodyViolation

        """
        self._check_except_count(node)
        self._check_try_body_length(node)
        self.generic_visit(node)

    def _check_except_count(self, node: ast.Try) -> None:
        if len(node.handlers) > constants.MAX_EXCEPT_CASES:
            self.add_violation(
                complexity.TooManyExceptCasesViolation(
                    node,
                    text=str(len(node.handlers)),
                    baseline=constants.MAX_EXCEPT_CASES,
                ),
            )

    def _check_try_body_length(self, node: ast.Try) -> None:
        if len(node.body) > self.options.max_try_body_length:
            self.add_violation(
                complexity.TooLongTryBodyViolation(
                    node,
                    text=str(len(node.body)),
                    baseline=self.options.max_try_body_length,
                ),
            )


@final
class YieldTupleVisitor(BaseNodeVisitor):
    """Finds too long ``tuples`` in ``yield`` expressions."""

    def visit_Yield(self, node: ast.Yield) -> None:
        """
        Helper to get all ``yield`` nodes in a function at once.

        Raises:
            TooLongYieldTupleViolation

        """
        self._check_yield_values(node)
        self.generic_visit(node)

    def _check_yield_values(self, node: ast.Yield) -> None:
        if isinstance(node.value, ast.Tuple):
            if len(node.value.elts) > constants.MAX_LEN_YIELD_TUPLE:
                self.add_violation(
                    complexity.TooLongYieldTupleViolation(
                        node,
                        text=str(len(node.value.elts)),
                        baseline=constants.MAX_LEN_YIELD_TUPLE,
                    ),
                )
