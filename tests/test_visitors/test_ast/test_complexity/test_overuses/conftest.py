"""Fixtures for testing string overuse."""

import ast

import pytest


def _create_string_literal(
    string: str, prefix: str = ''
) -> str | bytes:  # pragma: no cover
    node_value: str | bytes = ast.parse(prefix + string, mode='eval').body.value
    return node_value


def _node_location(
    tree: ast.Module, node_value: str | bytes
) -> tuple | None:  # pragma: no cover
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and node.value == node_value:
            return node.lineno, node.col_offset
    raise ValueError(
        'No constant node with given value found', tree, node_value
    )


@pytest.fixture(scope='session')
def overused_string_expected_location():
    """Function to find first constant node with given value."""

    def factory(
        tree: ast.Module, string: str, prefix: str = ''
    ) -> tuple | None:
        node_value = _create_string_literal(string, prefix)
        return _node_location(tree, node_value)

    return factory
