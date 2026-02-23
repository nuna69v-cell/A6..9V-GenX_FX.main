import sys
from unittest.mock import MagicMock

try:
    import talib
except ImportError:
    sys.modules["talib"] = MagicMock()
