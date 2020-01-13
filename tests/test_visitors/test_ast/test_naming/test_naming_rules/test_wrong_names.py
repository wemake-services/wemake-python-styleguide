# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('wrong_name', [
    'value',
    'no',
    'data',
])
def test_wrong_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    wrong_name,
):
    """Ensures that wrong names are not allowed."""
    tree = parse_ast_tree(mode(naming_template.format(wrong_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])
    assert_error_text(visitor, wrong_name)


@pytest.mark.parametrize('forbidden_name', [
    'visitor',
    'name_validator',
])
def test_name_in_forbidden_domain_names_option(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    options,
    mode,
    forbidden_name,
):
    """Ensures that names listed in `forbidden-domain-names` are forbidden."""
    tree = parse_ast_tree(mode(naming_template.format(forbidden_name)))

    visitor = WrongNameVisitor(
        options(forbidden_domain_names=[forbidden_name]),
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [WrongVariableNameViolation])
    assert_error_text(visitor, forbidden_name)
