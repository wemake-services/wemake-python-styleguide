from wemake_python_styleguide.violations.refactoring import (
    ImplicitElifViolation,
)
from wemake_python_styleguide.visitors.tokenize.conditions import IfElseVisitor

code_that_breaks = """
number = int(input())
if number == 1:
    print("1")
else:
    if number == 2: print("2")
"""

code_implict_if_else = """
if numbers:
    my_print('first')
else:
    if numbers:
        my_print('other')
"""


def test_if_else_one_line(
    assert_errors,
    default_options,
    parse_tokens,
):
    """Testing to see if ``if`` statement code is on one line."""
    tokens = parse_tokens(code_that_breaks)

    visitor = IfElseVisitor(default_options, tokens)
    visitor.run()

    assert_errors(visitor, [ImplicitElifViolation])


def test_if_else_implict(
    assert_errors,
    default_options,
    parse_tokens,
):
    """Testing to make sure implicit if works."""
    tokens = parse_tokens(code_implict_if_else)

    visitor = IfElseVisitor(default_options, tokens)
    visitor.run()

    assert_errors(visitor, [ImplicitElifViolation])
