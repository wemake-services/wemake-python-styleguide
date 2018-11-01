# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    TooLongNameViolation,
    TooShortNameViolation,
    WrongModuleNamePatternViolation,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'a.py',
    'some/package/z.py',
    '/root/x.py',
    'C:/f.py',
])
def test_too_short_filename(assert_errors, filename, default_options):
    """Testing that short file names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [
        TooShortNameViolation,
        WrongModuleNamePatternViolation,
    ])


def test_length_option(assert_errors, assert_error_text, options):
    """Ensures that option `--min-name-length` works."""
    filename = 'test.py'
    option_values = options(min_name_length=5)
    visitor = WrongModuleNameVisitor(option_values, filename=filename)
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])
    assert_error_text(visitor, filename.replace('.py', ''))


@pytest.mark.parametrize('filename', [
    'super_long_name_that_needs_to_be_much_shorter.py',
    'some/package/another_ridiculously_lengthly_name_that_wont_work.py',
    '/root/please_do_not_ever_make_names_long_like_this.py',
    'C:/hello_there_this_is_another_very_long_name.py',
])
def test_too_long_filename(assert_errors, filename, default_options):
    """Testing that long file names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [
        TooLongNameViolation,
        WrongModuleNamePatternViolation,
    ])


def test_length_option(assert_errors, assert_error_text, options):
    """Ensures that option `--max-name-length` works."""
    filename = 'very_long_name_that_should_not_pass_this_test.py'
    option_values = options(max_name_length=40)
    visitor = WrongModuleNameVisitor(option_values, filename=filename)
    visitor.run()

    assert_errors(visitor, [TooLongNameViolation])
    assert_error_text(visitor, filename.replace('.py', ''))
