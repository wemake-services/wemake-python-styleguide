import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    MultilineStringVisitor,
)

correct_assignment1 = '''
a = """abc
abc
"""
'''

correct_assignment2 = '''
a = """
abc
abc
"""
'''

correct_assignment3 = '''
a = """
abc
abc"""
'''

correct_docstring = '''
def test():
    """abc"""
'''

correct_multiline_docstring1 = '''
def test():
    """abc

    abc."""
'''

correct_multiline_docstring2 = '''
def test():
    """abc

    abc.
    """
'''

correct_multiline_docstring3 = '''
def test():
    """
    abc

    abc.
    """
'''

correct_sphinx_docs1 = '''
class Dataclass:
    x: int
    """Attribute docstring."""
'''

correct_sphinx_docs2 = '''
class Dataclass:
    x: int
    """Attribute
       docstring."""
'''

correct_sphinx_docs3 = '''
class Dataclass:
    x: int
    """
    Attribute
    docstring."""
'''

correct_sphinx_docs4 = '''
class Dataclass:
    x: int
    """
    Attribute
    docstring.
    """
'''

correct_function_call_newline1 = '''
f(
    """ab
    cd""",
)
'''

correct_function_call_newline2 = '''
f(
    name="""ab
    cd""",
)
'''


@pytest.mark.parametrize(
    'code',
    [
        correct_assignment1,
        correct_assignment2,
        correct_assignment3,
        correct_docstring,
        correct_multiline_docstring1,
        correct_multiline_docstring2,
        correct_multiline_docstring3,
        correct_sphinx_docs1,
        correct_sphinx_docs2,
        correct_sphinx_docs3,
        correct_sphinx_docs4,
        correct_function_call_newline1,
        correct_function_call_newline2,
    ],
)
def test_correct_multiline_string_use(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct multiline strings uses work."""
    file_tokens = parse_tokens(code)

    visitor = MultilineStringVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


wrong_compare = '''
a = 'abc'
if a > """ab
cd""":
    ...
'''

wrong_function_call = '''
f("""ab
cd""")
'''

wrong_string_function1 = r'''
a = """abc
abc
""".split('\n')
'''

wrong_string_function2 = r'''
a = """
abc
abc
""".split('\n')
'''

wrong_function_call_newline = '''
f(
    name + """ab
    cd""",
)
'''


@pytest.mark.parametrize(
    'code',
    [
        wrong_compare,
        wrong_function_call,
        wrong_string_function1,
        wrong_string_function2,
        wrong_function_call_newline,
    ],
)
def test_wrong_multiline_string_use(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong multiline string uses raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = MultilineStringVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongMultilineStringUseViolation])
