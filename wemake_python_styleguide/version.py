import os

from wemake_python_styleguide.compat.packaging import get_version

#: This is a package name. It is basically the name of the root folder.
pkg_name = os.path.basename(os.path.dirname(__file__))

#: We store the version number inside the `pyproject.toml`.
pkg_version = get_version(pkg_name)
