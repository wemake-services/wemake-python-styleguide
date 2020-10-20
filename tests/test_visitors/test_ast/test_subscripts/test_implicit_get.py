import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitDictGetViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import (
    ImplicitDictGetVisitor,
)

if_template1 = """
if {0}:
    {1}
"""

if_template2 = """
if {0}:
    {1}
else:
    ...
"""

if_template3 = """
if some:
    ...
elif {0}:
    {1}
else:
    ...
"""

if_template4 = """
if some:
    ...
elif {0}:
    {1}
"""

if_template5 = """
if some:
    ...
elif {0}:
    {1}
elif other:
    ...
"""


@pytest.mark.parametrize('template', [
    if_template1,
    if_template2,
    if_template3,
    if_template4,
    if_template5,
])
@pytest.mark.parametrize(('compare', 'expression'), [
    ('"key" in some_dict', 'some_dict["key"]'),
    ('1 in some_dict', 'some_dict[1]'),

    ('key in some_dict', 'some_dict[key]'),
    ('attr.key in some_dict', 'some_dict[attr.key]'),
    ('call() in some_dict', 'some_dict[call()]'),
    ('call(1, 2, 3) in some_dict', 'some_dict[call(1, 2, 3)]'),
    ('some[index] in some_dict', 'some_dict[some[index]]'),
])
def test_implicit_dict_get(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    compare,
    expression,
):
    """Testing that implicit `.get` is detected."""
    tree = parse_ast_tree(template.format(compare, expression))

    visitor = ImplicitDictGetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitDictGetViolation])


@pytest.mark.parametrize('template', [
    if_template1,
    if_template2,
    if_template3,
    if_template4,
    if_template5,
])
@pytest.mark.parametrize(('compare', 'expression'), [
    ('"key" not in some_dict', 'some_dict["key"]'),
    ('1 in some_dict', 'some_dict["1"]'),
    ('"key" in some_dict', 'some_dict[key]'),

    ('key in some_dict', 'some_other_dict[key]'),
    ('attr.key in some_dict', 'some_dict.get(attr.key)'),
    ('call() in some_dict', 'some_dict[call(1, 2, 3)]'),
    ('call(1, 2, 3) in some_dict', 'some_dict[call(1, 2)]'),
    ('some[index] in some_dict', 'some_dict[some]'),
])
def test_correct_if(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    compare,
    expression,
):
    """Testing that correct `if` can be used."""
    tree = parse_ast_tree(template.format(compare, expression))

    visitor = ImplicitDictGetVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
