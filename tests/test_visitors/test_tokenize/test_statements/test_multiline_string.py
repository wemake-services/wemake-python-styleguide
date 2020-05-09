import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongMultilineStringUseViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    MultilineStringVisitor,
)

correct_assignment = '''
a = """dskl
fsv
"""
'''

correct_docstring = '''
def test():
    """{0}"""
'''


@pytest.mark.parametrize('code', [
    correct_assignment,
    correct_docstring,
])
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


incorrect_compare = '''
a = 'abc'
if a > """ab
cd""":
    pass
'''

incorrect_function_call = '''
f("""ab
cd""")
'''


@pytest.mark.parametrize('code', [
    incorrect_compare,
    incorrect_function_call,
])
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
