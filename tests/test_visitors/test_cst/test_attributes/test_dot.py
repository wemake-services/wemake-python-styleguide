# -*- coding: utf-8 -*-

import libcst
import pytest

from wemake_python_styleguide.violations.consistency import (
    UnnecessarySpaceAroundDotViolation,
)
from wemake_python_styleguide.visitors.cst.attributes import (
    AttributeCSTVisitor,
)

# Correct:

correct_attribute = 'some.set(1,2)'

correct_import = 'from .a import b'

correct_float = 'b = .5'

transfer = """
some_model = (
    MyModel.objects.filter(...)
        .exclude(...)
)
"""

# Wrong:

wrong_attribute_case1 = 'some. set(1,2)'

wrong_attribute_case2 = 'some .set(1,2)'

wrong_attribute_case3 = 'some . set(1,2)'

wrong_attribute_case4 = 'some.set(1,2) .set(1,2)'


@pytest.mark.parametrize('code', [
    correct_attribute,
    correct_import,
    correct_float,
    transfer,
])
def test_correct_dot(
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct dot position not raise a warning."""
    cst = libcst.parse_module(code)

    visitor = AttributeCSTVisitor(default_options, cst=cst)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_attribute_case1,
    wrong_attribute_case2,
    wrong_attribute_case3,
    wrong_attribute_case4,
])
def test_wrong_dot(
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect dot position raise a warning."""
    cst = libcst.parse_module(code)

    visitor = AttributeCSTVisitor(default_options, cst=cst)
    visitor.run()

    assert_errors(visitor, [UnnecessarySpaceAroundDotViolation])
