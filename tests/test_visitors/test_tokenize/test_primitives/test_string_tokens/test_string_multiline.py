import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UselessMultilineStringViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    MultilineStringVisitor,
)

multiline_single = """'''
abc
'''"""

multiline_double = '''"""
abc
"""'''

# Docstrings:

module_docstring_single = "'''{0}'''"
module_docstring_double = '"""{0}"""'

class_docstring_single = """
class Test:
    '''{0}'''
"""

class_docstring_double = '''
class Test:
    """{0}"""
'''

method_docstring_single = """
class Test:
    def __init__(self):
        '''{0}'''
"""

method_docstring_double = '''
class Test:
    def __init__(self):
        """{0}"""
'''

function_docstring_single = """
def test():
    '''{0}'''
"""

function_docstring_double = '''
def test():
    """{0}"""
'''

attribute_docstring_double1 = '''
class A:
    x: int
    """{0}"""
'''

attribute_docstring_double2 = '''
class A:
    x: int
    """
    {0}
    """
'''


@pytest.mark.parametrize(
    'primitive',
    [
        '"""abc"""',
        "'''abc'''",
        '""""""',
        "r'''abc.'''",
        'b"""some"""',
    ],
)
def test_incorrect_multiline_strings(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that incorrect multiline strings are forbidden."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = MultilineStringVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(
        visitor,
        [UselessMultilineStringViolation],
        ignored_types=WrongMultilineStringUseViolation,
    )


@pytest.mark.parametrize(
    'primitive',
    [
        '""',
        "''",
        '"Big text"',
        "'Format 123'",
        multiline_single,
        multiline_double,
    ],
)
def test_correct_multiline_string(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that correct multiline strings are allowed."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = MultilineStringVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [], ignored_types=WrongMultilineStringUseViolation)


@pytest.mark.parametrize(
    'code',
    [
        module_docstring_single,
        module_docstring_double,
        class_docstring_single,
        class_docstring_double,
        method_docstring_single,
        method_docstring_double,
        function_docstring_single,
        function_docstring_double,
        attribute_docstring_double1,
        attribute_docstring_double2,
    ],
)
@pytest.mark.parametrize(
    'primitive',
    [
        '',  # empty,
        'abc',  # one line
        'one\ntwo',  # multiline
    ],
)
def test_correct_multiline_docstrings(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    primitive,
    mode,
):
    """Ensures that correct singleline and multiline docstrings are allowed."""
    file_tokens = parse_tokens(mode(code.format(primitive)))

    visitor = MultilineStringVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
