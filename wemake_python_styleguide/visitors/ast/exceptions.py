import ast
from collections import Counter
from typing import ClassVar, Set

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
    NonTrivialExceptViolation,
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


@final
class WrongTryExceptVisitor(BaseNodeVisitor):
    """Responsible for examining ``try`` and friends."""

    _bad_returning_nodes: ClassVar[AnyNodes] = (
        ast.Return,
        ast.Raise,
        ast.Break,
    )

    def visit_Try(self, node: ast.Try) -> None:
        """Used for find ``finally`` in ``try`` blocks without ``except``."""
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
        find_returning = exceptions.find_returning_nodes
        try_has, except_has, else_has, finally_has = find_returning(
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
        """Visits all try nodes in the tree."""
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

    _trivial_except_arg_nodes: ClassVar[AnyNodes] = (ast.Name, ast.Attribute)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Checks all ``ExceptionHandler`` nodes."""
        self._check_useless_except(node)
        self._check_exception_type(node)
        self._check_except_expression(node)
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

    def _check_except_expression(self, node: ast.ExceptHandler) -> None:
        # Catch-all 'except' is actually okay in this case
        if node.type is None:
            return

        if isinstance(node.type, self._trivial_except_arg_nodes):
            return

        if isinstance(node.type, ast.Tuple):
            all_elements_are_trivial = all((
                isinstance(element, self._trivial_except_arg_nodes)
                for element in node.type.elts
            ))
            if all_elements_are_trivial:
                return

        self.add_violation(NonTrivialExceptViolation(node.type))
