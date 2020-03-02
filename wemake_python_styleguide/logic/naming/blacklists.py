from functools import lru_cache
from typing import FrozenSet

from wemake_python_styleguide.constants import VARIABLE_NAMES_BLACKLIST
from wemake_python_styleguide.types import ConfigurationOptions


@lru_cache()
def variable_names_blacklist_from(
    options: ConfigurationOptions,
) -> FrozenSet[str]:
    """Creates variable names blacklist from options and constants."""
    variable_names_blacklist = {
        *VARIABLE_NAMES_BLACKLIST,
        *options.forbidden_domain_names,
    }
    return frozenset(
        variable_names_blacklist - set(options.allowed_domain_names),
    )
