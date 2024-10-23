import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    transports=["websocket"],
)
app = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")

game_state = {"players": {}}


@sio.event
async def connect(sid, environ):
    """
    Обработчик подключения игрока.
    """
    print(f"connect {sid}")
    game_state["players"][sid] = {"x": 0, "y": 0}  # Добавляем игрока

    # Отправляем начальное состояние игры клиенту
    await sio.emit("update_game_state", game_state, to=sid)


@sio.event
async def disconnect(sid):
    """
    Обработчик отключения игрока.
    """
    print(f"disconnect {sid}")
    game_state["players"].pop(sid, None)  # Удаляем игрока


@sio.event
async def move_player(sid, data):
    """
    Обработчик перемещения игрока.
    """
    if sid in game_state["players"]:
        game_state["players"][sid]["x"] += data["dx"]
        game_state["players"][sid]["y"] += data["dy"]

    # Обновляем всем состояние игры
    await sio.emit("update_game_state", game_state)
