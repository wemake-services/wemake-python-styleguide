# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    TooShortModuleNameViolation,
    WrongModuleNamePatternViolation,
)
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
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
        TooShortModuleNameViolation,
        WrongModuleNamePatternViolation,
    ])


def test_length_option(assert_errors, options):
    """Ensures that option `--min-module-name-length` works."""
    option_values = options(min_module_name_length=5)
    visitor = WrongModuleNameVisitor(option_values, filename='test.py')
    visitor.run()

    assert_errors(visitor, [TooShortModuleNameViolation])
