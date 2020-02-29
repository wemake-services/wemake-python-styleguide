# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.compat.constants import PY38
from wemake_python_styleguide.violations.best_practices import (
    ComplexDefaultValueViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

function_with_defaults = """
def function(arg, with_default={0}):
    ...
"""

function_with_posonlydefaults = """
def function(with_default={0}, /):
    ...
"""

function_with_kwdefaults1 = """
def function(*, with_default={0}):
    ...
"""

function_with_kwdefaults2 = """
def function(*, arg, with_default={0}):
    ...
"""

method_with_defaults = """
class Test(object):
    def function(self, with_default={0}):
        ...
"""

method_with_posonlydefaults = """
class Test(object):
    def function(self, with_default={0}, /):
        ...
"""

method_with_kwdefaults = """
class Test(object):
    def function(self, *, with_default={0}):
        ...
"""


@pytest.mark.parametrize('template', [
    function_with_defaults,
    pytest.param(
        function_with_posonlydefaults,
        marks=pytest.mark.skipif(not PY38, reason='posonly appered in 3.8'),
    ),
    function_with_kwdefaults1,
    function_with_kwdefaults2,
    method_with_defaults,
    pytest.param(
        method_with_posonlydefaults,
        marks=pytest.mark.skipif(not PY38, reason='posonly appered in 3.8'),
    ),
    method_with_kwdefaults,
])
@pytest.mark.parametrize('code', [
    "'PYFLAKES_DOCTEST' in os.environ",
    'call()',
    'call().attr',
    '-call()',
    '+call()',
    'index[1]',
    'index["s"]',
    'index[name][name]',
    'index[1].attr',
    '-index[1].attr',
    'index[1].attr.call().sub',
    'compare == 1',
    'var + 2',
    'a and b',
])
def test_wrong_function_defaults(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    code,
    mode,
):
    """Testing that wrong function defaults are forbidden."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ComplexDefaultValueViolation])


@pytest.mark.parametrize('template', [
    function_with_defaults,
    pytest.param(
        function_with_posonlydefaults,
        marks=pytest.mark.skipif(not PY38, reason='posonly appered in 3.8'),
    ),
    function_with_kwdefaults1,
    function_with_kwdefaults2,
    method_with_defaults,
    pytest.param(
        method_with_posonlydefaults,
        marks=pytest.mark.skipif(not PY38, reason='posonly appered in 3.8'),
    ),
    method_with_kwdefaults,
])
@pytest.mark.parametrize('code', [
    "'string'",
    "b''",
    '1',
    '-0',
    'variable',
    '-variable',
    'module.attr',
    '-module.attr',
    '(1, 2)',
    '()',
    'None',
    'True',
    'False',
    '...',
])
def test_correct_function_defaults(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    code,
    mode,
):
    """Testing that correct function defaults passes validation."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
