import pygame
import sys
import random


def start_spatial_game():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Просторен однос: Лева и десна рака - Три нивоа")

    # Colors
    TEXT_COLOR = (45, 52, 54)
    SUCCESS_COLOR = (39, 174, 96)
    ERROR_COLOR = (231, 76, 60)
    PRIMARY_COLOR = (52, 152, 219)
    HIGHLIGHT_COLOR = (241, 196, 15)
    BG_COLOR = (236, 240, 241)

    # Fonts
    title_font = pygame.font.SysFont("Arial", 32, bold=True)
    feedback_font = pygame.font.SysFont("Arial", 28, bold=True)
    level_font = pygame.font.SysFont("Arial", 24, bold=True)
    button_font = pygame.font.SysFont("Arial", 20, bold=True)

    # Load sounds
    try:
        correct_sound = pygame.mixer.Sound("sounds/correct.wav")
        wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
    except:
        correct_sound = None
        wrong_sound = None

    # Load images
    def load_image(path, size=None):
        try:
            image = pygame.image.load(path)
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except:
            # Create placeholder surface
            surf = pygame.Surface(size if size else (100, 100))
            surf.fill((200, 200, 200))
            return surf

    # Load game images
    bg_img = load_image("../Pictures-Game2/background.jpg", (WIDTH, HEIGHT))
    bg_img2 = load_image("../Pictures-Game2/room-image.jpg", (WIDTH, HEIGHT))
    monkey_img = load_image("../Pictures-Game2/monkey-no background.png", (150, 150))
    banana_img = load_image("../Pictures-Game2/banana.png", (80, 80))

    # Location game images
    table_img = load_image("../Pictures-Game2/table.png", (120, 120))
    chair_img = load_image("../Pictures-Game2/chair.png", (120, 120))
    bed_img = load_image("../Pictures-Game2/bed.png", (120, 120))
    tv_img = load_image("../Pictures-Game2/tv.png", (120, 120))
    toy_car_img = load_image("../Pictures-Game2/box.png", (80, 80))
    toy_ball_img = load_image("../Pictures-Game2/ball.png", (80, 80))
    toy_doll_img = load_image("../Pictures-Game2/cup.png", (80, 80))
    toy_book_img = load_image("../Pictures-Game2/book.png", (80, 80))

    # Game state variables
    current_screen = "level_selection"  # level_selection, game, location_game, completion
    current_level = None
    current_step = 0
    total_steps = 0
    instructions = []
    completed_levels = []

    # Game objects
    monkeys = []
    hand_zones = []
    banana = None
    dragging_banana = False
    banana_offset = (0, 0)

    # Location game objects
    objects = []
    locations = []
    drop_zones = []
    draggable_object = None
    dragging_object = False
    object_offset = (0, 0)

    # Feedback
    feedback_text = ""
    feedback_color = TEXT_COLOR
    feedback_timer = 0

    def draw_button(surface, rect, color, border_color, text, font, text_color=(0, 0, 0)):
        pygame.draw.rect(surface, border_color, rect, border_radius=10)
        pygame.draw.rect(surface, color, rect.inflate(-4, -4), border_radius=8)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
        return rect

    def draw_text_with_shadow(surface, text, font, color, shadow_color, pos, center=True):
        shadow_surf = font.render(text, True, shadow_color)
        text_surf = font.render(text, True, color)

        if center:
            shadow_rect = shadow_surf.get_rect(center=(pos[0] + 2, pos[1] + 2))
            text_rect = text_surf.get_rect(center=pos)
        else:
            shadow_rect = (pos[0] + 2, pos[1] + 2)
            text_rect = pos

        surface.blit(shadow_surf, shadow_rect)
        surface.blit(text_surf, text_rect)

    def show_feedback(text, color, duration=2000):
        nonlocal feedback_text, feedback_color, feedback_timer
        feedback_text = text
        feedback_color = color
        feedback_timer = pygame.time.get_ticks() + duration

    def setup_easy_level():
        nonlocal current_level, current_step, total_steps, instructions, monkeys, hand_zones, banana
        current_level = "easy"
        current_step = 0
        total_steps = 2
        instructions = [
            "Земи ја бананата и стави ја во ЛЕВАТА рака на мајмунот",
            "Сега стави ја бананата во ДЕСНАТА рака на мајмунот"
        ]

        # Setup monkey and hand zones
        monkey_x = WIDTH // 2
        monkey_y = HEIGHT // 2
        monkeys = [{"pos": (monkey_x, monkey_y), "rect": pygame.Rect(monkey_x - 75, monkey_y - 75, 150, 150)}]

        # Hand zones (left and right relative to monkey's perspective)
        hand_zones = [
            {"side": "left", "rect": pygame.Rect(monkey_x - 150, monkey_y - 40, 80, 80), "occupied": False},
            {"side": "right", "rect": pygame.Rect(monkey_x + 70, monkey_y - 40, 80, 80), "occupied": False}
        ]

        # Setup banana
        banana = {"pos": [WIDTH // 2, HEIGHT - 150], "rect": pygame.Rect(WIDTH // 2 - 40, HEIGHT - 150 - 40, 80, 80)}

    def setup_medium_level():
        nonlocal current_level, current_step, total_steps, instructions, monkeys, hand_zones, banana
        current_level = "medium"
        current_step = 0
        total_steps = 4
        instructions = [
            "Стави ја бананата во ЛЕВАТА рака на првиот мајмун",
            "Стави ја бананата во ДЕСНАТА рака на вториот мајмун",
            "Стави ја бананата во ЛЕВАТА рака на вториот мајмун",
            "Стави ја бананата во ДЕСНАТА рака на првиот мајмун"
        ]

        # Setup two monkeys
        monkey1_x = WIDTH // 3
        monkey2_x = 2 * WIDTH // 3
        monkey_y = HEIGHT // 2

        monkeys = [
            {"pos": (monkey1_x, monkey_y), "rect": pygame.Rect(monkey1_x - 75, monkey_y - 75, 150, 150)},
            {"pos": (monkey2_x, monkey_y), "rect": pygame.Rect(monkey2_x - 75, monkey_y - 75, 150, 150)}
        ]

        # Hand zones for both monkeys
        hand_zones = [
            {"side": "left", "monkey": 0, "rect": pygame.Rect(monkey1_x - 150, monkey_y - 40, 80, 80),
             "occupied": False},
            {"side": "right", "monkey": 0, "rect": pygame.Rect(monkey1_x + 70, monkey_y - 40, 80, 80),
             "occupied": False},
            {"side": "left", "monkey": 1, "rect": pygame.Rect(monkey2_x - 150, monkey_y - 40, 80, 80),
             "occupied": False},
            {"side": "right", "monkey": 1, "rect": pygame.Rect(monkey2_x + 70, monkey_y - 40, 80, 80),
             "occupied": False}
        ]

        banana = {"pos": [WIDTH // 2, HEIGHT - 150], "rect": pygame.Rect(WIDTH // 2 - 40, HEIGHT - 150 - 40, 80, 80)}

    def setup_location_game():
        nonlocal current_level, current_step, total_steps, instructions, objects, locations, drop_zones
        current_level = "location"
        current_step = 0
        total_steps = 4
        instructions = [
            "Стави го автомобилчето ЛЕВО од масата",
            "Стави ја топката ДЕСНО од столот",
            "Стави ја куклата ЛЕВО од креветот",
            "Стави ја книгата ДЕСНО од телевизорот"
        ]

        # Setup locations (furniture)
        locations = [
            {"name": "table", "pos": (WIDTH // 4, HEIGHT // 2), "image": table_img},
            {"name": "chair", "pos": (3 * WIDTH // 4, HEIGHT // 2), "image": chair_img},
            {"name": "bed", "pos": (WIDTH // 4, 3 * HEIGHT // 4), "image": bed_img},
            {"name": "tv", "pos": (3 * WIDTH // 4, 3 * HEIGHT // 4), "image": tv_img}
        ]

        # Setup objects (toys)
        objects = [
            {"name": "car", "pos": [WIDTH // 2 - 100, HEIGHT // 4], "image": toy_car_img, "placed": False},
            {"name": "ball", "pos": [WIDTH // 2 - 30, HEIGHT // 4], "image": toy_ball_img, "placed": False},
            {"name": "doll", "pos": [WIDTH // 2 + 40, HEIGHT // 4], "image": toy_doll_img, "placed": False},
            {"name": "book", "pos": [WIDTH // 2 + 110, HEIGHT // 4], "image": toy_book_img, "placed": False}
        ]

        # Setup drop zones
        drop_zones = []
        for i, location in enumerate(locations):
            left_zone = pygame.Rect(location["pos"][0] - 150, location["pos"][1] - 40, 80, 80)
            right_zone = pygame.Rect(location["pos"][0] + 70, location["pos"][1] - 40, 80, 80)

            drop_zones.append({
                "location": location["name"],
                "side": "left",
                "rect": left_zone,
                "occupied": False
            })
            drop_zones.append({
                "location": location["name"],
                "side": "right",
                "rect": right_zone,
                "occupied": False
            })

    def check_banana_placement():
        nonlocal current_step
        if not banana:
            return

        banana_rect = pygame.Rect(banana["pos"][0] - 40, banana["pos"][1] - 40, 80, 80)

        # Get current instruction requirements
        if current_level == "easy":
            required_side = "left" if current_step == 0 else "right"
            for zone in hand_zones:
                if zone["side"] == required_side and banana_rect.colliderect(zone["rect"]):
                    if correct_sound:
                        correct_sound.play()
                    show_feedback("Одлично! Точно!", SUCCESS_COLOR)
                    zone["occupied"] = True
                    current_step += 1
                    if current_step >= total_steps:
                        completed_levels.append("easy")
                        return "completed"
                    return "correct"

        elif current_level == "medium":
            step_requirements = [
                {"monkey": 0, "side": "left"},  # Step 0
                {"monkey": 1, "side": "right"},  # Step 1
                {"monkey": 1, "side": "left"},  # Step 2
                {"monkey": 0, "side": "right"}  # Step 3
            ]

            if current_step < len(step_requirements):
                req = step_requirements[current_step]
                for zone in hand_zones:
                    if (zone.get("monkey") == req["monkey"] and
                            zone["side"] == req["side"] and
                            banana_rect.colliderect(zone["rect"])):
                        if correct_sound:
                            correct_sound.play()
                        show_feedback("Одлично! Точно!", SUCCESS_COLOR)
                        zone["occupied"] = True
                        current_step += 1
                        if current_step >= total_steps:
                            completed_levels.append("medium")
                            return "completed"
                        return "correct"

        return "none"

    def check_object_placement():
        nonlocal current_step
        if not draggable_object:
            return

        object_rect = pygame.Rect(draggable_object["pos"][0] - 40, draggable_object["pos"][1] - 40, 80, 80)

        # Define step requirements
        step_requirements = [
            {"object": "car", "location": "table", "side": "left"},
            {"object": "ball", "location": "chair", "side": "right"},
            {"object": "doll", "location": "bed", "side": "left"},
            {"object": "book", "location": "tv", "side": "right"}
        ]

        if current_step < len(step_requirements):
            req = step_requirements[current_step]
            for zone in drop_zones:
                if (zone["location"] == req["location"] and
                        zone["side"] == req["side"] and
                        object_rect.colliderect(zone["rect"]) and
                        draggable_object["name"] == req["object"]):
                    if correct_sound:
                        correct_sound.play()
                    show_feedback("Одлично! Точно!", SUCCESS_COLOR)
                    zone["occupied"] = True
                    draggable_object["placed"] = True
                    current_step += 1
                    if current_step >= total_steps:
                        completed_levels.append("location")
                        return "completed"
                    return "correct"

        return "none"

    # Main game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if current_screen == "level_selection":
                    # Level selection buttons
                    easy_btn_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 120, 400, 60)
                    medium_btn_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 40, 400, 60)
                    location_btn_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 40, 400, 60)
                    back_btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50)

                    if easy_btn_rect.collidepoint(pos):
                        setup_easy_level()
                        current_screen = "game"
                    elif medium_btn_rect.collidepoint(pos):
                        setup_medium_level()
                        current_screen = "game"
                    elif location_btn_rect.collidepoint(pos):
                        setup_location_game()
                        current_screen = "location_game"
                    elif back_btn_rect.collidepoint(pos):
                        from main.cpc import main  # Импорт на главната функција
                        main()  # Return to main menu

                elif current_screen == "game":
                    # Check banana dragging
                    if banana and pygame.Rect(banana["pos"][0] - 40, banana["pos"][1] - 40, 80, 80).collidepoint(pos):
                        dragging_banana = True
                        banana_offset = (pos[0] - banana["pos"][0], pos[1] - banana["pos"][1])

                    # Back button
                    back_btn_rect = pygame.Rect(50, HEIGHT - 100, 150, 50)
                    if back_btn_rect.collidepoint(pos):
                        current_screen = "level_selection"

                elif current_screen == "location_game":
                    # Check object dragging
                    for obj in objects:
                        if not obj["placed"]:
                            obj_rect = pygame.Rect(obj["pos"][0] - 40, obj["pos"][1] - 40, 80, 80)
                            if obj_rect.collidepoint(pos):
                                draggable_object = obj
                                dragging_object = True
                                object_offset = (pos[0] - obj["pos"][0], pos[1] - obj["pos"][1])
                                break

                    # Back button
                    back_btn_rect = pygame.Rect(50, HEIGHT - 100, 150, 50)
                    if back_btn_rect.collidepoint(pos):
                        current_screen = "level_selection"

                elif current_screen == "completion":
                    # Continue button
                    continue_btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
                    if continue_btn_rect.collidepoint(pos):
                        current_screen = "level_selection"

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_banana:
                    result = check_banana_placement()
                    if result == "completed":
                        current_screen = "completion"
                    elif result != "correct":
                        if wrong_sound:
                            wrong_sound.play()
                        show_feedback("Обиди се повторно!", ERROR_COLOR)
                    dragging_banana = False

                if dragging_object:
                    result = check_object_placement()
                    if result == "completed":
                        current_screen = "completion"
                    elif result != "correct":
                        if wrong_sound:
                            wrong_sound.play()
                        show_feedback("Обиди се повторно!", ERROR_COLOR)
                    dragging_object = False
                    draggable_object = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_banana and banana:
                    banana["pos"][0] = event.pos[0] - banana_offset[0]
                    banana["pos"][1] = event.pos[1] - banana_offset[1]

                if dragging_object and draggable_object:
                    draggable_object["pos"][0] = event.pos[0] - object_offset[0]
                    draggable_object["pos"][1] = event.pos[1] - object_offset[1]

        # Clear screen
        screen.fill(BG_COLOR)

        # Draw current screen
        if current_screen == "level_selection":
            screen.blit(bg_img, (0, 0))

            # Title
            draw_text_with_shadow(screen, "Избери ниво на тежина",
                                  pygame.font.SysFont("Arial", 40, bold=True),
                                  (255, 255, 255), (0, 0, 0), (WIDTH // 2, 150))

            # Level buttons
            easy_color = SUCCESS_COLOR if "easy" not in completed_levels else (100, 100, 100)
            medium_color = HIGHLIGHT_COLOR if "medium" not in completed_levels else (100, 100, 100)
            location_color = PRIMARY_COLOR if "location" not in completed_levels else (100, 100, 100)

            easy_btn_rect = draw_button(screen, pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 120, 400, 60),
                                        easy_color, (0, 0, 0), "ЛЕСНО (1 мајмун, 2 чекори)", level_font,
                                        (255, 255, 255))
            medium_btn_rect = draw_button(screen, pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 40, 400, 60),
                                          medium_color, (0, 0, 0), "СРЕДНО (2 мајмуни, 4 чекори)", level_font,
                                          (255, 255, 255))
            location_btn_rect = draw_button(screen, pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 40, 400, 60),
                                            location_color, (0, 0, 0), "ТЕШКО (Лоцирање предмети)", level_font,
                                            (255, 255, 255))

            draw_button(screen, pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50),
                        ERROR_COLOR, (0, 0, 0), "Назад", button_font, (255, 255, 255))

        elif current_screen == "game":
            screen.blit(bg_img, (0, 0))

            # Level indicator
            level_text = "ЛЕСНО НИВО (1/3)" if current_level == "easy" else "СРЕДНО НИВО (2/3)"
            draw_text_with_shadow(screen, level_text, level_font, (0, 0, 0), (255, 255, 255), (WIDTH // 2, 80))

            # Instruction
            if current_step < len(instructions):
                draw_text_with_shadow(screen, instructions[current_step], title_font,
                                      (255, 255, 255), (0, 0, 0), (WIDTH // 2, 150))

            # Draw monkeys
            for monkey in monkeys:
                screen.blit(monkey_img, (monkey["pos"][0] - 75, monkey["pos"][1] - 75))

            # Draw hand zones (for debugging)
            for zone in hand_zones:
                color = (0, 255, 0) if zone["occupied"] else (255, 0, 0)
                pygame.draw.rect(screen, color, zone["rect"], 2)

            # Draw banana
            if banana:
                screen.blit(banana_img, (banana["pos"][0] - 40, banana["pos"][1] - 40))

            # Back button
            draw_button(screen, pygame.Rect(50, HEIGHT - 100, 150, 50),
                        (200, 200, 200), (0, 0, 0), "Назад", button_font)

        elif current_screen == "location_game":
            screen.blit(bg_img2, (0, 0))

            # Level indicator
            draw_text_with_shadow(screen, "ТЕШКО НИВО (3/3)", level_font, (0, 0, 0), (255, 255, 255), (WIDTH // 2, 80))

            # Instruction
            if current_step < len(instructions):
                draw_text_with_shadow(screen, instructions[current_step], title_font,
                                      (255, 255, 255), (0, 0, 0), (WIDTH // 2, 150))

            # Draw locations
            for location in locations:
                screen.blit(location["image"], (location["pos"][0] - 60, location["pos"][1] - 60))

            # Draw drop zones (for debugging)
            for zone in drop_zones:
                color = (0, 255, 0) if zone["occupied"] else (255, 0, 0)
                pygame.draw.rect(screen, color, zone["rect"], 2)

            # Draw objects
            for obj in objects:
                if not obj["placed"]:
                    screen.blit(obj["image"], (obj["pos"][0] - 40, obj["pos"][1] - 40))

            # Back button
            draw_button(screen, pygame.Rect(50, HEIGHT - 100, 150, 50),
                        (200, 200, 200), (0, 0, 0), "Назад", button_font)

        elif current_screen == "completion":
            screen.blit(bg_img, (0, 0))

            draw_text_with_shadow(screen, "Честитки! Го завршивте нивото!",
                                  title_font, (255, 255, 255), (0, 0, 0), (WIDTH // 2, HEIGHT // 2 - 50))

            draw_button(screen, pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50),
                        SUCCESS_COLOR, (0, 0, 0), "Продолжи", button_font, (255, 255, 255))

        # Draw feedback
        if feedback_text and current_time < feedback_timer:
            draw_text_with_shadow(screen, feedback_text, feedback_font,
                                  feedback_color, (0, 0, 0), (WIDTH // 2, HEIGHT - 200))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    start_spatial_game()