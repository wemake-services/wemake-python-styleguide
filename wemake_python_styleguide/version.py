# -*- coding: utf-8 -*-

import pkg_resources

pkg_name = 'wemake-python-styleguide'


def _get_version(dist_name: str) -> str:
    """Fetches distribution name. Contains a fix for Sphinx."""
    try:
        return pkg_resources.get_distribution(dist_name).version
    except pkg_resources.DistributionNotFound:
        return '0.0.0'


#: We store the version number inside the `pyproject.toml`:
pkg_version: str = _get_version(pkg_name)
