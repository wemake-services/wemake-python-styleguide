# -*- coding: utf-8 -*-

import ast
from collections import Counter
from typing import ClassVar, Iterable, List

import astor
from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics.operators import (
    count_unary_operator,
    get_parent_ignoring_unary,
    unwrap_unary_node,
)
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    IncorrectUnpackingViolation,
    MagicNumberViolation,
    MultipleAssignmentsViolation,
    NonUniqueItemsInSetViolation,
)
from wemake_python_styleguide.violations.consistency import (
    FormattedStringViolation,
    UselessOperatorsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongStringVisitor(BaseNodeVisitor):
    """Restricts to use ``f`` strings."""

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

        # Constructor usages:
        ast.FunctionDef,
        ast.AsyncFunctionDef,
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

    def _check_plus_sign(self, node: ast.Num) -> None:
        if not count_unary_operator(node, ast.UAdd) > 0:
            return
        self.add_violation(UselessOperatorsViolation(node, text=str(node.n)))

    def _check_minus_sign(self, node: ast.Num) -> None:
        if not count_unary_operator(node, ast.USub) > 1:
            return
        self.add_violation(UselessOperatorsViolation(node, text=str(node.n)))

    def _check_tilde_sign(self, node: ast.Num) -> None:
        if not count_unary_operator(node, ast.Invert) > 1:
            return
        self.add_violation(UselessOperatorsViolation(node, text=str(node.n)))

    def _check_not(self, node: ast.Num) -> None:
        if not count_unary_operator(node, ast.Not) > 1:
            return
        self.add_violation(UselessOperatorsViolation(node, text=str(node.n)))

    def visit_Num(self, node: ast.Num) -> None:
        """
        Checks numbers unnecessary operators inside the code.

        Raises:
            UselessOperatorsViolation

        """
        self._check_plus_sign(node)
        self._check_minus_sign(node)
        self._check_tilde_sign(node)
        self._check_not(node)
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
                self.add_violation(IncorrectUnpackingViolation(node))

    def visit_With(self, node: ast.With) -> None:
        """
        Checks assignments inside context managers to be correct.

        Raises:
            IncorrectUnpackingViolation

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
            IncorrectUnpackingViolation

        """
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node, node.target.elts)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Checks assignments to be correct.

        Raises:
            MultipleAssignmentsViolation
            IncorrectUnpackingViolation

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
