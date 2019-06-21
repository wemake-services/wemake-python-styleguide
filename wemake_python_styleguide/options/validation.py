# -*- coding: utf-8 -*-

from typing import Optional

import attr
from typing_extensions import final

from wemake_python_styleguide.types import ConfigurationOptions


def _min_max(
    min: Optional[int] = None,  # noqa: A002
    max: Optional[int] = None,  # noqa: A002
):
    """Validator to check that value is in bounds."""
    def factory(instance, attribute, field_value):
        min_contract = min is not None and field_value < min
        max_contract = max is not None and field_value > max
        if min_contract or max_contract:
            raise ValueError('Option {0} is out of bounds: {1}'.format(
                attribute.name,
                field_value,
            ))
    return factory


@final
@attr.dataclass(frozen=True, slots=True)
class _ValidatedOptions(object):
    """
    Here we write all the required structured validation for the options.

    It is an internal class and is not used anywhere else.
    """

    # General:
    min_name_length: int = attr.ib(validator=[_min_max(min=1)])
    i_control_code: bool
    max_name_length: int = attr.ib(validator=[_min_max(min=1)])

    # Complexity:
    max_arguments: int = attr.ib(validator=[_min_max(min=1)])
    max_local_variables: int = attr.ib(validator=[_min_max(min=1)])
    max_returns: int = attr.ib(validator=[_min_max(min=1)])
    max_expressions: int = attr.ib(validator=[_min_max(min=1)])
    max_module_members: int = attr.ib(validator=[_min_max(min=1)])
    max_methods: int = attr.ib(validator=[_min_max(min=1)])
    max_line_complexity: int = attr.ib(validator=[_min_max(min=1)])
    max_jones_score: int = attr.ib(validator=[_min_max(min=1)])
    max_imports: int = attr.ib(validator=[_min_max(min=1)])
    max_base_classes: int = attr.ib(validator=[_min_max(min=1)])
    max_decorators: int = attr.ib(validator=[_min_max(min=1)])
    max_string_usages: int = attr.ib(validator=[_min_max(min=1)])


def validate_options(options: ConfigurationOptions) -> ConfigurationOptions:
    """Validates all options from ``flake8``, uses a subset of them."""
    fields_to_validate = [
        field.name
        for field in attr.fields(_ValidatedOptions)
    ]
    options_subset = {
        field: getattr(options, field, None)
        for field in fields_to_validate
    }
    _ValidatedOptions(**options_subset)  # raises TypeError
    return options
