# -*- coding: utf-8 -*-

import libcst
from libcst.metadata import PositionProvider
from typing_extensions import final

from wemake_python_styleguide.violations.consistency import (
    UnnecessarySpaceAroundDotViolation,
)
from wemake_python_styleguide.visitors.base import BaseCSTVisitor


def _not_empty_whitespace(node: libcst.BaseParenthesizableWhitespace) -> bool:
    """Tells if this node value contains whitespaces."""
    return (
        isinstance(node, libcst.SimpleWhitespace) and bool(node.value)
    )


@final
class AttributeCSTVisitor(BaseCSTVisitor):
    """Ensures that attributes are used correctly."""

    def visit_Attribute(self, node: libcst.Attribute) -> None:
        """
        Checks the `Attribute` node.

        Raises:
            UnnecessarySpaceAroundDotViolation

        """
        self._check_dot(node.dot)

    def _check_dot(self, node: libcst.Dot) -> None:
        """Checks whitespaces around the dot."""
        has_whitespace = (
            _not_empty_whitespace(node.whitespace_before) or
            _not_empty_whitespace(node.whitespace_after)
        )

        if has_whitespace:
            self.add_violation(UnnecessarySpaceAroundDotViolation(
                self.get_metadata(PositionProvider, node),
            ))
