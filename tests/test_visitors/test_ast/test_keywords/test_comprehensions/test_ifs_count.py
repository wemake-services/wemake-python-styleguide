# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    MultipleIfsInComprehensionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongComprehensionVisitor,
)

# Lists:

list_ifs_multiple = """
def container():
    nodes = [xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c"]
"""

list_ifs_twice = """
def container():
    nodes = [xy for xy in "abc" if xy != "a" if xy != "b"]
"""

list_ifs_single = """
def container():
    nodes = [xy for xy in "abc" if xy != "a"]
"""

list_without_ifs = """
def container():
    nodes = [xy for xy in "abc"]
"""

# Dicts:

dict_ifs_multiple = """
def container():
    nodes = {xy: xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c"}
"""

dict_ifs_twice = """
def container():
    nodes = {xy: xy for xy in "abc" if xy != "a" if xy != "b"}
"""

dict_ifs_single = """
def container():
    nodes = {xy: xy for xy in "abc" if xy != "a"}
"""

dict_without_ifs = """
def container():
    nodes = {xy: xy for xy in "abc"}
"""

# Generator expressions:

gen_ifs_multiple = """
def container():
    nodes = (xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c")
"""

gen_ifs_twice = """
def container():
    nodes = (xy for xy in "abc" if xy != "a" if xy != "b")
"""

gen_ifs_single = """
def container():
    nodes = (xy for xy in "abc" if xy != "a")
"""

gen_without_ifs = """
def container():
    nodes = (no for xy in "abc")
"""

# Set comprehensions:

set_ifs_multiple = """
def container():
    nodes = {xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c"}
"""

set_ifs_twice = """
def container():
    nodes = {xy for xy in "abc" if xy != "a" if xy != "b"}
"""

set_ifs_single = """
def container():
    nodes = {xy for xy in "abc" if xy != "a"}
"""

set_without_ifs = """
def container():
    nodes = {xy for xy in "abc"}
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
def test_if_keyword_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using `if` keyword is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongComprehensionVisitor(default_options, tree=tree)
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
def test_multiple_if_keywords_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that using multiple `if` keywords is restricted."""
    tree = parse_ast_tree(mode(code))
    visitor = WrongComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleIfsInComprehensionViolation])
