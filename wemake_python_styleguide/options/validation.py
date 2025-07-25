from typing import Any, final

import attr

from wemake_python_styleguide.options import defaults


def _min_max(
    min: int | None = None,  # noqa: A002
    max: int | None = None,  # noqa: A002
):
    """Validator to check that value is in bounds."""

    def factory(instance, attribute, field_value):
        min_contract = min is not None and field_value < min
        max_contract = max is not None and field_value > max
        if min_contract or max_contract:
            raise ValueError(
                f'Option {attribute.name} is out of bounds: {field_value}',
            )

    return factory


def validate_domain_names_options(
    allowed_domain_names: tuple[str, ...],
    forbidden_domain_names: tuple[str, ...],
) -> None:
    """
    Validator to check that allowed and forbidden names doesn't intersect.

    Raises:
        ValueError - when domain names option is invalid.

    """
    if not allowed_domain_names or not forbidden_domain_names:
        return
    intersecting_names = set(allowed_domain_names) & set(forbidden_domain_names)
    if intersecting_names:
        raise ValueError(
            (
                'Names passed to `allowed_domain_name` and '
                + '`forbidden_domain_name` cannot intersect. '
                + 'Intersecting names: '
                + ', '.join(intersecting_names)
            ),
        )


@final
@attr.dataclass(slots=True, frozen=True)
class ValidatedOptions:
    """
    Here we write all the required structured validation for the options.

    It is an internal class and is not used anywhere else.
    """

    # General:
    min_name_length: int = attr.ib(validator=[_min_max(min=1)])
    max_name_length: int = attr.ib(validator=[_min_max(min=1)])
    max_noqa_comments: int = attr.ib(
        validator=[_min_max(min=1, max=defaults.MAX_NOQA_COMMENTS)],
    )
    nested_classes_whitelist: tuple[str, ...] = attr.ib(converter=tuple)
    allowed_domain_names: tuple[str, ...] = attr.ib(converter=tuple)
    forbidden_domain_names: tuple[str, ...] = attr.ib(converter=tuple)
    allowed_module_metadata: tuple[str, ...] = attr.ib(converter=tuple)
    forbidden_module_metadata: tuple[str, ...] = attr.ib(converter=tuple)
    forbidden_inline_ignore: tuple[str, ...] = attr.ib(converter=tuple)

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
    max_imported_names: int = attr.ib(validator=[_min_max(min=1)])
    max_base_classes: int = attr.ib(validator=[_min_max(min=1)])
    max_decorators: int = attr.ib(validator=[_min_max(min=1)])
    max_string_usages: int = attr.ib(validator=[_min_max(min=1)])
    max_awaits: int = attr.ib(validator=[_min_max(min=1)])
    max_try_body_length: int = attr.ib(validator=[_min_max(min=1)])
    max_module_expressions: int = attr.ib(validator=[_min_max(min=1)])
    max_function_expressions: int = attr.ib(validator=[_min_max(min=1)])
    max_asserts: int = attr.ib(validator=[_min_max(min=1)])
    max_access_level: int = attr.ib(validator=[_min_max(min=1)])
    max_attributes: int = attr.ib(validator=[_min_max(min=1)])
    max_raises: int = attr.ib(validator=[_min_max(min=1)])
    max_except_exceptions: int = attr.ib(validator=[_min_max(min=1)])
    max_cognitive_score: int = attr.ib(validator=[_min_max(min=1)])
    max_cognitive_average: int = attr.ib(validator=[_min_max(min=1)])
    max_call_level: int = attr.ib(validator=[_min_max(min=1)])
    max_annotation_complexity: int = attr.ib(validator=[_min_max(min=2)])
    max_import_from_members: int = attr.ib(validator=[_min_max(min=1)])
    max_tuple_unpack_length: int = attr.ib(validator=[_min_max(min=1)])
    max_type_params: int = attr.ib(validator=[_min_max(min=1)])
    max_match_subjects: int = attr.ib(validator=[_min_max(min=1)])
    max_match_cases: int = attr.ib(validator=[_min_max(min=1)])
    max_lines_in_finally: int = attr.ib(validator=[_min_max(min=1)])
    max_conditions: int = attr.ib(validator=[_min_max(min=1)])
    show_violation_links: bool
    exps_for_one_empty_line: int


def validate_options(options: Any) -> ValidatedOptions:
    """Validates all options from ``flake8``, uses a subset of them."""
    validate_domain_names_options(
        options.allowed_domain_names,
        options.forbidden_domain_names,
    )
    fields_to_validate = [field.name for field in attr.fields(ValidatedOptions)]
    options_subset = {
        field: getattr(options, field, None) for field in fields_to_validate
    }
    # Next line raises `TypeError` if `options_subset` is invalid.
    return ValidatedOptions(**options_subset)  # type: ignore[arg-type]
