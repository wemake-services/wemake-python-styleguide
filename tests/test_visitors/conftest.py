from collections.abc import Sequence
from typing import Final, TypeAlias, Union

import pytest

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    BaseViolation,
    TokenizeViolation,
)
from wemake_python_styleguide.visitors.base import BaseVisitor

_IgnoredTypes: TypeAlias = Union[
    type[BaseViolation],
    tuple[type[BaseViolation], ...],
    None,
]
_ERROR_FORMAT: Final = ': {0}'


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""

    def factory(
        visitor: BaseVisitor,
        expected_errors: Sequence[str],
        *,
        ignored_types: _IgnoredTypes = None,
    ) -> None:
        if ignored_types:
            real_errors = [
                error
                for error in visitor.violations
                if not isinstance(error, ignored_types)
            ]
        else:
            real_errors = visitor.violations

        assert len(expected_errors) == len(real_errors)

        for index, error in enumerate(real_errors):
            assert expected_errors[index].disabled_since is None
            assert error.code == expected_errors[index].code
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
        baseline: int | None = None,
        *,
        multiple: bool = False,
        ignored_types: _IgnoredTypes = None,
    ) -> None:
        if ignored_types:
            real_errors = [
                error
                for error in visitor.violations
                if not isinstance(error, ignored_types)
            ]
        else:
            real_errors = visitor.violations

        if not multiple:
            assert len(real_errors) == 1

        violation = real_errors[0]

        assert _ERROR_FORMAT in violation.error_template
        assert violation.error_template.endswith(_ERROR_FORMAT)

        reproduction = violation.__class__(
            node=violation._node,  # noqa: WPS437
            text=text,
            baseline=baseline,
        )
        assert reproduction.message() == violation.message()

    return factory
