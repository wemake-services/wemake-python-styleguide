# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict, Union

from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.types import AnyFunctionDef, AnyImport, final
from wemake_python_styleguide.violations.complexity import (
    TooManyConditionsViolation,
    TooManyImportsViolation,
    TooManyMethodsViolation,
    TooManyModuleMembersViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

ConditionNodes = Union[ast.If, ast.While, ast.IfExp]
ModuleMembers = Union[ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef]


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
        parent = getattr(node, 'parent', None)
        is_real_method = is_method(getattr(node, 'function_type', None))

        if isinstance(parent, ast.Module) and not is_real_method:
            self._public_items_count += 1

    def _post_visit(self) -> None:
        if self._public_items_count > self.options.max_module_members:
            self.add_violation(TooManyModuleMembersViolation())

    def visit_module_members(self, node: ModuleMembers) -> None:
        """
        Counts the number of ModuleMembers in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
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
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.ClassDef):
            self._methods[parent] += 1

    def _post_visit(self) -> None:
        for node, count in self._methods.items():
            if count > self.options.max_methods:
                self.add_violation(
                    TooManyMethodsViolation(node, text=node.name),
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
@alias('visit_condition', (
    'visit_While',
    'visit_IfExp',
    'visit_If',
))
class ConditionsVisitor(BaseNodeVisitor):
    """Checks ``if`` and ``while`` statements for condition counts."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked conditions."""
        super().__init__(*args, **kwargs)
        self._conditions: DefaultDict[ast.AST, int] = defaultdict(int)

    def _check_conditions(self, node: ast.AST) -> None:
        for condition in ast.walk(node):
            if isinstance(condition, (ast.And, ast.Or)):
                self._conditions[node] += 1

    def _post_visit(self) -> None:
        for node, count in self._conditions.items():
            if count > self.options.max_conditions - 1:
                self.add_violation(
                    TooManyConditionsViolation(node, text=str(count)),
                )

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Counts the number of conditions in list comprehensions.

        Raises:
            TooManyConditionsViolation

        """
        if node.ifs:
            # We only check the first `if`, since it is forbidden
            # to have more than one at a time
            # by `MultipleIfsInComprehensionViolation`
            self._check_conditions(node.ifs[0])
        self.generic_visit(node)

    def visit_condition(self, node: ConditionNodes) -> None:
        """
        Counts the number of conditions.

        Raises:
            TooManyConditionsViolation

        """
        self._check_conditions(node.test)
        self.generic_visit(node)
