# -*- coding: utf-8 -*-

import ast
from textwrap import dedent
from typing import Sequence

import pytest

from wemake_python_styleguide.compat import maybe_set_parent
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


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
