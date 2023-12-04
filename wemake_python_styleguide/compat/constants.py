import sys

from typing_extensions import Final

#: This indicates that we are running on python3.9+
PY39: Final = sys.version_info >= (3, 9)

#: This indicates that we are running on python3.10+
PY310: Final = sys.version_info >= (3, 10)
