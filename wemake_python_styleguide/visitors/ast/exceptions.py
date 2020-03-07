import ast
from collections import Counter
from typing import ClassVar, Set, Tuple

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.tree import exceptions
from wemake_python_styleguide.logic.walk import is_contained
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    BaseExceptionViolation,
    DuplicateExceptionViolation,
    IncorrectExceptOrderViolation,
    LoopControlFinallyViolation,
    TryExceptMultipleReturnPathViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UselessExceptCaseViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    NestedTryViolation,
    UselessFinallyViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


def _find_returing_nodes(
    node: ast.Try,
    bad_returning_nodes: AnyNodes,
) -> Tuple[bool, bool, bool, bool]:
    try_has = any(
        is_contained(line, bad_returning_nodes)
        for line in node.body
    )
    except_has = any(
        is_contained(except_handler, bad_returning_nodes)
        for except_handler in node.handlers
    )
    else_has = any(
        is_contained(line, bad_returning_nodes)
        for line in node.orelse
    )
    finally_has = any(
        is_contained(line, bad_returning_nodes)
        for line in node.finalbody
    )
    return try_has, except_has, else_has, finally_has


@final
class WrongTryExceptVisitor(BaseNodeVisitor):
    """Responsible for examining ``try`` and friends."""

    _bad_returning_nodes: ClassVar[AnyNodes] = (
        ast.Return,
        ast.Raise,
        ast.Break,
    )

    def visit_Try(self, node: ast.Try) -> None:
        """
        Used for find ``finally`` in ``try`` blocks without ``except``.

        Raises:
            UselessFinallyViolation
            DuplicateExceptionViolation
            TryExceptMultipleReturnPathViolation
            IncorrectExceptOrderViolation
            LoopControlFinallyViolation

        """
        self._check_if_needs_except(node)
        self._check_duplicate_exceptions(node)
        self._check_return_path(node)
        self._check_exception_order(node)
        self._check_break_or_continue_in_finally(node)
        self.generic_visit(node)

    def _check_if_needs_except(self, node: ast.Try) -> None:
        if not node.finalbody or node.handlers:
            return

        context = nodes.get_context(node)
        if isinstance(context, FunctionNodes) and context.decorator_list:
            # This is used inside a decorated function, it might be the only
            # way to handle this situation. Eg: ``@contextmanager``
            return

        self.add_violation(UselessFinallyViolation(node))

    def _check_duplicate_exceptions(self, node: ast.Try) -> None:
        exceptions_list = exceptions.get_all_exception_names(node)

        for exc_name, count in Counter(exceptions_list).items():
            if count > 1:
                self.add_violation(
                    DuplicateExceptionViolation(node, text=exc_name),
                )

    def _check_return_path(self, node: ast.Try) -> None:
        try_has, except_has, else_has, finally_has = _find_returing_nodes(
            node, self._bad_returning_nodes,
        )

        if finally_has and (try_has or except_has or else_has):
            self.add_violation(TryExceptMultipleReturnPathViolation(node))
        elif else_has and try_has:
            self.add_violation(TryExceptMultipleReturnPathViolation(node))

    def _check_exception_order(self, node: ast.Try) -> None:
        built_in_exceptions = exceptions.traverse_exception(BaseException)
        exceptions_list = exceptions.get_all_exception_names(node)
        seen: Set[str] = set()

        for exception in exceptions_list:
            bases = built_in_exceptions.get(exception)

            if bases is not None:
                if any(base in seen for base in bases):
                    self.add_violation(IncorrectExceptOrderViolation(node))
                else:
                    seen.add(exception)

    def _check_break_or_continue_in_finally(self, node: ast.Try) -> None:
        has_wrong_nodes = any(
            is_contained(line, (ast.Break, ast.Continue))
            for line in node.finalbody
        )

        if has_wrong_nodes:
            self.add_violation(LoopControlFinallyViolation(node))


@final
class NestedTryBlocksVisitor(BaseNodeVisitor):
    """Ensures that there are no nested ``try`` blocks."""

    def visit_Try(self, node: ast.Try) -> None:
        """
        Visits all try nodes in the tree.

        Raises:
            NestedTryViolation

        """
        self._check_nested_try(node)
        self.generic_visit(node)

    def _check_nested_try(self, node: ast.Try) -> None:
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Try) and sub_node is not node:
                self.add_violation(NestedTryViolation(sub_node))


@final
class WrongExceptHandlerVisitor(BaseNodeVisitor):
    """Responsible for examining ``ExceptionHandler``."""

    _base_exception: ClassVar[str] = 'BaseException'

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """
        Checks all ``ExceptionHandler`` nodes.

        Raises:
            BaseExceptionViolation
            UselessExceptCaseViolation

        """
        self._check_useless_except(node)
        self._check_exception_type(node)
        self.generic_visit(node)

    def _check_useless_except(self, node: ast.ExceptHandler) -> None:
        if len(node.body) != 1:
            return

        body = node.body[0]
        if not isinstance(body, ast.Raise):
            return

        if isinstance(body.exc, ast.Call):
            return

        if isinstance(body.exc, ast.Name) and node.name:
            if body.exc.id != node.name:
                return

        self.add_violation(UselessExceptCaseViolation(node))

    def _check_exception_type(self, node: ast.ExceptHandler) -> None:
        exception_name = node.type
        if exception_name is None:
            return

        exception_id = getattr(exception_name, 'id', None)
        if exception_id == self._base_exception:
            self.add_violation(BaseExceptionViolation(node))
