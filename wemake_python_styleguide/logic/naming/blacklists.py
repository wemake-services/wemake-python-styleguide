from functools import cache

from wemake_python_styleguide.constants import (
    MODULE_METADATA_VARIABLES_BLACKLIST,
    VARIABLE_NAMES_BLACKLIST,
)
from wemake_python_styleguide.options.validation import ValidatedOptions


@cache
def variable_names_blacklist_from(
    options: ValidatedOptions,
) -> frozenset[str]:
    """Creates variable names blacklist from options and constants."""
    variable_names_blacklist = {
        *VARIABLE_NAMES_BLACKLIST,
        *options.forbidden_domain_names,
    }
    return frozenset(
        variable_names_blacklist - set(options.allowed_domain_names),
    )


@cache
def module_metadata_blacklist(
    options: ValidatedOptions,
) -> frozenset[str]:
    """Creates module metadata blacklist from options and constants."""
    module_metadata_blacklist = {
        *MODULE_METADATA_VARIABLES_BLACKLIST,
        *options.forbidden_module_metadata,
    }
    return frozenset(
        module_metadata_blacklist - set(options.allowed_module_metadata),
    )
