# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import DefaultDict

from wemake_python_styleguide.errors.complexity import (
    TooManyMethodsViolation,
    TooManyModuleMembersViolation,
)
from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.logics.limits import has_just_exceeded_limit
from wemake_python_styleguide.types import ModuleMembers
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class ModuleMembersVisitor(BaseNodeVisitor):
    """Counts classes and functions in a module."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._public_items_count = 0

    def _check_members_count(self, node: ModuleMembers):
        """This method increases the number of module members."""
        parent = getattr(node, 'parent', None)
        is_real_method = is_method(getattr(node, 'function_type', None))

        if isinstance(parent, ast.Module) and not is_real_method:
            self._public_items_count += 1
            max_members = self.options.max_module_members
            if has_just_exceeded_limit(self._public_items_count, max_members):
                self.add_error(
                    TooManyModuleMembersViolation(node, text=self.filename),
                )

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Counts the number of `class`es in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._check_members_count(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Counts the number of functions in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._check_members_count(node)
        self.generic_visit(node)


class MethodMembersVisitor(BaseNodeVisitor):
    """Counts methods in a single class."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked methods in different classes."""
        super().__init__(*args, **kwargs)
        self._methods: DefaultDict[ast.ClassDef, int] = defaultdict(int)

    def _check_method(self, node: ast.FunctionDef):
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.ClassDef):
            self._methods[parent] += 1
            max_methods = self.options.max_methods
            if has_just_exceeded_limit(self._methods[parent], max_methods):
                self.add_error(TooManyMethodsViolation(node, text=parent.name))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Counts the number of methods in a single class.

        Raises:
            TooManyMethodsViolation

        """
        self._check_method(node)
        self.generic_visit(node)
