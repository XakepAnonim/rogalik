"""
Запуск pygame.
"""

import asyncio

import pygame
import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.event
def response(data):
    print("Response from server:", data)


@sio.event
def disconnect():
    print("Disconnected from server")


async def main() -> None:
    """
    Основной метод для запуска pygame.
    """
    sio.connect("http://localhost:8000/socket")

    # Пример отправки события
    sio.emit("action", {"action": "my_event", "data": "Hello from Pygame!"})

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    sio.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
