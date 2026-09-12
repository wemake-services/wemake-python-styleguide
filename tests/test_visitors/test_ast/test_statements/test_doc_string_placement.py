import pytest

from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.violations.best_practices import (
    WrongDocStringPlacementViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    DocStringPlacementVisitor,
)

module_docstring = '{0}'

function_docstring = """
def some():
    {0}
"""

class_docstring = """
class Some:
    {0}
"""

module_attribute = """
first = 1
{0}
"""

annotated_module_attribute = """
first: int = 1
{0}
"""

class_attribute = """
class Some:
    'Class docs.'

    first = 1
    {0}
"""

instance_attribute = """
class Some:
    def __init__(self):
        'Method docs.'
        self.first = 1
        {0}
"""

instance_attribute_in_new = """
class Some:
    def __new__(cls):
        'Method docs.'
        cls.first = 1
        {0}
"""

type_alias = pytest.param(
    """
    type Some = int
    {0}
    """,
    marks=pytest.mark.skipif(
        not PY312,
        reason='`type` aliases are only in Python 3.12+',
    ),
)

foreign_attribute = """
some.first = 1
{0}
"""

instance_attribute_outside_constructor = """
class Some:
    def method(self):
        'Method docs.'
        self.first = 1
        {0}
"""

local_variable = """
def some():
    'Function docs.'
    first = 1
    {0}
"""

multiple_targets = """
first = second = 1
{0}
"""

inside_condition = """
def some(arg):
    'Function docs.'
    if arg:
        {0}
        return 1
    return 0
"""

after_call = """
def some():
    'Function docs.'
    print(1)
    {0}
"""

after_doc_string = """
def some():
    'Function docs.'
    {0}
"""


@pytest.mark.parametrize(
    'code',
    [
        module_docstring,
        function_docstring,
        class_docstring,
        module_attribute,
        annotated_module_attribute,
        class_attribute,
        instance_attribute,
        instance_attribute_in_new,
        type_alias,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"Doc"',
        "'Doc'",
        '"""Doc"""',
        "'''Doc'''",
    ],
)
def test_documenting_string(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    string_value,
):
    """Testing that strings documenting something are allowed."""
    tree = parse_ast_tree(code.format(string_value))

    visitor = DocStringPlacementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        foreign_attribute,
        instance_attribute_outside_constructor,
        local_variable,
        multiple_targets,
        inside_condition,
        after_call,
        after_doc_string,
    ],
)
@pytest.mark.parametrize(
    'string_value',
    [
        '"Doc"',
        "'Doc'",
        '"""Doc"""',
        "'''Doc'''",
    ],
)
def test_string_documenting_nothing(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    string_value,
):
    """Testing that strings documenting nothing are forbidden."""
    tree = parse_ast_tree(code.format(string_value))

    visitor = DocStringPlacementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongDocStringPlacementViolation])
