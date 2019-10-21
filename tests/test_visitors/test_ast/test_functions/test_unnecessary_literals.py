# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import LITERALS_BLACKLIST
from wemake_python_styleguide.violations.consistency import (
    UnnecessaryLiteralsViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    UnnecessaryLiteralsVisitor,
)

regular_call_without_args = '{0}()'
regular_call_with_args = '{0}(*args, **kwargs)'


@pytest.mark.parametrize('literal', LITERALS_BLACKLIST)
def test_unnecessary_literals(
    assert_errors,
    parse_ast_tree,
    literal,
    default_options,
    mode,
):
    """Testing that some literals without args are restricted."""
    tree = parse_ast_tree(mode(regular_call_without_args.format(literal)))

    visitor = UnnecessaryLiteralsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnnecessaryLiteralsViolation])


@pytest.mark.parametrize('literal', LITERALS_BLACKLIST)
def test_literals_with_args_called(
    assert_errors,
    parse_ast_tree,
    literal,
    default_options,
    mode,
):
    """Testing that literals with args are not restricted."""
    tree = parse_ast_tree(mode(regular_call_with_args.format(literal)))

    visitor = UnnecessaryLiteralsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
