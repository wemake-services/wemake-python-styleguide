# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.order import WrongOrderVisitor

# Templates to be checked

if_with_func_call = """
if len(a) > b:
    return 1
"""

if_with_complex_call1 = """
if random() + index - some > index:
    return 1
"""

if_with_complex_call2 = """
if (index - some) + (x + y) > index:
    return 1
"""

if_with_method_call = """
if index > some_object.get_index():
    return 1
"""

more_than_one_variable = """
if 0 < b < c:
    return 1
"""


@pytest.mark.parametrize('code', [
    if_with_func_call,
    if_with_complex_call1,
    if_with_complex_call2,
    if_with_method_call,
])
def test_functions_methods_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing : no violations with correct comparisons."""
    tree = parse_ast_tree(code)

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    more_than_one_variable,
])
def test_more_variables_comparison(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing : no violations with correct comparisons."""
    tree = parse_ast_tree(code)

    visitor = WrongOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
