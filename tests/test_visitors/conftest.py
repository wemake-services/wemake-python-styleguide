# -*- coding: utf-8 -*-

import ast
from collections import namedtuple
from textwrap import dedent
from typing import Sequence

import pytest

from wemake_python_styleguide.compat import maybe_set_parent
from wemake_python_styleguide.options import defaults
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor

Options = namedtuple('options', [
    'max_arguments',
    'max_expressions',
    'max_local_variables',
    'max_returns',
    'min_variable_length',
    'max_offset_blocks',
])


@pytest.fixture(scope='session')
def parse_ast_tree():
    """Helper function to convert code to ast."""
    def factory(code: str) -> ast.AST:
        return maybe_set_parent(ast.parse(dedent(code)))

    return factory


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor errors."""
    def factory(visiter: BaseNodeVisitor, errors: Sequence[str]):
        for index, error in enumerate(visiter.errors):
            assert len(errors) > index, visiter.errors
            assert error._code == errors[index]._code

        assert len(visiter.errors) == len(errors)

    return factory


@pytest.fixture(scope='session')
def options():
    """Returns the options builder."""
    def factory(**kwargs):
        default_values = {
            'max_arguments': defaults.MAX_ARGUMENTS,
            'max_expressions': defaults.MAX_EXPRESSIONS,
            'max_local_variables': defaults.MAX_LOCAL_VARIABLES,
            'max_returns': defaults.MAX_RETURNS,
            'min_variable_length': defaults.MIN_VARIABLE_LENGTH,
            'max_offset_blocks': defaults.MAX_OFFSET_BLOCKS,
        }

        default_values.update(kwargs)
        return Options(**default_values)

    return factory


@pytest.fixture(scope='session')
def default_options(options):
    """Returns the default options."""
    return options()
