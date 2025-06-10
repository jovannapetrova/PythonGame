import pygame
import sys

pygame.init()

# Цел екран
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Сортирање предмети (Drag and Drop)")

try:
    background = pygame.image.load("../pictures/brownclouds.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Грешка при вчитување на сликата: {e}")
    pygame.quit()
    sys.exit()

font = pygame.font.SysFont(None, 40)
title_font = pygame.font.SysFont(None, 60, bold=False)

players = []
current_player_index = -1  # нема активен играч на почеток
scores = {}
current_player = ""

def add_new_player():
    global current_player_index, current_player
    new_player_name = f"Играч {len(players) + 1}"
    players.append(new_player_name)
    scores[new_player_name] = 0
    current_player_index = len(players) - 1
    current_player = new_player_name

button_rect = pygame.Rect(10, HEIGHT - 50, 120, 40)
new_player_button_rect = pygame.Rect(button_rect.right + 20, HEIGHT - 50, 150, 40)

# Кутиите ќе ги подредиме хоризонтално, низ долната третина од екранот
box_width, box_height = 150, 150
box_spacing = 100
boxes = {}
start_x = (WIDTH - (len(tasks := [
    {"color": (0, 0, 255), "shape": "circle", "box": "blue", "description": "Стави ги сите сини кругови во сината кутија."},
    {"color": (255, 0, 0), "shape": "triangle", "box": "red", "description": "Стави ги сите црвени триаголници во црвената кутија."},
]) * box_width + (len(tasks) - 1) * box_spacing)) // 2
for i, task in enumerate(tasks):
    boxes[task["box"]] = pygame.Rect(
        start_x + i * (box_width + box_spacing),
        int(HEIGHT * 0.7),  # долу
        box_width,
        box_height
    )
add_new_player()
# Предмети ќе ги подредиме хоризонтално на горната половина
def reset_items_for_task():
    global items, scored_items
    task = tasks[current_task_index]
    items = []
    scored_items = set()  # За да не се бодуваат повеќе пати истите предмети
    num_correct = 3
    spacing = 150
    total_width = (num_correct + 2) * spacing  # 3 correct + 2 challenge
    start_x_items = (WIDTH - total_width) // 2 + spacing // 2

    # Правиме предмети со посакуваната боја и форма
    for i in range(num_correct):
        items.append({
            "color": task["color"],
            "pos": [start_x_items + i * spacing, int(HEIGHT * 0.3)],
            "radius": 30,
            "dragging": False,
            "shape": task["shape"],
            "scored": False,  # дали предметот веќе е бодуван
            "locked": False   # дали предметот е заклучен во кутијата
        })
    # Два предизвикувачки предмети
    other_color = (255, 0, 0) if task["color"] != (255, 0, 0) else (0, 0, 255)
    other_shape = "circle" if task["shape"] != "circle" else "triangle"
    for i in range(2):
        items.append({
            "color": other_color,
            "pos": [start_x_items + (num_correct + i) * spacing, int(HEIGHT * 0.3)],
            "radius": 30,
            "dragging": False,
            "shape": other_shape,
            "scored": False,
            "locked": False
        })

current_task_index = 0
reset_items_for_task()

dragging_item = None
offset_x = 0
offset_y = 0

def draw_triangle(surface, color, pos, size):
    x, y = pos
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    pygame.draw.polygon(surface, color, points)

def draw_3d_box(surface, rect, base_color):
    # Сенка (shadow)
    shadow_offset = 5
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
    pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=10)

    # Основна кутија
    pygame.draw.rect(surface, base_color, rect, border_radius=10)

    # Внатрешна сенка (темен раб од долу и десно)
    pygame.draw.line(surface, (0, 0, 0), rect.bottomleft, rect.bottomright, 3)
    pygame.draw.line(surface, (0, 0, 0), rect.topright, rect.bottomright, 3)

    # Светол раб (од горе и лево)
    light_color = tuple(min(255, c + 100) for c in base_color)
    pygame.draw.line(surface, light_color, rect.topleft, rect.topright, 3)
    pygame.draw.line(surface, light_color, rect.topleft, rect.bottomleft, 3)

def draw_3d_button(surface, rect, base_color, text, font):
    # Сенка
    shadow_offset = 4
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
    pygame.draw.rect(surface, (40, 40, 40), shadow_rect, border_radius=12)

    # Основно копче
    pygame.draw.rect(surface, base_color, rect, border_radius=12)

    # Темни рабови долу и десно
    pygame.draw.line(surface, (0, 0, 0), rect.bottomleft, rect.bottomright, 3)
    pygame.draw.line(surface, (0, 0, 0), rect.topright, rect.bottomright, 3)

    # Светли рабови горе и лево
    light_color = tuple(min(255, c + 80) for c in base_color)
    pygame.draw.line(surface, light_color, rect.topleft, rect.topright, 3)
    pygame.draw.line(surface, light_color, rect.topleft, rect.bottomleft, 3)

    # Текст
    text_surf = font.render(text, True, (0, 0, 0))
    surface.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                             rect.y + (rect.height - text_surf.get_height()) // 2))

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
    # 3D копче
    draw_3d_button(screen, back_button_rect, (150, 75, 0), "Назад", font)

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

def is_item_in_box(item, box_rect):
    x, y = item["pos"]
    # Проверуваме дали центарот на предметот е во границите на кутијата
    return box_rect.collidepoint(x, y)

def check_and_score_items():
    global scores, current_player_index, current_player, current_task_index, items
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
                    scores[current_player] += 1
                # Не го додаваме овој предмет во новата листа → ќе "исчезне"
                continue
            else:
                if item["scored"]:
                    scores[current_player] -= 1
                item["scored"] = False
        new_items.append(item)
    items = new_items

    if num_correct_in_box == num_correct_items and num_correct_items > 0:
        # Сите точни предмети се ставени во кутијата
        # Сменете задача (следна)
        current_task_index += 1
        if current_task_index >= len(tasks):
            current_task_index = 0
        reset_items_for_task()

def main():
    global dragging_item, offset_x, offset_y, current_player_index, current_player

    clock = pygame.time.Clock()
    running = True

    while running:
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

        # Текст горе, центриран
        current_task = tasks[current_task_index]
        title_text = current_task["description"]
        title_surf = title_font.render(title_text, True, (255, 255, 255))
        title_x = (WIDTH - title_surf.get_width()) // 2
        title_y = int(HEIGHT * 0.15)
        screen.blit(title_surf, (title_x, title_y))

        # Кутиите
        for key, rect in boxes.items():
            base_color = (0, 0, 255) if key == "blue" else (255, 0, 0)
            draw_3d_box(screen, rect, base_color)
            # Отстрани го прикажувањето на текстот над кутиите

        # Предметите
        for item in items:
            pos = item["pos"]
            color = item["color"]
            if item["shape"] == "circle":
                pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])
            elif item["shape"] == "triangle":
                draw_triangle(screen, color, (int(pos[0]), int(pos[1])), item["radius"])

        # Поени и играч
        score_text = font.render(f"Играч: {current_player}  |  Поени: {scores[current_player]}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Копчиња 3D
        draw_3d_button(screen, button_rect, (150, 75, 0), "Резултати", font)
        draw_3d_button(screen, new_player_button_rect, (150, 75, 0), "Нов играч", font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()