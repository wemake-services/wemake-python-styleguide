import pytest

from wemake_python_styleguide.violations.naming import (  # noqa: I001
    UnreadableNameViolation,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'still1name',
    'l1module',
    'the1interstep',
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
