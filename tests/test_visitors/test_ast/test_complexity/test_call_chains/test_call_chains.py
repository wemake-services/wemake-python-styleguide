# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooLongCallChainViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.calls import (
    CallChainsVisitor,
)

# incorrect expression
deep_call_chain = 'foo(a)(b)(c)(d)'

# correct expression
call_chain = 'bar(a)(b)'

# border expression
long_call_chain = 'baz(a)(b)(c)'


@pytest.mark.parametrize('code', [
    deep_call_chain,
    call_chain,
    long_call_chain,
])
def test_correct_cases(
    assert_errors,
    parse_ast_tree,
    code,
    options,
    mode,
):
    """Testing that expressions with correct call chain length work well."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_call_level=4)
    visitor = CallChainsVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('code', 'call_level'), [
    (call_chain, 2),
    (deep_call_chain, 4),
    (long_call_chain, 3),
])
def test_incorrect_cases(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    call_level,
    options,
    mode,
):
    """Testing that violations are raised when using a too long call chain."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_call_level=1)
    visitor = CallChainsVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongCallChainViolation])
    assert_error_text(visitor, str(call_level), option_values.max_call_level)
