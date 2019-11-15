# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    ConsecutiveYieldsViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    GeneratorKeywordsVisitor,
)

# Correct:

simple_yield = """
def some():
    yield 1
"""

conditional_yield1 = """
def some():
    yield 1
    if some:
        yield 2
"""

conditional_yield2 = """
def some():
    if some:
        yield 1
    yield 2
"""

seprated_yield1 = """
def some():
    yield 1
    print('---')
    yield 2
"""

seprated_yield2 = """
def some():
    yield 1
    print('---')
    yield 2
    print('---')
    yield 3
"""

yield_with_yield_from1 = """
def some():
    yield 1
    yield from (2, 3)
"""

yield_with_yield_from2 = """
def some():
    yield from (1, 2)
    yield 3
"""

# Wrong:

wrong_yield1 = """
def some():
    yield 1
    yield 2
"""

wrong_yield2 = """
def some():
    yield 1
    yield 2
    yield 3
"""

wrong_yield3 = """
def some():
    if some:
        yield 1
    yield 2
    yield 3
"""

wrong_yield4 = """
def some():
    if some:
        yield 1
        yield 2
    yield 3
"""

wrong_yield5 = """
def some():
    if some:
        yield 1
        yield 2
        yield 3
"""


@pytest.mark.parametrize('code', [
    simple_yield,
    conditional_yield1,
    conditional_yield2,
    seprated_yield1,
    seprated_yield2,
    yield_with_yield_from1,
    yield_with_yield_from2,
])
def test_yield_correct(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Ensure that `yield` can be used correctly."""
    tree = parse_ast_tree(mode(code))

    visitor = GeneratorKeywordsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_yield1,
    wrong_yield2,
    wrong_yield3,
    wrong_yield4,
    wrong_yield5,
])
def test_yield_inccorect(
    assert_errors,
    parse_ast_tree,
    code,
    mode,
    default_options,
):
    """Ensure that `yield` cannot follow the same node."""
    tree = parse_ast_tree(mode(code))

    visitor = GeneratorKeywordsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveYieldsViolation])
