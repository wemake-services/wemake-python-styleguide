# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    MultipleIfsInComprehensionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongListComprehensionVisitor,
)

# Lists:
async_wrapper = """
async def d():
    {comprehension}
    """

list_ifs_multiple = """
nodes = [node {async_stmt}for node in 'abc' if node != 'a' if node != 'b' if node != 'c']
"""

list_ifs_twice = """
nodes = [node {async_stmt}for node in 'abc' if node != 'a' if node != 'b']
"""

list_ifs_single = """
nodes = [node {async_stmt}for node in 'abc' if node != 'a']
"""

list_without_ifs = """
nodes = [node {async_stmt}for node in 'abc']
"""

# Dicts:

dict_ifs_multiple = """
nodes = {{xy: xy {async_stmt}for xy in 'abc' if xy != 'a' if xy != 'b' if xy != 'c'}}
"""

dict_ifs_twice = """
nodes = {{xy: xy {async_stmt}for xy in 'abc' if xy != 'a' if xy != 'b'}}
"""

dict_ifs_single = """
nodes = {{xy: xy {async_stmt}for xy in 'abc' if xy != 'a'}}
"""

dict_without_ifs = """
nodes = {{xy: xy {async_stmt}for xy in 'abc'}}
"""

# Generator expressions:

gen_ifs_multiple = """
nodes = (xy {async_stmt}for xy in 'abc' if xy != 'a' if xy != 'b' if xy != 'c')
"""

gen_ifs_twice = """
nodes = (xy {async_stmt}for xy in 'abc' if xy != 'a' if xy != 'b')
"""

gen_ifs_single = """
nodes = (xy {async_stmt}for xy in 'abc' if xy != 'a')
"""

gen_without_ifs = """
nodes = (no {async_stmt}for xy in 'abc')
"""

# Set comprehensions:

set_ifs_multiple = """
nodes = {{xy {async_stmt}for xy in 'abc' if xy != 'a' if xy != 'b' if xy != 'c'}}
"""

set_ifs_twice = """
nodes = {{xy {async_stmt}for xy in 'abc' if xy != 'a' if xy != 'b'}}
"""

set_ifs_single = """
nodes = {{xy {async_stmt}for xy in 'abc' if xy != 'a'}}
"""

set_without_ifs = """
nodes = {{xy {async_stmt}for xy in 'abc'}}
"""


@pytest.mark.parametrize('code', [
    list_ifs_single,
    list_without_ifs,
    dict_ifs_single,
    dict_without_ifs,
    gen_ifs_single,
    gen_without_ifs,
    set_ifs_single,
    set_without_ifs,
])
@pytest.mark.parametrize('is_async', [True, False])
def test_if_keyword_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    is_async,
    default_options,
):
    """Testing that using `if` keyword is allowed."""
    if is_async:
        code = code.format(async_stmt='async ').lstrip()  # remove heading \n symbol
        code = async_wrapper.format(comprehension=code)
    else:
        code = code.format(async_stmt='')
    tree = parse_ast_tree(code)

    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    list_ifs_multiple,
    list_ifs_twice,
    dict_ifs_multiple,
    dict_ifs_twice,
    gen_ifs_multiple,
    gen_ifs_twice,
    set_ifs_multiple,
    set_ifs_twice,
])
@pytest.mark.parametrize('is_async', [True, False])
def test_multiple_if_keywords_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    is_async,
    default_options,
):
    """Testing that using multiple `if` keywords is restricted."""
    if is_async:
        code = code.format(async_stmt='async ').lstrip()  # remove heading \n symbol
        code = async_wrapper.format(comprehension=code)
    else:
        code = code.format(async_stmt='')
    tree = parse_ast_tree(code)

    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleIfsInComprehensionViolation])
