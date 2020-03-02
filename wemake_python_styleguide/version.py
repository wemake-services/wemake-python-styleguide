from wemake_python_styleguide.compat.packaging import importlib_metadata


def _get_version(dist_name: str) -> str:  # pragma: no cover
    """Fetches distribution version."""
    try:
        return importlib_metadata.version(dist_name)
    except importlib_metadata.PackageNotFoundError:
        return ''  # readthedocs can not install `poetry` projects


pkg_name = 'wemake-python-styleguide'

#: We store the version number inside the `pyproject.toml`:
pkg_version = _get_version(pkg_name)
