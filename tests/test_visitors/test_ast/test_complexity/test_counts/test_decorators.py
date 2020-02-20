# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ModuleMembersVisitor,
    TooManyDecoratorsViolation,
)

function_with_decorators = """
@first
@second(param=4)
@third()
def function(): ...
"""

class_with_decorators = """
@first
@second(param=4)
@third()
class Test(object): ...
"""

method_with_decorators = """
class Test(object):
    @first
    @second(param=4)
    @third()
    def method(self): ...
"""

classmethod_with_decorators = """
class Test(object):
    @second(param=4)
    @third()
    @classmethod
    def method(cls): ...
"""


@pytest.mark.parametrize('code', [
    function_with_decorators,
    class_with_decorators,
    method_with_decorators,
    classmethod_with_decorators,
])
def test_decorators_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that correct amount of decorators works."""
    tree = parse_ast_tree(mode(code))

    visitor = ModuleMembersVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_with_decorators,
    class_with_decorators,
    method_with_decorators,
    classmethod_with_decorators,
])
def test_decorators_incorrect(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
    mode,
):
    """Testing that too large amount of decorators works."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_decorators=2)
    visitor = ModuleMembersVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyDecoratorsViolation])
    assert_error_text(visitor, '3', option_values.max_decorators)
