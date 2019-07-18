# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, List, Union

from typing_extensions import final

from wemake_python_styleguide.constants import MAX_LEN_YIELD_TUPLE
from wemake_python_styleguide.logic.functions import is_method
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyFunctionDef, AnyImport
from wemake_python_styleguide.violations.complexity import (
    TooLongCompareViolation,
    TooLongYieldTupleViolation,
    TooManyConditionsViolation,
    TooManyDecoratorsViolation,
    TooManyElifsViolation,
    TooManyExceptCasesViolation,
    TooManyImportsViolation,
    TooManyMethodsViolation,
    TooManyModuleMembersViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

ConditionNodes = Union[ast.If, ast.While, ast.IfExp]
ModuleMembers = Union[AnyFunctionDef, ast.ClassDef]


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

    def _check_members_count(self, node: ModuleMembers) -> None:
        """This method increases the number of module members."""
        is_real_method = is_method(getattr(node, 'function_type', None))

        if isinstance(get_parent(node), ast.Module) and not is_real_method:
            self._public_items_count += 1

    def _check_decorators_count(self, node: ModuleMembers) -> None:
        number_of_decorators = len(node.decorator_list)
        if number_of_decorators > self.options.max_decorators:
            self.add_violation(
                TooManyDecoratorsViolation(
                    node, text=str(number_of_decorators),
                ),
            )

    def _post_visit(self) -> None:
        if self._public_items_count > self.options.max_module_members:
            self.add_violation(
                TooManyModuleMembersViolation(
                    text=str(self._public_items_count),
                ),
            )

    def visit_module_members(self, node: ModuleMembers) -> None:
        """
        Counts the number of ModuleMembers in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._check_decorators_count(node)
        self._check_members_count(node)
        self.generic_visit(node)


@final
@alias('visit_any_import', (
    'visit_ImportFrom',
    'visit_Import',
))
class ImportMembersVisitor(BaseNodeVisitor):
    """Counts imports in a module."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._imports_count = 0

    def _post_visit(self) -> None:
        if self._imports_count > self.options.max_imports:
            self.add_violation(
                TooManyImportsViolation(text=str(self._imports_count)),
            )

    def visit_any_import(self, node: AnyImport) -> None:
        """
        Counts the number of ``import`` and ``from ... import ...``.

        Raises:
            TooManyImportsViolation

        """
        self._imports_count += 1
        self.generic_visit(node)


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class MethodMembersVisitor(BaseNodeVisitor):
    """Counts methods in a single class."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked methods in different classes."""
        super().__init__(*args, **kwargs)
        self._methods: DefaultDict[ast.ClassDef, int] = defaultdict(int)

    def _check_method(self, node: AnyFunctionDef) -> None:
        parent = get_parent(node)
        if isinstance(parent, ast.ClassDef):
            self._methods[parent] += 1

    def _post_visit(self) -> None:
        for node, count in self._methods.items():
            if count > self.options.max_methods:
                self.add_violation(
                    TooManyMethodsViolation(node, text=str(count)),
                )

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Counts the number of methods in a single class.

        Raises:
            TooManyMethodsViolation

        """
        self._check_method(node)
        self.generic_visit(node)


@final
class ConditionsVisitor(BaseNodeVisitor):
    """Checks booleans for condition counts."""

    #: Maximum number of conditions in a single ``if`` or ``while`` statement.
    _max_conditions: ClassVar[int] = 4

    #: Maximum number of compare nodes in a single expression.
    _max_compares: ClassVar[int] = 2

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
        if conditions_count > self._max_conditions:
            self.add_violation(
                TooManyConditionsViolation(node, text=str(conditions_count)),
            )

    def _check_compares(self, node: ast.Compare) -> None:
        is_all_equals = all(isinstance(op, ast.Eq) for op in node.ops)
        is_all_notequals = all(isinstance(op, ast.NotEq) for op in node.ops)
        can_be_longer = is_all_notequals or is_all_equals

        treshold = self._max_compares
        if can_be_longer:
            treshold += 1

        if len(node.ops) > treshold:
            self.add_violation(
                TooLongCompareViolation(node, text=str(len(node.ops))),
            )

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


@final
class ElifVisitor(BaseNodeVisitor):
    """Checks the number of ``elif`` cases inside conditions."""

    #: Maximum number of `elif` blocks in a single `if` condition:
    _max_elifs: ClassVar[int] = 3

    def __init__(self, *args, **kwargs) -> None:
        """Creates internal ``elif`` counter."""
        super().__init__(*args, **kwargs)
        self._if_children: DefaultDict[ast.If, List[ast.If]] = defaultdict(list)

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
            if real_children_length > self._max_elifs:
                self.add_violation(
                    TooManyElifsViolation(root, text=str(real_children_length)),
                )

    def visit_If(self, node: ast.If) -> None:
        """
        Checks condition not to reimplement switch.

        Raises:
            TooManyElifsViolation

        """
        self._check_elifs(node)
        self.generic_visit(node)


@final
class TryExceptVisitor(BaseNodeVisitor):
    """Visits all try/except nodes to ensure that they are not too complex."""

    #: Maximum number of ``except`` cases in a single ``try`` clause.
    _max_except_cases: ClassVar[int] = 3

    def _check_except_count(self, node: ast.Try) -> None:
        if len(node.handlers) > self._max_except_cases:
            self.add_violation(TooManyExceptCasesViolation(node))

    def visit_Try(self, node: ast.Try) -> None:
        """
        Ensures that try/except is correct.

        Raises:
            TooManyExceptCasesViolation

        """
        self._check_except_count(node)
        self.generic_visit(node)


@final
class YieldTupleVisitor(BaseNodeVisitor):
    """Finds too long ``tuples`` in ``yield`` expressions."""

    def _check_yield_values(self, node: ast.Yield) -> None:
        if isinstance(node.value, ast.Tuple):
            yield_list = [tup_item for tup_item in node.value.elts]
            if len(yield_list) > MAX_LEN_YIELD_TUPLE:
                self.add_violation(
                    TooLongYieldTupleViolation(
                        node, text=str(len(yield_list)),
                    ),
                )

    def visit_Yield(self, node: ast.Yield) -> None:
        """
        Helper to get all ``yield`` nodes in a function at once.

        Raises:
            TooLongYieldTupleViolation

        """
        self._check_yield_values(node)
        self.generic_visit(node)
