import sys

from typing_extensions import Final

#: This indicates that we are running on python3.8+
PY38: Final = sys.version_info >= (3, 8)
