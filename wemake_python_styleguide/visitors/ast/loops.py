# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, List, Optional, Union

from typing_extensions import final

from wemake_python_styleguide.logic.nodes import get_parent, is_contained
from wemake_python_styleguide.logic.variables import (
    is_valid_block_variable_definition,
)
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    LambdaInsideLoopViolation,
    LoopVariableDefinitionViolation,
    YieldInComprehensionViolation,
)
from wemake_python_styleguide.violations.complexity import (
    TooManyForsInComprehensionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultipleIfsInComprehensionViolation,
    UselessContinueViolation,
    WrongLoopIterTypeViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    UselessLoopElseViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

AnyForLoop = Union[ast.For, ast.AsyncFor]
AnyLoop = Union[ast.For, ast.While, ast.AsyncFor]
AnyComprehension = Union[
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
]


@final
@alias('visit_any_comprehension', (
    'visit_ListComp',
    'visit_DictComp',
    'visit_SetComp',
    'visit_GeneratorExp',
))
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
            parent = get_parent(node) or node
            self.add_violation(MultipleIfsInComprehensionViolation(parent))

    def _check_fors(self, node: ast.comprehension) -> None:
        parent = get_parent(node)
        self._fors[parent] = len(parent.generators)  # type: ignore

    def _check_contains_yield(self, node: AnyComprehension) -> None:
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Yield):
                self.add_violation(YieldInComprehensionViolation(node))

    def _post_visit(self) -> None:
        for node, for_count in self._fors.items():
            if for_count > self._max_fors:
                self.add_violation(TooManyForsInComprehensionViolation(node))

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` and ``for`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation
            TooManyForsInComprehensionViolation

        """
        self._check_ifs(node)
        self._check_fors(node)
        self.generic_visit(node)

    def visit_any_comprehension(self, node: AnyComprehension) -> None:
        """
        Finds incorrect patterns inside comprehensions.

        Raises:
            YieldInComprehensionViolation

        """
        self._check_contains_yield(node)
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
            self.add_violation(UselessLoopElseViolation(node))

    def _check_lambda_inside_loop(self, node: AnyLoop) -> None:
        for subnode in node.body:
            if is_contained(subnode, (ast.Lambda,)):
                self.add_violation(LambdaInsideLoopViolation(node))

    def _check_useless_continue(self, node: AnyLoop) -> None:
        nodes_at_line: DefaultDict[int, List[ast.AST]] = defaultdict(list)
        for sub_node in ast.walk(node):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno is not None:
                nodes_at_line[lineno].append(sub_node)

        last_line = nodes_at_line[sorted(nodes_at_line.keys())[-1]]
        if any(isinstance(last, ast.Continue) for last in last_line):
            self.add_violation(UselessContinueViolation(node))

    def visit_any_loop(self, node: AnyLoop) -> None:
        """
        Checks ``for`` and ``while`` loops.

        Raises:
            UselessLoopElseViolation
            LambdaInsideLoopViolation

        """
        self._check_loop_needs_else(node)
        self._check_lambda_inside_loop(node)
        self._check_useless_continue(node)
        self.generic_visit(node)


@final
@alias('visit_any_for_loop', (
    'visit_For',
    'visit_AsyncFor',
))
class WrongLoopDefinitionVisitor(BaseNodeVisitor):
    """Responsible for ``for`` loops and comprehensions definitions."""

    _forbidden_for_iters: ClassVar[AnyNodes] = (
        ast.List,
        ast.ListComp,
        ast.Dict,
        ast.DictComp,
        ast.Set,
        ast.SetComp,
    )

    def visit_any_for_loop(self, node: AnyForLoop) -> None:
        """
        Ensures that ``for`` loop definitions are correct.

        Raises:
            LoopVariableDefinitionViolation
            WrongLoopIterTypeViolation

        """
        self._check_variable_definitions(node.target)
        self._check_explicit_iter_type(node)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Ensures that comprehension definitions are correct.

        Raises:
            LoopVariableDefinitionViolation

        """
        self._check_variable_definitions(node.target)
        self.generic_visit(node)

    def _check_variable_definitions(self, node: ast.AST) -> None:
        if not is_valid_block_variable_definition(node):
            self.add_violation(LoopVariableDefinitionViolation(node))

    def _check_explicit_iter_type(self, node: AnyForLoop) -> None:
        if isinstance(node.iter, self._forbidden_for_iters):
            self.add_violation(WrongLoopIterTypeViolation(node))
