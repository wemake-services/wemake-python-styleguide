import ast
from typing import Set

from typing_extensions import final

from wemake_python_styleguide.compat.functions import get_slice_expr
from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.tree import functions, operators, slices
from wemake_python_styleguide.violations import (
    best_practices,
    consistency,
    refactoring,
)
from wemake_python_styleguide.visitors import base


@final
class SubscriptVisitor(base.BaseNodeVisitor):
    """Checks subscripts used in the code."""

    _marked_slices: Set[ast.Subscript] = set()

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Visits subscript."""
        self._check_redundant_subscript(node)

        if node in self._marked_slices:
            # Violation for that specific slice was already triggered earlier
            self._marked_slices.remove(node)
        else:
            self._check_consecutive_slices(node)

        self._check_slice_assignment(node)
        self.generic_visit(node)

    def _check_consecutive_slices(self, node: ast.Subscript):
        if not isinstance(node.slice, ast.Slice):
            return

        if not isinstance(node.value, ast.Subscript):
            return

        if not isinstance(node.value.slice, ast.Slice):
            return

        self.add_violation(best_practices.ConsecutiveSlicesViolation(node))

        # We do not want to trigger duplicate violations for each subsequent
        # subscript in the same chain, so we proactively mark them so
        # that visitor can skip them in the future.
        current_sub = node.value
        while isinstance(current_sub.value, ast.Subscript):
            if not isinstance(current_sub.value.slice, ast.Slice):
                break

            self._marked_slices.add(current_sub)
            current_sub = current_sub.value

    def _check_redundant_subscript(self, node: ast.Subscript) -> None:
        if not isinstance(node.slice, ast.Slice):
            return

        lower_ok = (
            node.slice.lower is None or (
                not self._is_zero(node.slice.lower) and
                not self._is_none(node.slice.lower)
            )
        )

        upper_ok = (
            node.slice.upper is None or
            not self._is_none(node.slice.upper)
        )

        step_ok = (
            node.slice.step is None or (
                not self._is_one(node.slice.step) and
                not self._is_none(node.slice.step)
            )
        )

        if not (lower_ok and upper_ok and step_ok):
            self.add_violation(
                consistency.RedundantSubscriptViolation(
                    node, text=str(node),
                ),
            )

    def _check_slice_assignment(self, node: ast.Subscript) -> None:
        if not isinstance(node.ctx, ast.Store):
            return

        subscript_slice_assignment = isinstance(node.slice, ast.Slice)

        slice_expr = get_slice_expr(node)
        slice_function_assignment = (
            isinstance(slice_expr, ast.Call) and
            functions.given_function_called(slice_expr, {'slice'})
        )

        if subscript_slice_assignment or slice_function_assignment:
            self.add_violation(
                consistency.AssignToSliceViolation(node),
            )

    def _is_none(self, component_value: ast.expr) -> bool:
        return (
            isinstance(component_value, ast.NameConstant) and
            component_value.value is None
        )

    def _is_zero(self, component_value: ast.expr) -> bool:
        return isinstance(component_value, ast.Num) and component_value.n == 0

    def _is_one(self, component_value: ast.expr) -> bool:
        return isinstance(component_value, ast.Num) and component_value.n == 1


@final
class ImplicitDictGetVisitor(base.BaseNodeVisitor):
    """Checks for correct ``.get`` usage in code."""

    def visit_If(self, node: ast.If) -> None:
        """Checks the compares."""
        self._check_implicit_get(node)
        self.generic_visit(node)

    def _check_implicit_get(self, node: ast.If) -> None:
        if not isinstance(node.test, ast.Compare):
            return
        if not isinstance(node.test.ops[0], ast.In):
            return

        checked_key = source.node_to_string(node.test.left)
        checked_collection = source.node_to_string(node.test.comparators[0])

        for sub in ast.walk(node):
            if not isinstance(sub, ast.Subscript):
                continue

            if slices.is_same_slice(checked_collection, checked_key, sub):
                self.add_violation(refactoring.ImplicitDictGetViolation(sub))


@final
class CorrectKeyVisitor(base.BaseNodeVisitor):
    """Checks for correct keys usage in your code."""

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Checks that key usage is correct, without any errors."""
        self._check_float_key(node)
        self._check_len_call(node)
        self.generic_visit(node)

    def _check_float_key(self, node: ast.Subscript) -> None:
        if self._is_float_key(get_slice_expr(node)):
            self.add_violation(best_practices.FloatKeyViolation(node))

    def _check_len_call(self, node: ast.Subscript) -> None:
        node_slice = get_slice_expr(node)
        is_len_call = (
            isinstance(node_slice, ast.BinOp) and
            isinstance(node_slice.op, ast.Sub) and
            self._is_wrong_len(
                node_slice,
                source.node_to_string(node.value),
            )
        )

        if is_len_call:
            self.add_violation(
                refactoring.ImplicitNegativeIndexViolation(node),
            )

    def _is_wrong_len(self, node: ast.BinOp, element: str) -> bool:
        return (
            isinstance(node.left, ast.Call) and
            bool(functions.given_function_called(node.left, {'len'})) and
            source.node_to_string(node.left.args[0]) == element
        )

    def _is_float_key(self, node: ast.expr) -> bool:
        real_node = operators.unwrap_unary_node(node)
        return (
            isinstance(real_node, ast.Num) and
            isinstance(real_node.n, float)
        )
