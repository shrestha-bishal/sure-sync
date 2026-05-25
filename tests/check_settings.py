from fastapi.testclient import TestClient
from web.app import app
import traceback

client = TestClient(app)
try:
    r = client.get("/settings/accounts")
    print("STATUS:", r.status_code)
    print(r.text)
except Exception:
    print("EXCEPTION RAISED")
    traceback.print_exc()
    raise
