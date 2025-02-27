import sys
from typing import Final

#: This indicates that we are running on python3.11+
PY311: Final = sys.version_info >= (3, 11)

# This indicates that we are running on python3.12+
PY312: Final = sys.version_info >= (3, 12)

# This indicates that we are running on python3.13+
PY313: Final = sys.version_info >= (3, 13)
