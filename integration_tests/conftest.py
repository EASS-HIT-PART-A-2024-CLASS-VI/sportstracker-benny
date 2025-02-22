# integration_tests/conftest.py
import pytest
import httpx

@pytest.fixture(scope="session")
def management_client():
    return httpx.Client(base_url="http://management_service:8000")

@pytest.fixture(scope="session")
def scoreboard_client():
    return httpx.Client(base_url="http://scoreboard_service:8000")

@pytest.fixture(scope="session")
def analytics_client():
    return httpx.Client(base_url="http://analytics_service:8000")
