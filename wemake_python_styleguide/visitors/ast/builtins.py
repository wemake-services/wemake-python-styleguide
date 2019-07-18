# -*- coding: utf-8 -*-

import ast
from collections import Counter, defaultdict
from typing import ClassVar, DefaultDict, Iterable, List, Mapping

import astor
from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.operators import (
    count_unary_operator,
    get_parent_ignoring_unary,
    unwrap_unary_node,
)
from wemake_python_styleguide.types import AnyNodes, AnyUnaryOp
from wemake_python_styleguide.violations.best_practices import (
    MagicNumberViolation,
    MultipleAssignmentsViolation,
    NonUniqueItemsInSetViolation,
    WrongUnpackingViolation,
)
from wemake_python_styleguide.violations.complexity import (
    OverusedStringViolation,
)
from wemake_python_styleguide.violations.consistency import (
    FormattedStringViolation,
    UselessOperatorsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongStringVisitor(BaseNodeVisitor):
    """Restricts several string usages."""

    def __init__(self, *args, **kwargs) -> None:
        """Inits the counter for constants."""
        super().__init__(*args, **kwargs)
        self._string_constants: DefaultDict[str, int] = defaultdict(int)

    def _check_string_constant(self, node: ast.Str) -> None:
        annotations = (
            ast.arg,
            ast.AnnAssign,
        )

        parent = get_parent(node)
        if isinstance(parent, annotations) and parent.annotation == node:
            return  # it is argument or variable annotation

        if isinstance(parent, FunctionNodes) and parent.returns == node:
            return  # it is return annotation

        self._string_constants[node.s] += 1

    def _post_visit(self) -> None:
        for string, usage_count in self._string_constants.items():
            if usage_count > self.options.max_string_usages:
                self.add_violation(
                    OverusedStringViolation(text=string or "''"),
                )

    def visit_Str(self, node: ast.Str) -> None:
        """
        Restricts to over-use string constants.

        Raises:
            OverusedStringViolation

        """
        self._check_string_constant(node)
        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        """
        Restricts to use ``f`` strings.

        Raises:
            FormattedStringViolation

        """
        self.add_violation(FormattedStringViolation(node))
        self.generic_visit(node)


@final
class MagicNumberVisitor(BaseNodeVisitor):
    """Checks magic numbers used in the code."""

    _allowed_parents: ClassVar[AnyNodes] = (
        ast.Assign,
        ast.AnnAssign,

        # Constructor usages:
        *FunctionNodes,
        ast.arguments,

        # Primitives:
        ast.List,
        ast.Dict,
        ast.Set,
        ast.Tuple,
    )

    def _check_is_magic(self, node: ast.Num) -> None:
        parent = get_parent_ignoring_unary(node)
        if isinstance(parent, self._allowed_parents):
            return

        if node.n in constants.MAGIC_NUMBERS_WHITELIST:
            return

        if isinstance(node.n, int) and node.n <= constants.NON_MAGIC_MODULO:
            return

        self.add_violation(MagicNumberViolation(node, text=str(node.n)))

    def visit_Num(self, node: ast.Num) -> None:
        """
        Checks numbers not to be magic constants inside the code.

        Raises:
            MagicNumberViolation

        """
        self._check_is_magic(node)
        self.generic_visit(node)


@final
class UselessOperatorsVisitor(BaseNodeVisitor):
    """Checks operators used in the code."""

    _limits: ClassVar[Mapping[AnyUnaryOp, int]] = {
        ast.UAdd: 0,
        ast.Invert: 1,
        ast.Not: 1,
        ast.USub: 1,
    }

    def _check_operator_count(self, node: ast.Num) -> None:
        for node_type, limit in self._limits.items():
            if count_unary_operator(node, node_type) > limit:
                self.add_violation(
                    UselessOperatorsViolation(node, text=str(node.n)),
                )

    def visit_Num(self, node: ast.Num) -> None:
        """
        Checks numbers unnecessary operators inside the code.

        Raises:
            UselessOperatorsViolation

        """
        self._check_operator_count(node)
        self.generic_visit(node)


@final
class WrongAssignmentVisitor(BaseNodeVisitor):
    """Visits all assign nodes."""

    def _check_assign_targets(self, node: ast.Assign) -> None:
        if len(node.targets) > 1:
            self.add_violation(MultipleAssignmentsViolation(node))

    def _check_unpacking_targets(
        self,
        node: ast.AST,
        targets: Iterable[ast.AST],
    ) -> None:
        for target in targets:
            if isinstance(target, ast.Starred):
                target = target.value
            if not isinstance(target, ast.Name):
                self.add_violation(WrongUnpackingViolation(node))

    def visit_With(self, node: ast.With) -> None:
        """
        Checks assignments inside context managers to be correct.

        Raises:
            WrongUnpackingViolation

        """
        for withitem in node.items:
            if isinstance(withitem.optional_vars, ast.Tuple):
                self._check_unpacking_targets(
                    node, withitem.optional_vars.elts,
                )
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """
        Checks assignments inside ``for`` loops to be correct.

        Raises:
            WrongUnpackingViolation

        """
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node, node.target.elts)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Checks assignments to be correct.

        Raises:
            MultipleAssignmentsViolation
            WrongUnpackingViolation

        """
        self._check_assign_targets(node)
        if isinstance(node.targets[0], ast.Tuple):
            self._check_unpacking_targets(node, node.targets[0].elts)
        self.generic_visit(node)


@final
class WrongCollectionVisitor(BaseNodeVisitor):
    """Ensures that collection definitions are correct."""

    _elements_in_sets: ClassVar[AnyNodes] = (
        ast.Str,
        ast.Bytes,
        ast.Num,
        ast.NameConstant,
        ast.Name,
    )

    def _report_set_elements(self, node: ast.Set, elements: List[str]) -> None:
        for element, count in Counter(elements).items():
            if count > 1:
                self.add_violation(
                    NonUniqueItemsInSetViolation(node, text=element),
                )

    def _check_set_elements(self, node: ast.Set) -> None:
        elements: List[str] = []
        for set_item in node.elts:
            real_set_item = unwrap_unary_node(set_item)
            if isinstance(real_set_item, self._elements_in_sets):
                source = astor.to_source(set_item)
                elements.append(source.strip().strip('(').strip(')'))
        self._report_set_elements(node, elements)

    def visit_Set(self, node: ast.Set) -> None:
        """
        Ensures that set literals do not have any duplicate items.

        Raises:
            NonUniqueItemsInSetViolation

        """
        self._check_set_elements(node)
        self.generic_visit(node)
