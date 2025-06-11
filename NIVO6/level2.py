import pygame
import sys
import os

pygame.init()

# Цел екран
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Сортирање предмети (Drag and Drop)")
results_button_rect = pygame.Rect(0, 0, 160, 55)
new_player_button_rect = pygame.Rect(0, 0, 160, 55)
pygame.init()
pygame.mixer.init()

wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")
correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
# Функција за вчитување слики со обработка на грешки
def load_image(name, scale=None):
    try:
        image = pygame.image.load(name)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except Exception as e:
        print(f"Грешка при вчитување на сликата {name}: {e}")
        # Создај празна површина како fallback
        return pygame.Surface((100, 100), pygame.SRCALPHA)


# Вчитување на сите слики
try:
    background = load_image("../pictures/landscape.png", (WIDTH, HEIGHT))
    panda_img = load_image("../pictures/panda.png", (100, 100))
    blue_basket_img = load_image("../pictures/bluebucket.png", (250, 250))
    red_basket_img = load_image("../pictures/redbucket.png", (250,250))
    panda_body_img = load_image("../pictures/sittingpanda.png", (200, 200))
except Exception as e:
    print(f"Грешка при вчитување на сликите: {e}")
    pygame.quit()
    sys.exit()

font = pygame.font.SysFont("Arial", 40)
title_font = pygame.font.SysFont("Arial", 50, bold=True)
bravo_font = pygame.font.SysFont("Arial", 80, bold=True)
small_font=pygame.font.SysFont("Arial", 30, bold=True)
players = []
current_player_index = -1  # нема активен играч на почеток
scores = {}
current_player = ""
show_bravo = False
bravo_timer = 0


def add_new_player():
    global current_player_index, current_player
    new_player_name = f"Играч {len(players) + 1}"
    players.append(new_player_name)
    scores[new_player_name] = 0
    current_player_index = len(players) - 1
    current_player = new_player_name


# Кутиите ќе ги подредиме хоризонтално, низ долната третина од екранот
box_width, box_height = 150, 150
box_spacing = 100
boxes = {}
start_x = (WIDTH - (len(tasks := [
    {"color": (0, 100, 255), "shape": "circle", "box": "blue",
     "description": "Стави ги сите сини кругови во сината кошница."},
    {"color": (255, 50, 50), "shape": "triangle", "box": "red",
     "description": "Стави ги сите црвени триаголници во црвената кошница."},
{"color": (0, 100, 255), "shape": "triangle", "box": "blue",
     "description": "Стави ги сите сини триаголници во сината кошница."},
    {"color": (255, 50, 50), "shape": "square", "box": "red",
     "description": "Стави ги сите црвени квадрати во црвената кошница."},


]) * box_width + (len(tasks) - 1) * box_spacing)) // 2 -270
for i, task in enumerate(tasks):
    boxes[task["box"]] = pygame.Rect(
        start_x + i * (box_width + box_spacing),
        int(HEIGHT * 0.5),  # долу
        box_width,
        box_height
    )

add_new_player()


import random

def reset_items_for_task():
    global items, scored_items, show_bravo, bravo_timer
    task = tasks[current_task_index]
    items = []
    scored_items = set()
    num_correct = 3  # број на точни предмети
    num_wrong = 2    # број на погрешни предмети
    spacing = 150

    # Правиме листа со предмети - прво точни
    correct_items = [{
        "color": task["color"],
        "shape": task["shape"],
        "radius": 30,
        "dragging": False,
        "scored": False,
        "locked": False
    } for _ in range(num_correct)]

    # Потоа предмети со спротивна боја и/или форма
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
        "locked": False
    } for _ in range(num_wrong)]

    # Сите предмети заедно
    items = correct_items + wrong_items

    # Измешај ги предметите
    random.shuffle(items)

    # Постави ги на хоризонтална линија, распоредени и измешани
    total_width = len(items) * spacing
    start_x_items = (WIDTH - total_width) // 2 + spacing // 2
    item_y_position = int(HEIGHT * 0.4)

    for i, item in enumerate(items):
        item["pos"] = [start_x_items + i * spacing, item_y_position]

    show_bravo = False
    bravo_timer = 0


current_task_index = 0
reset_items_for_task()

dragging_item = None
offset_x = 0
offset_y = 0


def draw_triangle(surface, color, pos, size):
    x, y = pos
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    pygame.draw.polygon(surface, color, points)
def draw_shadowed_circle(surface, color, pos, radius):
    # Креирај површина со alpha канал
    shadow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)

    # Црна боја со alpha 100 (од 0 до 255)
    shadow_color = (0, 0, 0, 100)

    # Центар на сенката на површината
    shadow_center = (radius * 2 + 3, radius * 2 + 3)  # +3 за поместување

    pygame.draw.circle(shadow_surf, shadow_color, shadow_center, radius)

    # Блитнувај ја сенката на главниот екран, позицијата ја намали за да биде правилно поставено
    surface.blit(shadow_surf, (pos[0] - radius * 2, pos[1] - radius * 2))

    # Цртај кругот врз сенката
    pygame.draw.circle(surface, color, pos, radius)


def draw_rounded_rect(surface, color, rect, radius=20):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_simple_button(surface, rect, color, border_color, text, font, text_color=(0, 0, 0)):
    # Надворешен светол раб
    pygame.draw.rect(surface, border_color, rect, border_radius=15, width=3)
    # Внатрешност
    pygame.draw.rect(surface, color, rect.inflate(-6, -6), border_radius=12)
    # Текст
    text_surf = font.render(text, True, text_color)
    surface.blit(text_surf, (rect.centerx - text_surf.get_width() // 2,
                             rect.centery - text_surf.get_height() // 2))

# Updated player panel and bravo panel positions with more spacing
def draw_player_panel():
    # Move panel down (increased y position from 20 to 50)
    player_rect = pygame.Rect(120, 50, 300, 80)  # Changed y from 20 to 50
    draw_rounded_rect(screen, (0, 50, 120), player_rect, 40)

    # Adjust panda image position to match
    screen.blit(panda_img, (player_rect.left - 70, player_rect.centery - 50))

    player_text = title_font.render(current_player, True, (255, 255, 255))
    screen.blit(player_text, (player_rect.x + 50, player_rect.centery - player_text.get_height() // 2))

def draw_bravo_panel():
    if all(item["scored"] or item["locked"] for item in items if item.get("correct", False)):
        bravo_text = bravo_font.render("", True, (0, 30, 100))
        # Постави текстот на некоја фиксна позиција (на пример, 450, 80)
        screen.blit(bravo_text, (450, 50))


def draw_instruction_panel():
    panel_width = WIDTH // 2
    instr_rect = pygame.Rect((WIDTH - panel_width) // 2, 140, panel_width, 80)
    draw_rounded_rect(screen, (150, 200, 255), instr_rect, 20)

    current_task = tasks[current_task_index]
    words = current_task["description"].split()
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

    # Ограничување по висина (опционално)
    max_lines = (instr_rect.height - 40) // 30
    if len(wrapped_text) > max_lines:
        wrapped_text = wrapped_text[:max_lines]
        wrapped_text[-1] += "..."

    # Прикажи текст внатре во правоаголникот
    for i, line in enumerate(wrapped_text):
        line_surface = small_font.render(line, True, (0, 50, 150))
        screen.blit(line_surface, (
            instr_rect.centerx - line_surface.get_width() // 2,
            instr_rect.y + 20 + i * 30
        ))



def draw_3d_button(surface, rect, base_color, highlight_color, text, font):
    # Сенка
    shadow_offset = 4
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
    pygame.draw.rect(surface, (40, 40, 40), shadow_rect, border_radius=12)

    # Основно копче
    pygame.draw.rect(surface, base_color, rect, border_radius=12)

    # Highlight ефект
    highlight_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height // 2)
    pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=12)

    # Темни рабови долу и десно
    pygame.draw.line(surface, (0, 0, 0), (rect.left + 5, rect.bottom - 5), (rect.right - 5, rect.bottom - 5), 3)
    pygame.draw.line(surface, (0, 0, 0), (rect.right - 5, rect.top + 5), (rect.right - 5, rect.bottom - 5), 3)

    # Текст
    text_surf = font.render(text, True, (0, 0, 0))
    surface.blit(text_surf, (rect.centerx - text_surf.get_width() // 2,
                             rect.centery - text_surf.get_height() // 2))


def draw_results_screen():
    # Светло кафеава позадина
    screen.fill((210, 180, 140))  # light brown

    # Дефинирај прозорец во средината
    panel_width = WIDTH * 0.5
    panel_height = HEIGHT * 0.6
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    # Цртај темно кафеаво правоаголно поле со заоблени агли
    pygame.draw.rect(screen, (139, 69, 19), panel_rect, border_radius=20)

    # Текстот ќе се појави во внатрешноста
    title = title_font.render("Резултати по играч:", True, (255, 255, 255))
    screen.blit(title, (panel_x + (panel_width - title.get_width()) // 2, panel_y + 20))

    # Прикажи секој резултат
    y_offset = panel_y + 100
    for player, score in scores.items():
        text = font.render(f"{player}: {score} поени", True, (255, 255, 255))
        screen.blit(text, (panel_x + (panel_width - text.get_width()) // 2, y_offset))
        y_offset += 40

    # Копче "Назад"
    back_button_width = 140
    back_button_height = 50
    back_button_rect = pygame.Rect(
        panel_x + (panel_width - back_button_width) // 2,
        panel_y + panel_height - back_button_height - 20,
        back_button_width,
        back_button_height
    )

    # Цртање заоблен правоаголник (без бордер)
    pygame.draw.rect(screen, (255, 165, 0), back_button_rect, border_radius=15)

    # Текстот на копчето
    text_surf = font.render("Назад", True, (0, 0, 0))  # црн текст
    screen.blit(text_surf, (
        back_button_rect.centerx - text_surf.get_width() // 2,
        back_button_rect.centery - text_surf.get_height() // 2
    ))

    pygame.display.flip()

    # Чекај клик на "Назад"
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

    # Ако е круг - дозволуваме маргина за да не бараме целосен внатре
    if item["shape"] == "circle":
        return (x + r - margin) >= box_rect.left and (x - r + margin) <= box_rect.right and \
            (y + r - margin) >= box_rect.top and (y - r + margin) <= box_rect.bottom

    # За квадрат и триаголник - приближно bounding box
    size = r
    if item["shape"] in ["square", "triangle"]:
        left = x - size
        right = x + size
        top = y - size
        bottom = y + size
        return (right - margin) >= box_rect.left and (left + margin) <= box_rect.right and \
            (bottom - margin) >= box_rect.top and (top + margin) <= box_rect.bottom

    # Default fallback
    return box_rect.collidepoint(x, y)


def draw_shadowed_triangle(surface, color, pos, size):
    shadow_surf = pygame.Surface((size * 6, size * 6), pygame.SRCALPHA)
    shadow_color = (0, 0, 0, 100)
    offset = 3

    # Функција за точки (повеќе ги поместуваме за да не излезат од површината)
    x, y = size * 3, size * 3  # Центар на површината
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]

    # Сенка (поместена)
    shadow_points = [(px + offset, py + offset) for px, py in points]
    pygame.draw.polygon(shadow_surf, shadow_color, shadow_points)

    # Триаголник
    pygame.draw.polygon(shadow_surf, color, points)

    # Блитнувај ја површината на главниот екран со позиција прилагодена
    surface.blit(shadow_surf, (pos[0] - size * 3, pos[1] - size * 3))
def draw_square(surface, color, pos, size):
    x, y = pos
    rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
    pygame.draw.rect(surface, color, rect)

# При цртање предмети
for item in items:
    pos = item["pos"]
    color = item["color"]
    if item["shape"] == "circle":
        draw_shadowed_circle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
    elif item["shape"] == "triangle":
        draw_shadowed_triangle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
    elif item["shape"] == "square":
        draw_square(screen, color, (int(pos[0]), int(pos[1])), item["radius"])



def check_and_score_items():
    global scores, current_player_index, current_player, current_task_index, items, show_bravo, bravo_timer
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
                    scores[current_player] += 5  # Повеќе поени за успех
                    item["scored"] = True
                    item["locked"] = True
                    correct_sound.play()  # ✅ Пушти "correct" звук
                    show_bravo = True
                    bravo_timer = pygame.time.get_ticks()
                continue  # Не го додаваме во новата листа → исчезнува
            else:
                # ⛔ Точен предмет, но не е во кутијата – не правиме ништо
                new_items.append(item)
        else:
            # Погрешен предмет
            if is_item_in_box(item, box_rect) and not item["locked"]:
                wrong_sound.play()  # ⛔ Пушти "wrong" звук
                item["locked"] = True
                all_correct = False
            new_items.append(item)

    items = new_items

    if num_correct_in_box == num_correct_items and num_correct_items > 0:
        # Сите точни предмети се ставени во кутијата
        # Сменете задача (следна)
        current_task_index += 1
        if current_task_index >= len(tasks):
            current_task_index = 0
        reset_items_for_task()


# Дефинирање на копчињата
button_rect = pygame.Rect(WIDTH // 2 - 320, HEIGHT - 80, 200, 60)
new_player_button_rect = pygame.Rect(WIDTH // 2 + 120, HEIGHT - 80, 200, 60)


def main():
    global dragging_item, offset_x, offset_y, current_player_index, current_player, show_bravo, bravo_timer

    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        if show_bravo and current_time - bravo_timer > 2000:  # 2 секунди
            show_bravo = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Проверка дали е кликнато копчето за резултати
                if button_rect.collidepoint(pos):
                    draw_results_screen()
                elif new_player_button_rect.collidepoint(pos):
                    add_new_player()
                else:
                    for item in items:
                        x, y = item["pos"]
                        radius = item["radius"]
                        dx = pos[0] - x
                        dy = pos[1] - y
                        # Поголема област за полесно селектирање (1.5x радиус)
                        if abs(dx) <= radius * 1.5 and abs(dy) <= radius * 1.5:
                            dragging_item = item
                            offset_x = dx
                            offset_y = dy
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_item:
                    # Кога ќе пуштиме предметот проверуваме дали е во кутија
                    check_and_score_items()
                dragging_item = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging_item:
                    mx, my = event.pos
                    dragging_item["pos"][0] = mx - offset_x
                    dragging_item["pos"][1] = my - offset_y

        # Цртање
        screen.blit(background, (0, 0))

        # Слика од панда долу лево
        screen.blit(panda_body_img, (50, HEIGHT - panda_body_img.get_height() - 50))

        # Панели
        draw_player_panel()
        draw_bravo_panel()
        draw_instruction_panel()

        # Предметите
        for item in items:
            pos = item["pos"]
            color = item["color"]
            if item["shape"] == "circle":
                draw_shadowed_circle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
            elif item["shape"] == "triangle":
                draw_shadowed_triangle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
            elif item["shape"] == "square":
                draw_square(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
        # Кошниците (користејќи слики)
        for key, rect in boxes.items():
            if key == "blue":
                screen.blit(blue_basket_img, rect)
            else:
                screen.blit(red_basket_img, rect)

        # Копчиња
        # Големина на копчиња
        button_width = 160
        button_height = 55

        # Копче "Резултати" под сината кошничка
        results_button_rect = pygame.Rect(
            boxes["blue"].centerx - button_width // 2,
            boxes["blue"].bottom + 200,
            button_width,
            button_height
        )
       # results_button_rect.x += 50

        # Копче "Нов играч" под црвената кошничка
        new_player_button_rect = pygame.Rect(
            boxes["red"].centerx - button_width // 2+50,
            boxes["red"].bottom + 200,
            button_width,
            button_height
        )


        # Бои
        blue_button_color = (173, 216, 230)
        blue_border_color = (224, 255, 255)

        red_button_color = (255, 182, 193)
        red_border_color = (255, 228, 225)

        # Цртање
        draw_simple_button(screen, results_button_rect, blue_button_color, blue_border_color, "Резултати", font)
        draw_simple_button(screen, new_player_button_rect, red_button_color, red_border_color, "Нов играч", font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()