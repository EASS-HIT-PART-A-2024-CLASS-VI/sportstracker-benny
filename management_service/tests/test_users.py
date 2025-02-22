import pytest
import httpx

@pytest.fixture(scope="session")
def client():
    base_url = "http://management_service:8000"
    return httpx.Client(base_url=base_url)

def test_register_new_user(client):
    # 1. Attempt to register a user
    payload = {"username": "test_user", "password": "test_pass"}
    resp = client.post("/register", json=payload)
    assert resp.status_code in (200, 201), f"Unexpected status {resp.status_code}, body: {resp.text}"

    data = resp.json()
    assert "id" in data, "User response must contain 'id'"
    assert data["username"] == "test_user"