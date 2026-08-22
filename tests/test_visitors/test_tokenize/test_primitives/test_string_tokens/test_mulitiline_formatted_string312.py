import sys

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
    )

PREFIXES = (
    'f',
    pytest.param(
        't',
        marks=pytest.mark.skipif(
            sys.version_info < (3, 14),
            reason='t-strings are only in Python 3.14+',
        ),
    ),
)

# Wrong:
single_quote_formatted_string_wrong = """x={0}'{{ 1
}}'
"""

fr_prefix_formatted_string_wrong = """x={0}r'{{1
}}'"""

double_quote_formatted_string_wrong = """x={0}" {{2}} {{ 1
}}"
"""

# Correct:
triple_quote_formatted_string_first_correct = """x={0}'''{{ 1
}}'''
"""

triple_quote_formatted_string_second_correct = '''x={0}"""{{ 1
}}"""
'''

single_line_formatted_string = (
    """formatted_string_complex = {0}'1+1={{1 + 1}}'  # noqa: WPS237"""
)

fr_prefix_formatted_string = (
    """formatted_string_complex = {0}r'1+1={{1 + 1}}'  # noqa: WPS237"""
)


@pytest.mark.parametrize('prefix', PREFIXES)
@pytest.mark.parametrize(
    'code',
    [
        triple_quote_formatted_string_first_correct,
        triple_quote_formatted_string_second_correct,
        single_line_formatted_string,
        fr_prefix_formatted_string,
    ],
)
def test_correctly_formatted_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    prefix,
):
    """Ensures that correct formatting works."""
    tokens = parse_tokens(code.format(prefix))
    visitor = MultilineFormattedStringTokenVisitor(
        default_options,
        file_tokens=tokens,
    )
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize('prefix', PREFIXES)
@pytest.mark.parametrize(
    'code',
    [
        single_quote_formatted_string_wrong,
        double_quote_formatted_string_wrong,
        fr_prefix_formatted_string_wrong,
    ],
)
def test_incorrectly_formatted_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    prefix,
):
    """Ensures that correct formatting works."""
    tokens = parse_tokens(code.format(prefix))
    visitor = MultilineFormattedStringTokenVisitor(
        default_options,
        file_tokens=tokens,
    )
    visitor.run()
    assert_errors(visitor, [MultilineFormattedStringViolation])
