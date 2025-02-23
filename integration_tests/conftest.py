# integration_tests/conftest.py
import pytest
import httpx
import time
MAX_RETRIES = 10
RETRY_DELAY = 2  # seconds

def wait_for_service(client, endpoint, expected_status=200):
    for _ in range(MAX_RETRIES):
        try:
            response = client.get(endpoint)
            if response.status_code == expected_status:
                return True
        except httpx.RequestError:
            pass
        time.sleep(RETRY_DELAY)
    return False

@pytest.fixture(scope="session")
def management_client():
    client = httpx.Client(base_url="http://management_service:8000")
    ready = wait_for_service(client, "/leagues", expected_status=200)
    assert ready, "Management service did not become ready in time."
    return client

@pytest.fixture(scope="session")
def scoreboard_client():
    return httpx.Client(base_url="http://scoreboard_service:8000")

@pytest.fixture(scope="session")
def analytics_client():
    return httpx.Client(base_url="http://analytics_service:8000")
