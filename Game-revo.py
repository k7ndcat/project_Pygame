import pygame
import sys
import random
import math


class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface, offset_x, offset_y):
        """Рисует шарик на переданной поверхности."""
        pygame.draw.circle(surface, self.color, (self.x + offset_x, self.y + offset_y), self.radius)

    def is_on(self, offset_x, offset_y):
        pass

    def cube_in(self):
        distance = math.sqrt((center[0] - self.x) ** 2 + (center[1] - self.y) ** 2)
        return distance < self.radius
    def is_overlapping(self, other_ball):
        """Проверяет наложение с другим шариком."""
        distance = math.sqrt((self.x - other_ball.x) ** 2 + (self.y - other_ball.y) ** 2)
        return distance < (self.radius + other_ball.radius)

    @staticmethod
    def generate_non_overlapping_balls(num_balls, radius, screen_width, screen_height):
        """Генерирует список шариков с случайными координатами без наложений."""
        balls = []
        while len(balls) < num_balls:
            new_x = random.randint(radius, screen_width - radius)
            new_y = random.randint(radius, screen_height - radius)
            new_ball = Ball(new_x, new_y, radius, RED)  # Цвет красный

            if all(not new_ball.is_overlapping(existing_ball) for existing_ball in balls):
                balls.append(new_ball)

        return balls


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
cube_y = (screen_size[1] - cube_size - 25)  # Позиция по Y (центр)
cube_сentrer = cube_x + cube_size // 2, cube_y + cube_size // 2
center = cube_сentrer

# Смещения для движения области
offset_x = 0
offset_y = 0
speed = 5  # Скорость движения области
clock = pygame.time.Clock()
# Генерация случайных объектов
num_balls = 50  # Количество шариков
ball_radius = 20

balls = Ball.generate_non_overlapping_balls(num_balls, ball_radius, screen_size[0], screen_size[1])

# Загрузка спрайтов
target_image = pygame.image.load('pngwing.com.png').convert_alpha()  # Замените 'target.png' на путь к вашему изображению мишени
gun_image = pygame.image.load('143013e2865f33cc72738bd54ce5ede1.png').convert_alpha()  # Замените 'gun.png' на путь к вашему изображению пистолета



# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(len(balls)):
                    if balls[i].cube_in():
                        del balls[i]
                        print('Попал')
                        break
                else:
                    print('Мимо')

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



    center = cube_сentrer[0] - offset_x, cube_сentrer[1] - offset_y
    # Ограничение смещения в пределах окна
    if offset_x < (-screen_size[0] // 2):
        offset_x = (-screen_size[0] // 2)
    elif offset_x > (screen_size[0] // 2 + cube_size):
        offset_x = (screen_size[0] // 2 + cube_size)
    offset_y = max(-cube_size, min(offset_y, screen_size[1]))

    # Заполнение фона белым цветом
    screen.fill((0,0,0))

    # Рисуем случайные объекты
    for ball in balls:
        ball.draw(screen, offset_x, offset_y)


    # Рисуем мишени на шариках
    for ball in balls:
        target_rect = target_image.get_rect(center=(ball.x + offset_x, ball.y + offset_y))
        screen.blit(target_image, target_rect.topleft)

    screen.blit(gun_image, (cube_сentrer[0] - gun_image.get_width() // 2,
                            cube_сentrer[1] - gun_image.get_height() // 2))


    # Обновление дисплея
    pygame.display.flip()
    clock.tick(60)
