import pytest

from wemake_python_styleguide.violations.naming import (
    WrongModuleNamePatternViolation,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'my_module.py',
    '_prefixed.py',
    '_prefixed_with_number2.py',
    'regression123.py',
])
def test_simple_filename(assert_errors, filename, default_options):
    """Testing that simple file names works well."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('filename', [
    'ending_.py',
    'MyModule.py',
    '1python.py',
    'some_More.py',
    'wrong+char.py',
])
def test_wrong_filename(
    assert_errors,
    filename,
    default_options,
):
    """Testing that incorrect names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [WrongModuleNamePatternViolation])
