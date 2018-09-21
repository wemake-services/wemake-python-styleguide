# -*- coding: utf-8 -*-

import pkg_resources

pkg_name = 'wemake-python-styleguide'

#: We store the version number inside the `pyproject.toml`:
pkg_version: str = pkg_resources.get_distribution(pkg_name).version
