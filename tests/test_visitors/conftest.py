from typing import Optional, Sequence

import pytest

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    TokenizeViolation,
)
from wemake_python_styleguide.visitors.base import BaseVisitor


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""
    def factory(
        visitor: BaseVisitor,
        errors: Sequence[str],
        ignored_types=None,
    ):
        if ignored_types:
            real_errors = [
                error
                for error in visitor.violations
                if not isinstance(error, ignored_types)
            ]
        else:
            real_errors = visitor.violations

        assert len(errors) == len(real_errors)

        for index, error in enumerate(real_errors):
            assert error.code == errors[index].code
            if isinstance(error, (ASTViolation, TokenizeViolation)):
                assert error._node is not None  # noqa: WPS437
                assert error._location() != (0, 0)  # noqa: WPS437

    return factory


@pytest.fixture(scope='session')
def assert_error_text():
    """Helper function to assert visitor violation's text."""
    def factory(
        visitor: BaseVisitor,
        text: str,
        baseline: Optional[int] = None,
        *,
        multiple: bool = False,
    ):
        if not multiple:
            assert len(visitor.violations) == 1

        violation = visitor.violations[0]
        error_format = ': {0}'

        assert error_format in violation.error_template
        assert violation.error_template.endswith(error_format)

        reproduction = violation.__class__(
            node=violation._node,  # noqa: WPS437
            text=text,
            baseline=baseline,
        )
        assert reproduction.message() == violation.message()

    return factory
