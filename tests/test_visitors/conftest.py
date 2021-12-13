from typing import Optional, Sequence, Tuple, Type, Union

import pytest
from typing_extensions import Final

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    BaseViolation,
    TokenizeViolation,
)
from wemake_python_styleguide.visitors.base import BaseVisitor

_IgnoredTypes = Union[
    Type[BaseViolation],
    Tuple[Type[BaseViolation], ...],
    None,
]
_ERROR_FORMAT: Final = ': {0}'


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""
    def factory(
        visitor: BaseVisitor,
        errors: Sequence[str],
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
