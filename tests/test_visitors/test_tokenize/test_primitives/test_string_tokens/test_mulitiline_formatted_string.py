import pytest

from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.violations.best_practices import (
    MultilineFormattedStringViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    MultilineFormattedStringTokenVisitor,
)

if not PY312:  # pragma: >=3.12 no cover
    pytest.skip(
        reason='unterminated string literal was added in 3.12',
        allow_module_level=True,
    )  # pragma: no cover

# Wrong:
single_quote_formatted_string_wrong = """x=f'{ 1
}'
"""

double_quote_formatted_string_wrong = """x=f" {2} { 1
}"
"""

# Correct:
triple_quote_formatted_string_first_correct = """x=f'''{ 1
}'''
"""

triple_quote_formatted_string_second_correct = '''x=f"""{ 1
}"""
'''
single_line_formatted_string = (
    """formatted_string_complex = f'1+1={1 + 1}'  # noqa: WPS237"""
)


@pytest.mark.parametrize(
    'code',
    [
        triple_quote_formatted_string_first_correct,
        triple_quote_formatted_string_second_correct,
        single_line_formatted_string,
    ],
)
def test_correctly_formatted_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct formatting works."""
    tokens = parse_tokens(code)
    visitor = MultilineFormattedStringTokenVisitor(
        default_options, file_tokens=tokens
    )
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        single_quote_formatted_string_wrong,
        double_quote_formatted_string_wrong,
    ],
)
def test_incorrectly_formatted_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct formatting works."""
    tokens = parse_tokens(code)
    visitor = MultilineFormattedStringTokenVisitor(
        default_options, file_tokens=tokens
    )
    visitor.run()
    assert_errors(visitor, [MultilineFormattedStringViolation])
