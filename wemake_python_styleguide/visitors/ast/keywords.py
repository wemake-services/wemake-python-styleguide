# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, Optional, Union

from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
    RaiseNotImplementedViolation,
    RedundantFinallyViolation,
    RedundantForElseViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.violations.complexity import (
    TooManyForsInComprehensionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultipleIfsInComprehensionViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor

AnyLoop = Union[ast.For, ast.While]


@final
class _ComprehensionComplexityCounter(object):
    """Helper class to encapsulate logic from the visitor."""

    def __init__(self) -> None:
        self.fors: DefaultDict[ast.ListComp, int] = defaultdict(int)

    def check_fors(self, node: ast.comprehension) -> None:
        parent = getattr(node, 'parent', node)
        if isinstance(parent, ast.ListComp):
            self.fors[parent] = len(parent.generators)


@final
class WrongRaiseVisitor(BaseNodeVisitor):
    """Finds wrong ``raise`` keywords."""

    def _check_exception_type(self, node: ast.Raise) -> None:
        exception = getattr(node, 'exc', None)
        if exception is None:
            return

        exception_func = getattr(exception, 'func', None)
        if exception_func:
            exception = exception_func

        exception_name = getattr(exception, 'id', None)
        if exception_name == 'NotImplemented':
            self.add_violation(RaiseNotImplementedViolation(node))

    def visit_Raise(self, node: ast.Raise) -> None:
        """
        Checks how ``raise`` keyword is used.

        Raises:
            RaiseNotImplementedViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)


@final
class WrongKeywordVisitor(BaseNodeVisitor):
    """Finds wrong keywords."""

    _forbidden_keywords: ClassVar[AnyNodes] = (
        ast.Pass,
        ast.Delete,
        ast.Global,
        ast.Nonlocal,
    )

    def _check_keyword(self, node: ast.AST) -> None:
        if isinstance(node, self._forbidden_keywords):
            self.add_violation(WrongKeywordViolation(node))

    def visit(self, node: ast.AST) -> None:
        """
        Used to find wrong keywords.

        Raises:
            WrongKeywordViolation

        """
        self._check_keyword(node)
        self.generic_visit(node)


@final
class WrongListComprehensionVisitor(BaseNodeVisitor):
    """Checks list comprehensions."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._counter = _ComprehensionComplexityCounter()

    def _check_ifs(self, node: ast.comprehension) -> None:
        if len(node.ifs) > 1:
            # We are trying to fix line number in the report,
            # since `comprehension` does not have this property.
            parent = getattr(node, 'parent', node)
            self.add_violation(MultipleIfsInComprehensionViolation(parent))

    def _check_fors(self) -> None:
        for node, for_count in self._counter.fors.items():
            if for_count > 2:
                self.add_violation(TooManyForsInComprehensionViolation(node))

    def _post_visit(self) -> None:
        self._check_fors()

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` and ``for`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation,
            TooManyForsInComprehensionViolation,

        """
        self._check_ifs(node)
        self._counter.check_fors(node)
        self.generic_visit(node)


@final
class WrongForElseVisitor(BaseNodeVisitor):
    """Responsible for restricting `else` in `for` loops without `break`."""

    def _does_loop_contain_node(
        self,
        loop: Optional[AnyLoop],
        to_check: ast.Break,
    ) -> bool:
        if loop is None:
            return False

        for inner_node in ast.walk(loop):
            if to_check is inner_node:
                return True
        return False

    def _has_break(self, node: ast.For) -> bool:
        closest_loop = None

        for subnode in ast.walk(node):
            if isinstance(subnode, (ast.For, ast.While)):
                if subnode is not node:
                    closest_loop = subnode

            if isinstance(subnode, ast.Break):
                is_nested_break = self._does_loop_contain_node(
                    closest_loop, subnode,
                )
                if not is_nested_break:
                    return True
        return False

    def _check_for_needs_else(self, node: ast.For) -> None:
        if node.orelse and not self._has_break(node):
            self.add_violation(RedundantForElseViolation(node=node))

    def visit_For(self, node: ast.For) -> None:
        """Used for find `else` block in `for` loops without `break`."""
        self._check_for_needs_else(node)
        self.generic_visit(node)


@final
class WrongTryFinallyVisitor(BaseNodeVisitor):
    """Responsible for restricting finally in try blocks without except."""

    def _check_for_needs_except(self, node: ast.Try) -> None:
        if node.finalbody and not node.handlers:
            self.add_violation(RedundantFinallyViolation(node=node))

    def visit_Try(self, node: ast.Try) -> None:
        """Used for find finally in try blocks without except."""
        self._check_for_needs_except(node)
        self.generic_visit(node)


@final
class WrongExceptionTypeVisitor(BaseNodeVisitor):
    """Finds usage of incorrect ``except`` exception types."""

    _base_exception: ClassVar[str] = 'BaseException'

    def _check_exception_type(self, node: ast.ExceptHandler) -> None:
        exception_name = getattr(node, 'type', None)
        if exception_name is None:
            return

        exception_id = getattr(exception_name, 'id', None)
        if exception_id == self._base_exception:
            self.add_violation(BaseExceptionViolation(node))

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Checks all ``ExceptionHandler`` nodes.

        Raises:
            BaseExceptionViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)
