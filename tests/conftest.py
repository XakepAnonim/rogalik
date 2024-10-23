import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from socketio.client import Client as SocketIOClient

from rogalik.server import create_server


@pytest.fixture
def anyio_backend():
    return 'asyncio'


app = create_server()


@pytest.fixture
def client():
    return TestClient(create_server())


@pytest.fixture
def socketio_client():
    return SocketIOClient()


@pytest.fixture
def async_client():
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )
