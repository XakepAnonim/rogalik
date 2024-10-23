import pytest


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


@pytest.mark.anyio()
async def test_root(async_client):
    async with async_client as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


@pytest.mark.anyio()
async def test_socketio(socketio_client):
    socketio_client.connect("/", namespaces=[])
    socketio_client.disconnect()
