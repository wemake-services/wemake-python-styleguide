# -*- coding: utf-8 -*-

# TODO: count the number of functions per file/class, classes per file

import ast

from wemake_python_styleguide.errors.complexity import (
    TooManyModuleMembersViolation,
)
from wemake_python_styleguide.logics.functions import is_method
from wemake_python_styleguide.logics.limits import has_just_exceeded_limit
from wemake_python_styleguide.types import ModuleMembers
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class _MembersCounter(object):
    """Helper class to encapsulate logics from the visitor."""

    def __init__(self, delegate: BaseNodeVisitor) -> None:
        self.delegate = delegate
        self.public_items_count = 0

    def check_members_count(self, node: ModuleMembers):
        """This method increases the number of module members."""
        parent = getattr(node, 'parent', None)
        is_class_method = is_method(getattr(node, 'function_type', None))

        if isinstance(parent, ast.Module) and not is_class_method:
            self.public_items_count += 1
            max_members = self.delegate.options.max_module_members
            if has_just_exceeded_limit(self.public_items_count, max_members):
                error = TooManyModuleMembersViolation(
                    node, text=self.delegate.filename,
                )
                self.delegate.add_error(error)


class ModuleMembersVisitor(BaseNodeVisitor):
    """Counts classes and functions in a module."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._counter = _MembersCounter(self)

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Counts the number of `class`es in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._counter.check_members_count(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Counts the number of functions in a single module.

        Raises:
            TooManyModuleMembersViolation

        """
        self._counter.check_members_count(node)
        self.generic_visit(node)
