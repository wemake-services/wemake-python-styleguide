import pytest

from wemake_python_styleguide.violations.best_practices import (
    OuterScopeShadowingViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Correct:

correct_for_loop1 = """
import ast

def wrapper():
    for i, j in ():
        print(i, j)
"""

correct_for_loop2 = """
from some import other

def wrapper():
    for i, j in ():
        return i, j
"""

correct_for_loop3 = """
import other

class Test():
    z = 1

def zz():
    z = 2

def wrapper():
    z = 3
    for i, j in ():
        yield i, j, z
"""

correct_for_comprehension = """
def test():
    compare = 0

def context():
    compare = 1
    nodes = [
        print(compare.left)
        for compare in node.values
        if isinstance(compare, ast.Compare)
    ]
"""

correct_except = """
import y

def context():
    e = 1

try:
    ...
except Exception as e:
    print(e)
"""

correct_with1 = """
def wrapper():
    with open() as (first, second):
        print(first, second)

class Test(object):
    first: str

    def __init__(self, second):
        self.first = 1
        self.second = second
"""

correct_with2 = """
def context(first):
    first = first + 1

def wrapper():
    with open() as first:
        print(first)
    print(wrapper)
"""

correct_with3 = """
def wrapper():
    with open() as first:
        print(first)
    print(wrapper)

def other():
    first = 1
    print(first)
"""

correct_class1 = """
class Test(object):
    first: int
    second = 2
    third: int = 3

    def method(self):
        first = 1
        second = 2
        third = 3

    def other(self):
        method = 1
"""

correct_class2 = """
class Test(object):
    first: int
    second = 2
    third: int = 3

    def method(self, first, second, third):
        self.first = first + 1
        self.second = second + 2
        self.third = third + 3
"""

correct_class3 = """
class First(object):
    a = 1

class Second(First):
    a = 2
"""

correct_class4 = """
a = 0

def test():
    ...

class First(object):
    a = 1

    def test(self):
        ...
"""

correct_walrus = """
import some

def function():
    if other := some:
        ...
"""

# Wrong:

import_overlap1 = """
import ast

def some():
    ast = 1
"""

import_overlap2 = """
import ast as ast_import

def some():
    ast_import = 1
"""

import_overlap3 = """
from system import ast

def some(ast):
    ast_import = ast + 1
"""

import_overlap4 = """
from system import ast as ast_import

def some():
    ast_import = ast + 1
"""

function_overlap1 = """
def test():
    ...

def other():
    test = 1
"""

function_overlap2 = """
def test():
    ...

def other(test):
    test1 = test + 1
"""

constant_overlap1 = """
a = 1

def func(a):
    ...
"""

constant_overlap2 = """
a = 1

def func():
    a = 2
"""

constant_overlap3 = """
a = 1

def func():
    for a in some():
        ...
"""

constant_overlap4 = """
a = 1

def func():
    try:
        ...
    except ValueError as a:
        ...
"""

constant_overlap5 = """
a = 1

def func():
    with open() as a:
        ...
"""

constant_overlap6 = """
a = 1

def func():
    import a
"""

walrus_overlap = """
import some

def function():
    if some := other():
        ...
"""


@pytest.mark.parametrize('code', [
    correct_for_loop1,
    correct_for_loop2,
    correct_for_loop3,
    correct_for_comprehension,
    correct_except,
    correct_with1,
    correct_with2,
    correct_with3,
    correct_class1,
    correct_class2,
    correct_class3,
    correct_class4,
    correct_walrus,
])
def test_variable_used_correctly(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that using variables inside a block is correct."""
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    import_overlap1,
    import_overlap2,
    import_overlap3,
    import_overlap4,
    function_overlap1,
    function_overlap2,
    constant_overlap1,
    constant_overlap2,
    constant_overlap3,
    constant_overlap4,
    constant_overlap5,
    constant_overlap6,
    walrus_overlap,
])
def test_outer_variable_shadow(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that shadowing vars are not allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [OuterScopeShadowingViolation])


def test_outer_variable_double_shadow(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that shadowing vars are not allowed."""
    code = """
    a = 1

    def test1():
        a = 2

    def test2(a):
        ...
    """
    tree = parse_ast_tree(mode(code))

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        OuterScopeShadowingViolation,
        OuterScopeShadowingViolation,
    ])
