import pygame
import sys

# Константы
WIDTH, HEIGHT = 400, 300
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50

# Цвета кнопок
BUTTON_COLOR_1 = (255, 0, 0)  # Красный
BUTTON_COLOR_2 = (0, 255, 0)  # Зеленый
BUTTON_COLOR_3 = (0, 0, 255)  # Синий
BUTTON_HOVER_COLOR = (150, 150, 150)

# Функция для рисования кнопки
def draw_button(screen, x, y, width, height, color, text=''):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Изменение цвета кнопки при наведении мыши
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Отображение текста на кнопке
    if text:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sniper')

    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Очистка экрана
        screen.fill((255, 255, 255))

        # Рисование кнопок с разными цветами и расположением
        draw_button(screen, 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR_1, 'Ruke')
        draw_button(screen, 50, 120, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR_2, 'Settings')
        draw_button(screen, 50, 190, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR_3, 'Play')

        # Обновление экрана
        pygame.display.flip()
