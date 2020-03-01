"""
Jones Complexity to count inline complexity.

Based on the original `jones-complexity` project:
https://github.com/Miserlou/JonesComplexity

Original project is licensed under MIT.
"""

import ast
from collections import defaultdict
from statistics import median
from typing import DefaultDict, List

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.violations.complexity import (
    JonesScoreViolation,
    LineComplexityViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class JonesComplexityVisitor(BaseNodeVisitor):
    """
    This visitor is used to find complex lines in the code.

    Calculates the number of AST nodes per line of code.
    Also calculates the median nodes/line score.
    Then compares these numbers to the given tressholds.

    Some nodes are ignored because there's no sense in analyzing them.
    Some nodes like type annotations are not affecting line complexity,
    so we do not count them.
    """

    _ignored_nodes = (
        ast.ClassDef,
        *FunctionNodes,
        ast.expr_context,
    )

    def __init__(self, *args, **kwargs) -> None:
        """Initializes line number counter."""
        super().__init__(*args, **kwargs)
        self._lines: DefaultDict[int, List[ast.AST]] = defaultdict(list)
        self._to_ignore: List[ast.AST] = []

    def visit(self, node: ast.AST) -> None:
        """
        Visits all nodes, sums the number of nodes per line.

        Then calculates the median value of all line results.

        Raises:
            JonesScoreViolation
            LineComplexityViolation

        """
        line_number = getattr(node, 'lineno', None)
        is_ignored = isinstance(node, self._ignored_nodes)

        if line_number is not None and not is_ignored:
            if not self._maybe_ignore_child(node):
                self._lines[line_number].append(node)

        self.generic_visit(node)

    def _post_visit(self) -> None:
        """
        Triggers after the whole module was processed.

        Checks each line for its complexity, compares it to the tresshold.
        We also calculate the final Jones score for the whole module.
        """
        for line_nodes in self._lines.values():
            complexity = len(line_nodes)
            if complexity > self.options.max_line_complexity:
                self.add_violation(
                    LineComplexityViolation(
                        line_nodes[0],
                        text=str(complexity),
                        baseline=self.options.max_line_complexity,
                    ),
                )

        node_counts = [len(nodes) for nodes in self._lines.values()]
        total_count = median(node_counts) if node_counts else 0

        if total_count > self.options.max_jones_score:
            self.add_violation(
                JonesScoreViolation(
                    text=str(total_count),
                    baseline=self.options.max_jones_score,
                ),
            )

    def _maybe_ignore_child(self, node: ast.AST) -> bool:
        if isinstance(node, ast.AnnAssign):
            self._to_ignore.extend(ast.walk(node.annotation))

        return node in self._to_ignore
