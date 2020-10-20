import pytest

from wemake_python_styleguide.violations.naming import (
    UnderscoredNumberNameViolation,
    UnreadableNameViolation,
    WrongModuleNamePatternViolation,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'the1long',
])
def test_unreadable_filename(assert_errors, filename, default_options):
    """Testing that unreadable characters combinations do not allowed."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [UnreadableNameViolation])


@pytest.mark.parametrize('filename', [
    'ordinary',
    'first_module',
])
def test_readable_filename(assert_errors, filename, default_options):
    """Testing that ordinary naming works well."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('filename', [
    'TestO_0',
])
def test_corner_case(assert_errors, filename, default_options):
    """Testing corner case related to underscore name patterns."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [
        WrongModuleNamePatternViolation,
        UnderscoredNumberNameViolation,
    ])
