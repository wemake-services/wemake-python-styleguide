import pytest

from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringTokenVisitor,
)


@pytest.mark.parametrize(
    'primitive',
    [
        '"name"',
        r'r"text with escape carac \n"',
        "b'unicode'",
        '"u"',
        '"12"',
        'b""',
    ],
)
def test_correct_strings(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that correct strings are fine."""
    file_tokens = parse_tokens(
        mode(primitives_usages.format(primitive)),
        do_compile=False,
    )

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
