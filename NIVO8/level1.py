import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Цртање модел")
clock = pygame.time.Clock()

# Бои
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 140, 0)

font = pygame.font.SysFont("Arial", 28)
button_font = pygame.font.SysFont("Arial", 20)

player_name = "Играч 1"
players_scores = []  # ќе чува речници со име и завршено ниво
player_counter = 1  # Глобален бројач за играчи
last_pos = None     # За чување на претходната позиција при цртање

# Вчитување слики
model_images = {
    "лесно": pygame.image.load("../pictures/house.png"),
    "средно": pygame.image.load("../pictures/flower.png"),
    "тешко": pygame.image.load("../pictures/car.png")
}

# Променливи
drawing = False
canvas = pygame.Surface((600, 400))  # Помала висина
canvas.fill(WHITE)
current_level = "лесно"

# Копчиња
buttons = {
    "new_player": pygame.Rect(10, 520, 140, 50),
    "show_scores": pygame.Rect(170, 520, 160, 50),
    "finish": pygame.Rect(800, 520, 180, 50),
    "лесно": pygame.Rect(550, 520, 80, 50),
    "средно": pygame.Rect(640, 520, 80, 50),
    "тешко": pygame.Rect(730, 520, 80, 50),
}

def draw_text(text, x, y, color=BLACK, font_obj=font):
    label = font_obj.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(text, rect, active=True):
    color = LIGHT_GREEN if active else GRAY
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = button_font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def reset_canvas():
    global canvas
    canvas.fill(WHITE)

def finish_drawing():
    global player_name, current_level, players_scores
    # Додади ниво како завршено
    players_scores.append({
        "name": player_name,
        "level": current_level
    })
    reset_canvas()


def main_loop():
    global drawing, player_name, players_scores, current_level, last_pos, player_counter

    running = True
    while running:
        screen.fill(LIGHT_BLUE)

        # Прикажи модел слика
        model_img = pygame.transform.scale(model_images[current_level], (300, 250))
        img_x, img_y = 680, 30
        screen.blit(model_img, (img_x, img_y))

        # Информација за ниво (под сликата, центрирана)
        level_text = f"Ниво: {current_level.title()}"
        level_label = font.render(level_text, True, ORANGE)
        level_rect = level_label.get_rect()
        level_rect.center = (img_x + 300 // 2, img_y + 250 + 20)  # 20 пиксели под сликата
        screen.blit(level_label, level_rect)

        # Инфо за играчот
        draw_text(f"Играч: {player_name}", 10, 10)

        # Цртање
        screen.blit(canvas, (50, 100))  # поместено надолу

        # Копчиња (сите заедно)
        draw_button("Нов играч", buttons["new_player"])
        draw_button("Прикажи резултати", buttons["show_scores"])
        draw_button("Заврши цртање", buttons["finish"])
        draw_button("Лесно", buttons["лесно"])
        draw_button("Средно", buttons["средно"])
        draw_button("Тешко", buttons["тешко"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if buttons["new_player"].collidepoint(mx, my):
                    player_counter += 1
                    player_name = f"Играч {player_counter}"
                    reset_canvas()

                elif buttons["show_scores"].collidepoint(mx, my):
                    # [код за резултати, не го менувам]

                    screen.fill((230, 230, 250))  # Светло виолетова позадина

                    draw_text("Завршени нивоа по играчи:", 100, 50, BLACK)
                    y_offset = 100

                    finished_levels_by_player = {}
                    for entry in players_scores:
                        name = entry["name"]
                        level = entry["level"]
                        if name not in finished_levels_by_player:
                            finished_levels_by_player[name] = set()
                        finished_levels_by_player[name].add(level)

                    for player, finished_levels in finished_levels_by_player.items():
                        levels_str = ", ".join(sorted([lvl.title() for lvl in finished_levels]))
                        draw_text(f"{player}: завршил {levels_str} ниво", 100, y_offset)
                        y_offset += 40

                    if not finished_levels_by_player:
                        draw_text("Нема внесени завршени нивоа.", 100, y_offset)
                        y_offset += 40

                    draw_text("Притисни било каде за враќање.", 100, screen.get_height() - 40, RED)

                    pygame.display.flip()
                    waiting = True
                    while waiting:
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif ev.type == pygame.MOUSEBUTTONDOWN:
                                waiting = False

                elif buttons["finish"].collidepoint(mx, my):
                    finish_drawing()

                elif buttons["лесно"].collidepoint(mx, my):
                    current_level = "лесно"
                    reset_canvas()

                elif buttons["средно"].collidepoint(mx, my):
                    current_level = "средно"
                    reset_canvas()

                elif buttons["тешко"].collidepoint(mx, my):
                    current_level = "тешко"
                    reset_canvas()

                elif 50 <= mx <= 650 and 100 <= my <= 500:
                    drawing = True
                    last_pos = (mx - 50, my - 100)

            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None

            elif event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                if 50 <= mx <= 650 and 100 <= my <= 500 and last_pos is not None:
                    rel_x = mx - 50
                    rel_y = my - 100
                    pygame.draw.line(canvas, BLACK, last_pos, (rel_x, rel_y), 2)
                    last_pos = (rel_x, rel_y)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_loop()
    pygame.quit()
    sys.exit()
