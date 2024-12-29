import ast
from typing import ClassVar, final

from wemake_python_styleguide.logic import nodes, walk
from wemake_python_styleguide.logic.tree import (
    compares,
    operators,
    pattern_matching,
)
from wemake_python_styleguide.logic.walrus import get_assigned_expr
from wemake_python_styleguide.types import AnyIf, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    FloatComplexCompareViolation,
    HeterogeneousCompareViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ConstantCompareViolation,
    ConstantConditionViolation,
    MultipleInCompareViolation,
    ReversedComplexCompareViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    FalsyConstantCompareViolation,
    NestedTernaryViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
class CompareSanityVisitor(BaseNodeVisitor):
    """Restricts the incorrect compares."""

    _less_ops: ClassVar[AnyNodes] = (ast.Gt, ast.GtE)

    def visit_Compare(self, node: ast.Compare) -> None:
        """Ensures that compares are written correctly."""
        self._check_literal_compare(node)
        self._check_heterogeneous_operators(node)
        self._check_reversed_complex_compare(node)
        self.generic_visit(node)

    def _check_literal_compare(self, node: ast.Compare) -> None:
        last_was_literal = nodes.is_literal(get_assigned_expr(node.left))
        for comparator in map(get_assigned_expr, node.comparators):
            next_is_literal = nodes.is_literal(comparator)
            if last_was_literal and next_is_literal:
                self.add_violation(ConstantCompareViolation(node))
                break
            last_was_literal = next_is_literal

    def _check_heterogeneous_operators(self, node: ast.Compare) -> None:
        if len(node.ops) == 1:
            return

        prototype = compares.get_similar_operators(node.ops[0])

        for op in node.ops:
            if not isinstance(op, prototype):
                self.add_violation(HeterogeneousCompareViolation(node))
                break

    def _check_reversed_complex_compare(self, node: ast.Compare) -> None:
        if len(node.ops) != 2:
            return

        is_less = all(isinstance(op, self._less_ops) for op in node.ops)
        if not is_less:
            return

        self.add_violation(ReversedComplexCompareViolation(node))


@final
class WrongConstantCompareVisitor(BaseNodeVisitor):
    """Restricts incorrect compares with constants."""

    _eq_compares: ClassVar[AnyNodes] = (
        ast.Eq,
        ast.NotEq,
        ast.Is,
        ast.IsNot,
    )

    def visit_Compare(self, node: ast.Compare) -> None:
        """Visits compare with constants."""
        self._check_constant(node.ops[0], node.left)

        for op, comparator in zip(node.ops, node.comparators, strict=False):
            self._check_constant(op, comparator)

        self.generic_visit(node)

    def _check_constant(self, op: ast.cmpop, comparator: ast.expr) -> None:
        if not isinstance(op, self._eq_compares):
            return
        real = get_assigned_expr(comparator)
        if not isinstance(real, ast.List | ast.Dict | ast.Tuple):
            return
        if walk.get_closest_parent(op, ast.Assert):
            return  # We allow any compares in `assert`

        length = (
            len(real.keys)
            if isinstance(
                real,
                ast.Dict,
            )
            else len(real.elts)
        )

        if not length:
            self.add_violation(FalsyConstantCompareViolation(comparator))


@final
@alias(
    'visit_any_if',
    (
        'visit_If',
        'visit_IfExp',
    ),
)
class WrongConditionalVisitor(BaseNodeVisitor):
    """Finds wrong conditional arguments."""

    _forbidden_nodes: ClassVar[AnyNodes] = (
        # Constants:
        ast.Constant,
        # Collections:
        ast.List,
        ast.Set,
        ast.Dict,
        ast.Tuple,
    )

    _forbidden_expression_parents: ClassVar[AnyNodes] = (
        ast.IfExp,
        ast.BoolOp,
        ast.BinOp,
        ast.UnaryOp,
        ast.Compare,
        ast.comprehension,
    )

    def visit_any_if(self, node: AnyIf) -> None:
        """Ensures that ``if`` nodes are using valid conditionals."""
        self._check_nested_ifexpr(node)
        self._check_constant_condition(node.test)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """Checks all possible comprehensions."""
        for expr in node.ifs:
            self._check_constant_condition(expr)
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        """Ensures that ``match`` nodes are using valid conditionals."""
        self._check_constant_condition(node.subject, is_match=True)
        self.generic_visit(node)

    def _check_constant_condition(
        self,
        node: ast.AST,
        *,
        is_match: bool = False,
    ) -> None:
        if isinstance(node, ast.BoolOp):
            for condition in node.values:
                self._check_constant_condition(condition)
        else:
            real_node = operators.unwrap_unary_node(get_assigned_expr(node))
            if is_match and not pattern_matching.is_constant_subject(real_node):
                return
            if not is_match and not isinstance(
                real_node,
                self._forbidden_nodes,
            ):
                return
            self.add_violation(ConstantConditionViolation(node))

    def _check_nested_ifexpr(self, node: AnyIf) -> None:
        is_nested_in_if = bool(
            isinstance(node, ast.If)
            and list(walk.get_subnodes_by_type(node.test, ast.IfExp)),
        )
        is_nested_poorly = walk.get_closest_parent(
            node,
            self._forbidden_expression_parents,
        )

        if is_nested_in_if or is_nested_poorly:
            self.add_violation(NestedTernaryViolation(node))


@final
class InCompareSanityVisitor(BaseNodeVisitor):
    """Restricts the incorrect ``in`` compares."""

    _in_nodes: ClassVar[AnyNodes] = (
        ast.In,
        ast.NotIn,
    )

    def visit_Compare(self, node: ast.Compare) -> None:
        """Ensures that compares are written correctly."""
        self._check_multiply_compares(node)
        self.generic_visit(node)

    def _check_multiply_compares(self, node: ast.Compare) -> None:
        count = sum(1 for op in node.ops if isinstance(op, self._in_nodes))
        if count > 1:
            self.add_violation(MultipleInCompareViolation(node))


@final
class WrongFloatComplexCompareVisitor(BaseNodeVisitor):
    """Restricts incorrect compares with ``float`` and ``complex``."""

    def visit_Compare(self, node: ast.Compare) -> None:
        """Ensures that compares are written correctly."""
        self._check_float_complex_compare(node)
        self.generic_visit(node)

    def _check_float_complex_compare(self, node: ast.Compare) -> None:
        any_float_or_complex = any(
            self._is_float_or_complex(comparator)
            for comparator in node.comparators
        ) or self._is_float_or_complex(node.left)
        if any_float_or_complex:
            self.add_violation(FloatComplexCompareViolation(node))

    def _is_float_or_complex(self, node: ast.AST) -> bool:
        node = operators.unwrap_unary_node(node)
        return isinstance(node, ast.Constant) and isinstance(
            node.value,
            float | complex,
        )
