try:
    from fastapi.testclient import TestClient

    print("FastAPI TestClient imported")
    from api.main import app

    print("api.main imported")
    from api.config import settings

    print("api.config imported")
except ImportError as e:
    print(f"Import failed: {e}")
