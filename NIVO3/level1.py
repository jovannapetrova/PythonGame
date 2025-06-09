import pygame
import random
import sys

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Количина - Броење форми")
# Вчитување и ресајз на background сликата
confetti_img = pygame.image.load("../pictures/confetti.png")
sad_face_img = pygame.image.load("../pictures/sad_face.png")
correct_sound = pygame.mixer.Sound("C:\\Users\\PC\\PycharmProjects\\CekorPoCekor\\sounds\\correct.wav")
wrong_sound = pygame.mixer.Sound("C:\\Users\\PC\\PycharmProjects\\CekorPoCekor\\sounds\\wrong.mp3")
background_img = pygame.image.load("../pictures/cloudsbackground.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

FONT = pygame.font.SysFont("Arial", 48)
SMALL_FONT = pygame.font.SysFont("Arial", 30)
BUTTON_FONT = pygame.font.SysFont("Arial", 28)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 180, 50)
BLUE = (50, 50, 220)
GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)

clock = pygame.time.Clock()

all_shapes = ["circle", "square", "triangle"]

def generate_shapes():
    target_shape = random.choice(all_shapes)
    target_count = random.randint(3, 6)
    distractor_count = random.randint(3, 5)
    shapes = []
    for _ in range(target_count):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(180, HEIGHT - 250)
        shapes.append((target_shape, x, y))
    for _ in range(distractor_count):
        shape_type = random.choice([s for s in all_shapes if s != target_shape])
        x = random.randint(100, WIDTH - 100)
        y = random.randint(180, HEIGHT - 250)
        shapes.append((shape_type, x, y))
    random.shuffle(shapes)
    return shapes, target_shape, target_count

def draw_shape(shape, size=60):
    name, x, y = shape
    if name == "circle":
        pygame.draw.circle(screen, BLUE, (x, y), size // 2)
    elif name == "square":
        pygame.draw.rect(screen, GREEN, (x - size // 2, y - size // 2, size, size))
    elif name == "triangle":
        pygame.draw.polygon(screen, RED, [(x, y - size // 2), (x - size // 2, y + size // 2), (x + size // 2, y + size // 2)])

def draw_shape_icon(shape_name, x, y, size=60):
    if shape_name == "circle":
        pygame.draw.circle(screen, BLUE, (x + size//2, y + size//2), size // 2)
    elif shape_name == "square":
        pygame.draw.rect(screen, GREEN, (x, y, size, size))
    elif shape_name == "triangle":
        pygame.draw.polygon(screen, RED, [(x + size//2, y), (x, y + size), (x + size, y + size)])

def generate_options(correct):
    options = set()
    options.add(correct)
    while len(options) < 3:
        options.add(random.randint(1, 9))
    options = list(options)
    random.shuffle(options)
    return options

def draw_button(text, x, y, w, h, color, action=None):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = BUTTON_FONT.render(text, True, BLACK)
    screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))
    return pygame.Rect(x, y, w, h)

score = 0
current_player = 1
player_scores = {}
showing_results = False

shapes, target_shape, correct_count = generate_shapes()
options = generate_options(correct_count)
selected = None
result = None

# UI позиции
LEFT_BUTTON_Y = HEIGHT - 70
LEVEL_BUTTON_Y = HEIGHT - 70
LEVEL_BUTTON_X_START = WIDTH - 660
LEVEL_BUTTON_WIDTH = 200
LEVEL_BUTTON_HEIGHT = 50
LEVEL_BUTTON_SPACING = 20

while True:
    if showing_results:
        screen.blit(background_img, (0, 0))

        title = FONT.render("Резултати", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (player, scr) in enumerate(sorted_scores):
            line = SMALL_FONT.render(f"{player}: {scr} поени", True, BLACK)
            screen.blit(line, (WIDTH // 2 - line.get_width() // 2, 100 + i * 35))

        back_btn = draw_button("Назад", WIDTH // 2 - 70, HEIGHT - 70, 140, 50, GRAY)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if back_btn.collidepoint(mx, my):
                        showing_results = False
                        waiting = False
        continue

    screen.blit(background_img, (0, 0))

    # Цртаме форми
    for shape in shapes:
        draw_shape(shape)

    # Прашање - подобро организирано со празно место
    question_x = WIDTH // 2 - 220
    question_y = 40
    question_text1 = FONT.render("Колку", True, BLACK)
    screen.blit(question_text1, (question_x, question_y))

    draw_shape_icon(target_shape, question_x + question_text1.get_width() + 30, question_y - 10, size=70)

    question_text2 = FONT.render("ИМА?", True, BLACK)
    screen.blit(question_text2, (question_x + question_text1.get_width() + 130, question_y))

    # Поени и играч - горен лев агол
    score_txt = SMALL_FONT.render(f"Поени: {score}", True, BLACK)
    screen.blit(score_txt, (20, 20))
    player_txt = SMALL_FONT.render(f"Играч: {current_player}", True, BLACK)
    screen.blit(player_txt, (20, 60))

    # Опции за одговор долу, во средина
    # Опции за одговор долу, во средина - ЦЕНТРИРАНИ
    option_rects = []
    option_count = len(options)
    total_width = option_count * 150  # ширина по број (150 пкс на број, можеш да ја промениш)
    start_x = (WIDTH - total_width) // 2 + 75  # почетна точка, +75 за половина од ширината на еден број (за центрирање)

    for i, val in enumerate(options):
        if selected is not None:
            if options[i] == correct_count and i == selected:
                color = GREEN
            elif i == selected:
                color = RED
            else:
                color = BLACK
        else:
            color = BLACK

        txt = pygame.font.SysFont("Arial", 48).render(str(val), True, color)  # Arial, 48pt, обичен
        rect = txt.get_rect(center=(start_x + i * 150, HEIGHT - 120))  # позиција во средина хоризонтално
        screen.blit(txt, rect)
        option_rects.append((rect, i))

    # Копчиња за левата страна (нов играч, резултати)
    new_player_btn = draw_button("Нов играч", 20, LEFT_BUTTON_Y, 180, 50, GRAY)
    results_btn = draw_button("Резултати", 220, LEFT_BUTTON_Y, 180, 50, GRAY)

    # Копчиња за ниво - доле десно, хоризонтално
    level_easy_btn = draw_button("Ниво: Лесно", LEVEL_BUTTON_X_START, LEVEL_BUTTON_Y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, GRAY)
    level_medium_btn = draw_button("Ниво: Средно", LEVEL_BUTTON_X_START + LEVEL_BUTTON_WIDTH + LEVEL_BUTTON_SPACING, LEVEL_BUTTON_Y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, GRAY)
    level_hard_btn = draw_button("Ниво: Тешко", LEVEL_BUTTON_X_START + 2*(LEVEL_BUTTON_WIDTH + LEVEL_BUTTON_SPACING), LEVEL_BUTTON_Y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, GRAY)

    # Прикажи резултат ако има
    if result:
        msg = FONT.render(result, True, BLACK)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 220))

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if new_player_btn.collidepoint(mx, my):
                player_scores[f"Играч {current_player}"] = score
                current_player += 1
                score = 0
                shapes, target_shape, correct_count = generate_shapes()
                options = generate_options(correct_count)
                selected = None
                result = None

            if results_btn.collidepoint(mx, my):
                player_scores[f"Играч {current_player}"] = score
                showing_results = True

            if level_easy_btn.collidepoint(mx, my):
                def generate_shapes_easy():
                    target_shape = random.choice(all_shapes)
                    target_count = random.randint(2, 4)
                    distractor_count = random.randint(1, 3)
                    shapes = []
                    for _ in range(target_count):
                        x = random.randint(100, WIDTH - 100)
                        y = random.randint(180, HEIGHT - 250)
                        shapes.append((target_shape, x, y))
                    for _ in range(distractor_count):
                        shape_type = random.choice([s for s in all_shapes if s != target_shape])
                        x = random.randint(100, WIDTH - 100)
                        y = random.randint(180, HEIGHT - 250)
                        shapes.append((shape_type, x, y))
                    random.shuffle(shapes)
                    return shapes, target_shape, target_count
                shapes, target_shape, correct_count = generate_shapes_easy()
                options = generate_options(correct_count)
                selected = None
                result = None

            if level_medium_btn.collidepoint(mx, my):
                def generate_shapes_medium():
                    target_shape = random.choice(all_shapes)
                    target_count = random.randint(3, 5)
                    distractor_count = random.randint(2, 4)
                    shapes = []
                    for _ in range(target_count):
                        x = random.randint(100, WIDTH - 100)
                        y = random.randint(180, HEIGHT - 250)
                        shapes.append((target_shape, x, y))
                    for _ in range(distractor_count):
                        shape_type = random.choice([s for s in all_shapes if s != target_shape])
                        x = random.randint(100, WIDTH - 100)
                        y = random.randint(180, HEIGHT - 250)
                        shapes.append((shape_type, x, y))
                    random.shuffle(shapes)
                    return shapes, target_shape, target_count
                shapes, target_shape, correct_count = generate_shapes_medium()
                options = generate_options(correct_count)
                selected = None
                result = None

            if level_hard_btn.collidepoint(mx, my):
                def generate_shapes_hard():
                    target_shape = random.choice(all_shapes)
                    target_count = random.randint(4, 7)
                    distractor_count = random.randint(3, 6)
                    shapes = []
                    for _ in range(target_count):
                        x = random.randint(100, WIDTH - 100)
                        y = random.randint(180, HEIGHT - 250)
                        shapes.append((target_shape, x, y))
                    for _ in range(distractor_count):
                        shape_type = random.choice([s for s in all_shapes if s != target_shape])
                        x = random.randint(100, WIDTH - 100)
                        y = random.randint(180, HEIGHT - 250)
                        shapes.append((shape_type, x, y))
                    random.shuffle(shapes)
                    return shapes, target_shape, target_count
                shapes, target_shape, correct_count = generate_shapes_hard()
                options = generate_options(correct_count)
                selected = None
                result = None

            # Проверка на одговор
            for rect, idx in option_rects:
                # Проверка на одговор
                for rect, idx in option_rects:
                    if rect.collidepoint(mx, my) and selected is None:
                        selected = idx
                        frozen = True  # Замрзни избор
                        if options[idx] == correct_count:
                            result = "Точно!"
                            score += 1
                            correct_sound.play()

                            # Екран со конфети
                            screen.blit(confetti_img, (
                            (WIDTH - confetti_img.get_width()) // 2, (HEIGHT - confetti_img.get_height()) // 2))
                            pygame.display.flip()
                            pygame.time.delay(2000)

                        else:
                            result = f"Неправилно! Точно е {correct_count}."
                            wrong_sound.play()

                            # Екран со тажен смајли
                            screen.blit(sad_face_img, (
                            (WIDTH - sad_face_img.get_width()) // 2, (HEIGHT - sad_face_img.get_height()) // 2))
                            pygame.display.flip()
                            pygame.time.delay(2000)

                        # Генерирај ново прашање после пауза
                        shapes, target_shape, correct_count = generate_shapes()
                        options = generate_options(correct_count)
                        selected = None
                        result = None
                        frozen = False
