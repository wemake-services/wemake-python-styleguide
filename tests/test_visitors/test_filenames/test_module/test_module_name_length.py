# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
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


def test_length_option(assert_errors, options):
    """Ensures that option `--min-name-length` works."""
    option_values = options(min_name_length=5)
    visitor = WrongModuleNameVisitor(option_values, filename='test.py')
    visitor.run()

    assert_errors(visitor, [TooShortNameViolation])
