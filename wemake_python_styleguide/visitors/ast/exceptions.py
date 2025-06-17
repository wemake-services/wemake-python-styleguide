import ast
from typing import ClassVar, final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.compat.types import AnyTry
from wemake_python_styleguide.logic import nodes
from wemake_python_styleguide.logic.tree import exceptions
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    IncorrectExceptOrderViolation,
    NonTrivialExceptViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    NestedTryViolation,
    UselessFinallyViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias(
    'visit_any_try',
    (
        'visit_Try',
        'visit_TryStar',
    ),
)
class WrongTryExceptVisitor(BaseNodeVisitor):
    """Responsible for examining ``try`` and friends."""

    def visit_any_try(self, node: AnyTry) -> None:
        """Used for find ``finally`` in ``try`` blocks without ``except``."""
        self._check_if_needs_except(node)
        self._check_exception_order(node)
        self.generic_visit(node)

    def _check_if_needs_except(self, node: AnyTry) -> None:
        if not node.finalbody or node.handlers:
            return

        context = nodes.get_context(node)
        if isinstance(context, FunctionNodes) and context.decorator_list:
            # This is used inside a decorated function, it might be the only
            # way to handle this situation. Eg: ``@contextmanager``
            return

        self.add_violation(UselessFinallyViolation(node))

    def _check_exception_order(self, node: AnyTry) -> None:
        built_in_exceptions = exceptions.traverse_exception(BaseException)
        exceptions_list = exceptions.get_all_exception_names(node)
        seen: set[str] = set()

        for exception in exceptions_list:
            bases = built_in_exceptions.get(exception)

            if bases is not None:
                if any(base in seen for base in bases):
                    self.add_violation(IncorrectExceptOrderViolation(node))
                else:
                    seen.add(exception)


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

    _trivial_except_arg_nodes: ClassVar[AnyNodes] = (ast.Name, ast.Attribute)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Checks all ``ExceptionHandler`` nodes."""
        self._check_except_expression(node)
        self.generic_visit(node)

    def _check_except_expression(self, node: ast.ExceptHandler) -> None:
        # Catch-all 'except' is actually okay in this case
        if node.type is None:
            return

        if isinstance(node.type, self._trivial_except_arg_nodes):
            return

        if isinstance(node.type, ast.Tuple):
            all_elements_are_trivial = all(
                isinstance(element, self._trivial_except_arg_nodes)
                for element in node.type.elts
            )
            if all_elements_are_trivial:
                return

        self.add_violation(NonTrivialExceptViolation(node.type))
