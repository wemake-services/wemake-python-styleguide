import sys

from typing_extensions import Final

#: This indicates that we are running on python3.10+
PY310: Final = sys.version_info >= (3, 10)

#: This indicates that we are running on python3.11+
PY311: Final = sys.version_info >= (3, 11)

# This indicates that we are running on python3.12+
PY312: Final = sys.version_info >= (3, 12)
