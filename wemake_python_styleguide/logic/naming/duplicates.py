import ast
from collections import defaultdict
from functools import reduce
from typing import DefaultDict

from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.tree.functions import given_function_called


def duplicated_isinstance_call(node: ast.BoolOp) -> list[str]:
    """Finds duplicate `isinstance` calls from `isinstance(a, ...) and ...`."""
    counter: DefaultDict[str, int] = defaultdict(int)

    for call in node.values:
        if not isinstance(call, ast.Call) or len(call.args) != 2:
            continue

        if not given_function_called(call, {'isinstance'}):
            continue

        isinstance_object = source.node_to_string(call.args[0])
        counter[isinstance_object] += 1

    return [
        node_name
        for node_name, count in counter.items()
        if count > 1
    ]


def get_duplicate_names(variables: list[set[str]]) -> set[str]:
    """
    Find duplicate names in different nodes.

    >>> get_duplicate_names([{'a', 'b'}, {'b', 'c'}])
    {'b'}
    """
    return reduce(
        lambda acc, element: acc.intersection(element),
        variables,
    )
