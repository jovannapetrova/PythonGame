import pygame
import sys
import os
import random


def start_level2():
    # Иницијализација
    pygame.init()
    pygame.mixer.init()

    # Екран
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Сортирање предмети (Level 2)")

    # Звуци
    try:
        wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")
        correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
    except:
        wrong_sound = None
        correct_sound = None

    # Слики
    def load_image(name, scale=None):
        try:
            image = pygame.image.load(name)
            if scale:
                image = pygame.transform.scale(image, scale)
            return image
        except:
            return pygame.Surface((100, 100), pygame.SRCALPHA)

    try:
        background = load_image("../Pictures-Game6/landscape.png", (WIDTH, HEIGHT))
        panda_img = load_image("../Pictures-Game6/panda.png", (100, 100))
        blue_basket_img = load_image("../Pictures-Game6/bluebucket.png", (250, 250))
        red_basket_img = load_image("../Pictures-Game6/redbucket.png", (250, 250))
        panda_body_img = load_image("../Pictures-Game6/sittingpanda.png", (200, 200))
    except:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((200, 230, 255))

    # Фонт
    font = pygame.font.SysFont("Arial", 40)
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    bravo_font = pygame.font.SysFont("Arial", 80, bold=True)
    small_font = pygame.font.SysFont("Arial", 30, bold=True)

    # Играчи и резултати
    players = []
    current_player_index = -1
    scores = {}
    current_player = ""
    show_bravo = False
    bravo_timer = 0

    def add_new_player():
        nonlocal current_player_index, current_player
        new_player_name = f"Играч {len(players) + 1}"
        players.append(new_player_name)
        scores[new_player_name] = 0
        current_player_index = len(players) - 1
        current_player = new_player_name

    # Задачи и кутии
    tasks = [
        {"color": (0, 100, 255), "shape": "circle", "box": "blue",
         "description": "Стави ги сите сини кругови во сината кошница."},
        {"color": (255, 50, 50), "shape": "triangle", "box": "red",
         "description": "Стави ги сите црвени триаголници во црвената кошница."},
        {"color": (0, 100, 255), "shape": "triangle", "box": "blue",
         "description": "Стави ги сите сини триаголници во сината кошница."},
        {"color": (255, 50, 50), "shape": "square", "box": "red",
         "description": "Стави ги сите црвени квадрати во црвената кошница."},
    ]

    # Креирање кутии
    boxes = {}
    start_x = (WIDTH - (len(tasks) * 250 + (len(tasks) - 1) * 100)) // 2 - 270
    for i, task in enumerate(tasks):
        boxes[task["box"]] = pygame.Rect(
            start_x + i * (250 + 60),
            int(HEIGHT * 0.5),
            250,
            250
        )

    # Играчки објекти
    items = []
    current_task_index = 0

    def reset_items_for_task():
        nonlocal items, show_bravo, bravo_timer
        task = tasks[current_task_index]
        items = []
        num_correct = 3
        num_wrong = 2
        spacing = 150

        correct_items = [{
            "color": task["color"],
            "shape": task["shape"],
            "radius": 30,
            "dragging": False,
            "scored": False,
            "locked": False,
            "correct": True
        } for _ in range(num_correct)]

        other_color = (255, 50, 50) if task["color"] != (255, 50, 50) else (0, 100, 255)
        shapes = ["circle", "triangle", "square"]
        other_shapes = [s for s in shapes if s != task["shape"]]
        other_shape = random.choice(other_shapes)

        wrong_items = [{
            "color": other_color,
            "shape": other_shape,
            "radius": 30,
            "dragging": False,
            "scored": False,
            "locked": False,
            "correct": False
        } for _ in range(num_wrong)]

        items = correct_items + wrong_items
        random.shuffle(items)

        total_width = len(items) * spacing
        start_x_items = (WIDTH - total_width) // 2 + spacing // 2
        item_y_position = int(HEIGHT * 0.4)

        for i, item in enumerate(items):
            item["pos"] = [start_x_items + i * spacing, item_y_position]

        show_bravo = False
        bravo_timer = 0

    reset_items_for_task()

    # Функции за цртање
    def draw_shadowed_circle(surface, color, pos, radius):
        shadow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, 100)
        shadow_center = (radius * 2 + 3, radius * 2 + 3)
        pygame.draw.circle(shadow_surf, shadow_color, shadow_center, radius)
        surface.blit(shadow_surf, (pos[0] - radius * 2, pos[1] - radius * 2))
        pygame.draw.circle(surface, color, pos, radius)

    def draw_shadowed_triangle(surface, color, pos, size):
        shadow_surf = pygame.Surface((size * 6, size * 6), pygame.SRCALPHA)
        shadow_color = (0, 0, 0, 100)
        offset = 3
        x, y = size * 3, size * 3
        points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
        shadow_points = [(px + offset, py + offset) for px, py in points]
        pygame.draw.polygon(shadow_surf, shadow_color, shadow_points)
        pygame.draw.polygon(shadow_surf, color, points)
        surface.blit(shadow_surf, (pos[0] - size * 3, pos[1] - size * 3))

    def draw_square(surface, color, pos, size):
        x, y = pos
        rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
        pygame.draw.rect(surface, color, rect)

    def draw_player_panel():
        player_rect = pygame.Rect(120, 50, 300, 80)
        pygame.draw.rect(screen, (0, 50, 120), player_rect, border_radius=40)
        screen.blit(panda_img, (player_rect.left - 70, player_rect.centery - 50))
        player_text = title_font.render(current_player, True, (255, 255, 255))
        screen.blit(player_text, (player_rect.x + 50, player_rect.centery - player_text.get_height() // 2))

    def draw_instruction_panel():
        panel_width = WIDTH // 2 + 150
        instr_rect = pygame.Rect((WIDTH - panel_width) // 2, 140, panel_width, 80)
        pygame.draw.rect(screen, (150, 200, 255), instr_rect, border_radius=20)

        task = tasks[current_task_index]
        words = task["description"].split()
        if not words:
            return

        wrapped_text = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + " " + word
            if font.size(test_line)[0] < instr_rect.width - 40:
                current_line = test_line
            else:
                wrapped_text.append(current_line)
                current_line = word
        wrapped_text.append(current_line)

        max_lines = (instr_rect.height - 40) // 30
        if len(wrapped_text) > max_lines:
            wrapped_text = wrapped_text[:max_lines]
            wrapped_text[-1] += "..."

        for i, line in enumerate(wrapped_text):
            line_surface = small_font.render(line, True, (0, 50, 150))
            screen.blit(line_surface, (
                instr_rect.centerx - line_surface.get_width() // 2,
                instr_rect.y + 20 + i * 30
            ))

    def draw_simple_button(surface, rect, color, border_color, text, font, text_color=(0, 0, 0)):
        pygame.draw.rect(surface, border_color, rect, border_radius=15, width=3)
        pygame.draw.rect(surface, color, rect.inflate(-6, -6), border_radius=12)
        text_surf = font.render(text, True, text_color)
        surface.blit(text_surf, (rect.centerx - text_surf.get_width() // 2,
                                 rect.centery - text_surf.get_height() // 2))

    def draw_results_screen():
        screen.fill((210, 180, 140))
        panel_width = WIDTH * 0.5
        panel_height = HEIGHT * 0.6
        panel_x = (WIDTH - panel_width) // 2
        panel_y = (HEIGHT - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        pygame.draw.rect(screen, (139, 69, 19), panel_rect, border_radius=20)
        title = title_font.render("Резултати по играч:", True, (255, 255, 255))
        screen.blit(title, (panel_x + (panel_width - title.get_width()) // 2, panel_y + 20))

        y_offset = panel_y + 100
        for player, score in scores.items():
            text = font.render(f"{player}: {score} поени", True, (255, 255, 255))
            screen.blit(text, (panel_x + (panel_width - text.get_width()) // 2, y_offset))
            y_offset += 40

        back_button_rect = pygame.Rect(
            panel_x + (panel_width - 140) // 2,
            panel_y + panel_height - 70,
            140,
            50
        )
        pygame.draw.rect(screen, (255, 165, 0), back_button_rect, border_radius=15)
        text_surf = font.render("Назад", True, (0, 0, 0))
        screen.blit(text_surf, (
            back_button_rect.centerx - text_surf.get_width() // 2,
            back_button_rect.centery - text_surf.get_height() // 2
        ))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(pos):
                        waiting = False

    def is_item_in_box(item, box_rect, margin=0):
        x, y = item["pos"]
        r = item.get("radius", 0)

        if item["shape"] == "circle":
            return (x + r - margin) >= box_rect.left and (x - r + margin) <= box_rect.right and \
                (y + r - margin) >= box_rect.top and (y - r + margin) <= box_rect.bottom

        size = r
        if item["shape"] in ["square", "triangle"]:
            left = x - size
            right = x + size
            top = y - size
            bottom = y + size
            return (right - margin) >= box_rect.left and (left + margin) <= box_rect.right and \
                (bottom - margin) >= box_rect.top and (top + margin) <= box_rect.bottom

        return box_rect.collidepoint(x, y)

    def check_and_score_items():
        nonlocal current_task_index, show_bravo, bravo_timer
        task = tasks[current_task_index]
        box_rect = boxes[task["box"]]

        num_correct_items = 0
        num_correct_in_box = 0

        new_items = []
        for item in items:
            is_correct = item["color"] == task["color"] and item["shape"] == task["shape"]

            if is_correct:
                num_correct_items += 1
                if is_item_in_box(item, box_rect):
                    num_correct_in_box += 1
                    if not item["scored"]:
                        scores[current_player] += 5
                        item["scored"] = True
                        item["locked"] = True
                        if correct_sound:
                            correct_sound.play()
                        show_bravo = True
                        bravo_timer = pygame.time.get_ticks()
                    continue
                else:
                    new_items.append(item)
            else:
                if is_item_in_box(item, box_rect) and not item["locked"]:
                    if wrong_sound:
                        wrong_sound.play()
                    item["locked"] = True
                new_items.append(item)

        items[:] = new_items

        if num_correct_in_box == num_correct_items and num_correct_items > 0:
            current_task_index += 1
            if current_task_index >= len(tasks):
                current_task_index = 0
            reset_items_for_task()

    # Главна играчка јамка
    dragging_item = None
    offset_x = 0
    offset_y = 0

    # Дефинирање на копчињата пред главниот game loop
    button_width = 160
    button_height = 55
    back_player_button_rect = pygame.Rect(
        boxes["blue"].centerx - button_width // 2 - 220,
        boxes["blue"].bottom + 40,
        button_width,
        button_height
    )
    results_button_rect = pygame.Rect(
        boxes["blue"].centerx - button_width // 2,
        boxes["blue"].bottom + 40,
        button_width,
        button_height
    )
    new_player_button_rect = pygame.Rect(
        boxes["red"].centerx - button_width // 2,
        boxes["red"].bottom + 40,
        button_width,
        button_height
    )

    # Бои за копчиња
    blue_button_color = (173, 216, 230)
    blue_border_color = (224, 255, 255)
    red_button_color = (255, 182, 193)
    red_border_color = (255, 228, 225)
    gray_button_color = (200, 200, 200)
    gray_border_color = (150, 150, 150)

    # Додај го првиот играч
    add_new_player()

    running = True
    clock = pygame.time.Clock()

    while running:
        current_time = pygame.time.get_ticks()
        if show_bravo and current_time - bravo_timer > 2000:
            show_bravo = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if results_button_rect.collidepoint(pos):
                    draw_results_screen()
                elif new_player_button_rect.collidepoint(pos):
                    add_new_player()
                elif back_player_button_rect.collidepoint(pos):
                    from NIVO6.level1 import start_colorsAndshapes_game
                    start_colorsAndshapes_game()
                else:
                    # Проверка за предмети
                    for item in items:
                        if item["locked"]:
                            continue
                        x, y = item["pos"]
                        radius = item["radius"]
                        dx = pos[0] - x
                        dy = pos[1] - y
                        if abs(dx) <= radius * 1.5 and abs(dy) <= radius * 1.5:
                            dragging_item = item
                            offset_x = dx
                            offset_y = dy
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_item:
                    check_and_score_items()
                    dragging_item = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_item:
                    mx, my = event.pos
                    dragging_item["pos"][0] = mx - offset_x
                    dragging_item["pos"][1] = my - offset_y

        # Цртање
        screen.blit(background, (0, 0))
        screen.blit(panda_body_img, (50, HEIGHT - panda_body_img.get_height() - 50))

        # Панели
        draw_player_panel()
        if show_bravo:
            bravo_text = bravo_font.render("БРАВО!", True, (0, 30, 100))
            screen.blit(bravo_text, (WIDTH // 2 - bravo_text.get_width() // 2, 50))
        draw_instruction_panel()

        # Предмети
        for item in items:
            pos = item["pos"]
            color = item["color"]
            if item["shape"] == "circle":
                draw_shadowed_circle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
            elif item["shape"] == "triangle":
                draw_shadowed_triangle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
            elif item["shape"] == "square":
                draw_square(screen, color, (int(pos[0]), int(pos[1])), item["radius"])

        # Кошници
        for key, rect in boxes.items():
            if key == "blue":
                screen.blit(blue_basket_img, rect)
            else:
                screen.blit(red_basket_img, rect)

        # Цртање на копчиња
        draw_simple_button(screen, results_button_rect, blue_button_color, blue_border_color, "Резултати", font)
        draw_simple_button(screen, new_player_button_rect, red_button_color, red_border_color, "Нов играч", font)
        draw_simple_button(screen, back_player_button_rect, gray_button_color, gray_border_color, "Назад", font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    start_level2()