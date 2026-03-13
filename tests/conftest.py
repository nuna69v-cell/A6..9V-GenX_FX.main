import os
import sys
from collections import deque
from unittest.mock import MagicMock

import pytest

# Set testing environment variables before any application code is imported
os.environ["TESTING"] = "true"
os.environ["EA_API_KEY"] = "test_api_key_12345"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["JWT_SECRET"] = "test_jwt_secret"

try:
    import talib
except ImportError:
    sys.modules["talib"] = MagicMock()


@pytest.fixture(autouse=True)
def clear_ea_state():
    """Clear global state in ea_http router between tests."""
    try:
        from api.routers import ea_http

        ea_http.ea_connections = {}
        assert isinstance(
            ea_http.pending_signals, deque
        ), "pending_signals must be a deque!"
        ea_http.pending_signals.clear()
        ea_http.trade_results.clear()
    except ImportError:
        pass
