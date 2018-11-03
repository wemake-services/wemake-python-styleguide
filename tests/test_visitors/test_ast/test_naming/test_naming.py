# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import VARIABLE_NAMES_BLACKLIST
from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
    PrivateNameViolation,
    TooLongNameViolation,
    TooShortNameViolation,
    UnderscoredNumberNameViolation,
    WrongVariableNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('wrong_name', VARIABLE_NAMES_BLACKLIST)
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


def test_short_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
):
    """Ensures that short names are not allowed."""
    short_name = 'y'
    tree = parse_ast_tree(mode(naming_template.format(short_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])
    assert_error_text(visitor, short_name)


def test_private_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
):
    """Ensures that private names are not allowed."""
    private_name = '__private'
    tree = parse_ast_tree(mode(naming_template.format(private_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])
    assert_error_text(visitor, private_name)


@pytest.mark.parametrize('underscored_name', [
    'with__underscore',
    'mutliple__under__score',
    'triple___underscore',
])
def test_underscored_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    underscored_name,
):
    """Ensures that underscored names are not allowed."""
    tree = parse_ast_tree(mode(naming_template.format(underscored_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveUnderscoresInNameViolation])
    assert_error_text(visitor, underscored_name)


@pytest.mark.parametrize('number_suffix', [
    'number_5',
    'between_45_letters',
    'with_multiple_groups_4_5',
])
def test_number_prefix_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    number_suffix,
):
    """Ensures that number suffix names are not allowed."""
    tree = parse_ast_tree(mode(naming_template.format(number_suffix)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberNameViolation])
    assert_error_text(visitor, number_suffix)


@pytest.mark.parametrize('correct_name', [
    'snake_case',
    '_protected_or_unused',
    'with_number5',
    'xy',
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


def test_long_variable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
):
    """Ensures that long names are not allowed."""
    long_name = 'incredibly_and_very_long_name_that_will_definitely_not_work'
    tree = parse_ast_tree(mode(naming_template.format(long_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongNameViolation])
    assert_error_text(visitor, long_name)
