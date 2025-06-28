import pygame
import sys
import random

from NIVO5.level1 import start_emotion_game

QUESTION_COUNT = 5


def start_level2():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption(" Препознај ја емоцијата - Ниво 2")

    # Colors
    colors = {
        'primary': (26, 26, 46),  # #1a1a2e
        'secondary': (15, 52, 96),  # #0f3460
        'accent': (233, 69, 96),  # #e94560
        'success': (39, 174, 96),  # #27ae60
        'error': (231, 76, 60),  # #e74c3c
        'text': (255, 255, 255),  # #ffffff
        'cyan': (78, 205, 196)  # #4ecdc4
    }

    # Fonts
    title_font = pygame.font.Font(None, 48)
    score_font = pygame.font.Font(None, 36)
    story_font = pygame.font.Font(None, 32)
    button_font = pygame.font.Font(None, 28)
    feedback_font = pygame.font.Font(None, 36)
    prompt_font = pygame.font.Font(None, 32)

    # Load sounds
    try:
        correct_sound = pygame.mixer.Sound("../sounds/correct.wav")
        wrong_sound = pygame.mixer.Sound("../sounds/wrong.mp3")
    except:
        correct_sound = None
        wrong_sound = None

    # Emotion images
    emotions_images = {
        "Среќно": pygame.image.load("../Pictures-Game5/среќен.png").convert_alpha(),
        "Тажно": pygame.image.load("../Pictures-Game5/тажен.png").convert_alpha(),
        "Луто": pygame.image.load("../Pictures-Game5/лут.png").convert_alpha(),
        "Исплашено": pygame.image.load("../Pictures-Game5/исплашен.png").convert_alpha(),
        "Засрамено": pygame.image.load("../Pictures-Game5/засрамен.png").convert_alpha(),
        "Возбудено": pygame.image.load("../Pictures-Game5/возбуден.png").convert_alpha(),
    }

    # Scale images
    for emotion in emotions_images:
        emotions_images[emotion] = pygame.transform.scale(emotions_images[emotion], (100, 100))

    # Stories and correct answers
    stories = [
        (
        "Јана го отвори малото, шарено кутивче што ѝ го подаде нејзиниот најблизок пријател. Во него имаше токму тоа што таа го посакуваше. Ѝ засветкаа очите, а лицето ѝ се рашири во голема насмевка.",
        "Среќно"),
        (
        "Додека шеташе по улицата, Миро го забележа своето старо, омилено топче. Но не беше како порано - беше напукнато и извалкано. Тој се наведна, го зеде в раце и неколку солзи му се стркалаа по образите.",
        "Тажно"),
        (
        "Марио се приближуваше до пешачкиот премин кога одеднаш забележа кола што доаѓа брзо. Се замрзна на место и срцето му затропа забрзано. Го фати за рака татка си и го стегна цврсто.",
        "Исплашено"),
        (
        "Кога наставничката ја повика Марија да зборува пред целото одделение, нејзиното лице поцрвене и таа почна да ја вртка блузата со рацете. Се трудеше да ги избегне сите погледи, чувствувајќи се малку непријатно.",
        "Засрамено"),
        (
        "Алекс постојано ѕиркаше низ прозорецот, броејќи ги часовите. Утре беше големиот ден - натпреварот со неговите другари. Не можеше да седи мирен и постојано размислуваше како ќе даде гол и ќе прослават заедно.",
        "Возбудено"),
        (
        "Петар се обиде неколку пати да каже нешто во групата, но никој не го слушаше. Сите зборуваа еден преку друг. Конечно, тој ги стисна тупаниците и со подигнат тон викна: 'Ајде малку и јас да кажам нешто!'",
        "Луто"),
    ]

    # Emotions list
    emotions = ["Среќно", "Тажно", "Луто", "Исплашено", "Засрамено", "Возбудено"]

    # Game state
    current_question = 0
    score = 0
    current_correct_answer = ""
    current_story = ""
    current_options = []
    feedback_text = ""
    feedback_color = colors['text']
    show_feedback = False
    feedback_timer = 0
    animation_running = False
    game_finished = False

    def draw_rounded_rect(surface, rect, color, border_radius=10):
        """Draw a rounded rectangle"""
        if border_radius > 0:
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)
        else:
            pygame.draw.rect(surface, color, rect)

    def draw_text_wrapped(surface, text, font, color, rect, line_spacing=5):
        """Draw text with word wrapping"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= rect.width - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        y_offset = 0
        for line in lines:
            if y_offset + font.get_height() > rect.height:
                break
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (rect.x + 10, rect.y + y_offset + 10))
            y_offset += font.get_height() + line_spacing

    def draw_button(surface, rect, text, font, bg_color, text_color, border_color=None, border_width=2):
        """Draw a button with rounded corners"""
        draw_rounded_rect(surface, rect, bg_color, 15)
        if border_color:
            pygame.draw.rect(surface, border_color, rect, border_width, border_radius=15)

        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def next_question():
        nonlocal current_question, current_correct_answer, current_story, current_options
        nonlocal feedback_text, show_feedback, animation_running, game_finished

        if current_question >= QUESTION_COUNT:
            game_finished = True
            return

        # Select random story
        story, correct_emotion = random.choice(stories)
        current_correct_answer = correct_emotion
        current_story = story

        # Create options (1 correct + 2 random)
        options = [correct_emotion]
        while len(options) < 3:
            option = random.choice(emotions)
            if option not in options:
                options.append(option)
        random.shuffle(options)
        current_options = options

        current_question += 1
        feedback_text = ""
        show_feedback = False
        animation_running = False

    def check_answer(selected_emotion):
        nonlocal score, feedback_text, feedback_color, show_feedback, feedback_timer, animation_running

        if animation_running:
            return

        animation_running = True

        if selected_emotion == current_correct_answer:
            score += 1
            feedback_text = " Точно!"
            feedback_color = colors['success']
            if correct_sound:
                correct_sound.play()
        else:
            feedback_text = f" Неточно! Точен одговор: {current_correct_answer}"
            feedback_color = colors['error']
            if wrong_sound:
                wrong_sound.play()

        show_feedback = True
        feedback_timer = pygame.time.get_ticks()

    def restart_game():
        nonlocal current_question, score, game_finished, show_feedback, animation_running
        current_question = 0
        score = 0
        game_finished = False
        show_feedback = False
        animation_running = False
        next_question()

    def return_to_main():
        """Return to main menu"""
        try:
            from main.cpc import main
            #pygame.quit()
            main()
        except ImportError:
            print("Main module not found!")
            pygame.quit()

    def draw_game_screen():
        # Fill background
        screen.fill(colors['primary'])

        # Draw title
        title_text = title_font.render(" ПРЕПОЗНАЈ ЈА ЕМОЦИЈАТА - Ниво 2", True, colors['cyan'])
        title_rect = title_text.get_rect(centerx=WIDTH // 2, y=30)
        screen.blit(title_text, title_rect)

        # Draw score
        score_text = score_font.render(f"РЕЗУЛТАТ: {score} / {QUESTION_COUNT}", True, colors['text'])
        score_bg_rect = pygame.Rect(WIDTH // 2 - 150, 90, 300, 50)
        draw_rounded_rect(screen, score_bg_rect, colors['secondary'], 10)
        score_rect = score_text.get_rect(center=score_bg_rect.center)
        screen.blit(score_text, score_rect)

        if not game_finished:
            # Draw story background
            story_bg_rect = pygame.Rect(40, 180, WIDTH - 100, 150)
            draw_rounded_rect(screen, story_bg_rect, colors['secondary'], 10)

            # Draw story text
            draw_text_wrapped(screen, current_story, story_font, colors['text'], story_bg_rect)

            # Draw prompt
            prompt_text = prompt_font.render("Која е неговата/нејзината емоција?", True, colors['text'])
            prompt_rect = prompt_text.get_rect(centerx=WIDTH // 2, y=360)
            screen.blit(prompt_text, prompt_rect)

            # Draw option buttons
            button_width = 350
            button_height = 80
            button_spacing = 50
            total_width = len(current_options) * button_width + (len(current_options) - 1) * button_spacing
            start_x = (WIDTH - total_width) // 2
            button_y = 420
            image_y = button_y + button_height + 20

            for i, option in enumerate(current_options):
                button_x = start_x + i * (button_width + button_spacing)
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                # Check if mouse is over button
                mouse_pos = pygame.mouse.get_pos()
                is_hovered = button_rect.collidepoint(mouse_pos) and not animation_running

                button_color = colors['accent'] if is_hovered else colors['secondary']
                border_color = colors['cyan'] if is_hovered else colors['cyan']

                draw_button(screen, button_rect, option, button_font, button_color, colors['text'], border_color)

                # Draw emotion image below the button
                if option in emotions_images:
                    image = emotions_images[option]
                    image_rect = image.get_rect(centerx=button_rect.centerx, y=image_y)
                    screen.blit(image, image_rect)

                # Store button rect for click detection
                if not hasattr(draw_game_screen, 'button_rects'):
                    draw_game_screen.button_rects = []
                if len(draw_game_screen.button_rects) <= i:
                    draw_game_screen.button_rects.append(button_rect)
                else:
                    draw_game_screen.button_rects[i] = button_rect

            # Draw feedback
            if show_feedback:
                feedback_surface = feedback_font.render(feedback_text, True, feedback_color)
                feedback_rect = feedback_surface.get_rect(centerx=WIDTH // 2, y=image_y + 130)
                screen.blit(feedback_surface, feedback_rect)

        else:
            # Game finished screen
            percent = (score / QUESTION_COUNT) * 100

            if percent >= 80:
                message = " ОДЛИЧНО!"
                message_color = colors['success']
            elif percent >= 60:
                message = " ДОБРО!"
                message_color = (243, 156, 18)  # Orange
            else:
                message = " ВЕЖБАЈ ПОВЕЌЕ!"
                message_color = colors['error']

            # Draw final message
            final_text = f"КРАЈ НА ИГРАТА\n\nВаш резултат: {score} од {QUESTION_COUNT}\n{message}"
            lines = final_text.split('\n')

            y_offset = 250
            for i, line in enumerate(lines):
                if line.strip():
                    color = message_color if i == len(lines) - 1 else colors['text']
                    line_surface = story_font.render(line, True, color)
                    line_rect = line_surface.get_rect(centerx=WIDTH // 2, y=y_offset)
                    screen.blit(line_surface, line_rect)
                y_offset += 40

            # Draw restart button
            restart_button_rect = pygame.Rect(WIDTH // 2 - 150, 450, 300, 60)
            draw_button(screen, restart_button_rect, " ИГРАЈ ПОВТОРНО", button_font, colors['accent'], colors['text'],
                        colors['cyan'])

            # Store restart button rect
            draw_game_screen.restart_button_rect = restart_button_rect

        # Draw back button
        back_button_rect = pygame.Rect(50, HEIGHT - 80, 150, 50)
        draw_button(screen, back_button_rect, "Главно мени", button_font, colors['secondary'], colors['text'],
                    colors['cyan'])
        draw_game_screen.back_button_rect = back_button_rect

    # Initialize button rects
    draw_game_screen.button_rects = []
    draw_game_screen.restart_button_rect = None
    draw_game_screen.back_button_rect = None

    # Start first question
    next_question()

    # Main game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        # Handle feedback timer
        if show_feedback and current_time - feedback_timer > 2000:
            show_feedback = False
            animation_running = False
            next_question()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()

                    # Check back button
                    if draw_game_screen.back_button_rect and draw_game_screen.back_button_rect.collidepoint(mouse_pos):
                        try:
                            return_to_main()
                            running = False
                        except ImportError:
                            print("Could not import start_level1 function")
                        return

                    if not game_finished:
                        # Check option buttons
                        if not animation_running:
                            for i, button_rect in enumerate(draw_game_screen.button_rects):
                                if button_rect.collidepoint(mouse_pos):
                                    selected_emotion = current_options[i]
                                    check_answer(selected_emotion)
                                    break
                    else:
                        # Check restart button
                        if draw_game_screen.restart_button_rect and draw_game_screen.restart_button_rect.collidepoint(
                                mouse_pos):
                            restart_game()

        # Draw everything
        draw_game_screen()

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    start_level2()