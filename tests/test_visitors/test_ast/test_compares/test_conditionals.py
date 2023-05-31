import pytest

from wemake_python_styleguide.violations.consistency import (
    ConstantConditionViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConditionalVisitor,
)

create_variable = """
variable = 1
{0}
"""

if_statement = 'if {0}: ...'
ternary = 'ternary = 0 if {0} else 1'

list_comprehension = """
def container():
    [x for x in [1, 2, 3] if {0}]
"""

set_comprehension = """
def container():
    {{
        x
        for x in [1, 2, 3]
        if {0}
    }}
"""

dict_comprehension = """
def container():
    {{
        x: '1'
        for x in [1, 2, 3]
        if {0}
    }}
"""

gen_comprehension = """
def container():
    (x for x in [1, 2, 3] if {0})
"""


@pytest.mark.parametrize('code', [
    if_statement,
    ternary,
    list_comprehension,
    set_comprehension,
    dict_comprehension,
    gen_comprehension,
])
@pytest.mark.parametrize('comparators', [
    'variable < 3',
    'variable',
    'variable is True',
    'variable is False',
    '[1, 2, 3].size > 3',
    'variable is None',
    'variable is int or not some()',
    '(unique := some()) is True',
])
def test_valid_conditional(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
    mode,
):
    """Testing that conditionals work well."""
    tree = parse_ast_tree(
        mode(create_variable.format(code.format(comparators))),
    )

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    if_statement,
    ternary,
    # list_comprehension,
    # set_comprehension,
    # dict_comprehension,
    # gen_comprehension,
])
@pytest.mark.parametrize('comparators', [
    'True',
    'False',
    'None',
    '4',
    '-4.8',
    '--0.0',
    '"test"',
    "b'bytes'",
    '("string in brackets")',
    '{test : "1"}',
    '{"set"}',
    '("tuple",)',
    '["list"]',
    'variable or False',
    'variable and False',
    'variable or True',
    'variable and True',
    '(unique := True)',
    '(unique := -1)',
])
def test_constant_condition(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
    mode,
):
    """Testing that violations are when using invalid conditional."""
    tree = parse_ast_tree(
        mode(create_variable.format(code.format(comparators))),
    )

    visitor = WrongConditionalVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantConditionViolation])
