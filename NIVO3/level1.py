import pygame
import random
import sys
from NIVO3.level2 import start_kolicina_level2
pygame.init()
def start_kolicina_game():
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Количина - Броење форми")
    # Вчитување и ресајз на background сликата
    confetti_img = pygame.image.load("../Pictures-Game3/confetti.png")
    sad_face_img = pygame.image.load("../Pictures-Game3/sad_face.png")
    character_img = pygame.image.load("../Pictures-Game3/person.png")  # Load character image
    character_img = pygame.transform.scale(character_img, (200, 200))  # Resize character
    correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
    wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()

    # После ова, скалирај ја сликата:
    background_img = pygame.image.load("../Pictures-Game3/bk.png").convert()
    background_img = pygame.transform.smoothscale(background_img, (WIDTH, HEIGHT))

    panda_img = pygame.image.load("../Pictures-Game3/panda.png")  # Заменете го со вистинскиот пат
    panda_img = pygame.transform.scale(panda_img, (50, 50))  # Големина на пандата
    FONT = pygame.font.SysFont("Arial", 48)
    SMALL_FONT = pygame.font.SysFont("Arial", 30)
    BUTTON_FONT = pygame.font.SysFont("Arial", 28)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 50, 50)
    GREEN = (50, 180, 50)
    BLUE = (50, 50, 220)
    GRAY = (220, 220, 220, 150)  # Now with transparency (alpha)
    DARK_GRAY = (120, 120, 120)

    clock = pygame.time.Clock()

    all_shapes = ["circle", "square", "triangle"]

    # Define the central rectangle for easy level
    EASY_AREA_WIDTH = WIDTH // 20
    EASY_AREA_HEIGHT = HEIGHT // 2 - 50
    EASY_AREA_X = (WIDTH - EASY_AREA_WIDTH) // 2
    EASY_AREA_Y = (HEIGHT - EASY_AREA_HEIGHT) // 2 - 90

    def generate_shapes_easy():
        target_shape = random.choice(all_shapes)
        target_count = random.randint(2, 4)
        distractor_count = random.randint(1, 3)
        shapes = []
        for _ in range(target_count):
            x = random.randint(EASY_AREA_X, EASY_AREA_X + EASY_AREA_WIDTH)
            y = random.randint(EASY_AREA_Y, EASY_AREA_Y + EASY_AREA_HEIGHT)
            shapes.append((target_shape, x, y))
        for _ in range(distractor_count):
            shape_type = random.choice([s for s in all_shapes if s != target_shape])
            x = random.randint(EASY_AREA_X, EASY_AREA_X + EASY_AREA_WIDTH)
            y = random.randint(EASY_AREA_Y, EASY_AREA_Y + EASY_AREA_HEIGHT)
            shapes.append((shape_type, x, y))
        random.shuffle(shapes)
        return shapes, target_shape, target_count

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

    def generate_shapes_hard():
        target_shape = random.choice(all_shapes)
        target_count = random.randint(8, 12)  # Повеќе таргет форми за тешко ниво
        distractor_count = random.randint(6, 10)  # И повеќе дистрактори
        shapes = []

        # Генерирај ги таргет формите на случајни позиции
        for _ in range(target_count):
            x = random.randint(80, WIDTH - 80)
            y = random.randint(150, HEIGHT - 150)
            shapes.append((target_shape, x, y))

        # Генерирај дистрактор форми (различен тип)
        for _ in range(distractor_count):
            shape_type = random.choice([s for s in all_shapes if s != target_shape])
            x = random.randint(80, WIDTH - 80)
            y = random.randint(150, HEIGHT - 150)
            shapes.append((shape_type, x, y))

        random.shuffle(shapes)
        bg_elements = []  # Празно, нема карактери
        return shapes, target_shape, target_count, bg_elements

    def draw_shape(shape, size=60):
        name, x, y = shape
        if name == "circle":
            pygame.draw.circle(screen, BLUE, (x, y), size // 2)
        elif name == "square":
            pygame.draw.rect(screen, GREEN, (x - size // 2, y - size // 2, size, size))
        elif name == "triangle":
            pygame.draw.polygon(screen, RED,
                                [(x, y - size // 2), (x - size // 2, y + size // 2), (x + size // 2, y + size // 2)])

    def draw_shape_icon(shape_name, x, y, size=60):
        if shape_name == "circle":
            pygame.draw.circle(screen, BLUE, (x + size // 2, y + size // 2), size // 2)
        elif shape_name == "square":
            pygame.draw.rect(screen, GREEN, (x, y, size, size))
        elif shape_name == "triangle":
            pygame.draw.polygon(screen, RED, [(x + size // 2, y), (x, y + size), (x + size, y + size)])

    def generate_options(correct):
        options = set()
        options.add(correct)
        while len(options) < 3:
            options.add(random.randint(1, 9))
        options = list(options)
        random.shuffle(options)
        return options

    def draw_button(text, x, y, w, h, color, action=None):
        button_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        button_surface.fill(color)
        screen.blit(button_surface, (x, y))
        label = BUTTON_FONT.render(text, True, BLACK)
        screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))
        return pygame.Rect(x, y, w, h)

    score = 0
    current_player = 1
    player_scores = {}
    showing_results = False
    current_level = "easy"  # Default level

    shapes, target_shape, correct_count = generate_shapes_easy()
    options = generate_options(correct_count)
    selected = None
    result = None
    bg_elements = []  # For hard level background elements

    # UI позиции
    LEFT_BUTTON_Y = HEIGHT - 80  # Moved up to make room for taller buttons
    LEVEL_BUTTON_Y = HEIGHT - 80  # Moved up to make room for taller buttons
    LEVEL_BUTTON_X_START = WIDTH - 660
    LEVEL_BUTTON_WIDTH = 200
    LEVEL_BUTTON_HEIGHT = 70  # Taller buttons
    LEVEL_BUTTON_SPACING = 20

    while True:
        if showing_results:
            screen.blit(background_img, (0, 0))

            title = FONT.render("Резултати", True, BLACK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

            sorted_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
            for i, (player, scr) in enumerate(sorted_scores):
                line = SMALL_FONT.render(f"{player}: {scr} поени", True, BLACK)
                screen.blit(line, (WIDTH // 2 - line.get_width() // 2, 230 + i * 35))

            back_btn = draw_button("Назад", WIDTH // 2 - 70, HEIGHT - 80, 140, 70, GRAY)
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

        # Draw character in top right with 15px margin
        screen.blit(character_img, (WIDTH - character_img.get_width() - 15, 5))

        # Draw the central rectangle for easy level
        if current_level == "easy":
            pygame.draw.rect(screen, WHITE, (EASY_AREA_X, EASY_AREA_Y, EASY_AREA_WIDTH, EASY_AREA_HEIGHT), 2)

        # Draw background elements for hard level
        if current_level == "hard":
            for elem_x, elem_y in bg_elements:
                screen.blit(character_img, (elem_x, elem_y))

        # Цртаме форми
        for shape in shapes:
            draw_shape(shape)

        # Димензии на правоаголникот за прашањето
        question_rect_width = 500  # Ширина
        question_rect_height = 80  # Висина
        question_rect_x = WIDTH // 2 - question_rect_width // 2  # Центрирано
        question_rect_y = 30  # Од горниот раб

        # Нацртај провиден правоаголник (RGBA за провидност)
        question_surface = pygame.Surface((question_rect_width, question_rect_height), pygame.SRCALPHA)
        question_surface.fill((220, 220, 220, 180))  # Сиво со провидност
        screen.blit(question_surface, (question_rect_x, question_rect_y - 20))

        # Текст "Колку" (почетокот е во правоаголникот, но поместен десно)
        question_text1 = FONT.render("Колку", True, BLACK)
        screen.blit(
            question_text1,
            (question_rect_x + 70,  # Поместено десно за да не се преклопува со пандата
             question_rect_y + question_rect_height // 2 - question_text1.get_height() // 2 - 20)
        )

        # Икона на формата што се бара
        draw_shape_icon(
            target_shape,
            question_rect_x + 70 + question_text1.get_width() + 15,  # Поместено уште десно
            question_rect_y + question_rect_height // 2 - 50,
            size=60
        )

        # Текст "ИМА?"
        question_text2 = FONT.render("ИМА?", True, BLACK)
        screen.blit(
            question_text2,
            (question_rect_x + 70 + question_text1.get_width() + 15 + 60 + 10,  # Поместено уште десно
             question_rect_y + question_rect_height // 2 - question_text2.get_height() // 2 - 20)
        )

        # Поени и играч - горен лев агол
        score_txt = SMALL_FONT.render(f"Поени: {score}", True, BLACK)
        screen.blit(score_txt, (20, 20))
        player_txt = SMALL_FONT.render(f"Играч: {current_player}", True, BLACK)
        screen.blit(player_txt, (20, 60))

        # Опции за одговор долу, во средина
        option_rects = []
        option_count = len(options)
        total_width = option_count * 150  # ширина по број (150 пкс на број, можеш да ја промениш)
        start_x = (
                              WIDTH - total_width) // 2 + 75  # почетна точка, +75 за половина од ширината на еден број (за центрирање)

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
            rect = txt.get_rect(center=(start_x + i * 150, HEIGHT - 140))  # позиција во средина хоризонтално
            screen.blit(txt, rect)
            option_rects.append((rect, i))

        # Копчиња за левата страна (нов играч, резултати) - now taller
        new_player_btn = draw_button("Нов играч", 20, LEFT_BUTTON_Y, 180, 70, GRAY)
        results_btn = draw_button("Резултати", 220, LEFT_BUTTON_Y, 180, 70, GRAY)
        back_main_btn = draw_button("Назад", 420, LEFT_BUTTON_Y, 180, 70, GRAY)
        next_btn = draw_button("Следно", 620, LEFT_BUTTON_Y, 180, 70, (180, 180, 255))

        # Копчиња за ниво - доле десно, хоризонтално - now taller
        level_easy_btn = draw_button("Ниво: Лесно", LEVEL_BUTTON_X_START, LEVEL_BUTTON_Y, LEVEL_BUTTON_WIDTH,
                                     LEVEL_BUTTON_HEIGHT, GRAY if current_level != "easy" else GREEN)
        level_medium_btn = draw_button("Ниво: Средно", LEVEL_BUTTON_X_START + LEVEL_BUTTON_WIDTH + LEVEL_BUTTON_SPACING,
                                       LEVEL_BUTTON_Y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT,
                                       GRAY if current_level != "medium" else GREEN)
        level_hard_btn = draw_button("Ниво: Тешко",
                                     LEVEL_BUTTON_X_START + 2 * (LEVEL_BUTTON_WIDTH + LEVEL_BUTTON_SPACING),
                                     LEVEL_BUTTON_Y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT,
                                     GRAY if current_level != "hard" else GREEN)

        # Прикажи резултат ако има
        if result:
            msg = FONT.render(result, True, BLACK)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_main_btn.collidepoint(mx, my):
                    running = False
                    from main.cpc import main
                    main()  # Назад кон почетното мени (cpc.py)
                if new_player_btn.collidepoint(mx, my):
                    player_scores[f"Играч {current_player}"] = score
                    current_player += 1
                    score = 0
                    if current_level == "easy":
                        shapes, target_shape, correct_count = generate_shapes_easy()
                    elif current_level == "medium":
                        shapes, target_shape, correct_count = generate_shapes_medium()
                    elif current_level == "hard":
                        shapes, target_shape, correct_count, bg_elements = generate_shapes_hard()
                    options = generate_options(correct_count)
                    selected = None
                    result = None
                if next_btn.collidepoint(mx, my):
                    player_scores[f"Играч {current_player}"] = score  # зачувај резултат
                    pygame.mixer.stop()  # стопирај звук ако има
                    start_kolicina_level2()  # одведи не во следното ниво

                if results_btn.collidepoint(mx, my):
                    player_scores[f"Играч {current_player}"] = score
                    showing_results = True

                if level_easy_btn.collidepoint(mx, my):
                    current_level = "easy"
                    shapes, target_shape, correct_count = generate_shapes_easy()
                    options = generate_options(correct_count)
                    selected = None
                    result = None
                    bg_elements = []

                if level_medium_btn.collidepoint(mx, my):
                    current_level = "medium"
                    shapes, target_shape, correct_count = generate_shapes_medium()
                    options = generate_options(correct_count)
                    selected = None
                    result = None
                    bg_elements = []

                if level_hard_btn.collidepoint(mx, my):
                    current_level = "hard"
                    shapes, target_shape, correct_count, bg_elements = generate_shapes_hard()
                    options = generate_options(correct_count)
                    selected = None
                    result = None

                # Проверка на одговор
                for rect, idx in option_rects:
                    if rect.collidepoint(mx, my) and selected is None:
                        selected = idx
                        if options[idx] == correct_count:
                            score += 1
                            correct_sound.play()  # Only play correct sound when correct
                        elif options[idx] != correct_count:
                            wrong_sound.play()
                        # Генерирај ново прашање после пауза
                        pygame.time.delay(500)  # Small delay before next question
                        if current_level == "easy":
                            shapes, target_shape, correct_count = generate_shapes_easy()
                        elif current_level == "medium":
                            shapes, target_shape, correct_count = generate_shapes_medium()
                        elif current_level == "hard":
                            shapes, target_shape, correct_count, bg_elements = generate_shapes_hard()
                        options = generate_options(correct_count)
                        selected = None
                        result = None