import ast
from typing import ClassVar, final

from wemake_python_styleguide.logic import source, walk
from wemake_python_styleguide.logic.naming import name_nodes
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

    _marked_slices: ClassVar[set[ast.Subscript]] = set()

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

        lower_ok = node.slice.lower is None or (
            not self._is_zero(node.slice.lower)
            and not self._is_none(node.slice.lower)
        )

        upper_ok = node.slice.upper is None or not self._is_none(
            node.slice.upper,
        )

        step_ok = node.slice.step is None or (
            not self._is_one(node.slice.step)
            and not self._is_none(node.slice.step)
        )

        if not (lower_ok and upper_ok and step_ok):
            self.add_violation(
                consistency.RedundantSubscriptViolation(
                    node,
                ),
            )

    def _check_slice_assignment(self, node: ast.Subscript) -> None:
        if not isinstance(node.ctx, ast.Store):
            return

        subscript_slice_assignment = isinstance(node.slice, ast.Slice)

        slice_expr = node.slice
        slice_function_assignment = isinstance(
            slice_expr,
            ast.Call,
        ) and functions.given_function_called(slice_expr, {'slice'})

        if subscript_slice_assignment or slice_function_assignment:
            self.add_violation(
                consistency.AssignToSliceViolation(node),
            )

    def _is_none(self, component_value: ast.expr) -> bool:
        return (
            isinstance(component_value, ast.Constant)
            and component_value.value is None
        )

    def _is_zero(self, component_value: ast.expr) -> bool:
        return (
            isinstance(component_value, ast.Constant)
            and component_value.value == 0
        )

    def _is_one(self, component_value: ast.expr) -> bool:
        return (
            isinstance(component_value, ast.Constant)
            and component_value.value == 1
        )


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
        if self._is_float_key(node.slice):
            self.add_violation(best_practices.FloatKeyViolation(node))

    def _check_len_call(self, node: ast.Subscript) -> None:
        node_slice = node.slice
        is_len_call = (
            isinstance(node_slice, ast.BinOp)
            and isinstance(node_slice.op, ast.Sub)
            and self._is_wrong_len(
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
            isinstance(node.left, ast.Call)
            and bool(functions.given_function_called(node.left, {'len'}))
            and source.node_to_string(node.left.args[0]) == element
        )

    def _is_float_key(self, node: ast.expr) -> bool:
        real_node = operators.unwrap_unary_node(node)
        return isinstance(real_node, ast.Constant) and isinstance(
            real_node.value, float
        )


@final
class StricterSliceOperations(base.BaseNodeVisitor):
    """Check for stricter operation with slices."""

    def visit_Slice(self, node: ast.Slice):
        """Check that there is no stricter way to use slices."""
        self._check_reverse_through_slice(node)
        self._check_copy_through_slice(node)
        self._check_pop_through_slice(node)
        self.generic_visit(node)

    def _check_reverse_through_slice(self, node: ast.Slice):
        if walk.get_closest_parent(node, ast.Assign):
            if not (
                node.lower is None
                and node.upper is None
                and node.step is not None
                and self._is_negative_one_const(node.step)
            ):
                return

            self.add_violation(
                best_practices.NonStrictSliceOperationsViolation(node)
            )

    def _check_copy_through_slice(self, node: ast.Slice):
        if walk.get_closest_parent(node, ast.Assign):
            if not (
                node.lower is None and node.upper is None and node.step is None
            ):
                return

            self.add_violation(
                best_practices.NonStrictSliceOperationsViolation(node)
            )

    def _check_pop_through_slice(self, node: ast.Slice):
        assign = walk.get_closest_parent(node, ast.Assign)
        if not (
            isinstance(assign, ast.Assign)
            and node.lower is None
            and node.upper is not None
            and self._is_negative_one_const(node.upper)
        ):
            return

        subscript = walk.get_closest_parent(node, ast.Subscript)
        if not (
            isinstance(subscript, ast.Subscript)
            and isinstance(subscript.value, ast.Name)
        ):
            return

        right_variable_name = subscript.value.id
        for left_variable in name_nodes.flat_variable_names([assign]):
            if left_variable == right_variable_name:
                self.add_violation(
                    best_practices.NonStrictSliceOperationsViolation(node)
                )

    def _is_negative_one_const(self, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.UnaryOp)
            and isinstance(node.op, ast.USub)
            and isinstance(node.operand, ast.Constant)
            and node.operand.value == 1
        )
