import pygame
import sys
import random
import math
import time

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
BLACK = (0, 0, 0)


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

    def cube_in(self, center):
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



# Функция для отображения текста
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x - text_surface.get_width() // 2,
                                y - text_surface.get_height() // 2))


# Экран регистрации пользователя
def registration_screen():
    input_box_name = pygame.Rect(50, 200, 500, 50)
    input_box_password = pygame.Rect(50, 300, 500, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_name = color_inactive
    color_password = color_inactive
    active_name = False
    active_password = False
    name_text = ''
    password_text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_name.collidepoint(event.pos):
                    active_name = True
                    active_password = False
                elif input_box_password.collidepoint(event.pos):
                    active_password = True
                    active_name = False
                else:
                    active_name = False
                    active_password = False

                color_name = color_active if active_name else color_inactive
                color_password = color_active if active_password else color_inactive

            if event.type == pygame.KEYDOWN:
                if active_name:
                    if event.key == pygame.K_RETURN:
                        print(
                            f"Имя: {name_text}, Пароль: {password_text}")  # Здесь можно добавить логику для проверки учетной записи.
                        return name_text.strip() or "Игрок"
                    elif event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    else:
                        name_text += event.unicode

                if active_password:
                    if event.key == pygame.K_RETURN:
                        print(
                            f"Имя: {name_text}, Пароль: {password_text}")  # Здесь можно добавить логику для проверки учетной записи.
                        return name_text.strip() or "Игрок"
                    elif event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

        screen.fill((0,0,0))
        font = pygame.font.SysFont('arial', 24)
        screen.blit(font.render('Введите ваше имя', True, (255, 255, 255)), (50, 160))
        screen.blit(font.render('Введите пароль', True, (255, 255, 255)), (50,260))


        txt_surface_name = pygame.font.Font(None, 32).render(name_text, True, WHITE)
        input_box_name.w = max(200, txt_surface_name.get_width() + 10)

        screen.blit(txt_surface_name, (input_box_name.x + 5, input_box_name.y + 5))
        pygame.draw.rect(screen, color_name, input_box_name, 2)



        # Отображаем пароль как звёздочки
        txt_surface_password = pygame.font.Font(None, 52).render('*' * len(password_text), True, WHITE)
        input_box_password.w = max(200, txt_surface_password.get_width() + 10)

        screen.blit(txt_surface_password, (input_box_password.x + 5, input_box_password.y + 5))
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        screen.blit(font.render('Нажмите Enter для продолжения', True, (255, 255, 255)), (50, 360))


        pygame.display.flip()

def show_result_screen_game1(elapsed_time, penalty):
    """Отображает экран с результатами."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont('arial', 36)

        # Форматирование строки времени и штрафа
        time_string = f"Общее время: {elapsed_time / 10:.1f} сек"
        penalty_string = f"Штрафные секунды: {penalty * 3} сек"
        record = f"Рекорд: {penalty} сек"

        # Рендеринг текста
        time_surface = font.render(time_string, True, (255, 255, 255))
        penalty_surface = font.render(penalty_string, True, (255, 255, 255))
        record_surface = font.render(record, True, (255, 255, 255))

        # Отображение текста на экране
        screen.blit(time_surface, (50, 200))
        screen.blit(penalty_surface, (50, 250))
        screen.blit(record_surface, (50, 300))

        pygame.display.flip()


def game1(player_name):
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

    # Генерация случайных объектов
    num_balls = 50  # Количество шариков
    ball_radius = 20

    balls = Ball.generate_non_overlapping_balls(num_balls, ball_radius, screen_size[0], screen_size[1])
    penalty = 0  # штрафные секунды (3)
    # Загрузка спрайтов
    target_image = pygame.image.load(
        'pngwing.com.png').convert_alpha()  # Замените 'target.png' на путь к вашему изображению мишени
    gun_image = pygame.image.load(
        '143013e2865f33cc72738bd54ce5ede1.png').convert_alpha()  # Замените 'gun.png' на путь к вашему изображению пистолета
    clock = pygame.time.Clock()
    start_time = time.time()

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
                        if balls[i].cube_in(center):
                            del balls[i]
                            print('Попал')
                            break
                    else:
                        print('Мимо')
                        penalty += 1

        if not balls:
            end_time = time.time()  # Время окончания игры
            total_time = end_time - start_time + penalty * 3  # Общее время с учетом штрафа
            show_result_screen_game1(elapsed_time + penalty * 3 * 10, penalty)
            break
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

        screen.fill((0, 0, 0))
        # Текущее время игры без учета штрафов
        current_time = time.time() - start_time

        # Рисуем случайные объекты
        for ball in balls:
            ball.draw(screen, offset_x, offset_y)

        elapsed_time = pygame.time.get_ticks() // 100  # Переводим в секунды
        font = pygame.font.SysFont('arial', 24)
        # Форматирование строки времени
        time_string = f"{current_time + penalty * 3:.1f} с"

        # Рендеринг текста
        text_surface = font.render(time_string, True, (255, 255, 255))  # Белый текст

        # Отображение текста на экране
        screen.blit(text_surface, (10, 10))
        # Рисуем мишени на шариках
        for ball in balls:
            target_rect = target_image.get_rect(center=(ball.x + offset_x, ball.y + offset_y))
            screen.blit(target_image, target_rect.topleft)

        screen.blit(gun_image, (cube_сentrer[0] - gun_image.get_width() // 2,
                                cube_сentrer[1] - gun_image.get_height() // 2))

        # Обновление дисплея
        pygame.display.flip()
        clock.tick(60)


# Главное меню игры с выбором режима
def main_menu():
    player_name = registration_screen()  # Получаем имя пользователя

    while True:
        screen.fill(WHITE)

        draw_text(screen,
                  f'Добро пожаловать, {player_name}!',
                  48,
                  BLACK,
                  screen_size[0] // 2,
                  screen_size[1] // 4)

        draw_text(screen,
                  'Выберите режим игры:',
                  36,
                  BLACK,
                  screen_size[0] // 2,
                  screen_size[1] // 2 - 50)

        draw_text(screen,
                  '1. Без промахов',
                  36,
                  BLACK,
                  screen_size[0] // 2,
                  screen_size[1] // 2)

        draw_text(screen,
                  '2. На скорость',
                  36,
                  BLACK,
                  screen_size[0] // 2,
                  screen_size[1] // 2 + 50)

        draw_text(screen,
                  'Нажмите 1 или 2, чтобы выбрать режим.',
                  24,
                  BLACK,
                  screen_size[0] // 2,
                  screen_size[1] // 2 + 150)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Режим без промахов
                    print(1)
                    game1(player_name)
                elif event.key == pygame.K_2:  # Режим на скорость
                    game2(player_name)  '''  # Эта функция должна быть реализована


# Запуск главного меню игры
main_menu()
