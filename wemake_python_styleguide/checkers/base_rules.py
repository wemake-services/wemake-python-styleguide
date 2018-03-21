# -*- coding: utf-8 -*-

import ast
from typing import Generator

from wemake_python_styleguide.checkers.base.checker import BaseChecker
from wemake_python_styleguide.checkers.base.visitor import BaseNodeVisitor
from wemake_python_styleguide.errors import (
    BareRiseViolation,
    RiseNotImplementedViolation,
)


class _WrongRaiseVisitor(BaseNodeVisitor):
    def visit_Raise(self, node: ast.Raise):
        exception = getattr(node, 'exc', None)
        if not exception:
            parent = getattr(node, 'parent')
            if not isinstance(parent, ast.ExceptHandler):
                self.add_error(BareRiseViolation(node))
        else:
            exception_func = getattr(exception, 'func', None)
            if exception_func:
                exception = exception_func

            exception_name = getattr(exception, 'id', None)
            if exception_name == 'NotImplemented':
                self.add_error(
                    RiseNotImplementedViolation(node, text=exception_name),
                )

        self.generic_visit(node)


class BaseRulesChecker(BaseChecker):
    """This class is responsible for finding base rules violations."""

    name = 'wms-base-rules'

    def run(self) -> Generator[tuple, None, None]:
        """Runs the check."""
        visiter = _WrongRaiseVisitor()
        visiter.visit(self.tree)

        # for node in ast.walk(self.tree):
        #     print(node, vars(node))

        for error in visiter.errors:
            lineno, col_offset, message = error.items()
            yield lineno, col_offset, message, type(self)
