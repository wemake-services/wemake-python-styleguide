# -*- coding: utf-8 -*-

import pkg_resources

#: We store the version number inside the `pyproject.toml`:
version: str = pkg_resources.get_distribution(
    'wemake-python-styleguide',
).version
