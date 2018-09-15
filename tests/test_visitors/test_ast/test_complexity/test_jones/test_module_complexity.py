# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.jones import (
    JonesComplexityVisitor,
    JonesScoreViolation,
)

module_without_nodes = ''
module_with_nodes = """
some = 1 + 2
other = [number for number in range(0, some)]
"""


@pytest.mark.parametrize('code', [
    module_without_nodes,
    module_with_nodes,
])
def test_module_score(assert_errors, parse_ast_tree, code, default_options):
    """Testing that regular nodes do not raise errors."""
    tree = parse_ast_tree(code)

    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    module_without_nodes,
    module_with_nodes,
])
def test_module_score_error(assert_errors, parse_ast_tree, code, options):
    """Testing that regular nodes do raise errors."""
    tree = parse_ast_tree(code)

    option_values = options(max_jones_score=-1)
    visitor = JonesComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [JonesScoreViolation])
