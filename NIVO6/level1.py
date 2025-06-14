import pygame
import random
import sys
from NIVO6.level2 import start_level2

def start_colorsAndshapes_game():
    # Иницијализација
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Препознавање бои и форми")
    clock = pygame.time.Clock()

    # Слики и звуци
    try:
        background_image = pygame.image.load("../Pictures-Game6/landscape.png")
        background_image = pygame.transform.scale(background_image, screen.get_size())
    except:
        background_image = None

    try:
        panda_image = pygame.image.load("../Pictures-Game6/panda.png")
        panda_image = pygame.transform.scale(panda_image, (80, 80))
    except:
        panda_image = None
    try:
        panda_image1 = pygame.image.load("../Pictures-Game6/sittingpanda.png")
        panda_image1 = pygame.transform.scale(panda_image1, (120, 120))
    except:
        panda_image1 = None
    try:
        star_image = pygame.image.load("../Pictures-Game6/star.png")
        star_image = pygame.transform.scale(star_image, (40, 40))
    except:
        star_image = None

    try:
        smiley_image = pygame.image.load("../Pictures-Game6/smile.png")
        smiley_image = pygame.transform.scale(smiley_image, (40, 40))
    except:
        smiley_image = None

    try:
        lion_image = pygame.image.load("../Pictures-Game6/lion.png")
        lion_image = pygame.transform.scale(lion_image, (40, 40))
    except:
        lion_image = None

    confetti_image = pygame.image.load("../Pictures-Game6/bravo.png")
    try_again_image = pygame.image.load("../Pictures-Game6/sad_face.png")
    correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
    wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")

    # Фонтови
    font_big = pygame.font.SysFont("Arial", 60, bold=True)
    font_medium = pygame.font.SysFont("Arial", 40)
    font_small = pygame.font.SysFont("Arial", 30)

    # Бои
    COLOR_BACKGROUND = (245, 235, 220)
    COLOR_PANEL = (230, 220, 205)
    COLOR_TEXT_DARK = (255, 255, 255)
    COLOR_TEXT_LIGHT = (255, 255, 255)
    COLOR_PLAYER_BOX = (200, 220, 240)  # Темна сина за играчот
    COLOR_TEXT_WHITE = (255, 255, 255)
    COLOR_SCORE_BOX = (200, 220, 240)  # Светла сина за поените
    COLOR_CHALLENGE_BOX = (220, 210, 190)  # Светла кафеава за предизвикот
    COLOR_TRANSPARENT_BOX = (230, 220, 205, 150)  # Провидена кутичка

    # Бои за копчиња
    COLOR_BUTTON_BASE = (210, 200, 185)
    COLOR_BUTTON_HIGHLIGHT = (255, 255, 255)
    COLOR_BUTTON_SHADOW = (150, 130, 110)
    COLOR_BUTTON_ACTIVE = (180, 170, 155)
    COLOR_ORANGE_BUTTON = (255, 165, 0)
    COLOR_GREEN_BUTTON = (50, 205, 50)
    COLOR_YELLOW_BUTTON = (255, 215, 0)
    COLOR_RED_BUTTON = (255, 69, 0)

    # Бои на објектите
    colors = {
        "црвен": (255, 69, 0),
        "син": (30, 144, 255),
        "зелен": (50, 205, 50),
        "жолт": (255, 215, 0)
    }
    shapes = ["круг", "квадрат", "триаголник", "правоаголник"]

    # Играч и поени
    players = {"Играч 1": 0}
    current_player = "Играч 1"
    score = 0

    # Нивоа
    levels = ["лесно", "средно", "тешко"]
    current_level = "лесно"

    # Режими
    showing_results = False
    selected_objects = []

    def lighten_color(color, amount=0.3):
        # Функција која ја осветлува бојата (color е RGB tuple), amount е колку да ја осветлиме (0-1)
        r = min(int(color[0] + (255 - color[0]) * amount), 255)
        g = min(int(color[1] + (255 - color[1]) * amount), 255)
        b = min(int(color[2] + (255 - color[2]) * amount), 255)
        return (r, g, b)

    # --- Функции за цртање ---
    def draw_3d_box(surface, rect, base_color, highlight_color, shadow_color, border_radius=8):
        # Shadow
        pygame.draw.rect(surface, shadow_color, (rect.x + 3, rect.y + 3, rect.width, rect.height),
                         border_radius=border_radius)
        # Base
        pygame.draw.rect(surface, base_color, rect, border_radius=border_radius)
        # Highlight7
        # pygame.draw.line(surface, highlight_color, (rect.x, rect.y), (rect.x + rect.width, rect.y), 3)
        # pygame.draw.line(surface, highlight_color, (rect.x, rect.y), (rect.x, rect.y + rect.height), 3)

    def draw_button(surface, rect, text, font, base_color, highlight_color, shadow_color, is_active=False, icon=None):
        # Основно копче со border_radius
        border_radius = 20

        # Цртање само едноставен полукруг
        pygame.draw.rect(surface, base_color, rect, border_radius=border_radius)

        # Светла нијанса како тенка рамка (не создава ефект на второ копче)
        border_color = lighten_color(base_color, 0.4)
        pygame.draw.rect(surface, border_color, rect, width=3, border_radius=border_radius)

        # Ако е активен, додај мала проѕирност врз копчето
        if is_active:
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((*COLOR_BUTTON_ACTIVE[:3], 80))  # мала проѕирност
            surface.blit(s, rect.topleft)

        # Текст и икона
        text_surf = font.render(text, True, COLOR_TEXT_DARK)
        text_rect = text_surf.get_rect(center=rect.center)

        if icon:
            text_rect.y += 15
            icon_rect = icon.get_rect(centerx=rect.centerx, top=rect.top + 5)
            surface.blit(icon, icon_rect)

        surface.blit(text_surf, text_rect)

    def draw_player_info():
        width, height = screen.get_size()

        # Player box (left) - помал и поинаку позициониран
        player_box = pygame.Rect(260, 20, 250, 70)  # Помала ширина
        pygame.draw.rect(screen, COLOR_PLAYER_BOX, player_box, border_radius=12)

        if panda_image:
            panda_rect = panda_image.get_rect(left=player_box.left - 30, centery=player_box.centery)
            screen.blit(panda_image, panda_rect)

        player_text = font_small.render(f"{current_player}", True, (0, 0, 0))
        screen.blit(player_text, (player_box.left + 50, player_box.centery - player_text.get_height() // 2))

        # Score box (right) - помал
        score_box = pygame.Rect(width - 500, 20, 250, 70)
        pygame.draw.rect(screen, COLOR_SCORE_BOX, score_box, border_radius=12)

        if star_image:
            star_rect = star_image.get_rect(centerx=score_box.left + 40, centery=score_box.centery)
            screen.blit(star_image, star_rect)

        score_text = font_small.render(f"Поени: {players[current_player]}", True, (0, 0, 0))
        screen.blit(score_text, (score_box.left + 70, score_box.centery - score_text.get_height() // 2))

    def draw_challenge_box():
        width, height = screen.get_size()

        # Уште помала ширина (на пр. 70% од оригиналната)
        box_width = int((width - 200) * 0.7)  # Или фиксна вредност како 600
        x_pos = (width - box_width) // 2  # Автоматско центрирање

        challenge_box = pygame.Rect(x_pos, 120, box_width, 80)  # Намалена и висина

        s = pygame.Surface((challenge_box.width, challenge_box.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*COLOR_TRANSPARENT_BOX[:3], 180), (0, 0, challenge_box.width, challenge_box.height),
                         border_radius=12)  # Помали заоблени агли
        pygame.draw.rect(s, COLOR_BUTTON_HIGHLIGHT, (0, 0, challenge_box.width, challenge_box.height), 2,
                         border_radius=12)
        screen.blit(s, challenge_box)

        # Текстот останува ист
        # font_medium.set_bold(True)
        text_surf = font_medium.render(challenge_text, True, COLOR_TEXT_DARK)
        screen.blit(text_surf, (challenge_box.centerx - text_surf.get_width() // 2,
                                challenge_box.centery - text_surf.get_height() // 2))

        # Draw example shape above the challenge text
        example_box = pygame.Rect(challenge_box.centerx - 240, challenge_box.top - 100, 500, 70)

        s_example = pygame.Surface((example_box.width, example_box.height), pygame.SRCALPHA)
        pygame.draw.rect(s_example, (*COLOR_TRANSPARENT_BOX[:3], 180), (0, 0, example_box.width, example_box.height),
                         border_radius=8)
        pygame.draw.rect(s_example, COLOR_BUTTON_HIGHLIGHT, (0, 0, example_box.width, example_box.height), 2,
                         border_radius=8)
        screen.blit(s_example, example_box)

        # Draw the target shape in the example box
        if target_objects:
            color_name, shape_name, _ = target_objects[0]  # Take the first target
            example_rect = pygame.Rect(example_box.centerx - 25, example_box.centery - 25, 50, 50)
            draw_object(color_name, shape_name, example_rect)

    def draw_objects_area():
        width, height = screen.get_size()

        # Иста ширина како challenge_box за усогласеност
        box_width = int((width - 200) * 0.7)
        x_pos = (width - box_width) // 2

        # Намалена висина за објектите
        objects_area = pygame.Rect(x_pos, 220, box_width, height - 450)  # Помалку високо

        s = pygame.Surface((objects_area.width, objects_area.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*COLOR_TRANSPARENT_BOX[:3], 150), (0, 0, objects_area.width, objects_area.height),
                         border_radius=12)
        pygame.draw.rect(s, COLOR_BUTTON_HIGHLIGHT, (0, 0, objects_area.width, objects_area.height), 2,
                         border_radius=12)
        screen.blit(s, objects_area)

        # Панда декорациите се прилагодени
        if panda_image1:
            panda_scaled = pygame.transform.scale(panda_image1, (120, 120))  # Помали панди
            left_panda = pygame.transform.flip(panda_scaled, True, False)
            screen.blit(left_panda, (objects_area.left - 195, objects_area.centery - 180))
            screen.blit(panda_scaled, (objects_area.right + 95, objects_area.centery - 180))

        return objects_area  # Return the area so we can use it for object placement

    def draw_bottom_buttons():
        width, height = screen.get_size()
        btn_y = height - 150
        offset = 60
        # Results button
        results_btn = pygame.Rect(width // 2 - 400 - offset, btn_y, 180, 90)
        draw_button(screen, results_btn, "Резултати", font_small,
                    COLOR_BUTTON_BASE, COLOR_BUTTON_HIGHLIGHT, COLOR_BUTTON_SHADOW)

        # New Player button
        new_player_btn = pygame.Rect(width // 2 - 200 - offset, btn_y, 180, 90)
        draw_button(screen, new_player_btn, "Нов Играч", font_small,
                    COLOR_ORANGE_BUTTON, COLOR_BUTTON_HIGHLIGHT, (200, 120, 0))

        # Level buttons
        level_btns = []
        btn_width = 150
        spacing = 20
        start_x = width // 2 + 20 - offset

        # Easy button
        easy_btn = pygame.Rect(start_x, btn_y, btn_width, 90)
        draw_button(screen, easy_btn, "Лесно", font_small,
                    COLOR_GREEN_BUTTON, COLOR_BUTTON_HIGHLIGHT, (0, 100, 0),
                    current_level == "лесно", star_image)

        # Medium button
        medium_btn = pygame.Rect(start_x + btn_width + spacing, btn_y, btn_width, 90)
        draw_button(screen, medium_btn, "Средно", font_small,
                    COLOR_YELLOW_BUTTON, COLOR_BUTTON_HIGHLIGHT, (180, 150, 0),
                    current_level == "средно", smiley_image)

        # Hard button
        hard_btn = pygame.Rect(start_x + 2 * (btn_width + spacing), btn_y, btn_width, 90)
        draw_button(screen, hard_btn, "Тешко", font_small,
                    COLOR_RED_BUTTON, COLOR_BUTTON_HIGHLIGHT, (150, 0, 0),
                    current_level == "тешко", lion_image)
        # Next button (нова копче веднаш десно од Hard, мала маргина 10 пкс)
        next_btn_x = hard_btn.right + 150  # 10 пиксели од десната страна на hard_btn
        next_btn_width = 150
        next_btn = pygame.Rect(next_btn_x, btn_y, next_btn_width, 90)
        draw_button(screen, next_btn, "Следно", font_small,
                    (100, 100, 255), COLOR_BUTTON_HIGHLIGHT, (0, 0, 150))
        back_btn_x = results_btn.right - 470
        back_btn_width = 150
        back_btn = pygame.Rect(back_btn_x, btn_y, back_btn_width, 90)
        draw_button(screen, back_btn, "Назад", font_small,
                    (100, 100, 255), COLOR_BUTTON_HIGHLIGHT, (0, 0, 150))
        return {
            "results": results_btn,
            "new_player": new_player_btn,
            "easy": easy_btn,
            "medium": medium_btn,
            "hard": hard_btn,
            "next": next_btn,
            "back":back_btn,

        }

    def bojaformalevel2():

        start_level2()
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
            challenge_text = f"Избери {count} {color} {shape}"
            target_objects = [(color, shape, count)]
        else:
            count1 = random.randint(1, 2)
            count2 = random.randint(1, 2)
            color1 = random.choice(list(colors.keys()))
            shape1 = random.choice(shapes)
            color2 = random.choice(list(colors.keys()))
            shape2 = random.choice(shapes)
            while (color1 == color2 and shape1 == shape2) or (color1 == color2) or (shape1 == shape2):
                color2 = random.choice(list(colors.keys()))
                shape2 = random.choice(shapes)
            challenge_text = f"Избери {count1} {color1} {shape1} и {count2} {color2} {shape2}"
            target_objects = [(color1, shape1, count1), (color2, shape2, count2)]

    # Објекти
    objects = []

    def generate_objects():
        global objects
        objects = []
        width, height = screen.get_size()

        # Get the objects area rectangle
        objects_area = pygame.Rect((width - int((width - 200) * 0.7)) // 2, 220,
                                   int((width - 200) * 0.7), height - 450)

        # Calculate safe area (smaller than objects_area to keep shapes fully visible)
        safe_area = objects_area.inflate(-80, -80)

        # Target objects
        for color, shape, count in target_objects:
            for _ in range(count):
                # Generate position within safe area
                x = random.randint(safe_area.left, safe_area.right - 60)
                y = random.randint(safe_area.top, safe_area.bottom - 60)
                objects.append((color, shape, pygame.Rect(x, y, 60, 60)))

        # Additional random objects
        num_to_add = 10 - len(objects)
        for _ in range(num_to_add):
            color = random.choice(list(colors.keys()))
            shape = random.choice(shapes)
            x = random.randint(safe_area.left, safe_area.right - 60)
            y = random.randint(safe_area.top, safe_area.bottom - 60)
            objects.append((color, shape, pygame.Rect(x, y, 60, 60)))

        random.shuffle(objects)

    def draw_object(color_name, shape, rect, selected=False):
        color = colors[color_name]
        if selected:
            pygame.draw.rect(screen, COLOR_TEXT_DARK, rect.inflate(10, 10), 4, border_radius=8)

        if shape == "круг":
            pygame.draw.circle(screen, color, rect.center, 30)
        elif shape == "квадрат":
            pygame.draw.rect(screen, color, rect, border_radius=8)
        elif shape == "правоаголник":
            # Adjust rectangle dimensions to fit better
            rect_adjusted = pygame.Rect(rect.x, rect.y + 10, 80, 40)
            pygame.draw.rect(screen, color, rect_adjusted, border_radius=8)
        elif shape == "триаголник":
            points = [
                (rect.centerx, rect.top + 5),
                (rect.left + 5, rect.bottom - 5),
                (rect.right - 5, rect.bottom - 5)
            ]
            pygame.draw.polygon(screen, color, points)

    def show_feedback(correct):
        screen_width, screen_height = screen.get_size()

        if correct:
            # Прикажи конфети позадина
            scaled_confetti = pygame.transform.scale(confetti_image, (screen_width, screen_height))
            screen.blit(scaled_confetti, (0, 0))

            # Прикажи текст "БРАВО"
            bravo_text = font_big.render("БРАВО!", True, (0, 100, 0))  # зелена боја
            screen.blit(bravo_text, (
                screen_width // 2 - bravo_text.get_width() // 2,
                screen_height // 2 - bravo_text.get_height() // 2
            ))

            correct_sound.play()
        else:
            scaled_try_again = pygame.transform.scale(try_again_image, (screen_width, screen_height))
            screen.blit(scaled_try_again, (0, 0))

            try_again_text = font_big.render("ОБИДИ СЕ ПОВТОРНО!", True, (200, 0, 0))  # црвена боја

            # Центрирано по x, поставено најгоре по y (пример: y = 60)
            screen.blit(try_again_text, (
                screen_width // 2 - try_again_text.get_width() // 2,
                60
            ))

            wrong_sound.play()

        pygame.display.flip()
        pygame.time.delay(2000)

    # Иницијализација на првиот предизвик
    new_challenge()
    generate_objects()

    # Главна јамка
    running = True
    while running:
        width, height = screen.get_size()

        # Draw background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(COLOR_BACKGROUND)

        if showing_results:
            # Results screen
            title_surf = font_big.render("Резултати", True, COLOR_TEXT_DARK)
            screen.blit(title_surf, (width // 2 - title_surf.get_width() // 2, 80))

            y_offset = 200
            for name, points in players.items():
                result_text_surf = font_medium.render(f"{name}: {points} поени", True, COLOR_TEXT_DARK)
                screen.blit(result_text_surf, (width // 2 - result_text_surf.get_width() // 2, y_offset))
                y_offset += 60

            back_btn_rect = pygame.Rect(width // 2 - 180, height - 120, 360, 70)
            draw_button(screen, back_btn_rect, "Кликни за назад", font_medium,
                        COLOR_BUTTON_BASE, COLOR_BUTTON_HIGHLIGHT, COLOR_BUTTON_SHADOW)
        else:
            # Draw all game elements
            draw_player_info()
            draw_challenge_box()
            objects_area = draw_objects_area()  # Get the objects area rectangle
            buttons = draw_bottom_buttons()

            # Draw game objects
            for color, shape, rect in objects:
                is_selected = (color, shape, rect) in selected_objects
                draw_object(color, shape, rect, is_selected)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if showing_results:
                    if back_btn_rect.collidepoint(pos):
                        showing_results = False
                else:
                    # Check level buttons
                    if buttons["easy"].collidepoint(pos):
                        current_level = "лесно"
                        new_challenge()
                        generate_objects()
                    elif buttons["medium"].collidepoint(pos):
                        current_level = "средно"
                        new_challenge()
                        generate_objects()
                    elif buttons["hard"].collidepoint(pos):
                        current_level = "тешко"
                        new_challenge()
                        generate_objects()
                    # Check other buttons
                    elif buttons["results"].collidepoint(pos):
                        showing_results = True
                    elif buttons["new_player"].collidepoint(pos):
                        # global current_player, players
                        new_index = len(players) + 1
                        new_player_name = f"Играч {new_index}"
                        players[new_player_name] = 0  # Додај го новиот играч со поени 0
                        current_player = new_player_name  # Префрли се на новиот играч
                    elif buttons["next"].collidepoint(pos):
                        # Овде повикај ја функцијата која треба да ја стартува следната игра / ниво
                        bojaformalevel2()
                    elif buttons["back"].collidepoint(pos):
                        # Овде повикај ја функцијата која треба да ја стартува следната игра / ниво
                        from main.cpc import main
                        main()
                    else:
                        # Check object selection (only within objects area)
                        if objects_area.collidepoint(pos):
                            for color, shape, rect in objects:
                                if rect.collidepoint(pos):
                                    if (color, shape, rect) in selected_objects:
                                        selected_objects.remove((color, shape, rect))
                                    else:
                                        selected_objects.append((color, shape, rect))

                            # Check if selection matches target
                            if len(selected_objects) == sum(count for _, _, count in target_objects):
                                correct = True
                                selected_colors_shapes = [(color, shape) for color, shape, _ in selected_objects]

                                for color, shape, count in target_objects:
                                    if selected_colors_shapes.count((color, shape)) != count:
                                        correct = False
                                        break

                                if correct:
                                    players[current_player] += 1

                                    show_feedback(True)
                                    new_challenge()
                                    generate_objects()
                                else:
                                    show_feedback(False)
                                    selected_objects.clear()

        pygame.display.flip()
        clock.tick(30)

