# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.complexity import (
    TooManyExceptCasesViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TryExceptVisitor,
)

complex_try_except = """
try:
    do_some_bad_things()
except ValueError:
    print('value')
except KeyError:
    print('key')
except IndexError as exc:
    print('index', exc)
except TypeError:
    print('type')
"""


def test_try_except_count_default(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(complex_try_except)

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyExceptCasesViolation])


def test_try_except_count_custom_settings(
    assert_errors,
    parse_ast_tree,
    options,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(complex_try_except)

    option_values = options(max_except_cases=4)
    visitor = TryExceptVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
