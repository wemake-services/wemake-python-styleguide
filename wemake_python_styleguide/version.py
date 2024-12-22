from pathlib import Path
from typing import Final

from wemake_python_styleguide.compat.packaging import get_version

#: This is a package name. It is basically the name of the root folder.
pkg_name: Final = str(Path(__file__).parent.name)

#: We store the version number inside the `pyproject.toml`.
pkg_version: Final = get_version(pkg_name)
