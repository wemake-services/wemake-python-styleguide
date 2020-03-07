import ast
from functools import partial
from typing import (  # noqa: WPS235
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

_NodeType = TypeVar('_NodeType')
_DefaultType = TypeVar('_DefaultType')


def normalize_dict_elements(node: ast.Dict) -> Sequence[ast.AST]:
    """
    Normalizes ``dict`` elements and enforces consistent order.

    We had a problem that some ``dict`` objects might not have some keys.

    Example::

        some_dict = {**one, **two}

    This ``dict`` contains two values and zero keys.
    This function will normalize this structure to use
    values instead of missing keys.

    See also:
        https://github.com/wemake-services/wemake-python-styleguide/issues/450

    """
    elements: List[ast.AST] = []
    for dict_key, dict_value in zip(node.keys, node.values):
        if dict_key is None:
            elements.append(dict_value)
        else:
            elements.append(dict_key)
    return elements


def sequence_of_node(
    node_types: Tuple[Type[_NodeType], ...],
    sequence: Sequence[ast.stmt],
) -> Iterable[Sequence[_NodeType]]:
    """Find sequence of node by type."""
    is_desired_type = partial(
        lambda types, node: isinstance(node, types), node_types,
    )

    sequence_iterator = iter(sequence)
    previous_node = next(sequence_iterator, None)
    node_sequence: List[_NodeType] = []

    while previous_node is not None:
        current_node = next(sequence_iterator, None)

        if all(map(is_desired_type, (previous_node, current_node))):
            node_sequence.append(cast(_NodeType, previous_node))
        elif node_sequence:
            yield [*node_sequence, cast(_NodeType, previous_node)]
            node_sequence = []

        previous_node = current_node


def first(
    sequence: Iterable[_NodeType],
    default: Optional[_DefaultType] = None,
) -> Union[_NodeType, _DefaultType, None]:
    """Get first variable from sequence or default."""
    return next(iter(sequence), default)
