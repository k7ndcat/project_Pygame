import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Установка размеров окна
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Случайные объекты вокруг кубика")

# Определение цветов
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Параметры кубика
cube_size = 50
cube_x = (screen_size[0] - cube_size) // 2  # Позиция по X (центр)
cube_y = (screen_size[1] - cube_size - 25)   # Позиция по Y (центр)

# Смещения для движения области
offset_x = 0
offset_y = 0
speed = 5  # Скорость движения области
clock = pygame.time.Clock()
# Генерация случайных объектов
num_objects = 30  # Количество случайных объектов
objects = []

for _ in range(num_objects):
    obj_x = random.randint(0, screen_size[0] - cube_size)
    obj_y = random.randint(0, screen_size[1] - cube_size)
    objects.append((obj_x, obj_y))

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получаем состояние клавиш
    keys = pygame.key.get_pressed()

    # Движение области вокруг кубика
    if keys[pygame.K_w]:  # W - вверх
        offset_y += speed
    if keys[pygame.K_s]:  # S - вниз
        offset_y -= speed
    if keys[pygame.K_a]:  # A - влево
        offset_x += speed
    if keys[pygame.K_d]:  # D - вправоффв
        offset_x -= speed

    # Ограничение смещения в пределах окна
    offset_x = max(-screen_size[0], min(offset_x, screen_size[0] - cube_size))
    offset_y = max(-screen_size[1], min(offset_y, screen_size[1] - cube_size))

    # Заполнение фона белым цветом
    screen.fill(WHITE)

    # Рисуем случайные объекты
    for obj_x, obj_y in objects:
        pygame.draw.circle(screen, RED, (obj_x + offset_x, obj_y + offset_y), 20)  # Случайные красные круги

    # Рисуем кубик в центре экрана
    pygame.draw.rect(screen, BLUE, (cube_x, cube_y, cube_size, cube_size))

    # Обновление дисплея
    pygame.display.flip()
    clock.tick(60)
