# -*- coding: utf-8 -*-

import pkg_resources


def _get_version(dist_name: str) -> str:  # pragma: no cover
    """Fetches distribution name. Contains a fix for Sphinx."""
    try:
        return pkg_resources.get_distribution(dist_name).version
    except pkg_resources.DistributionNotFound:
        return ''  # readthedocs can not install `poetry` projects


pkg_name = 'wemake-python-styleguide'

#: We store the version number inside the `pyproject.toml`:
pkg_version: str = _get_version(pkg_name)
