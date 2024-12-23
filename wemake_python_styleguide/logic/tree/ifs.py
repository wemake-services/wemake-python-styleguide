import ast
from collections.abc import Iterable, Sequence
from typing import ClassVar, TypeAlias, final

from wemake_python_styleguide.types import AnyIf, AnyNodes

_IfAndElifASTNode: TypeAlias = ast.If | list[ast.stmt]


def has_else(node: ast.If) -> bool:
    """Tells if this node or ``if`` chain ends with an ``else`` statement."""
    return bool(tuple(chain(node))[-1])


def chain(node: ast.If) -> Iterable[_IfAndElifASTNode]:
    """
    Yields the whole chain of ``if`` statements.

    This function also does not go up in the tree
    to find all parent ``if`` nodes. The rest order is preserved.
    The first one to return is the node itself.

    The last element of array is always a list of expressions that represent
    the last ``elif`` or ``else`` node in the chain.
    That's ugly, but that's how ``ast`` works in python.
    """
    iterator: _IfAndElifASTNode = node
    yield iterator

    while True:
        if not isinstance(iterator, ast.If):
            return

        next_if = iterator.orelse
        if len(next_if) == 1 and isinstance(next_if[0], ast.If):
            yield next_if[0]
            iterator = next_if[0]
        else:
            yield next_if
            iterator = next_if


@final
class NegatedIfConditions:
    """Finds negated ``if`` nodes."""

    _negated_ops: ClassVar[AnyNodes] = (
        ast.NotEq,
        ast.IsNot,
        ast.NotIn,
    )

    def __init__(self) -> None:
        """Collects visited nodes not to double report them."""
        self._visited_ifs: set[ast.If] = set()

    def negated_nodes(self, node: AnyIf) -> Sequence[AnyIf]:
        """Returns the list of negated nodes to raise violations on."""
        if isinstance(node, ast.If):
            return self._process_if(node)
        return self._process_ifexpr(node)

    def _process_if(self, node: ast.If) -> Sequence[ast.If]:
        if not has_else(node):
            return []
        negated_nodes = []
        regular_nodes = []
        for subnode in chain(node):
            if not isinstance(subnode, ast.If) or subnode in self._visited_ifs:
                continue
            self._visited_ifs.add(subnode)

            if self._is_negated_if_condition(subnode):
                negated_nodes.append(subnode)
            else:
                regular_nodes.append(subnode)

        if not regular_nodes and len(negated_nodes) > 1:
            return []  # we allow all negated nodes in `if/elif/else`
        return negated_nodes

    def _process_ifexpr(self, node: ast.IfExp) -> Sequence[ast.IfExp]:
        if not self._is_negated_if_condition(node):
            return []
        return [node]

    def _is_negated_if_condition(self, node: AnyIf) -> bool:
        return (
            isinstance(node.test, ast.UnaryOp)
            and isinstance(node.test.op, ast.Not)
        ) or (
            isinstance(node.test, ast.Compare)
            and all(
                isinstance(elem, self._negated_ops) for elem in node.test.ops
            )
        )
