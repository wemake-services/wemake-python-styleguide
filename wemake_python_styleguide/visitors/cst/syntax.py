# -*- coding: utf-8 -*-

from typing_extensions import final
from libcst import Attribute, Dot
from libcst.metadata import PositionProvider

from wemake_python_styleguide.logic.cst import not_empty_whitespace
from wemake_python_styleguide.visitors.base import BaseCSTVisitor
from wemake_python_styleguide.violations.consistency import (
    UnnecessarySpaceAroundDotViolation,
)


@final
class AttributeCSTVisitor(BaseCSTVisitor):
    """"""

    def visit_Attribute(self, node: Attribute) -> None:
        """
        Checks whitespace around the dot.

        Raises:
            UnnecessarySpaceAroundDotViolation

        """
        self._check_dot(node.dot)

    def _check_dot(self, node: Dot) -> None:
        has_whitespace = (
            not_empty_whitespace(node.whitespace_before) or
            not_empty_whitespace(node.whitespace_after)
        )

        if has_whitespace:
            self.add_violation(UnnecessarySpaceAroundDotViolation(
                self.get_metadata(PositionProvider, node)))
