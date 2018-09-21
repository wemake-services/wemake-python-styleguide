# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import INIT
from wemake_python_styleguide.errors.general import (
    EmptyModuleViolation,
    InitModuleHasLogicViolation,
)
from wemake_python_styleguide.logics.filenames import is_stem_in_list
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongContentsVisitor(BaseNodeVisitor):
    """Restricts to have empty modules."""

    def _is_init(self) -> bool:
        return is_stem_in_list(self.filename, [INIT])

    def _is_doc_string(self, node: ast.stmt) -> bool:  # TODO: move
        if not isinstance(node, ast.Expr):
            return False
        return isinstance(node.value, ast.Str)

    def _check_module_contents(self, node: ast.Module) -> None:
        if self._is_init():
            return
        if not node.body:
            self.add_error(EmptyModuleViolation(node))

    def _check_init_contents(self, node: ast.Module) -> None:
        if not self._is_init() or not node.body:
            return

        if not self.options.i_control_code:
            return

        if len(node.body) > 1:
            self.add_error(InitModuleHasLogicViolation(node))
            return

        if not self._is_doc_string(node.body[0]):
            self.add_error(InitModuleHasLogicViolation(node))

    def visit_Module(self, node: ast.Module) -> None:
        """
        Checks that module has something other than module definition.

        We have completely different rules
        for ``__init__.py`` and regular files.
        Since, we believe that ``__init__.py`` must be empty.
        But, other files must have contents.

        Raises:
            EmptyModuleViolation
            InitModuleHasLogicViolation

        """
        self._check_init_contents(node)
        self._check_module_contents(node)
        self.generic_visit(node)
