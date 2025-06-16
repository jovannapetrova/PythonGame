import pygame
import sys
import random
import math
import unicodedata
import os


def run_macedonian_game():
    """Main function to run the Macedonian letter learning game"""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Set up fullscreen display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("🎮 Игра: Која слика започнува со буквата? 🎮")

    # Fonts
    title_font = pygame.font.SysFont("Arial", 22, bold=True)
    button_font = pygame.font.SysFont("Arial", 16, bold=True)
    feedback_font = pygame.font.SysFont("Arial", 24, bold=True)
    big_font = pygame.font.SysFont("Arial", 32, bold=True)
    small_font = pygame.font.SysFont("Arial", 16)
    text_font = pygame.font.SysFont("Arial", 24)  # Larger font for level 3 text

    # Colors
    BG_COLOR = (224, 246, 255)
    BUTTON_COLOR = (50, 205, 50)
    BUTTON_HOVER = (34, 139, 34)
    CORRECT_COLOR = (144, 238, 144)
    WRONG_COLOR = (255, 107, 107)
    SELECTED_COLOR = (255, 215, 0)
    PROGRESS_COLOR = (46, 139, 87)
    LEVEL2_COLOR = (30, 144, 255)
    LEVEL3_COLOR = (255, 215, 0)
    BACK_BUTTON_COLOR = (255, 69, 0)
    BACK_BUTTON_HOVER = (255, 99, 71)
    TEXT_BG_COLOR = (240, 248, 255)  # Light background for text in level 3
    TEXT_BORDER_COLOR = (100, 149, 237)  # Border color for text box

    # Macedonian Cyrillic alphabet
    MACEDONIAN_ALPHABET = "АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ"

    # Image paths dictionary
    images = {
        "јаболко": "../Pictures-Game4/јаболко.png",
        "авион": "../Pictures-Game4/авион.png",
        "вазна": "../Pictures-Game4/вазна.png",
        "банана": "../Pictures-Game4/банана.png",
        "грозје": "../Pictures-Game4/грозје1.png",
        "куќа": "../Pictures-Game4/куќа.png",
        "жирафа": "../Pictures-Game4/жирафа.png",
        "око": "../Pictures-Game4/око.png",
        "молив": "../Pictures-Game4/молив.png",
        "верверица": "../Pictures-Game4/верверица.png",
        "нож": "../Pictures-Game4/нож.png",
    }

    # Load images
    loaded_images = {}
    for word, path in images.items():
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (180, 180))
            loaded_images[word] = img
        except:
            placeholder = pygame.Surface((180, 180))
            placeholder.fill((200, 200, 200))
            loaded_images[word] = placeholder

    # Load background image for celebration
    try:
        celebration_bg = pygame.image.load("../Pictures-Game4/background_image.png")
        celebration_bg = pygame.transform.scale(celebration_bg, (WIDTH, HEIGHT))
    except:
        celebration_bg = pygame.Surface((WIDTH, HEIGHT))
        celebration_bg.fill(BG_COLOR)

    # Unicode normalization functions
    def normalize_mk(text):
        return unicodedata.normalize('NFC', text.lower())

    def mk_contains(text, substring):
        return normalize_mk(substring) in normalize_mk(text)

    def mk_startswith(text, substring):
        return normalize_mk(text).startswith(normalize_mk(substring))

    # Load random texts from a file
    def load_random_text():
        try:
            with open('random_texts.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
            return random.choice(lines).strip()
        except:
            return "Македонија е убава земја. Живееме во мир и хармонија."

    # Play sound function
    def play_sound(file_path):
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.play()
        except:
            pass

    # Confetti system
    class ConfettiParticle:
        def __init__(self):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(-500, -50)
            self.size = random.randint(8, 25)
            self.color = random.choice([
                (255, 107, 107), (78, 205, 196), (69, 183, 209),
                (150, 206, 180), (255, 234, 167), (221, 160, 221),
                (255, 140, 148), (152, 216, 200)
            ])
            self.shape = random.choice(["circle", "star", "heart", "rectangle"])
            self.speed = random.randint(3, 8)
            self.rotation = random.randint(0, 360)
            self.rotation_speed = random.randint(-10, 10)

        def update(self):
            self.y += self.speed
            self.x += random.randint(-2, 2)
            self.rotation += self.rotation_speed
            return self.y < HEIGHT

        def draw(self, surface):
            if self.shape == "circle":
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            elif self.shape == "rectangle":
                rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
                pygame.draw.rect(surface, self.color, rect)
            elif self.shape == "star":
                self.draw_star(surface)
            elif self.shape == "heart":
                self.draw_heart(surface)

        def draw_star(self, surface):
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                radius = self.size if i % 2 == 0 else self.size // 2
                px = self.x + radius * math.cos(angle)
                py = self.y + radius * math.sin(angle)
                points.append((px, py))
            if len(points) > 2:
                pygame.draw.polygon(surface, self.color, points)

        def draw_heart(self, surface):
            points = [
                (self.x, self.y + self.size // 4),
                (self.x - self.size // 4, self.y),
                (self.x - self.size // 2, self.y + self.size // 4),
                (self.x - self.size // 2, self.y + self.size // 2),
                (self.x, self.y + self.size),
                (self.x + self.size // 2, self.y + self.size // 2),
                (self.x + self.size // 2, self.y + self.size // 4),
                (self.x + self.size // 4, self.y)
            ]
            if len(points) > 2:
                pygame.draw.polygon(surface, self.color, points)

    # Game state variables
    confetti_particles = []
    confetti_active = False
    confetti_timer = 0
    progress = 0
    level = 1
    progress_needed = 3
    selected_correct = 0
    total_correct = 0
    target_letter = ""
    correct_word = ""
    correct_words = []
    game_complete = False
    show_feedback = False
    feedback_text = ""
    feedback_color = (0, 0, 0)
    feedback_timer = 0

    # Button class
    class Button:
        def __init__(self, x, y, width, height, text, word=None, is_back_button=False):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.word = word
            self.is_back_button = is_back_button
            self.color = BACK_BUTTON_COLOR if is_back_button else BUTTON_COLOR
            self.hover_color = BACK_BUTTON_HOVER if is_back_button else BUTTON_HOVER
            self.state = "normal"
            self.hover = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.hover = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and self.state != "disabled":
                    return True
            return False

        def draw(self, surface):
            color = self.color
            if self.state == "selected":
                color = SELECTED_COLOR
            elif self.state == "correct":
                color = CORRECT_COLOR
            elif self.state == "wrong":
                color = WRONG_COLOR
            elif self.hover and self.state == "normal":
                color = self.hover_color

            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, width=2, border_radius=10)

            text_color = (255, 255, 255) if self.state != "wrong" else (0, 0, 0)
            if self.is_back_button:
                text_color = (255, 255, 255)

            text_surface = button_font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    # Current game state
    displayed_words = []
    image_buttons = []
    game_text = ""
    text_input = ""
    text_count = 0
    show_text_input = False
    input_active = False

    def count_letter_in_text(letter, text):
        return normalize_mk(text).count(normalize_mk(letter))

    def start_confetti():
        nonlocal confetti_particles, confetti_active, confetti_timer
        confetti_particles = [ConfettiParticle() for _ in range(200)]
        confetti_active = True
        confetti_timer = pygame.time.get_ticks()

    def update_confetti():
        nonlocal confetti_particles, confetti_active
        if not confetti_active:
            return

        confetti_particles = [p for p in confetti_particles if p.update()]

        if not confetti_particles or pygame.time.get_ticks() - confetti_timer > 3000:
            confetti_active = False

    def draw_confetti(surface):
        if confetti_active:
            for particle in confetti_particles:
                particle.draw(surface)

    def show_game_feedback(text, color, duration=2000):
        nonlocal show_feedback, feedback_text, feedback_color, feedback_timer
        show_feedback = True
        feedback_text = text
        feedback_color = color
        feedback_timer = pygame.time.get_ticks() + duration

    def check_selection(button):
        nonlocal progress, level, selected_correct, total_correct, correct_words

        selected_word = button.word
        button.state = "selected"

        if level == 2:
            all_correct_words = [word for word in images.keys() if mk_contains(word, target_letter)]

            if selected_word in all_correct_words:
                if button.state != "disabled":
                    selected_correct += 1
                    button.state = "correct"
                    button.text = "✓ ТОЧНО"

                    if selected_correct == total_correct:
                        progress += 1
                        if progress >= progress_needed:
                            level += 1
                            progress = 0
                            show_game_feedback("Честитки! Помина на ниво " + str(level) + "!", (0, 0, 255))
                        else:
                            show_game_feedback("БРАВО! Ги избравте сите точни слики! 🎉", (34, 139, 34))
                        play_sound("sounds/clap.mp3")
                        start_confetti()
                        pygame.time.wait(2000)
                        start_game()
                    else:
                        show_game_feedback(f"Точно! Избрана е {selected_correct} од {total_correct} точни слики.",
                                           (34, 139, 34))
                        play_sound("sounds/correct.mp3")
                else:
                    show_game_feedback("Обиди се повторно! Ти можеш! 💪", (255, 68, 68))
            else:
                button.state = "wrong"
                button.text = "✗ ГРЕШКА"
                show_game_feedback("Обиди се повторно! Ти можеш! 💪", (255, 68, 68))
                play_sound("sounds/try_again.mp3")
                pygame.time.wait(1500)
                button.state = "normal"
                button.text = "ИЗБЕРИ"
        else:
            if selected_word == correct_word:
                button.state = "correct"
                button.text = "✓ ТОЧНО"
                progress += 1

                if (level == 1 and progress >= progress_needed) or (level == 3 and progress >= progress_needed):
                    if level == 3:
                        show_game_complete()
                    else:
                        level += 1
                        progress = 0
                        show_game_feedback("Честитки! Помина на ниво " + str(level) + "!", (0, 0, 255))
                        pygame.time.wait(2000)
                        start_game()
                else:
                    show_game_feedback("БРАВО! 🎉", (34, 139, 34))
                    pygame.time.wait(2000)
                    start_game()

                play_sound("sounds/clap.mp3")
                start_confetti()
            else:
                button.state = "wrong"
                button.text = "✗ ГРЕШКА"
                show_game_feedback("Обиди се повторно! Ти можеш! 💪", (255, 68, 68))
                play_sound("sounds/try_again.mp3")
                pygame.time.wait(1500)
                button.state = "normal"
                button.text = "ИЗБЕРИ"

    def show_game_complete():
        nonlocal game_complete
        game_complete = True
        play_sound("sounds/victory.mp3")
        start_confetti()

    def reset_game():
        nonlocal level, progress, selected_correct, total_correct, game_complete
        level = 1
        progress = 0
        selected_correct = 0
        total_correct = 0
        game_complete = False
        start_game()

    def start_game():
        nonlocal target_letter, correct_word, correct_words, total_correct, selected_correct
        nonlocal displayed_words, image_buttons, game_text, show_text_input, text_input, text_count, input_active

        selected_correct = 0
        image_buttons = []
        show_text_input = False
        text_input = ""
        input_active = False

        if level == 1:
            while True:
                target_letter = random.choice(MACEDONIAN_ALPHABET)
                valid_words = [word for word in images.keys() if mk_startswith(word, target_letter)]
                if valid_words:
                    break

            correct_word = random.choice(valid_words)
            game_text = f"Која слика започнува со буквата '{target_letter}'?"

            other_words = random.sample([word for word in images.keys() if word != correct_word], 2)
            displayed_words = [correct_word] + other_words
            random.shuffle(displayed_words)

            start_x = (WIDTH - (3 * 250 + 2 * 60)) // 2
            for i, word in enumerate(displayed_words):
                x = start_x + i * (250 + 60)
                y = HEIGHT // 2
                button = Button(x, y, 200, 50, "ИЗБЕРИ", word)
                image_buttons.append(button)

        elif level == 2:
            while True:
                target_letter = random.choice(MACEDONIAN_ALPHABET)
                correct_words = [word for word in images.keys() if mk_contains(word, target_letter)]
                if 1 <= len(correct_words) <= 4:
                    break

            total_correct = len(correct_words)
            game_text = f"Изберете ги сите слики што ја содржат буквата '{target_letter}'?"

            incorrect_words = [word for word in images.keys() if not mk_contains(word, target_letter)]
            num_incorrect = max(1, min(4 - total_correct, len(incorrect_words)))
            other_words = random.sample(incorrect_words, num_incorrect)

            displayed_words = correct_words + other_words
            random.shuffle(displayed_words)

            start_x = (WIDTH - (len(displayed_words) * 200 + (len(displayed_words) - 1) * 40)) // 2
            for i, word in enumerate(displayed_words):
                x = start_x + i * (200 + 40)
                y = HEIGHT // 2
                button = Button(x, y, 180, 50, "ИЗБЕРИ", word)
                image_buttons.append(button)

        elif level == 3:
            while True:
                game_text = load_random_text()
                target_letter = random.choice(MACEDONIAN_ALPHABET)
                text_count = count_letter_in_text(target_letter, game_text)
                if text_count > 0:
                    break

            show_text_input = True
            text_input = ""
            input_active = True

    def handle_text_input(event):
        nonlocal text_input, input_active
        if not input_active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text_input = text_input[:-1]
            elif event.unicode.isdigit():
                text_input += event.unicode

    def check_text_input_answer():
        nonlocal progress, text_input, input_active

        try:
            user_answer = int(text_input)
            if user_answer == text_count:
                progress += 1
                if progress >= progress_needed:
                    show_game_complete()
                else:
                    show_game_feedback("БРАВО! 🎉", (34, 139, 34))
                    pygame.time.wait(2000)
                    start_game()
                play_sound("sounds/clap.mp3")
                start_confetti()
            else:
                show_game_feedback("Обиди се повторно! Ти можеш! 💪", (255, 68, 68))
                play_sound("sounds/try_again.mp3")
                text_input = ""
        except ValueError:
            show_game_feedback("Внесете валиден број!", (255, 68, 68))
            play_sound("sounds/try_again.mp3")
            text_input = ""

    def draw_progress_bar(surface):
        bar_width = 500
        bar_height = 30
        bar_x = (WIDTH - bar_width) // 2
        bar_y = 50

        pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), border_radius=15)

        progress_width = int((progress / progress_needed) * bar_width)
        if progress_width > 0:
            pygame.draw.rect(surface, PROGRESS_COLOR, (bar_x, bar_y, progress_width, bar_height), border_radius=15)

        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), width=2, border_radius=15)

        text = small_font.render(f"Напредок: {progress}/{progress_needed}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, bar_y - 20))
        surface.blit(text, text_rect)

    def draw_text_with_highlight(surface, text, target_letter, y_pos):
        # Create a text box background
        text_box = pygame.Rect(50, y_pos - 20, WIDTH - 100, HEIGHT // 2)
        pygame.draw.rect(surface, TEXT_BG_COLOR, text_box, border_radius=10)
        pygame.draw.rect(surface, TEXT_BORDER_COLOR, text_box, width=2, border_radius=10)

        # Split text into words and render with highlighted target letter
        words = text.split()
        x_pos = 70  # Start a bit more indented
        y = y_pos
        max_width = WIDTH - 140  # Adjusted for the larger text box
        line_height = 30  # Increased line height for better readability

        for word in words:
            word_surface = text_font.render(word + " ", True, (0, 0, 0))
            if x_pos + word_surface.get_width() > max_width:
                x_pos = 70
                y += line_height

            # Render each character separately to highlight the target letter
            current_x = x_pos
            for char in word:
                char_surface = text_font.render(char, True,
                                                (255, 0, 0) if normalize_mk(char) == normalize_mk(target_letter) else (
                                                0, 0, 0))
                surface.blit(char_surface, (current_x, y))
                current_x += char_surface.get_width()

            # Add space after word
            space_width = text_font.size(" ")[0]
            x_pos = current_x + space_width

    # Initialize first game
    start_game()

    # Create back button
    back_button = Button(20, 20, 100, 40, "НАЗАД", is_back_button=True)

    # Main game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        if show_feedback and current_time > feedback_timer:
            show_feedback = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif show_text_input:
                    handle_text_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle back button click
                if back_button.handle_event(event):
                    # pygame.quit()
                    from main.cpc import main  # Импорт на главната функција
                    main()  # Return to main menu
                    # return

                if game_complete:
                    restart_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
                    if restart_rect.collidepoint(event.pos):
                        reset_game()
                else:
                    if show_text_input:
                        input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 150, 200, 40)
                        if input_rect.collidepoint(event.pos):
                            input_active = True
                        else:
                            input_active = False

                        submit_rect = pygame.Rect(WIDTH // 2 + 70, HEIGHT - 150, 80, 40)
                        if submit_rect.collidepoint(event.pos):
                            check_text_input_answer()
                    else:
                        for button in image_buttons:
                            if button.handle_event(event):
                                check_selection(button)
            else:
                for button in image_buttons:
                    button.handle_event(event)
                back_button.handle_event(event)

        update_confetti()

        screen.fill(BG_COLOR)

        if confetti_active:
            screen.blit(celebration_bg, (0, 0))

        # Draw back button (always visible)
        back_button.draw(screen)

        if game_complete:
            text_surface = big_font.render("БРАВО! Ја завршивте играта! 🎉", True, (255, 215, 0))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(text_surface, text_rect)

            restart_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
            pygame.draw.rect(screen, (76, 175, 80), restart_rect, border_radius=15)
            restart_text = title_font.render("Нова игра", True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(center=restart_rect.center)
            screen.blit(restart_text, restart_text_rect)
        else:
            draw_progress_bar(screen)

            color = PROGRESS_COLOR
            if level == 2:
                color = LEVEL2_COLOR
            elif level == 3:
                color = LEVEL3_COLOR

            if level == 3:
                instruction_text = f"Колку пати се појавува буквата '{target_letter}' во текстот?"
                text_surface = title_font.render(instruction_text, True, color)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, 120))
                screen.blit(text_surface, text_rect)

                # Draw the text with highlighted letters
                draw_text_with_highlight(screen, game_text, target_letter, 160)

                # Input field
                input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 150, 200, 40)
                pygame.draw.rect(screen, (255, 255, 255), input_rect)
                pygame.draw.rect(screen, (0, 0, 0), input_rect, width=2)

                input_text = text_font.render(text_input, True, (0, 0, 0))
                screen.blit(input_text, (input_rect.x + 10, input_rect.y + 5))

                label_text = text_font.render("Одговор:", True, (0, 0, 0))
                screen.blit(label_text, (input_rect.x - 100, input_rect.y + 5))

                submit_rect = pygame.Rect(input_rect.right + 20, input_rect.y, 100, 40)
                pygame.draw.rect(screen, (76, 175, 80), submit_rect, border_radius=5)
                submit_text = text_font.render("Прати", True, (255, 255, 255))
                submit_text_rect = submit_text.get_rect(center=submit_rect.center)
                screen.blit(submit_text, submit_text_rect)

                if input_active and pygame.time.get_ticks() % 1000 < 500:
                    cursor_x = input_rect.x + 10 + text_font.size(text_input)[0]
                    pygame.draw.line(screen, (0, 0, 0), (cursor_x, input_rect.y + 5),
                                     (cursor_x, input_rect.y + 35), 2)
            else:
                text_surface = title_font.render(game_text, True, color)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, 120))
                screen.blit(text_surface, text_rect)

                for i, word in enumerate(displayed_words):
                    button = image_buttons[i]

                    img_rect = pygame.Rect(button.rect.x - 10, button.rect.y - 200, 180, 180)
                    screen.blit(loaded_images[word], img_rect)

                    pygame.draw.rect(screen, (135, 206, 235), img_rect.inflate(8, 8), width=4, border_radius=5)

                    button.draw(screen)

        if show_feedback:
            feedback_surface = feedback_font.render(feedback_text, True, feedback_color)
            feedback_rect = feedback_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            bg_rect = feedback_rect.inflate(20, 10)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect, width=2, border_radius=10)
            screen.blit(feedback_surface, feedback_rect)

        draw_confetti(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_macedonian_game()