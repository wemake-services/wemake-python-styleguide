import pytest

from wemake_python_styleguide.violations.best_practices import ShebangViolation
from wemake_python_styleguide.visitors.tokenize import comments

template_empty = ''
template_newlines = '\n\n'
template_regular = '{0}'

template_with_leading_comment = """{0}
# some other
"""

template_regular_comment = 'x = 1{0}'


@pytest.mark.parametrize('template', [
    template_regular,
    template_with_leading_comment,
])
@pytest.mark.parametrize(('code', 'executable'), [
    ('x = 1', False),
    ('#!/bin/python', True),
])
def test_correct_shebang_executable1(
    make_file,
    assert_errors,
    parse_file_tokens,
    default_options,
    template,
    code,
    executable,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(
        'test_file.py',
        template.format(code),
        is_executable=executable,
    )
    file_tokens = parse_file_tokens(path_to_file)

    visitor = comments.ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_regular_comment,
    template_empty,
])
@pytest.mark.parametrize(('code', 'executable'), [
    ('#!/bin/some', False),
    ('#!/bin/python', False),
    ('# any text', False),
    ('   # any text with padding', False),
])
def test_correct_shebang_executable2(
    make_file,
    assert_errors,
    parse_file_tokens,
    default_options,
    template,
    code,
    executable,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(
        'test_file.py',
        template.format(code),
        is_executable=executable,
    )
    file_tokens = parse_file_tokens(path_to_file)

    visitor = comments.ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_regular,
    template_with_leading_comment,
    template_regular_comment,
    template_empty,
])
@pytest.mark.parametrize(('code', 'executable'), [
    ('#!/bin/python', False),
    ('#!/bin/python', True),
    ('# any text', False),
    ('# any text', True),
])
def test_shebang_on_windows(
    make_file,
    monkeypatch,
    assert_errors,
    parse_file_tokens,
    default_options,
    template,
    code,
    executable,
):
    """Testing cases when no errors should be reported."""
    monkeypatch.setattr(comments, 'is_windows', lambda: True)
    path_to_file = make_file(
        'test_file.py',
        template.format(code),
        is_executable=executable,
    )
    file_tokens = parse_file_tokens(path_to_file)

    visitor = comments.ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_regular,
    template_with_leading_comment,
    template_regular_comment,
    template_empty,
])
@pytest.mark.parametrize(('code', 'executable'), [
    ('#!/bin/python', False),
    ('#!/bin/python', True),
    ('# any text', False),
    ('# any text', True),
])
def test_shebang_with_stdin(
    make_file,
    monkeypatch,
    assert_errors,
    parse_file_tokens,
    default_options,
    template,
    code,
    executable,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(
        'test_file.py',
        template.format(code),
        is_executable=executable,
    )
    file_tokens = parse_file_tokens(path_to_file)

    visitor = comments.ShebangVisitor(
        default_options,
        filename='stdin',
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('template', [
    template_regular,
    template_with_leading_comment,
])
@pytest.mark.parametrize(('code', 'executable'), [
    ('#!/bin/python', False),
    ('# regular comment', True),
])
def test_wrong_shebang_executable(
    make_file,
    assert_errors,
    parse_file_tokens,
    default_options,
    template,
    code,
    executable,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(
        'test_file.py',
        template.format(code),
        is_executable=executable,
    )
    file_tokens = parse_file_tokens(path_to_file)

    visitor = comments.ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [ShebangViolation])


@pytest.mark.parametrize('template', [
    template_with_leading_comment,
])
@pytest.mark.parametrize('code', [
    '#!/bin/other',  # does not include `python`
    ' #!/bin/python',  # has extra whitespace
    '\n\n#!python',  # has extra newlines
])
def test_wrong_shebang_format(
    make_file,
    assert_errors,
    parse_file_tokens,
    default_options,
    template,
    code,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(
        'test_file.py',
        template.format(code),
        is_executable=True,
    )
    file_tokens = parse_file_tokens(path_to_file)

    visitor = comments.ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [ShebangViolation])
