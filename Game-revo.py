import pygame
import sys
import random
import math
import time
import sqlite3
import hashlib

# Инициализация Pygame
pygame.init()

# Установка размеров окна
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Game Revo")
count = 0
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


# Функция для создания базы данных
def create_database(db_name='game_records.db'):
    """Создает базу данных и необходимые таблицы, если они не существуют."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы для пользователей (id, login, password)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Создание таблицы для рекордов игры 2 (id, record)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records_game2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record INTEGER DEFAULT 0
        )
    ''')

    # Создание таблицы для рекордов игры 1 (id, record1, record2, record3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records_game1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record1 INTEGER DEFAULT -1,
            record2 INTEGER DEFAULT -1,
            record3 INTEGER DEFAULT -1
        )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Функция для регистрации пользователя
def register_user(login, password):
    """Регистрирует нового пользователя и заполняет базовые значения рекордов."""
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        # Вставка нового пользователя
        cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, hashed_password))
        user_id = cursor.lastrowid  # Получаем ID нового пользователя

        # Вставка базовых значений в таблицы рекордов
        cursor.execute("INSERT INTO records_game2 (record) VALUES (?)", (-1,))
        cursor.execute("INSERT INTO records_game1 (record1, record2, record3) VALUES (?, ?, ?)", (-1, -1, -1))

        conn.commit()
        return True  # Успешная регистрация
    except sqlite3.IntegrityError:
        return False  # Имя пользователя уже занято

    conn.close()


# Функция для проверки учетных данных пользователя
def check_user(login, password):
    """Проверяет учетные данные пользователя."""
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE login=? AND password=?", (login, hashed_password))
    user = cursor.fetchone()

    conn.close()

    return user is not None


def registration_screen():
    create_database()  # Создаем базу данных, если она не существует

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

    error_message = ''  # Переменная для хранения сообщения об ошибке

    # Определение размеров кнопок
    button_width = 200
    button_height = 50

    # Определение областей для кнопок
    sign_up_rect = pygame.Rect(50, 360, button_width, button_height)  # Кнопка Sign Up
    sign_in_rect = pygame.Rect(300, 360, button_width, button_height)  # Кнопка Sign In

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Обработка закрытия окна
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
                    if event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    else:
                        name_text += event.unicode

                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

            # Обработка нажатия кнопок "Sign Up" и "Sign In"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if sign_up_rect.collidepoint(mouse_pos):
                    if name_text.strip() and password_text.strip():
                        if register_user(name_text.strip(), password_text):
                            name_text = ''
                            password_text = ''
                            error_message = ''
                        else:
                            error_message = "Имя пользователя уже занято."
                    else:
                        error_message = "Недопустимый формат: имя и пароль не могут быть пустыми."

                elif sign_in_rect.collidepoint(mouse_pos):
                    if check_user(name_text.strip(), password_text):
                        print(f"Добро пожаловать обратно {name_text}!")
                        return name_text.strip() or "Игрок"
                    else:
                        error_message = "Неверные учетные данные. Попробуйте снова."

        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 24)

        screen.blit(font.render('Введите ваше имя', True, (255, 255, 255)), (50, 160))
        screen.blit(font.render('Введите пароль', True, (255, 255, 255)), (50, 260))

        txt_surface_name = pygame.font.Font(None, 32).render(name_text, True, WHITE)
        input_box_name.w = max(200, txt_surface_name.get_width() + 10)

        screen.blit(txt_surface_name, (input_box_name.x + 5, input_box_name.y + 5))
        pygame.draw.rect(screen, color_name, input_box_name, 2)

        # Отображаем пароль как звёздочки
        txt_surface_password = pygame.font.Font(None, 32).render('*' * len(password_text), True, WHITE)
        input_box_password.w = max(200, txt_surface_password.get_width() + 10)

        screen.blit(txt_surface_password, (input_box_password.x + 5, input_box_password.y + 5))
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        # Отображение кнопок "Sign Up" и "Sign In"
        pygame.draw.rect(screen, (100, 255, 100), sign_up_rect)
        sign_up_surface = font.render('Sign Up', True, (0, 0, 0))
        screen.blit(sign_up_surface,
                    (sign_up_rect.x + (button_width - sign_up_surface.get_width()) // 2,
                     sign_up_rect.y + (button_height - sign_up_surface.get_height()) // 2))

        pygame.draw.rect(screen, (255, 100, 100), sign_in_rect)
        sign_in_surface = font.render('Sign In', True, (0, 0, 0))
        screen.blit(sign_in_surface,
                    (sign_in_rect.x + (button_width - sign_in_surface.get_width()) // 2,
                     sign_in_rect.y + (button_height - sign_in_surface.get_height()) // 2))

        # Отображение сообщения об ошибке
        if error_message:
            error_surface = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (50, 430))

        pygame.display.flip()


def show_result_screen_game1(elapsed_time, penalty, difficulty):
    global player_name

    """Получает текущий рекорд и обновляет его, если новый результат лучше."""
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()

    # Выполняем запрос для получения id
    cursor.execute("SELECT id FROM users WHERE login=?", (player_name,))
    id = cursor.fetchone()[0]  # Получаем первую запись



    # Определяем, какое поле использовать в зависимости от сложности
    if difficulty == 15:
        cursor.execute("SELECT record1 FROM records_game1 WHERE id=?", (id,))
        record = cursor.fetchone()
        record = record[0]
        record_field = "record1"
    elif difficulty == 25:
        cursor.execute("SELECT record2 FROM records_game1 WHERE id=?", (id,))
        record = cursor.fetchone()
        record = record[0]
        record_field = "record2"
    elif difficulty == 40:
        cursor.execute("SELECT record3 FROM records_game1 WHERE id=?", (id,))
        record = cursor.fetchone()
        record = record[0]
        record_field = "record3"


    # Если рекорд отсутствует (-1) или новый результат лучше, обновляем его
    if record == -1 or float(elapsed_time) < record:
        cursor.execute(f"UPDATE records_game1 SET {record_field}=? WHERE id=?", (float(elapsed_time), id))
        conn.commit()


    conn.close()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont('arial', 36)

        # Получаем текущий рекорд и проверяем, нужно ли его обновить


        # Форматирование строк для отображения
        time_string = f"Общее время: {elapsed_time:.1f} сек"
        penalty_string = f"Штрафные секунды: {penalty * 3} сек"

        if record == -1 or float(elapsed_time) < record:
            record_message = f"Рекорд обновлен! Новый рекорд: {elapsed_time:.1f} сек"
        else:
            record_message = f"Текущий рекорд: {record:.1f} сек"

        # Рендеринг текста
        time_surface = font.render(time_string, True, (255, 255, 255))
        penalty_surface = font.render(penalty_string, True, (255, 255, 255))
        record_surface = font.render(record_message, True, (255, 255, 255))

        # Отображение текста на экране
        screen.blit(time_surface, (50, 200))
        screen.blit(penalty_surface, (50, 250))
        screen.blit(record_surface, (50, 300))

        pygame.display.flip()


def game1(num_balls):
    # Инициализация Pygame
    pygame.init()

    # Установка размеров окна
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Game_Revo_1")

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
    # Количество шариков
    ball_radius = 20

    balls = Ball.generate_non_overlapping_balls(num_balls, ball_radius, screen_size[0], screen_size[1])
    penalty = 0  # штрафные секунды (3)
    # Загрузка спрайтов
    target_image = pygame.image.load(
        'pngwing.com.png').convert_alpha()
    gun_image = pygame.image.load(
        'pisto.png').convert_alpha()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choose_difficulty()

        if not balls:
            show_result_screen_game1(elapsed_time, penalty, num_balls)
            break
        # Получаем состояние клавиш
        keys = pygame.key.get_pressed()

        # Движение области вокруг кубика
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # W или стрелка вверх
            offset_y += speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # S или стрелка вниз
            offset_y -= speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # A или стрелка влево
            offset_x += speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # D или стрелка вправо
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

        elapsed_time = float(f"{current_time + penalty * 3:.1f}")   # Переводим в секунды
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


def show_loss_screen_timeout(current_score):
    """Отображает экран с сообщением о проигрыше из-за истечения времени."""
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()
    # Выполняем запрос для получения id
    cursor.execute("SELECT id FROM users WHERE login=?", (player_name,))
    id = cursor.fetchone()[0]  # Получаем первую запись

    # Запрос всех рекордов из таблицы records_game2
    cursor.execute("SELECT * FROM records_game2")
    record = cursor.fetchall()[0]  # Получаем все записи
    record = record[1]

    if record < current_score:
        cursor.execute(f"UPDATE records_game2 SET record=? WHERE id=?", (current_score, id))
        conn.commit()


    conn.close()



    pygame.init()

    # Установка размеров окна
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Game_Revo_time")

    button_width = 300
    button_height = 60
    restart_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 50, button_width,
                               button_height)  # "Начать сначала"
    menu_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 120, button_width,
                            button_height)  # "Главное меню"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Проверяем левую кнопку мыши
                    mouse_pos = event.pos
                    if restart_rect.collidepoint(mouse_pos):
                        game2()
                    elif menu_rect.collidepoint(mouse_pos):
                        main_menu()

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont('arial', 36)

        # Форматирование строки с сообщением о проигрыше
        loss_message = "Вы проиграли! Время вышло."
        score_string = f"Текущий счет: {current_score} мишеней"
        if record > current_score:
            record_string = f"Рекорд: {record} мишеней"
        else:
            record_string = f"Рекорд: {current_score} мишеней"
        # Рендеринг текста
        loss_surface = font.render(loss_message, True, (255, 0, 0))  # Красный текст
        score_surface = font.render(score_string, True, (255, 255, 255))
        record_surface = font.render(record_string, True, (255, 255, 255))

        # Отображение текста на экране
        screen.blit(loss_surface, (50, 100))
        screen.blit(score_surface, (50, 150))
        screen.blit(record_surface, (50, 200))

        # Кнопка "Начать сначала"
        pygame.draw.rect(screen, (100, 100, 255), restart_rect)
        restart_surface = font.render('Начать сначала', True, (255, 255, 255))
        screen.blit(restart_surface,
                    (restart_rect.x + (button_width - restart_surface.get_width()) // 2,
                     restart_rect.y + (button_height - restart_surface.get_height()) // 2))

        # Кнопка "Главное меню"
        pygame.draw.rect(screen, (100, 100, 255), menu_rect)
        menu_surface = font.render('Главное меню', True, (255, 255, 255))
        screen.blit(menu_surface,
                    (menu_rect.x + (button_width - menu_surface.get_width()) // 2,
                     menu_rect.y + (button_height - menu_surface.get_height()) // 2))

        pygame.display.flip()


def show_loss_screen_miss(current_score):
    """Отображает экран с сообщением о проигрыше из-за промаха."""
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()
    # Выполняем запрос для получения id
    cursor.execute("SELECT id FROM users WHERE login=?", (player_name,))
    id = cursor.fetchone()[0]  # Получаем первую запись

    # Запрос всех рекордов из таблицы records_game2
    cursor.execute("SELECT * FROM records_game2")
    record = cursor.fetchall()[0]  # Получаем все записи
    record = record[1]

    if record < current_score:
        cursor.execute(f"UPDATE records_game2 SET record=? WHERE id=?", (current_score, id))
        conn.commit()

    conn.close()

    pygame.init()

    # Установка размеров окна
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Game_Revo_miss")
    # Определение областей для кнопок

    button_width = 300
    button_height = 60
    restart_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 50, button_width,
                               button_height)  # "Начать сначала"
    menu_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 120, button_width,
                            button_height)  # "Главное меню"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Проверяем левую кнопку мыши
                    mouse_pos = event.pos
                    if restart_rect.collidepoint(mouse_pos):
                        game2()

                    elif menu_rect.collidepoint(mouse_pos):
                        main_menu()

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont('arial', 36)

        # Форматирование строки с сообщением о проигрыше
        loss_message = "Вы проиграли! Вы промахнулись."
        score_string = f"Текущий счет: {current_score} мишеней"
        if record > current_score:
            record_string = f"Рекорд: {record} мишеней"
        else:
            record_string = f"Рекорд: {current_score} мишеней"

        # Рендеринг текста
        loss_surface = font.render(loss_message, True, (255, 0, 0))  # Красный текст
        score_surface = font.render(score_string, True, (255, 255, 255))
        record_surface = font.render(record_string, True, (255, 255, 255))

        # Отображение текста на экране
        screen.blit(loss_surface, (50, 100))
        screen.blit(score_surface, (50, 150))
        screen.blit(record_surface, (50, 200))

        # Кнопка "Начать сначала"
        pygame.draw.rect(screen, (100, 100, 255), restart_rect)
        restart_surface = font.render('Начать сначала', True, (255, 255, 255))
        screen.blit(restart_surface,
                    (restart_rect.x + (button_width - restart_surface.get_width()) // 2,
                     restart_rect.y + (button_height - restart_surface.get_height()) // 2))

        # Кнопка "Главное меню"
        pygame.draw.rect(screen, (100, 100, 255), menu_rect)
        menu_surface = font.render('Главное меню', True, (255, 255, 255))
        screen.blit(menu_surface,
                    (menu_rect.x + (button_width - menu_surface.get_width()) // 2,
                     menu_rect.y + (button_height - menu_surface.get_height()) // 2))
        pygame.display.flip()


def game2():
    global count
    # Инициализация Pygame
    pygame.init()

    # Установка размеров окна
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Game_Revo_2")

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
    ball_radius = 30

    # Загрузка спрайтов
    target_image = pygame.image.load('target2.png').convert_alpha()  # Замените 'target.png' на путь к вашему изображению мишени
    gun_image = pygame.image.load(
        '143013e2865f33cc72738bd54ce5ede1.png').convert_alpha()  # Замените 'gun.png' на путь к вашему изображению пистолета
    clock = pygame.time.Clock()
    ball = Ball(random.randint(ball_radius, screen_size[0] - ball_radius),
                random.randint(ball_radius, screen_size[1] - ball_radius), ball_radius, 'WhITE')
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
                    if ball.cube_in(center):
                        print('Попал')
                        count += 1
                        start_time = time.time()
                        ball = Ball(random.randint(center[0] + ball_radius - screen_size[0] // 2,
                                                   center[0] + screen_size[0] // 2 - ball_radius),
                                    random.randint(center[1] + ball_radius - screen_size[1] + 25 + cube_size // 2,
                                                   center[1] + 25 - ball_radius - cube_size // 2), ball_radius, 'Red')

                    else:
                        print('Мимо')
                        show_loss_screen_miss(count)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        # Получаем состояние клавиш
        keys = pygame.key.get_pressed()

        # Движение области вокруг кубика
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # W или стрелка вверх
            offset_y += speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # S или стрелка вниз
            offset_y -= speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # A или стрелка влево
            offset_x += speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # D или стрелка вправо
            offset_x -= speed

        center = cube_сentrer[0] - offset_x, cube_сentrer[1] - offset_y
        # Ограничение смещения в пределах окна

        screen.fill((0, 0, 0))
        # Получение времени работы программы в миллисекундах
        current_time = f'{3 + start_time - time.time():.1f}'  # Переводим в секунды
        if float(current_time) <= 0:
            show_loss_screen_timeout(count)

        # Рисуем случайные объекты
        ball.draw(screen, offset_x, offset_y)

        elapsed_time = pygame.time.get_ticks() // 100  # Переводим в секунды
        font = pygame.font.SysFont('arial', 24)
        # Форматирование строки времени
        time_string = f"{current_time} с"

        # Рендеринг текста
        text_surface = font.render(time_string, True, (255, 255, 255))  # Белый текст

        # Отображение текста на экране
        screen.blit(text_surface, (10, 10))
        # Рисуем мишени на шариках
        target_rect = target_image.get_rect(center=(ball.x + offset_x, ball.y + offset_y))
        screen.blit(target_image, target_rect.topleft)

        screen.blit(gun_image, (cube_сentrer[0] - gun_image.get_width() // 2,
                                cube_сentrer[1] - gun_image.get_height() // 2))

        # Обновление дисплея
        pygame.display.flip()
        clock.tick(60)


# Главное меню игры с выбором режима
def main_menu():
    global player_name

    # Установка шрифтов
    title_font = pygame.font.Font(None, 48)
    menu_font = pygame.font.Font(None, 36)
    instruction_font = pygame.font.Font(None, 24)

    # Определение размеров кнопок
    button_width = 300
    button_height = 60

    # Определение областей для кнопок
    option1_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 - 40, button_width,
                               button_height)  # "Без промахов"
    option2_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 40, button_width,
                               button_height)  # "На скорость"
    rules_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 140, button_width,
                             button_height)  # "Правила"

    while True:
        screen.fill(BLACK)

        # Отображение заголовка
        title_surface = title_font.render(f'Добро пожаловать, {player_name}!', True, WHITE)
        screen.blit(title_surface, (screen_size[0] // 2 - title_surface.get_width() // 2, screen_size[1] // 4))

        # Отображение меню
        menu_surface = menu_font.render('Выберите режим игры:', True, WHITE)
        screen.blit(menu_surface, (screen_size[0] // 2 - menu_surface.get_width() // 2, screen_size[1] // 2 - 100))

        # Кнопка "Без промахов"
        pygame.draw.rect(screen, (100, 100, 255), option1_rect)  # Цвет кнопки
        option1_surface = menu_font.render('Без промахов', True, WHITE)
        screen.blit(option1_surface, (option1_rect.x + (button_width - option1_surface.get_width()) // 2,
                                      option1_rect.y + (button_height - option1_surface.get_height()) // 2))

        # Кнопка "На скорость"
        pygame.draw.rect(screen, (100, 100, 255), option2_rect)
        option2_surface = menu_font.render('На скорость', True, WHITE)
        screen.blit(option2_surface, (option2_rect.x + (button_width - option2_surface.get_width()) // 2,
                                      option2_rect.y + (button_height - option2_surface.get_height()) // 2))

        # Кнопка "Правила"
        pygame.draw.rect(screen, (100, 100, 255), rules_rect)
        rules_surface = menu_font.render('Правила', True, WHITE)
        screen.blit(rules_surface, (rules_rect.x + (button_width - rules_surface.get_width()) // 2,
                                    rules_rect.y + (button_height - rules_surface.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player_name = registration_screen()
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Проверяем левую кнопку мыши
                    mouse_pos = event.pos
                    if option1_rect.collidepoint(mouse_pos):
                        game2()
                    elif option2_rect.collidepoint(mouse_pos):
                        choose_difficulty()  # Переход к выбору сложности
                    elif rules_rect.collidepoint(mouse_pos):
                        show_rules()  # Функция для отображения правил игры


def choose_difficulty():
    """Функция для выбора уровня сложности."""

    # Установка шрифтов
    title_font = pygame.font.Font(None, 48)
    menu_font = pygame.font.Font(None, 36)

    # Определение размеров кнопок
    button_width = 300
    button_height = 60

    # Определение областей для кнопок
    easy_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 - button_height - 20,
                            button_width, button_height)  # Легкий уровень
    medium_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + 20,
                              button_width, button_height)  # Средний уровень
    hard_rect = pygame.Rect((screen_size[0] - button_width) // 2, screen_size[1] // 2 + button_height + 60,
                            button_width, button_height)  # Сложный уровень

    while True:
        screen.fill(BLACK)

        # Отображение заголовка
        title_surface = title_font.render('Выберите уровень сложности:', True, WHITE)
        screen.blit(title_surface,
                    (screen_size[0] // 2 - title_surface.get_width() // 2,
                     screen_size[1] // 4))

        # Кнопка "Легкий"
        pygame.draw.rect(screen, (100, 255, 100), easy_rect)
        easy_surface = menu_font.render('Легкий', True, BLACK)
        screen.blit(easy_surface,
                    (easy_rect.x + (button_width - easy_surface.get_width()) // 2,
                     easy_rect.y + (button_height - easy_surface.get_height()) // 2))

        # Кнопка "Средний"
        pygame.draw.rect(screen, (255, 255, 100), medium_rect)
        medium_surface = menu_font.render('Средний', True, BLACK)
        screen.blit(medium_surface,
                    (medium_rect.x + (button_width - medium_surface.get_width()) // 2,
                     medium_rect.y + (button_height - medium_surface.get_height()) // 2))

        # Кнопка "Сложный"
        pygame.draw.rect(screen, (255, 100, 100), hard_rect)
        hard_surface = menu_font.render('Сложный', True, BLACK)
        screen.blit(hard_surface,
                    (hard_rect.x + (button_width - hard_surface.get_width()) // 2,
                     hard_rect.y + (button_height - hard_surface.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if easy_rect.collidepoint(mouse_pos):
                        game1(15)
                    elif medium_rect.collidepoint(mouse_pos):
                        game1(25)  # Функция для запуска игры на среднем уровне
                    elif hard_rect.collidepoint(mouse_pos):
                        game1(40)  # Функция для запуска игры на сложном уровне
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()


def game_speed_mode(player_name, game_speed):
    """Функция запускает игру с заданным уровнем сложности."""
    print(f"Запуск игры {game_speed} для игрока {player_name}.")
    # Здесь вы можете вызвать соответствующую функцию игры с параметрами сложности.


def show_rules():
    """Отображает экран с правилами игры."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        font = pygame.font.Font(None, 36)

        rules_texts = [
            "Правила игры:",
            "Управление происходит на кнопки 'WASD или 'стрелочки'",
            "Выстрел происходит на 'space'",
            "",
            "Игра 'Без промохов'",
            "На сбитие одной мишени - 3 секунды",
            "Если не успели или промахнулись— игра закончится.",
            "",
            "Игра 'На скорость'",
            "Вам нужно сбить все мишени за минимальное время",
            "За каждый промах начисляется штраф в 3 секунды", "",
            "Нажмите ESC для возврата в меню."

        ]

        for i, line in enumerate(rules_texts):
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface, (10, 50 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

    # Запуск главного меню игры


player_name = registration_screen()
print(player_name)
main_menu()
