import pygame
import sys
import json



def level3(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    button_font = pygame.font.SysFont("Arial", 24, bold=True)


    screen_width, screen_height = screen.get_size()


    background = pygame.image.load("../Pictures-Game8/tabla.png").convert()
    background = pygame.transform.smoothscale(background, (screen_width, screen_height))

    coloring_image_tmp = pygame.image.load("../Pictures-Game8/house1.png")
    coloring_image = coloring_image_tmp.convert()

    final_image = pygame.image.load("../Pictures-Game8/finalhouse.png").convert_alpha()

    target_width = final_image.get_width() - 100
    target_height = final_image.get_height() - 250
    coloring_image = pygame.transform.smoothscale(coloring_image, (target_width, target_height))
    final_image = pygame.transform.smoothscale(final_image, (target_width, target_height))

    spacing = 50
    total_width = target_width * 2 + spacing
    start_x = (screen_width - total_width) // 2 + 50

    bg_x = start_x
    bg_y = (screen_height - target_height) // 2 + 130

    final_x = start_x + target_width + spacing
    final_y = bg_y

    bg_width, bg_height = target_width, target_height

    palette_colors = {
        1: (255, 0, 0),
        2: (255, 165, 0),
        3: (255, 255, 0),
        4: (0, 255, 0),
        5: (0, 0, 255),
        6: (128, 0, 128)
    }

    palette_radius = 30
    palette_spacing = 25
    num_colors = len(palette_colors)

    palette_start_x = (screen_width - (num_colors * (2 * palette_radius + palette_spacing) - palette_spacing)) // 2 - 100
    palette_y = 130

    palette_pos = {}
    for i, num in enumerate(sorted(palette_colors.keys())):
        palette_pos[num] = (palette_start_x + i * (2 * palette_radius + palette_spacing) + palette_radius, palette_y)

    selected_color = None
    selected_number = None

    with open("../NIVO8/areas.json", "r") as f:
        areas = json.load(f)

    for a in areas:
        a["color"] = None
        a["visited"] = False

    # Load decorative elements
    try:
        decor_left = pygame.image.load("decor_left.png").convert_alpha()
        decor_left = pygame.transform.scale(decor_left, (150, 150))
    except:
        decor_left = None

    try:
        decor_right = pygame.image.load("decor_right.png").convert_alpha()
        decor_right = pygame.transform.scale(decor_right, (150, 150))
    except:
        decor_right = None

    try:
        button_sound = pygame.mixer.Sound("button_hover.wav")
        button_click_sound = pygame.mixer.Sound("button_click.wav")
    except:
        button_sound = None
        button_click_sound = None

    def draw_areas():
        for a in areas:
            x, y, w, h = a["rect"]
            x += bg_x
            y += bg_y
            if a["color"]:
                s = pygame.Surface((w, h), pygame.SRCALPHA)
                s.fill((*a["color"], 150))
                screen.blit(s, (x, y))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h), 2)
            text = font.render(str(a["number"]), True, (0, 0, 0))
            tx = x + w // 2 - text.get_width() // 2
            ty = y + h // 2 - text.get_height() // 2
            screen.blit(text, (tx, ty))

    def draw_palette():
        for num, pos in palette_pos.items():
            color = palette_colors[num]
            pygame.draw.circle(screen, color, pos, palette_radius)
            pygame.draw.circle(screen, (0, 0, 0), pos, palette_radius, 3)
            text = font.render(str(num), True, (0, 0, 0))
            screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2))

        if selected_color:
            indicator_x = screen_width // 2
            indicator_y = palette_y + palette_radius * 2 + 20

            pygame.draw.circle(screen, selected_color, (indicator_x, indicator_y), 25)
            pygame.draw.circle(screen, (0, 0, 0), (indicator_x, indicator_y), 25, 3)

            text = font.render(f"Селектирана боја: {selected_number}", True, (255, 255, 255))
            screen.blit(text, (indicator_x - text.get_width() // 2, indicator_y + 40))

    def all_colored():
        return all(a["visited"] for a in areas)

    def show_congrats_screen():
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        try:
            confetti_img = pygame.image.load("../Pictures-Game8/confetti.png")
            confetti_bg = pygame.transform.scale(confetti_img, (screen_width, screen_height))
            screen.blit(confetti_bg, (0, 0))
        except:
            pass

        congrats_font = pygame.font.SysFont("Arial", 50, bold=True)
        text1 = congrats_font.render("БРАВО!", True, (255, 255, 0))
        text2 = font.render("Сè е обоено точно!", True, (255, 255, 255))
        text3 = font.render("Кликни на 'Следна слика' за да продолжиш.", True, (255, 255, 255))

        screen.blit(text1, ((screen_width - text1.get_width()) // 2, screen_height // 2 - 80))
        screen.blit(text2, ((screen_width - text2.get_width()) // 2, screen_height // 2 - 20))
        screen.blit(text3, ((screen_width - text3.get_width()) // 2, screen_height // 2 + 20))

    def draw_button(x, y, width, height, text, color, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = (x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height)

        current_color = hover_color if is_hovered else color

        pygame.draw.rect(screen, current_color, (x, y, width, height), border_radius=15)
        border_color = (255, 255, 255) if is_hovered else (200, 200, 200)
        pygame.draw.rect(screen, border_color, (x, y, width, height), 3, border_radius=15)

        text_surf = button_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surf, text_rect)

        shadow = pygame.Surface((width, 5), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 30))
        screen.blit(shadow, (x, y + height))

        return pygame.Rect(x, y, width, height), is_hovered

    running = True
    finished = False
    draw_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)

    prev_hovered_button = None

    while running:
        screen.blit(background, (0, 0))

        if decor_left:
            screen.blit(decor_left, (10, screen_height - 160))
        if decor_right:
            screen.blit(decor_right, (screen_width - 160, screen_height - 160))

        coloring_bg = pygame.Surface((bg_width + 20, bg_height + 20), pygame.SRCALPHA)
        coloring_bg.fill((255, 255, 255, 200))
        screen.blit(coloring_bg, (bg_x - 10, bg_y - 10))

        screen.blit(coloring_image, (bg_x, bg_y))
        screen.blit(draw_surface, (bg_x, bg_y))

        draw_areas()
        draw_palette()

        ref_bg = pygame.Surface((target_width + 20, target_height + 20), pygame.SRCALPHA)
        ref_bg.fill((255, 255, 255, 200))
        screen.blit(ref_bg, (final_x - 10, final_y - 10))
        screen.blit(final_image, (final_x, final_y))
        backmenu_btn, backmenu_hovered = draw_button(
            screen_width // 2 + 260,
            screen_height // 2 - 310,
            200, 50,
            "Главно мени",
            (200, 0, 0),
            (230, 0, 0)
        )
        restart_btn, restart_hovered = draw_button(
            palette_start_x + 600,
            palette_y + palette_radius - 60,
            200, 50,
            "Рестарт",
            (0, 120, 255),
            (0, 150, 255)
        )

        back_btn, back_hovered = draw_button(
            screen_width // 2 + 260,
            screen_height // 2 - 385,
            200, 50,
            "Назад",
            (200, 0, 0),
            (230, 0, 0)
        )

        next_btn, next_hovered = None, None
        if finished:
            next_btn, next_hovered = draw_button(
                final_x + (target_width - 200) // 2,
                final_y + target_height + 20,
                200, 50,
                "Следна слика",
                (0, 200, 0),
                (0, 230, 0)
            )

        current_hovered = restart_btn if restart_hovered else next_btn if next_hovered else back_btn if back_hovered else backmenu_btn if backmenu_hovered else None
        if button_sound and current_hovered != prev_hovered_button:
            button_sound.play()
        prev_hovered_button = current_hovered

        if finished:
            show_congrats_screen()

        mouse_pressed = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        local_x = mx - bg_x
        local_y = my - bg_y

        if mouse_pressed[0] and not finished and selected_color:
            painted = False
            for a in areas:
                x, y, w, h = a["rect"]
                abs_x = x + bg_x
                abs_y = y + bg_y
                if abs_x <= mx <= abs_x + w and abs_y <= my <= abs_y + h:
                    if a["number"] == selected_number:
                        pygame.draw.circle(draw_surface, selected_color + (255,), (local_x, local_y), 12)
                        a["visited"] = True
                        a["color"] = selected_color
                    painted = True
                    break
            if not painted:
                pygame.draw.circle(draw_surface, selected_color + (255,), (local_x, local_y), 12)

            if all_colored() and not finished:
                try:
                    pygame.mixer.Sound("correct.wav").play()
                except:
                    pass
                finished = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos

                    if restart_btn.collidepoint(mx, my):
                        if button_click_sound:
                            button_click_sound.play()
                        for a in areas:
                            a["color"] = None
                            a["visited"] = False
                        draw_surface.fill((0, 0, 0, 0))
                        finished = False
                        selected_color = None
                        selected_number = None

                    if back_btn.collidepoint(mx, my):
                        if button_click_sound:
                            button_click_sound.play()
                        running = False
                        from NIVO8.level1 import start_drawing_game
                        start_drawing_game()
                    elif backmenu_btn.collidepoint(mx, my):
                        if button_click_sound:
                            button_click_sound.play()
                        running = False
                        from main.cpc import main
                        main()
                    elif finished and next_btn and next_btn.collidepoint(mx, my):
                        if button_click_sound:
                            button_click_sound.play()

                        running = False

                    elif not finished:
                        for num, pos in palette_pos.items():
                            px, py = pos
                            if (mx - px) ** 2 + (my - py) ** 2 <= palette_radius ** 2:
                                if button_click_sound:
                                    button_click_sound.play()
                                selected_color = palette_colors[num]
                                selected_number = num
                                break

        pygame.display.flip()
        clock.tick(60)

