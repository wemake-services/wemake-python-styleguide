# -*- coding: utf-8 -*-

import ast
from collections import namedtuple
from textwrap import dedent
from typing import Sequence

import pytest

from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


def _maybe_set_parent(tree: ast.AST) -> ast.AST:
    """
    Sets parents for all nodes that do not have this prop.

    This step is required due to how `flake8` works.
    It does not set the same properties as `ast` module.

    This function was the cause of `issue-112`.

    Version changed: 0.0.11

    """
    for statement in ast.walk(tree):
        for child in ast.iter_child_nodes(statement):
            if not hasattr(child, 'parent'):  # noqa: Z112
                setattr(child, 'parent', statement)

    return tree


def _to_dest_option(long_option_name: str) -> str:
    return long_option_name[2:].replace('-', '_')


@pytest.fixture(scope='session')
def parse_ast_tree():
    """Helper function to convert code to ast."""
    def factory(code: str) -> ast.AST:
        return _maybe_set_parent(ast.parse(dedent(code)))

    return factory


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor errors."""
    def factory(visitor: BaseNodeVisitor, errors: Sequence[str]):
        for index, error in enumerate(visitor.errors):
            assert len(errors) > index, visitor.errors
            assert error.code == errors[index].code

        assert len(visitor.errors) == len(errors)

    return factory


@pytest.fixture(scope='session')
def options():
    """Returns the options builder."""
    default_values = {
        _to_dest_option(option.long_option_name): option.default
        for option in Configuration.all_options()
    }

    Options = namedtuple('options', default_values.keys())

    def factory(**kwargs):
        final_options = default_values.copy()
        final_options.update(kwargs)
        return Options(**final_options)

    return factory


@pytest.fixture(scope='session')
def default_options(options):
    """Returns the default options."""
    return options()
