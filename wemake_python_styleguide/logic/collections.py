# -*- coding: utf-8 -*-

import ast
from functools import partial
from typing import Any, Iterable, List, Sequence, Tuple, Type


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
            elements.append(dict_value)  # type: ignore
        else:
            elements.append(dict_key)
    return elements


def sequence_of_node(
    node_type: Tuple[Type[ast.stmt]],
    sequence: Sequence[ast.stmt],
) -> Iterable[Sequence[ast.stmt]]:
    """Find sequence of node by type."""
    is_desired_type = partial(
        lambda types, input_: isinstance(input_, types), node_type,
    )

    sequence = iter(sequence)
    previous_node = next(sequence, None)
    node_sequence = []

    while previous_node is not None:
        current_node = next(sequence, None)

        if all(map(is_desired_type, (previous_node, current_node))):
            node_sequence.append(previous_node)
        elif node_sequence:
            yield [*node_sequence, previous_node]
            node_sequence = []

        previous_node = current_node


def first(sequence: Iterable[Any], default: Any = None) -> Any:
    """Get first variable from sequence or default."""
    return next(iter(sequence), default)
