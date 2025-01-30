import tokenize
from collections.abc import Sequence
from typing import Final, TypeAlias

import pytest

from wemake_python_styleguide.logic.source import node_to_string
from wemake_python_styleguide.violations.base import (
    ASTViolation,
    BaseViolation,
    TokenizeViolation,
)
from wemake_python_styleguide.visitors.base import (
    BaseNodeVisitor,
    BaseTokenVisitor,
    BaseVisitor,
)

_IgnoredTypes: TypeAlias = (
    type[BaseViolation] | tuple[type[BaseViolation], ...] | None
)
_ERROR_FORMAT: Final = ': {0}'


def _produce_error_message(visitor: BaseVisitor) -> str:  # pragma: no cover
    if isinstance(visitor, BaseNodeVisitor):
        return f'\n{node_to_string(visitor.tree)}'
    if isinstance(visitor, BaseTokenVisitor):
        return f'\n {tokenize.untokenize(visitor.file_tokens)}'
    return ''


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

        assert len(real_errors) == len(expected_errors), _produce_error_message(
            visitor,
        )

        for index, error in enumerate(real_errors):
            assert expected_errors[index].disabled_since is None
            assert error.code == expected_errors[index].code
            if isinstance(error, ASTViolation | TokenizeViolation):
                assert error._node is not None  # noqa: SLF001
                assert error._location() != (0, 0)  # noqa: SLF001

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
            node=violation._node,  # noqa: SLF001
            text=text,
            baseline=baseline,
        )
        assert reproduction.message() == violation.message()

    return factory


@pytest.fixture(scope='session')
def assert_error_location():
    """Helper function to assert visitor violation location is expected."""

    def factory(
        visitor: BaseVisitor,
        expected: tuple[int, int],
    ) -> None:
        assert len(visitor.violations) == 1
        violation = visitor.violations[0]
        assert violation._location() == expected  # noqa: SLF001

    return factory
