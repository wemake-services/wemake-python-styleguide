# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors.general import FormattedStringViolation
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongStringVisitor(BaseNodeVisitor):
    """Restricts to use `f` strings."""

    def visit_JoinedStr(self, node: ast.JoinedStr):
        """
        Restricts to use `f` strings.

        Raises:
            FormattedStringViolation

        """
        self.add_error(FormattedStringViolation(node))
        self.generic_visit(node)
