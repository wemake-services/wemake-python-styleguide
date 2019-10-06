# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ApproximateConstantViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongNumberVisitor


@pytest.mark.parametrize('variable_name,variable_value', [
    ('pi', '3.14'),
    ('tau', '6.28'),
    ('e', '2.718'),
    ('my_e', '2.72'),
    ('my_pi', '3.141'),
    ('my_tau', '6.282'),
])
def test_violation_on_approximate_constants(
    assert_errors,
    parse_ast_tree,
    default_options,
    variable_name,
    variable_value,
):
    """Ensures that usage of approximate constants not allowed."""
    tree = parse_ast_tree('{0} = {1}'.format(variable_name, variable_value))
    visitor = WrongNumberVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ApproximateConstantViolation])
