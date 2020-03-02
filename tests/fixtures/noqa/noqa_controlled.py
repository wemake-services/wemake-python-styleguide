"""
This file contains all violations which may be tweaked using
`i_control_code` or `i_dont_control_code` options.

It is used for some of e2e tests to check that `i_control_code` works.
"""

import sys as sys  # noqa: WPS113


def __getattr__():  # noqa: WPS413
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/461
    anti_z428 = 1
