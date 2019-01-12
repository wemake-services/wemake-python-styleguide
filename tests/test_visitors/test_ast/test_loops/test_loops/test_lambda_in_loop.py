# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    LambdaInsideLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

lambda_inside_for_loop = """
def wrapper():
    for index in range(10):
        print(lambda: index)
"""

nested_lambda_inside_for_loop = """
def wrapper():
    for index in range(10):
        if some:
            print(lambda: index)
"""

lambda_inside_while_loop = """
while True:
    print(lambda: index)
"""

nested_lambda_inside_while_loop = """
while True:
    if some:
        print(lambda: index)
"""


@pytest.mark.parametrize('code', [
    lambda_inside_for_loop,
    nested_lambda_inside_for_loop,
    lambda_inside_while_loop,
    nested_lambda_inside_while_loop,
])
def test_lambda_body(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that lambda can not be inside a loop's body."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LambdaInsideLoopViolation])
