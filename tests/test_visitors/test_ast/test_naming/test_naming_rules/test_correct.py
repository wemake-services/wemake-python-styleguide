# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('correct_name', [
    'snake_case',
    '_protected',
    'with_number5',
])
def test_naming_correct(
    assert_errors,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    correct_name,
):
    """Ensures that correct names are allowed."""
    tree = parse_ast_tree(mode(naming_template.format(correct_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('allowed_name', [
    'item',
    'items',
    'handle',
    'other_name',  # unknown values are ignored silently
])
def test_name_in_allowed_domain_names_option(
    assert_errors,
    parse_ast_tree,
    naming_template,
    options,
    mode,
    allowed_name,
):
    """Ensures that names listed in `allowed-domain-names` are allowed."""
    tree = parse_ast_tree(mode(naming_template.format(allowed_name)))

    visitor = WrongNameVisitor(
        options(allowed_domain_names=[allowed_name]),
        tree=tree,
    )
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize('name', [
    'handle',
    'visitor',
])
def test_name_in_both_domain_names_options(
    assert_errors,
    parse_ast_tree,
    naming_template,
    options,
    mode,
    name,
):
    """Check case when both domain-names options passed.

    Ensures that `allowed-domain-names` takes precedence over
    `forbidden-domain-names`.
    """
    tree = parse_ast_tree(mode(naming_template.format(name)))

    visitor = WrongNameVisitor(
        options(forbidden_domain_names=[name], allowed_domain_names=[name]),
        tree=tree,
    )
    visitor.run()
    assert_errors(visitor, [])
