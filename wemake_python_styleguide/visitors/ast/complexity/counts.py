# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict

from wemake_python_styleguide.errors.complexity import (
    TooManyImportsViolation,
    TooManyMethodsViolation,
    TooManyModuleMembersViolation,
)
from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.types import AnyImport, ModuleMembers
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


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
            self.add_error(TooManyModuleMembersViolation())

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Counts the number of `class`es in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._check_members_count(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Counts the number of functions in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._check_members_count(node)
        self.generic_visit(node)


class ImportMembersVisitor(BaseNodeVisitor):
    """Counts imports in a module."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._imports_count = 0

    def _post_visit(self) -> None:
        if self._imports_count > self.options.max_imports:
            self.add_error(
                TooManyImportsViolation(text=str(self._imports_count)),
            )

    def visit_Import(self, node: AnyImport) -> None:
        """
        Counts the number of ``import`` and ``from ... import ...``.

        Raises:
            TooManyImportsViolation

        """
        self._imports_count += 1
        self.generic_visit(node)

    visit_ImportFrom = visit_Import


class MethodMembersVisitor(BaseNodeVisitor):
    """Counts methods in a single class."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked methods in different classes."""
        super().__init__(*args, **kwargs)
        self._methods: DefaultDict[ast.ClassDef, int] = defaultdict(int)

    def _check_method(self, node: ast.FunctionDef) -> None:
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.ClassDef):
            self._methods[parent] += 1

    def _post_visit(self) -> None:
        for node, count in self._methods.items():
            if count > self.options.max_methods:
                self.add_error(TooManyMethodsViolation(text=node.name))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Counts the number of methods in a single class.

        Raises:
            TooManyMethodsViolation

        """
        self._check_method(node)
        self.generic_visit(node)
