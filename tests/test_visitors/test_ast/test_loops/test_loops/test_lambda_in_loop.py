import pytest

from wemake_python_styleguide.violations.best_practices import (
    LambdaInsideLoopViolation,
)
from wemake_python_styleguide.visitors.ast.loops import WrongLoopVisitor

# Wrong:

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

nested_argument_lambda_inside_for_loop = """
def wrapper():
    for index in range(10):
        if some:
            print(lambda index=inde: index)
"""

lambda_inside_while_loop = """
while True:
    print(lambda: index)
    break
"""

nested_lambda_inside_while_loop = """
while True:
    if some:
        print(lambda: index)
    break
"""

lambda_inside_set = """
def wrapper():
    return {lambda x=x: x for x in some()}
"""

lambda_inside_list = """
def wrapper():
    return [lambda x: x for x in some()]
"""

lambda_inside_gen = """
def wrapper():
    return (lambda x: x for x in some())
"""

lambda_inside_dict_key = """
def wrapper():
    return {call(lambda: x): 1 for x in some()}
"""

lambda_inside_dict_value = """
def wrapper():
    return {"x": (lambda: x) for x in some()}
"""

# Correct:

correct_lambda_inside_for = """
def wrapper():
    for some in map(lambda x: x * 2, items):
        ...
"""

correct_lambda_inside_set = """
def wrapper():
    return {x * 2: x for x in map(lambda x: x / 2)}
"""

correct_lambda_inside_list = """
def wrapper():
    return [x for x in some() if callback(lambda: x)]
"""


@pytest.mark.parametrize('code', [
    lambda_inside_for_loop,
    nested_lambda_inside_for_loop,
    nested_argument_lambda_inside_for_loop,
    lambda_inside_while_loop,
    nested_lambda_inside_while_loop,
    lambda_inside_list,
    lambda_inside_set,
    lambda_inside_gen,
    lambda_inside_dict_key,
    lambda_inside_dict_value,
])
def test_lambda_body(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that lambda cannot be inside a loop's body."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LambdaInsideLoopViolation])


@pytest.mark.parametrize('code', [
    correct_lambda_inside_for,
    correct_lambda_inside_list,
    correct_lambda_inside_set,
])
def test_correct_lambda_body(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that lambda can be near loops."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongLoopVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
