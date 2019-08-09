# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    TooLongNameViolation,
    TooShortNameViolation,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'a.py',
    'relative/_a.py',
    'C:/a_.py',
    'some/package/z.py',
    '/root/x.py',
    'C:/f.py',
])
def test_too_short_filename(assert_errors, filename, default_options):
    """Testing that short file names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])


@pytest.mark.parametrize('filename', [
    # Regression for 596:
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/596
    'io.py',
])
def test_normal_module_name(assert_errors, filename, default_options):
    """Testing that short file names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])


def test_length_option(assert_errors, assert_error_text, options):
    """Ensures that option `--min-name-length` works."""
    filename = 'test.py'
    option_values = options(min_name_length=5)
    visitor = WrongModuleNameVisitor(option_values, filename=filename)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])
    assert_error_text(visitor, filename.replace('.py', ''))


@pytest.mark.parametrize('filename', [
    'super_long_name_that_needs_to_be_much_shorter_to_fit_the_rule.py',
    'package/another_ridiculously_lengthly_name_that_defies_this_rule.py',
    '/root/please_do_not_ever_make_names_long_and_confusing_like_this.py',
    'C:/hello_there_this_is_another_very_long_name_that_will_not_work.py',
])
def test_too_long_filename(assert_errors, filename, default_options):
    """Testing that long file names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [TooLongNameViolation])


def test_max_length_option(assert_errors, assert_error_text, options):
    """Ensures that option `--max-name-length` works."""
    max_length = 55
    filename = 'very_long_name_that_should_not_pass_unless_changed_shorter.py'
    option_values = options(max_name_length=max_length)
    visitor = WrongModuleNameVisitor(option_values, filename=filename)
    visitor.run()

    assert_errors(visitor, [TooLongNameViolation])
    assert_error_text(visitor, filename.replace('.py', ''))
