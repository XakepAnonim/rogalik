import pygame
import socketio

# Параметры Pygame
WIDTH, HEIGHT = 640, 480
FPS = 60

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogalik Client")
clock = pygame.time.Clock()

# Подключение к серверу через socketio
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from server")


@sio.event
def update_game_state(data):
    """
    Обновление состояния игры на основе данных с сервера.
    """
    print(f"Received game state: {data}")


def main():
    # Подключаемся к серверу
    sio.connect("http://127.0.0.1:8000", transports=["websocket"])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Основной игровой цикл
        screen.fill((0, 0, 0))  # Заливка экрана чёрным
        pygame.display.flip()
        clock.tick(FPS)

    # Завершение работы
    sio.disconnect()
    pygame.quit()


if __name__ == "__main__":
    main()
