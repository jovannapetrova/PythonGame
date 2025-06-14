import pygame
import random

def start_kolicina_level2():
    pygame.init()

    # Fullscreen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Игра со форми")

    # Load images and sounds
    confetti_img = pygame.image.load("../Pictures-Game3/confetti.png")
    sad_face_img = pygame.image.load("../Pictures-Game3/sad_face.png")
    background_img = pygame.image.load("../pictures/cloudsbackground.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    cloud_img = pygame.image.load("../pictures/clouds.png").convert_alpha()

    mask = pygame.mask.from_surface(cloud_img)
    crop_rect = mask.get_bounding_rects()[0]

    cropped_cloud = pygame.Surface((crop_rect.width, crop_rect.height), pygame.SRCALPHA)
    cropped_cloud.blit(cloud_img, (0, 0), crop_rect)

    cloud_w, cloud_h = 350, 160
    cloud_img = pygame.transform.scale(cropped_cloud, (cloud_w, cloud_h))

    correct_sound = pygame.mixer.Sound("C:\\Users\\PC\\PycharmProjects\\CekorPoCekor\\sounds\\correct.wav")
    wrong_sound = pygame.mixer.Sound("C:\\Users\\PC\\PycharmProjects\\CekorPoCekor\\sounds\\wrong.mp3")

    # Fonts
    FONT = pygame.font.SysFont("Comic Sans MS", 26)
    BIG_FONT = pygame.font.SysFont("Comic Sans MS", 54)
    OPTION_FONT = pygame.font.SysFont("Comic Sans MS", 48)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PINK = (255, 182, 193)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    SHAPE_COLORS = {
        'кругови': (255, 100, 100),
        'триаголници': (255, 215, 0),
        'квадрати': (100, 200, 255)
    }

    all_shapes = ['кругови', 'триаголници', 'квадрати']
    shape_size = 30

    # Shape drawing functions
    def draw_circle(x, y, size=shape_size):
        pygame.draw.circle(screen, SHAPE_COLORS['кругови'], (x, y), size)

    def draw_square(x, y, size=shape_size):
        pygame.draw.rect(screen, SHAPE_COLORS['квадрати'], (x - size, y - size, size * 2, size * 2), border_radius=8)

    def draw_triangle(x, y, size=shape_size):
        points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
        pygame.draw.polygon(screen, SHAPE_COLORS['триаголници'], points)

    def show_feedback(is_correct):
        if is_correct:
            correct_sound.play()
            img = confetti_img
            text = "                 Браво! Точен одговор!"
            color = GREEN
            bg_color = WHITE  # Боја за цел екран кога е точен одговор
        else:
            wrong_sound.play()
            img = sad_face_img
            text = f"Погрешно! Точен одговор: {correct_answer}"
            color = RED
            bg_color = WHITE  # Боја за цел екран кога е погрешен одговор

        screen.fill(bg_color)  # Пополнуваме го целиот екран со боја
        txt_surf = BIG_FONT.render(text, True, color)
        screen.blit(txt_surf, (WIDTH // 2 - txt_surf.get_width() // 2, 100))
        img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(img, img_rect)
        pygame.display.flip()
        pygame.time.wait(1500)

    def draw_shape(shape, x, y):
        if shape == 'кругови':
            draw_circle(x, y)
        elif shape == 'квадрати':
            draw_square(x, y)
        elif shape == 'триаголници':
            draw_triangle(x, y)

    def generate_cloud(min_shapes=2, max_shapes=7):
        return [random.choice(all_shapes) for _ in range(random.randint(min_shapes, max_shapes))]

    def draw_cloud(x, y):
        screen.blit(cloud_img, (x, y))

    def count_shape_in_cloud(cloud, shape):
        return cloud.count(shape)

    def generate_options(correct_answer):
        options = [correct_answer]
        while len(options) < 4:
            choice = random.randint(max(0, correct_answer - 3), correct_answer + 3)
            if choice not in options:
                options.append(choice)
        random.shuffle(options)
        return options

    def draw_operator(x, y, operator):
        op_surf = BIG_FONT.render(operator, True, BLACK)
        screen.blit(op_surf, (x, y))

    def draw_button(text, rect, active=False):
        pygame.draw.rect(screen, PINK, rect, border_radius=12)
        border_color = GREEN if active else BLACK
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=12)

        font_size = 26
        btn_font = pygame.font.SysFont("Comic Sans MS", font_size)
        txt_surf = btn_font.render(text, True, BLACK)

        while (txt_surf.get_width() > rect.width - 10 or txt_surf.get_height() > rect.height - 10) and font_size > 10:
            font_size -= 1
            btn_font = pygame.font.SysFont("Comic Sans MS", font_size)
            txt_surf = btn_font.render(text, True, BLACK)

        screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width()) // 2,
                               rect.y + (rect.height - txt_surf.get_height()) // 2))

    def draw_cloud_shapes(cloud, x, y, w, h):
        num = len(cloud)
        if num == 0:
            return
        shape_spacing = (w - 60) // max(1, num)
        shape_size_small = 20
        center_y = y + h // 2

        # Почнуваме од десната страна на облакот
        start_x = x + w - 30  # 30 пиксели маргина од десната страна

        # Цртаме од десно кон лево
        for i, shape in enumerate(cloud):
            pos_x = start_x - i * shape_spacing
            draw_shape_with_size(shape, pos_x, center_y, shape_size_small)

    def draw_shape_with_size(shape, x, y, size):
        if shape == 'кругови':
            pygame.draw.circle(screen, SHAPE_COLORS['кругови'], (x, y), size)
        elif shape == 'квадрати':
            pygame.draw.rect(screen, SHAPE_COLORS['квадрати'], (x - size, y - size, size * 2, size * 2),
                             border_radius=6)
        elif shape == 'триаголници':
            points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
            pygame.draw.polygon(screen, SHAPE_COLORS['триаголници'], points)

    def generate_question(level):
        while True:
            if level == 1:  # Лесно
                num_clouds = 2
                operator = random.choice(['+', '-'])
            elif level == 2:  # Средно
                num_clouds = 3
                operator = '+'
            else:  # Тешко
                num_clouds = 3
                operator = random.choice(['+', '-'])

            clouds = [generate_cloud(2, 6) for _ in range(num_clouds)]
            shape = random.choice(all_shapes)

            if operator == '+':
                correct = sum(count_shape_in_cloud(c, shape) for c in clouds)
            else:
                correct = count_shape_in_cloud(clouds[0], shape)
                for c in clouds[1:]:
                    correct -= count_shape_in_cloud(c, shape)

            if correct >= 0:
                return f"Колку {shape} има во облаците?", clouds, shape, operator, correct

    # Game state
    players = []
    current_player_index = 0

    def add_new_player():
        players.append({'name': f"Играч {len(players) + 1}", 'points': 0})

    add_new_player()
    level = 1
    level_names = ["Лесно", "Средно", "Тешко"]

    # GUI layout
    btn_w, btn_h = 160, 50
    level_buttons = [
        pygame.Rect(WIDTH - 20 - (i + 1) * (btn_w + 20), HEIGHT - 80, btn_w, btn_h)
        for i in range(3)
    ]

    show_results_btn = pygame.Rect(30, HEIGHT - 100, 200, 50)
    new_player_btn = pygame.Rect(250, HEIGHT - 100, 200, 50)
    back_level_btn = pygame.Rect(250, HEIGHT - 100, 200, 50)
    question_text, clouds, shape, operator, correct_answer = generate_question(level)
    options = generate_options(correct_answer)
    selected = None
    result = None
    show_results = False

    def reset_game(selected_level):
        global level, question_text, clouds, shape, operator, correct_answer, options, selected, result, show_results
        level = level_names.index(selected_level) + 1
        question_text, clouds, shape, operator, correct_answer = generate_question(level)
        options = generate_options(correct_answer)
        selected = None
        result = None
        show_results = False

    reset_game("Лесно")

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background_img, (0, 0))
        current_player = players[current_player_index]

        screen.blit(FONT.render(f"Играч: {current_player['name']}", True, BLACK), (20, 20))
        screen.blit(FONT.render(f"Поени: {current_player['points']}", True, BLACK), (20, 70))

        if show_results:
            y = 150
            for p in players:
                score = BIG_FONT.render(f"{p['name']}: {p['points']} поени", True, BLACK)
                screen.blit(score, (WIDTH // 2 - score.get_width() // 2, y))
                y += 70
            draw_button("Нов играч", new_player_btn)
            draw_button("Назад", show_results_btn)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_player_btn.collidepoint(event.pos):
                        add_new_player()
                        current_player_index = len(players) - 1
                        reset_game(level_names[level - 1])
                    elif show_results_btn.collidepoint(event.pos):
                        show_results = False
            clock.tick(30)
            continue

        q_surf = BIG_FONT.render(question_text, True, BLACK)
        screen.blit(q_surf, (WIDTH // 2 - q_surf.get_width() // 2, 120))

        cloud_w, cloud_h = 350, 160
        space = 100
        total_clouds_width = len(clouds) * cloud_w + (len(clouds) - 1) * space
        start_x = WIDTH // 2 - total_clouds_width // 2
        for i, c in enumerate(clouds):
            x = start_x + i * (cloud_w + space)
            y = HEIGHT // 2 - cloud_h // 2
            draw_cloud(x, y)
            draw_cloud_shapes(c, x, y, cloud_w, cloud_h)

        if len(clouds) == 2:
            draw_operator(start_x + cloud_w + space // 2 - 10, HEIGHT // 2 - 30, operator)
        elif len(clouds) == 3:
            # Цртај оператор помеѓу првиот и вториот облак
            draw_operator(start_x + cloud_w + space // 2 - 10, HEIGHT // 2 - 30, operator)
            # За едноставност, кај 3 облаци ќе го повториме операторот меѓу вториот и третиот облак
            draw_operator(start_x + 2 * (cloud_w + space) - 30, HEIGHT // 2 - 30, operator)

        # Draw numeric options
        btn_y = HEIGHT - 220
        total_w = 4 * 130 + 3 * 30
        start_opt_x = WIDTH // 2 - total_w // 2

        for i, opt in enumerate(options):
            rect = pygame.Rect(start_opt_x + i * (130 + 30), btn_y, 130, 70)
            color = GREEN if selected == opt else PINK
            pygame.draw.rect(screen, color, rect, border_radius=12)
            txt_surf = OPTION_FONT.render(str(opt), True, BLACK)
            screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width()) // 2,
                                   rect.y + (rect.height - txt_surf.get_height()) // 2))

        # Draw buttons: Нов играч и Прикажи резултати
        draw_button("Нов играч", new_player_btn)
        draw_button("Прикажи резултати", show_results_btn)
        draw_button("Претходен левел", back_level_btn)
        # Draw level buttons bottom right
        for i, rect in enumerate(level_buttons):
            is_active = (level == i + 1)
            draw_button(level_names[i], rect, active=is_active)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Check options clicked
                btn_y = HEIGHT - 220
                for i, opt in enumerate(options):
                    rect = pygame.Rect(WIDTH // 2 - (4 * 130 + 3 * 30) // 2 + i * (130 + 30), btn_y, 130, 70)
                    if rect.collidepoint(mx, my):
                        selected = opt
                        if selected == correct_answer:
                            current_player['points'] += 1
                            show_feedback(True)
                        else:
                            show_feedback(False)
                        reset_game(level_names[level - 1])
                        break

                # Check new player button
                if new_player_btn.collidepoint(mx, my):
                    add_new_player()
                    current_player_index = len(players) - 1
                    reset_game(level_names[level - 1])
                if back_level_btn.collidepoint(mx, my):
                    running = False
                    from NIVO3.level1 import start_kolicina_game
                    start_kolicina_game()
                # Check show results button
                if show_results_btn.collidepoint(mx, my):
                    show_results = True

                # Check level buttons
                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(mx, my):
                        reset_game(level_names[i])
                        current_player_index = 0
                        break

        clock.tick(30)

    pygame.quit()