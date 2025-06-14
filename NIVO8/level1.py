import pygame
import sys
from NIVO8.level2 import start_coloring_level
from NIVO8.level3 import level3

def start_drawing_game():
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
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
    players_scores = []
    player_counter = 1
    last_pos = None
    drawing = False

    model_images = {
        "лесно": pygame.image.load("../Pictures-Game8/house.png"),
        "средно": pygame.image.load("../Pictures-Game8/flower.png"),
        "тешко": pygame.image.load("../Pictures-Game8/car.png")
    }

    # Центриран canvas со поголема големина
    canvas_width, canvas_height = 1200, 900
    canvas = pygame.Surface((canvas_width, canvas_height))
    canvas.fill(WHITE)
    canvas_x = (WIDTH - canvas_width) // 2 -100
    canvas_y = 80  # малку погоре за повеќе простор

    current_level = "лесно"

    buttons = {
        "new_player": pygame.Rect(20, HEIGHT - 70, 140, 50),
        "show_scores": pygame.Rect(180, HEIGHT - 70, 200, 50),
        "finish": pygame.Rect(WIDTH - 200, HEIGHT - 70, 180, 50),
        "лесно": pygame.Rect(WIDTH - 470, HEIGHT - 70, 80, 50),
        "средно": pygame.Rect(WIDTH - 380, HEIGHT - 70, 80, 50),
        "тешко": pygame.Rect(WIDTH - 290, HEIGHT - 70, 80, 50),
        "go_to_level2": pygame.Rect(390, HEIGHT - 70, 220, 50),
        "go_to_level3": pygame.Rect(620, HEIGHT - 70, 220, 50),
        "back": pygame.Rect(920, HEIGHT - 70, 220, 50),


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
        nonlocal canvas
        canvas.fill(WHITE)

    def finish_drawing():
        nonlocal player_name, current_level, players_scores
        players_scores.append({
            "name": player_name,
            "level": current_level
        })
        reset_canvas()

    running = True
    while running:
        screen.fill(LIGHT_BLUE)

        # Прикажи модел слика
        model_img = pygame.transform.scale(model_images[current_level], (300, 250))
        img_x, img_y = WIDTH - 330, 30
        screen.blit(model_img, (img_x, img_y))

        # Информација за ниво
        level_text = f"Ниво: {current_level.title()}"
        level_label = font.render(level_text, True, ORANGE)
        level_rect = level_label.get_rect()
        level_rect.center = (img_x + 150, img_y + 270)
        screen.blit(level_label, level_rect)

        draw_text(f"Играч: {player_name}", 20, 20)

        # Цртање
        screen.blit(canvas, (canvas_x, canvas_y))

        # Копчиња
        for key, rect in buttons.items():
            draw_button(key.capitalize() if key in ["лесно", "средно", "тешко"] else {
                "new_player": "Нов играч",
                "show_scores": "Прикажи резултати",
                "finish": "Заврши цртање",
                "go_to_level2":"Следен левел 2",
                "go_to_level3": "Следен левел 3",
                "back": "Назад",
            }[key], rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if buttons["new_player"].collidepoint(mx, my):
                    player_counter += 1
                    player_name = f"Играч {player_counter}"
                    reset_canvas()




                elif buttons["go_to_level2"].collidepoint(mx, my):

                    running = False
                    start_coloring_level()


                elif buttons["go_to_level3"].collidepoint(mx, my):

                    running = False
                    level3(screen)

                elif buttons["back"].collidepoint(mx, my):

                    running = False
                    from main.cpc import main
                    main()




                elif buttons["show_scores"].collidepoint(mx, my):
                    screen.fill((230, 230, 250))
                    draw_text("Завршени нивоа по играчи:", 100, 50, BLACK)
                    y_offset = 100

                    finished_levels_by_player = {}
                    for entry in players_scores:
                        name = entry["name"]
                        level = entry["level"]
                        finished_levels_by_player.setdefault(name, set()).add(level)

                    for player, finished_levels in finished_levels_by_player.items():
                        levels_str = ", ".join(sorted([lvl.title() for lvl in finished_levels]))
                        draw_text(f"{player}: завршил {levels_str} ниво", 100, y_offset)
                        y_offset += 40

                    if not finished_levels_by_player:
                        draw_text("Нема внесени завршени нивоа.", 100, y_offset)

                    draw_text("Притисни било каде за враќање.", 100, HEIGHT - 40, RED)
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

                elif canvas_x <= mx <= canvas_x + canvas_width and canvas_y <= my <= canvas_y + canvas_height:
                    drawing = True
                    last_pos = (mx - canvas_x, my - canvas_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None

            elif event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                if canvas_x <= mx <= canvas_x + canvas_width and canvas_y <= my <= canvas_y + canvas_height:
                    rel_x = mx - canvas_x
                    rel_y = my - canvas_y
                    pygame.draw.line(canvas, BLACK, last_pos, (rel_x, rel_y), 2)
                    last_pos = (rel_x, rel_y)

        pygame.display.flip()
        clock.tick(30)

