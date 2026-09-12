import pytest

from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.violations.best_practices import (
    WrongDocStringPlacementViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    DocStringPlacementVisitor,
)

module_docstring = "'Docs.'"

function_docstring = """
def some():
    'Docs.'
"""

class_docstring = """
class Some:
    'Docs.'
"""

module_attribute = """
first = 1
'Docs.'
"""

annotated_module_attribute = """
first: int = 1
'Docs.'
"""

class_attribute = """
class Some:
    'Class docs.'

    first = 1
    'Docs.'
"""

instance_attribute = """
class Some:
    def __init__(self):
        'Method docs.'
        self.first = 1
        'Docs.'
"""

type_alias = pytest.param(
    """
    type Some = int
    'Docs.'
    """,
    marks=pytest.mark.skipif(
        not PY312,
        reason='`type` aliases are only in Python 3.12+',
    ),
)

foreign_attribute = """
some.first = 1
'Docs.'
"""

instance_attribute_outside_constructor = """
class Some:
    def method(self):
        'Method docs.'
        self.first = 1
        'Docs.'
"""

local_variable = """
def some():
    'Function docs.'
    first = 1
    'Docs.'
"""

multiple_targets = """
first = second = 1
'Docs.'
"""

inside_condition = """
def some(arg):
    'Function docs.'
    if arg:
        'Docs.'
        return 1
    return 0
"""

after_call = """
def some():
    'Function docs.'
    print(1)
    'Docs.'
"""

after_doc_string = """
def some():
    'Function docs.'
    'Docs.'
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
        type_alias,
    ],
)
def test_documenting_string(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that strings documenting something are allowed."""
    tree = parse_ast_tree(code)

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
def test_string_documenting_nothing(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that strings documenting nothing are forbidden."""
    tree = parse_ast_tree(code)

    visitor = DocStringPlacementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongDocStringPlacementViolation])
