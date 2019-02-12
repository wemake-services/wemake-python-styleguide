# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ComplexDefaultValuesViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

function_with_defaults = """
def __init__(
    self,
    tree,
    filename='(none)',
    builtins=None,
    withDoctest={0},
    tokens=(),
):
    pass
"""

bad_default = "'PYFLAKES_DOCTEST' in os.environ"
good_default = 'SHOULD_USE_DOCTEST'


@pytest.mark.parametrize('code', [
    function_with_defaults,
    bad_default,
])
def test_wrong_function_defaults(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that wrong function defaults are forbidden."""
    tree = parse_ast_tree(function_with_defaults.format(bad_default))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexDefaultValuesViolation])


@pytest.mark.parametrize('code', [
    function_with_defaults,
    good_default,
])
def test_correct_function_defaults(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that correct function defaults passes validation."""
    tree = parse_ast_tree(mode(function_with_defaults.format(good_default)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
