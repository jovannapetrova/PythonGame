import pygame
import random
import sys

# Иницијализација
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Препознавање бои и форми")
clock = pygame.time.Clock()

# Слики и звуци
bg_image = pygame.image.load("../pictures/cloudsbackground.png")
confetti_image = pygame.image.load("../pictures/confetti.png")
try_again_image = pygame.image.load("../pictures/sad_face.png")
correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")

# Фонтови
font_big = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 30)

# Бои
colors = {
    "црвен": (255, 0, 0),
    "син": (0, 0, 255),
    "зелен": (0, 255, 0),
    "жолт": (255, 255, 0)
}
shapes = ["круг", "квадрат", "триаголник", "правоаголник"]

# Играч и поени
players = {}
current_player = "Играч1"
score = 0

# Нивоа
levels = ["лесно", "средно", "тешко"]
current_level = "лесно"

# Режими
showing_results = False
selected_objects = []

# Предизвик
def new_challenge():
    global challenge_text, target_objects
    selected_objects.clear()
    if current_level == "лесно":
        color = random.choice(list(colors.keys()))
        shape = random.choice(shapes)
        challenge_text = f"Избери го {color}иот {shape}"
        target_objects = [(color, shape, 1)]
    elif current_level == "средно":
        count = random.randint(2, 3)
        color = random.choice(list(colors.keys()))
        shape = random.choice(shapes)
        challenge_text = f"Избери {count} {color}и {shape}и"
        target_objects = [(color, shape, count)]
    else:
        count1 = random.randint(2, 3)
        count2 = random.randint(2, 3)
        color1 = random.choice(list(colors.keys()))
        shape1 = random.choice(shapes)
        color2 = random.choice(list(colors.keys()))
        shape2 = random.choice(shapes)
        while color1 == color2 and shape1 == shape2:
            color2 = random.choice(list(colors.keys()))
            shape2 = random.choice(shapes)
        challenge_text = f"Избери {count1} {color1}и {shape1}и и {count2} {color2}и {shape2}и"
        target_objects = [(color1, shape1, count1), (color2, shape2, count2)]

# Објекти
objects = []
def generate_objects():
    global objects
    objects = []
    width, height = screen.get_size()
    for color, shape, count in target_objects:
        for _ in range(count):
            x = random.randint(100, width - 100)
            y = random.randint(150, height - 150)
            objects.append((color, shape, pygame.Rect(x, y, 60, 60)))

    while len(objects) < 8:
        color = random.choice(list(colors.keys()))
        shape = random.choice(shapes)
        if not any((color == t[0] and shape == t[1]) for t in target_objects):
            x = random.randint(100, width - 100)
            y = random.randint(150, height - 150)
            objects.append((color, shape, pygame.Rect(x, y, 60, 60)))

def draw_object(color_name, shape, rect, selected=False):
    color = colors[color_name]
    if selected:
        pygame.draw.rect(screen, (0, 0, 0), rect.inflate(10, 10), 3)
    if shape == "круг":
        pygame.draw.circle(screen, color, rect.center, 30)
    elif shape == "квадрат":
        pygame.draw.rect(screen, color, rect)
    elif shape == "правоаголник":
        pygame.draw.rect(screen, color, pygame.Rect(rect.x, rect.y, 80, 40))
    elif shape == "триаголник":
        points = [
            (rect.centerx, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom)
        ]
        pygame.draw.polygon(screen, color, points)

def show_feedback(correct):
    if correct:
        screen.blit(pygame.transform.scale(confetti_image, screen.get_size()), (0, 0))
        correct_sound.play()
    else:
        screen.blit(pygame.transform.scale(try_again_image, screen.get_size()), (0, 0))
        wrong_sound.play()
    pygame.display.flip()
    pygame.time.delay(2000)

def draw_challenge():
    width, height = screen.get_size()
    text_prefix = "Избери "
    y_start = 20
    spacing = 10  # растојание меѓу елементите

    if current_level == "лесно":
        color, shape, count = target_objects[0]
        count_text = ""
        prefix_surf = font_big.render(text_prefix + count_text, True, (0, 0, 0))
        shape_rect = pygame.Rect(0, 0, 60, 60)

        total_width = prefix_surf.get_width() + spacing + shape_rect.width
        x_start = (width - total_width) // 2

        screen.blit(prefix_surf, (x_start, y_start))
        shape_rect.topleft = (x_start + prefix_surf.get_width() + spacing, y_start + 5)
        draw_object(color, shape, shape_rect)

    elif current_level == "средно":
        color, shape, count = target_objects[0]
        count_text = f"{count} "
        prefix_surf = font_big.render(text_prefix + count_text, True, (0, 0, 0))
        shape_rect = pygame.Rect(0, 0, 60, 60)

        total_width = prefix_surf.get_width() + spacing + shape_rect.width
        x_start = (width - total_width) // 2

        screen.blit(prefix_surf, (x_start, y_start))
        shape_rect.topleft = (x_start + prefix_surf.get_width() + spacing, y_start + 5)
        draw_object(color, shape, shape_rect)

    else:
        # Тешко ниво
        prefix_surf = font_big.render(text_prefix, True, (0, 0, 0))
        parts = []
        for color, shape, count in target_objects:
            count_surf = font_big.render(str(count), True, (0, 0, 0))
            shape_rect = pygame.Rect(0, 0, 60, 60)
            parts.append((count_surf, color, shape, shape_rect))

        total_width = prefix_surf.get_width() + spacing
        for count_surf, _, _, shape_rect in parts:
            total_width += count_surf.get_width() + spacing + shape_rect.width + spacing

        x_start = (width - total_width) // 2
        offset_x = x_start

        screen.blit(prefix_surf, (offset_x, y_start))
        offset_x += prefix_surf.get_width() + spacing

        for count_surf, color, shape, shape_rect in parts:
            screen.blit(count_surf, (offset_x, y_start))
            offset_x += count_surf.get_width() + spacing
            shape_rect.topleft = (offset_x, y_start + 5)
            draw_object(color, shape, shape_rect)
            offset_x += shape_rect.width + spacing


new_challenge()
generate_objects()

# Главна јамка
running = True
while running:
    width, height = screen.get_size()
    screen.blit(pygame.transform.scale(bg_image, (width, height)), (0, 0))

    if showing_results:
        y = 100
        title = font_big.render("Резултати", True, (0, 0, 0))
        screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        for name, points in players.items():
            result_text = font_small.render(f"{name}: {points} поени", True, (0, 0, 0))
            screen.blit(result_text, (100, y))
            y += 40
        back_text = font_small.render("Кликни било каде за назад", True, (50, 50, 50))
        screen.blit(back_text, (100, height - 80))
    else:
        draw_challenge()
        score_text = font_small.render(f"{current_player} | Поени: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        results_btn = pygame.Rect(10, height - 40, 120, 30)
        new_player_btn = pygame.Rect(140, height - 40, 120, 30)
        pygame.draw.rect(screen, (200, 200, 200), results_btn)
        pygame.draw.rect(screen, (200, 200, 200), new_player_btn)
        screen.blit(font_small.render("Резултати", True, (0, 0, 0)), (20, height - 35))
        screen.blit(font_small.render("Нов играч", True, (0, 0, 0)), (150, height - 35))

        # Копчиња за нивоа (хоризонтално)
        level_buttons = []
        btn_width, btn_height = 130, 30
        spacing = 10
        total_width = (btn_width + spacing) * len(levels) - spacing
        start_x = width - total_width - 10
        for i, level in enumerate(levels):
            btn_rect = pygame.Rect(start_x + i * (btn_width + spacing), height - 40, btn_width, btn_height)
            level_buttons.append((btn_rect, level))
            color = (150, 150, 150) if current_level == level else (200, 200, 200)
            pygame.draw.rect(screen, color, btn_rect)
            screen.blit(font_small.render(level.capitalize(), True, (0, 0, 0)), (btn_rect.x + 10, btn_rect.y + 5))

        # Цртање на објектите
        for color, shape, rect in objects:
            selected = (color, shape, rect) in selected_objects
            draw_object(color, shape, rect, selected)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if showing_results:
                showing_results = False
            else:
                if results_btn.collidepoint(pos):
                    showing_results = True
                elif new_player_btn.collidepoint(pos):
                    current_player = f"Играч{len(players)+1}"
                    score = 0
                    players[current_player] = score
                    new_challenge()
                    generate_objects()
                    selected_objects.clear()
                else:
                    # Клик на копчиња за нивоа
                    for btn_rect, level in level_buttons:
                        if btn_rect.collidepoint(pos):
                            current_level = level
                            new_challenge()
                            generate_objects()
                            selected_objects.clear()
                            break
                    else:
                        # Клик на објекти
                        for obj in objects:
                            if obj[2].collidepoint(pos) and obj not in selected_objects:
                                selected_objects.append(obj)
                                break

                        # Проверка дали е точен избор
                        if current_level in ["лесно", "средно"]:
                            needed = target_objects[0][2]
                            selected_correct = [obj for obj in selected_objects if (obj[0], obj[1]) == (target_objects[0][0], target_objects[0][1])]
                            if len(selected_correct) == needed:
                                score += 1
                                players[current_player] = score
                                show_feedback(True)
                                new_challenge()
                                generate_objects()
                                selected_objects.clear()
                            elif len(selected_objects) >= needed:
                                show_feedback(False)
                                selected_objects.clear()
                        else:
                            # Тешко ниво - проверка за два типа објекти
                            needed1 = target_objects[0][2]
                            needed2 = target_objects[1][2]
                            selected_correct1 = [obj for obj in selected_objects if (obj[0], obj[1]) == (target_objects[0][0], target_objects[0][1])]
                            selected_correct2 = [obj for obj in selected_objects if (obj[0], obj[1]) == (target_objects[1][0], target_objects[1][1])]
                            total_needed = needed1 + needed2
                            if len(selected_correct1) == needed1 and len(selected_correct2) == needed2:
                                if len(selected_objects) == total_needed:
                                    score += 1
                                    players[current_player] = score
                                    show_feedback(True)
                                    new_challenge()
                                    generate_objects()
                                    selected_objects.clear()
                            elif len(selected_objects) >= total_needed:
                                show_feedback(False)
                                selected_objects.clear()

    pygame.display.flip()
    clock.tick(30)