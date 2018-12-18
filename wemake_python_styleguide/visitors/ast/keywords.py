# -*- coding: utf-8 -*-

import ast
from collections import Counter, defaultdict
from typing import ClassVar, DefaultDict, List, Optional, Union

import astor

from wemake_python_styleguide.logics.nodes import is_contained
from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
    DuplicateExceptionViolation,
    LambdaInsideLoopViolation,
    RaiseNotImplementedViolation,
    RedundantFinallyViolation,
    RedundantLoopElseViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.violations.complexity import (
    TooManyForsInComprehensionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultipleContextManagerAssignmentsViolation,
    MultipleIfsInComprehensionViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

AnyLoop = Union[ast.For, ast.While, ast.AsyncFor]
AnyWith = Union[ast.With, ast.AsyncWith]


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
class WrongComprehensionVisitor(BaseNodeVisitor):
    """Checks comprehensions for correctness."""

    _max_ifs: ClassVar[int] = 1
    _max_fors: ClassVar[int] = 2

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._fors: DefaultDict[ast.AST, int] = defaultdict(int)

    def _check_ifs(self, node: ast.comprehension) -> None:
        if len(node.ifs) > self._max_ifs:
            # We are trying to fix line number in the report,
            # since `comprehension` does not have this property.
            parent = getattr(node, 'parent', node)
            self.add_violation(MultipleIfsInComprehensionViolation(parent))

    def _check_fors(self, node: ast.comprehension) -> None:
        parent = getattr(node, 'parent', node)
        self._fors[parent] = len(parent.generators)

    def _post_visit(self) -> None:
        for node, for_count in self._fors.items():
            if for_count > self._max_fors:
                self.add_violation(TooManyForsInComprehensionViolation(node))

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` and ``for`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation,
            TooManyForsInComprehensionViolation,

        """
        self._check_ifs(node)
        self._check_fors(node)
        self.generic_visit(node)


@final
@alias('visit_any_loop', (
    'visit_For',
    'visit_While',
    'visit_AsyncFor',
))
class WrongLoopVisitor(BaseNodeVisitor):
    """Responsible for examining loops."""

    def _does_loop_contain_node(  # TODO: move, reuse in annotations.py
        self,
        loop: Optional[AnyLoop],
        to_check: ast.Break,
    ) -> bool:
        if loop is None:
            return False

        for inner_node in ast.walk(loop):
            # We are checking this specific node, not just any `break`:
            if to_check is inner_node:
                return True
        return False

    def _has_break(self, node: AnyLoop) -> bool:
        closest_loop = None

        for subnode in ast.walk(node):
            if isinstance(subnode, (ast.For, ast.AsyncFor, ast.While)):
                if subnode is not node:
                    closest_loop = subnode

            if isinstance(subnode, ast.Break):
                is_nested_break = self._does_loop_contain_node(
                    closest_loop, subnode,
                )
                if not is_nested_break:
                    return True
        return False

    def _check_loop_needs_else(self, node: AnyLoop) -> None:
        if node.orelse and not self._has_break(node):
            self.add_violation(RedundantLoopElseViolation(node))

    def _check_lambda_inside_loop(self, node: AnyLoop) -> None:
        for subnode in node.body:
            if is_contained(subnode, (ast.Lambda,)):
                self.add_violation(LambdaInsideLoopViolation(node))

    def visit_any_loop(self, node: AnyLoop) -> None:
        """
        Checks ``for`` and ``while`` loops.

        Raises:
            RedundantLoopElseViolation
            LambdaInsideLoopViolation

        """
        self._check_loop_needs_else(node)
        self._check_lambda_inside_loop(node)
        self.generic_visit(node)


@final
class WrongTryExceptVisitor(BaseNodeVisitor):
    """Responsible for examining ``try`` and friends."""

    _base_exception: ClassVar[str] = 'BaseException'

    def _check_if_needs_except(self, node: ast.Try) -> None:
        if node.finalbody and not node.handlers:
            self.add_violation(RedundantFinallyViolation(node))

    def _check_exception_type(self, node: ast.ExceptHandler) -> None:
        exception_name = getattr(node, 'type', None)
        if exception_name is None:
            return

        exception_id = getattr(exception_name, 'id', None)
        if exception_id == self._base_exception:
            self.add_violation(BaseExceptionViolation(node))

    def _check_duplicate_exceptions(self, node: ast.Try) -> None:
        exceptions: List[str] = []
        for exc_handler in node.handlers:
            # There might be complex things hidden inside an exception type,
            # so we want to get the string representation of it:
            if isinstance(exc_handler.type, ast.Name):
                exceptions.append(astor.to_source(exc_handler.type).strip())
            elif isinstance(exc_handler.type, ast.Tuple):
                exceptions.extend([
                    astor.to_source(node).strip()
                    for node in exc_handler.type.elts
                ])

        counts = Counter(exceptions)
        for exc_name, count in counts.items():
            if count > 1:
                self.add_violation(
                    DuplicateExceptionViolation(node, text=exc_name),
                )

    def visit_Try(self, node: ast.Try) -> None:
        """
        Used for find finally in try blocks without except.

        Raises:
            RedundantFinallyViolation
            DuplicateExceptionViolation

        """
        self._check_if_needs_except(node)
        self._check_duplicate_exceptions(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Checks all ``ExceptionHandler`` nodes.

        Raises:
            BaseExceptionViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)


@final
@alias('visit_any_with', (
    'visit_With',
    'visit_AsyncWith',
))
class WrongContextManagerVisitor(BaseNodeVisitor):
    """Checks context managers."""

    def _check_target_assignment(self, node: AnyWith):
        if len(node.items) > 1:
            self.add_violation(
                MultipleContextManagerAssignmentsViolation(node),
            )

    def visit_any_with(self, node: AnyWith) -> None:
        """
        Checks the number of assignments for context managers.

        Raises:
            MultipleContextManagerAssignmentsViolation

        """
        self._check_target_assignment(node)
        self.generic_visit(node)
