# -*- coding: utf-8 -*-

from wemake_python_styleguide.errors.general import FormattedStringViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongStringVisitor(BaseNodeVisitor):
    """Restricts to use `f` strings."""

    def visit_JoinedStr(self, node) -> None:  # type is not defined in ast yet
        """
        Restricts to use `f` strings.

        Raises:
            FormattedStringViolation

        """
        self.add_error(FormattedStringViolation(node))
        self.generic_visit(node)
