# -*- coding: utf-8 -*-

from typing import Set

from wemake_python_styleguide.constants import VARIABLE_NAMES_BLACKLIST
from wemake_python_styleguide.types import ConfigurationOptions


def variable_names_blacklist_from(options: ConfigurationOptions) -> Set[str]:
    """Creates variable names blacklist from options and constants."""
    variable_names_blacklist = {
        *VARIABLE_NAMES_BLACKLIST,
        *options.forbidden_domain_names,
    }
    return variable_names_blacklist - set(options.allowed_domain_names)
