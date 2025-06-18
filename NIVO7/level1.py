import pygame
import sys
import random


def start_social_skills_game():
    # Иницијализација
    pygame.init()
    pygame.mixer.init()

    # Екран
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Игра за социјални вештини")

    # Звуци
    try:
        correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
        wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")
    except:
        correct_sound = None
        wrong_sound = None

    # Бои
    BG_COLOR = (255, 209, 102)  # Светло жолта
    BUTTON_COLOR = (6, 214, 160)  # Мента зелена
    TEXT_COLOR = (7, 59, 76)  # Темно сина
    CORRECT_COLOR = (21, 87, 36)  # Темно зелена
    WRONG_COLOR = (114, 28, 36)  # Темно црвена
    FEEDBACK_BG_CORRECT = (212, 237, 218)  # Светло зелена
    FEEDBACK_BG_WRONG = (248, 215, 218)  # Светло розова
    FEEDBACK_COLOR = (17, 138, 178)  # Сина

    # Фонтови
    title_font = pygame.font.SysFont("Arial", int(HEIGHT * 0.04), bold=True)
    question_font = pygame.font.SysFont("Arial", int(HEIGHT * 0.03))
    button_font = pygame.font.SysFont("Arial", int(HEIGHT * 0.025))
    feedback_font = pygame.font.SysFont("Arial", int(HEIGHT * 0.025), bold=True)

    # Податоци за играта
    level1_questions = [
        {
            "question": "Што треба да направиш ако некој ти каже: 'Добро утро'?",
            "options": ["Игнорирај го", "Кажи: 'Добро утро'", "Почни да плачеш"],
            "correct": 1
        },
        {
            "question": "Ако некој сака да игра со тебе, што ќе направиш?",
            "options": ["Кажи: 'Ајде да играме!'", "Се свртиш и избегаш", "Кажи му да си оди"],
            "correct": 0
        }
    ]

    # Level 2 - Branching Story
    level2_story = {
        "start": {
            "scene": "Ти си во училиште. Како ќе поздравиш другар?",
            "options": [
                ("Здраво! Како си? ", "friendly_response"),
                ("Не сакам да зборувам. ", "angry_response"),
                ("Дај ми ги твоите моливи! ", "demanding_response")
            ],
            "image": ""
        },
        "friendly_response": {
            "scene": "Твојот другар се насмевнува и ти вели: 'Добро сум! Сакаш да играме заедно?'",
            "options": [
                ("Да, ајде! ", "play_together"),
                ("Не, не ми се игра. ", "dont_play"),
                ("Само ако ја играме мојата игра. ", "my_game_only")
            ],
            "image": ""
        },
        "angry_response": {
            "scene": "Твојот другар изгледа повреден и си заминува. Што ќе направиш?",
            "options": [
                ("Ќе го испратам и ќе му се извинам. ", "apologize"),
                ("Не ми е гајле. ", "dont_care"),
                ("Ќе му викам 'Не бегај!'", "chase_friend")
            ],
            "image": ""
        },
        "demanding_response": {
            "scene": "Твојот другар се чуди зошто бараш моливи веднаш. Што ќе кажеш?",
            "options": [
                ("Извини, може ли да ми позајмиш молив? ", "polite_request"),
                ("Ми требаат сега! ", "insist_demand"),
                ("Заборавив моите дома. ", "explain_reason")
            ],
            "image": "️"
        },
        # Friendly response endings
        "play_together": {
            "scene": "Играте заедно и се забавувате. Другарот ти вели: 'Многу е убаво кога си дружељубив!'",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Одлично! Умееш да бидеш пријател и да се спријателиш со другите!"
        },
        "dont_play": {
            "scene": "Твојот другар изгледа малку разочаран, но прифаќа. После неколку минути, се осмелуваш да му се придружиш.",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Добро е да ги изразиш своите чувства, но исто така е убаво да се обидеш да се спријателиш!"
        },
        "my_game_only": {
            "scene": "Твојот другар се согласува, но не му се допаѓа што мора да ја игра твојата игра. Играта не е толку забавна.",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Понекогаш е подобро да се договорите за игра што ќе им се допадне и на двајцата!"
        },
        # Angry response endings
        "apologize": {
            "scene": "Твојот другар прифаќа извинување и вие повторно сте пријатели. Како се чувствуваш?",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Браво! Извинувањето е знак на силна личност и ги поправа грешките."
        },
        "dont_care": {
            "scene": "Твојот другар продолжува да си оди и целото утро се чувствуваш самотно.",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Не е добро да ги игнорираме чувствата на другите. Можеш да се извиниш и подоцна."
        },
        "chase_friend": {
            "scene": "Твојот другар се исплаши и трча да се жали на наставникот. Наставникот ќе разговара со вас двајца.",
            "options": [],
            "image": "️",
            "end": True,
            "feedback": "Наметнувањето може да ги исплаши другите. Подобро е да се разговара мирно."
        },
        # Demanding response endings
        "polite_request": {
            "scene": "Твојот другар ти дава молив и вели: 'Секако! Следниот пат само побарај поубаво.'",
            "options": [],
            "image": "️",
            "end": True,
            "feedback": "Добро одбрано! Убаво е да бидеш учтив кога нешто го бараш."
        },
        "insist_demand": {
            "scene": "Твојот другар се налути и одбива да ти даде молив. Сега и двајцата сте лути.",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Наметливиот тон може да ги разлути другите. Обиди се да бидеш поубав следниот пат."
        },
        "explain_reason": {
            "scene": "Твојот другар разбира и ти дава молив: 'Еве, ама следниот пат запамти да ги носиш своите.'",
            "options": [],
            "image": "",
            "end": True,
            "feedback": "Објаснувањето на ситуацијата помага другите да разберат и да ти помогнат!"
        }
    }

    # Глобални променливи
    current_level = 1
    current_question = 0
    score = 0
    current_story_node = "start"
    feedback_text = ""
    feedback_color = TEXT_COLOR
    feedback_bg = BG_COLOR
    show_feedback = False
    feedback_timer = 0
    game_state = "level1"  # "level1", "level2", "game_over"
    waiting_for_next = False

    confetti_particles = []
    CONFETTI_COLORS = [(255, 107, 107), (78, 205, 196), (69, 183, 209),
                       (243, 156, 18), (231, 76, 60), (155, 89, 182)]

    def create_confetti(x, y, count=30):

        for _ in range(count):
            confetti_particles.append({
                'x': x,
                'y': y,
                'size': random.randint(5, 10),
                'color': random.choice(CONFETTI_COLORS),
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-5, -1),
                'life': random.randint(40, 60)
            })

    def update_confetti():

        for p in confetti_particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['dy'] += 0.1  # Gravity
            p['life'] -= 1

            if p['life'] <= 0:
                confetti_particles.remove(p)

    def draw_confetti(surface):

        for p in confetti_particles:
            alpha = min(255, p['life'] * 5)  # Fade out
            s = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            s.fill((*p['color'], alpha))
            surface.blit(s, (p['x'], p['y']))

    def wrap_text(text, font, max_width):

        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def draw_button(surface, rect, color, border_color, text, font, text_color=TEXT_COLOR):
        """Црта копче со текст"""
        pygame.draw.rect(surface, border_color, rect, border_radius=15, width=3)
        pygame.draw.rect(surface, color, rect.inflate(-6, -6), border_radius=12)

        lines = wrap_text(text, font, rect.width - 20)
        total_height = len(lines) * font.get_height()
        start_y = rect.centery - total_height // 2

        for i, line in enumerate(lines):
            text_surf = font.render(line, True, text_color)
            text_x = rect.centerx - text_surf.get_width() // 2
            text_y = start_y + i * font.get_height()
            surface.blit(text_surf, (text_x, text_y))

    def draw_text_centered(surface, text, font, color, y, max_width=None):

        if max_width:
            lines = wrap_text(text, font, max_width)
            total_height = len(lines) * font.get_height()
            start_y = y - total_height // 2

            for i, line in enumerate(lines):
                text_surf = font.render(line, True, color)
                text_x = WIDTH // 2 - text_surf.get_width() // 2
                text_y = start_y + i * font.get_height()
                surface.blit(text_surf, (text_x, text_y))
        else:
            text_surf = font.render(text, True, color)
            text_x = WIDTH // 2 - text_surf.get_width() // 2
            surface.blit(text_surf, (text_x, y))

    def show_feedback_message(message, is_correct=None):
        nonlocal feedback_text, feedback_color, feedback_bg, show_feedback, feedback_timer
        feedback_text = message
        show_feedback = True
        feedback_timer = pygame.time.get_ticks()

        if is_correct is True:
            feedback_color = CORRECT_COLOR
            feedback_bg = FEEDBACK_BG_CORRECT
            # Create confetti at center screen
            create_confetti(WIDTH // 2, HEIGHT // 2)
            if correct_sound:
                correct_sound.play()
        elif is_correct is False:
            feedback_color = WRONG_COLOR
            feedback_bg = FEEDBACK_BG_WRONG
            if wrong_sound:
                wrong_sound.play()
        else:
            feedback_color = FEEDBACK_COLOR
            feedback_bg = (232, 244, 253)  # Светло сина

    def draw_level1():
        nonlocal waiting_for_next

        draw_text_centered(screen, "Ниво 1: Основни социјални вештини", title_font, TEXT_COLOR, HEIGHT * 0.1)

        emoji_font = pygame.font.SysFont("Arial", 80)
        draw_text_centered(screen, "", emoji_font, TEXT_COLOR, HEIGHT * 0.2)

        if current_question < len(level1_questions):
            question = level1_questions[current_question]
            draw_text_centered(screen, question["question"], question_font, TEXT_COLOR, HEIGHT * 0.35, WIDTH * 0.8)

            button_width = WIDTH * 0.6
            button_height = HEIGHT * 0.08
            start_y = HEIGHT * 0.5

            for i, option in enumerate(question["options"]):
                button_rect = pygame.Rect(
                    WIDTH // 2 - button_width // 2,
                    start_y + i * (button_height + 20),
                    button_width,
                    button_height
                )

                if not waiting_for_next:
                    draw_button(screen, button_rect, BUTTON_COLOR, TEXT_COLOR, option, button_font)
                else:

                    if i == question["correct"]:
                        draw_button(screen, button_rect, FEEDBACK_BG_CORRECT, CORRECT_COLOR, option, button_font,
                                    CORRECT_COLOR)
                    else:
                        draw_button(screen, button_rect, (200, 200, 200), (100, 100, 100), option, button_font,
                                    (100, 100, 100))

        score_text = f"Поени: {score}/{len(level1_questions)}"
        draw_text_centered(screen, score_text, question_font, TEXT_COLOR, HEIGHT * 0.85)

    def draw_level2():

        draw_text_centered(screen, "Ниво 2: Приказна за другарство", title_font, TEXT_COLOR, HEIGHT * 0.1)

        scene = level2_story[current_story_node]

        emoji_font = pygame.font.SysFont("Arial", 80)
        draw_text_centered(screen, scene["image"], emoji_font, TEXT_COLOR, HEIGHT * 0.2)

        draw_text_centered(screen, scene["scene"], question_font, TEXT_COLOR, HEIGHT * 0.35, WIDTH * 0.8)

        if not scene.get("end", False):
            button_width = WIDTH * 0.6
            button_height = HEIGHT * 0.08
            start_y = HEIGHT * 0.5

            for i, (option_text, _) in enumerate(scene["options"]):
                button_rect = pygame.Rect(
                    WIDTH // 2 - button_width // 2,
                    start_y + i * (button_height + 20),
                    button_width,
                    button_height
                )
                draw_button(screen, button_rect, BUTTON_COLOR, TEXT_COLOR, option_text, button_font)
        else:

            restart_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT * 0.75, 300, 60)
            draw_button(screen, restart_rect, BUTTON_COLOR, TEXT_COLOR, "Започни нова приказна", button_font)

    def draw_feedback():
        if show_feedback and feedback_text:

            panel_width = min(WIDTH * 0.6, 500)
            panel_height = min(HEIGHT * 0.15, 120)
            panel_rect = pygame.Rect(
                WIDTH // 2 - panel_width // 2,
                HEIGHT // 2 - panel_height // 2,
                panel_width,
                panel_height
            )

            s = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            s.fill((*feedback_bg, 220))
            screen.blit(s, panel_rect)

            pygame.draw.rect(screen, feedback_color, panel_rect, 3, border_radius=15)

            lines = wrap_text(feedback_text, feedback_font, panel_width - 40)
            total_height = len(lines) * feedback_font.get_height()
            start_y = panel_rect.centery - total_height // 2

            for i, line in enumerate(lines):
                text_surf = feedback_font.render(line, True, feedback_color)
                text_rect = text_surf.get_rect(centerx=panel_rect.centerx,
                                               y=start_y + i * feedback_font.get_height())
                screen.blit(text_surf, text_rect)

            if feedback_bg == FEEDBACK_BG_CORRECT:
                update_confetti()
                draw_confetti(screen)

    def draw_back_button():
        back_rect = pygame.Rect(50, HEIGHT - 100, 200, 50)
        draw_button(screen, back_rect, (239, 71, 111), (200, 50, 90), "Назад кон главното мени", button_font,
                    (255, 255, 255))
        return back_rect

    def handle_level1_click(pos):
        nonlocal current_question, score, game_state, waiting_for_next

        if waiting_for_next:
            return

        if current_question < len(level1_questions):
            question = level1_questions[current_question]
            button_width = WIDTH * 0.6
            button_height = HEIGHT * 0.08
            start_y = HEIGHT * 0.5

            for i, option in enumerate(question["options"]):
                button_rect = pygame.Rect(
                    WIDTH // 2 - button_width // 2,
                    start_y + i * (button_height + 20),
                    button_width,
                    button_height
                )

                if button_rect.collidepoint(pos):
                    correct = question["correct"]
                    waiting_for_next = True

                    if i == correct:
                        score += 1
                        show_feedback_message("Точно! Браво!", True)
                        if correct_sound:
                            correct_sound.play()
                    else:
                        correct_answer = question["options"][correct]
                        show_feedback_message(f"Не е точно. Точниот одговор е: {correct_answer}", False)
                        if wrong_sound:
                            wrong_sound.play()

                    return

    def handle_level2_click(pos):
        nonlocal current_story_node, game_state

        scene = level2_story[current_story_node]

        if scene.get("end", False):

            restart_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT * 0.75, 300, 60)
            if restart_rect.collidepoint(pos):
                current_story_node = "start"
                show_feedback_message("", None)
        else:

            button_width = WIDTH * 0.6
            button_height = HEIGHT * 0.08
            start_y = HEIGHT * 0.5

            for i, (option_text, next_node) in enumerate(scene["options"]):
                button_rect = pygame.Rect(
                    WIDTH // 2 - button_width // 2,
                    start_y + i * (button_height + 20),
                    button_width,
                    button_height
                )

                if button_rect.collidepoint(pos):
                    current_story_node = next_node
                    next_scene = level2_story[current_story_node]

                    if next_scene.get("end", False):
                        show_feedback_message(next_scene["feedback"], None)
                    break

    def check_level1_progression():
        nonlocal current_question, game_state, waiting_for_next

        if waiting_for_next and pygame.time.get_ticks() - feedback_timer > 3000:
            waiting_for_next = False
            current_question += 1

            if current_question >= len(level1_questions):

                show_feedback_message(f"Го заврши Ниво 1! ({score}/{len(level1_questions)})", None)
                game_state = "level2"
            else:
                show_feedback_message("", None)

    running = True
    clock = pygame.time.Clock()

    while running:
        current_time = pygame.time.get_ticks()

        if show_feedback and current_time - feedback_timer > 3000:
            show_feedback = False
            feedback_text = ""
            if not (game_state == "level1" and waiting_for_next):
                confetti_particles.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                back_rect = draw_back_button()
                if back_rect.collidepoint(pos):
                    from main.cpc import main
                    main()

                if game_state == "level1":
                    handle_level1_click(pos)
                elif game_state == "level2":
                    handle_level2_click(pos)

        if game_state == "level1":
            check_level1_progression()

        screen.fill(BG_COLOR)

        if game_state == "level1":
            draw_level1()
        elif game_state == "level2":
            draw_level2()

        draw_feedback()
        draw_back_button()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    start_social_skills_game()