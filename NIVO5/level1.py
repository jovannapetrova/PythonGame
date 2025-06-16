import pygame
import sys
import random
import math
import os
from threading import Thread

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
QUESTION_COUNT = 5


def start_emotion_game():
    # Screen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("🎭 Препознај ја емоцијата - Advanced Edition")

    # Colors
    colors = {
        'primary': (26, 26, 46),
        'secondary': (15, 52, 96),
        'accent': (233, 69, 96),
        'success': (39, 174, 96),
        'warning': (243, 156, 18),
        'error': (231, 76, 60),
        'text': (255, 255, 255),
        'glow': (78, 205, 196)
    }

    # Fonts
    title_font = pygame.font.Font(None, max(36, WIDTH // 40))
    question_font = pygame.font.Font(None, max(24, WIDTH // 50))
    score_font = pygame.font.Font(None, max(18, WIDTH // 70))
    button_font = pygame.font.Font(None, max(20, WIDTH // 60))
    feedback_font = pygame.font.Font(None, max(32, WIDTH // 45))

    # Game state
    current_question = 0
    score = 0
    emotions = {
        "Среќно": "../Pictures-Game5/среќен.png",
        "Тажно": "../Pictures-Game5/тажен.png",
        "Луто": "../Pictures-Game5/лут.png",
        "Исплашено": "../Pictures-Game5/исплашен.png",
        "Засрамено": "../Pictures-Game5/засрамен.png",
        "Возбудено": "../Pictures-Game5/возбуден.png",
    }
    current_correct_answer = ""
    option_buttons = []
    particles = []
    confetti_pieces = []

    # Animation states
    feedback_text = ""
    feedback_color = colors['text']
    feedback_pulse_time = 0
    show_feedback = False

    # Load images with error handling
    def load_image(path, size=None):
        try:
            image = pygame.image.load(path)
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except:
            # Create placeholder surface if image fails to load
            surf = pygame.Surface(size if size else (100, 100))
            surf.fill((100, 100, 100))
            return surf

    # Load emotion images
    emotion_images = {}
    for emotion, path in emotions.items():
        emotion_images[emotion] = load_image(path, (150, 150))

    # Particle system for background
    def create_particle():
        if len(particles) < 30:
            particle = {
                'x': random.randint(0, WIDTH),
                'y': HEIGHT,
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-2, -0.5),
                'size': random.randint(2, 6),
                'color': random.choice([colors['glow'], colors['accent'], colors['warning'], (155, 89, 182)]),
                'life': 255
            }
            particles.append(particle)

    def update_particles():
        for particle in particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 2
            if particle['y'] < -10 or particle['life'] <= 0:
                particles.remove(particle)

    def draw_particles(surface):
        for particle in particles:
            alpha = max(0, min(255, particle['life']))
            color = (*particle['color'], alpha)
            temp_surf = pygame.Surface((particle['size'], particle['size']))
            temp_surf.set_alpha(alpha)
            temp_surf.fill(particle['color'])
            surface.blit(temp_surf, (particle['x'], particle['y']))

    # Confetti system
    def create_confetti():
        confetti_pieces.clear()
        for _ in range(60):
            piece = {
                'x': WIDTH // 2,
                'y': HEIGHT // 2,
                'dx': random.uniform(-15, 15),
                'dy': random.uniform(-20, -5),
                'color': random.choice([(255, 107, 107), (78, 205, 196), (69, 183, 209),
                                      (243, 156, 18), (231, 76, 60), (155, 89, 182)]),
                'size': random.randint(6, 15),
                'life': 60
            }
            confetti_pieces.append(piece)

    def update_confetti():
        for piece in confetti_pieces[:]:
            piece['x'] += piece['dx']
            piece['y'] += piece['dy']
            piece['dy'] += 1  # Gravity
            piece['life'] -= 1
            if piece['life'] <= 0:
                confetti_pieces.remove(piece)

    def draw_confetti(surface):
        for piece in confetti_pieces:
            alpha = int(255 * (piece['life'] / 60))
            temp_surf = pygame.Surface((piece['size'], piece['size']))
            temp_surf.set_alpha(alpha)
            temp_surf.fill(piece['color'])
            surface.blit(temp_surf, (piece['x'], piece['y']))

    # UI Drawing functions
    def draw_rounded_rect(surface, rect, color, border_radius=0, border_color=None, border_width=0):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)
        if border_color and border_width > 0:
            pygame.draw.rect(surface, border_color, rect, border_width, border_radius=border_radius)

    def draw_progress_bar():
        """Draw progress bar"""
        bar_width = WIDTH // 3
        bar_height = 15
        bar_x = (WIDTH - bar_width) // 2
        bar_y = HEIGHT // 6

        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        draw_rounded_rect(screen, bg_rect, colors['secondary'], 7)

        # Progress
        progress = current_question / QUESTION_COUNT
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
            draw_rounded_rect(screen, progress_rect, colors['glow'], 7)

    def draw_button(rect, text, emotion, image, hover=False):
        """Draw a styled button with image and text"""
        # Button background with hover effect
        bg_color = colors['secondary'] if not hover else (colors['secondary'][0] + 20,
                                                        colors['secondary'][1] + 20,
                                                        colors['secondary'][2] + 20)
        border_color = colors['glow'] if not hover else colors['accent']

        draw_rounded_rect(screen, rect, bg_color, 20, border_color, 3)

        # Draw image
        img_rect = image.get_rect()
        img_rect.centerx = rect.centerx
        img_rect.centery = rect.centery - 20
        screen.blit(image, img_rect)

        # Draw text
        text_surf = button_font.render(text, True, colors['text'])
        text_rect = text_surf.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.bottom = rect.bottom - 15
        screen.blit(text_surf, text_rect)

        return rect

    def get_next_question():
        """Set up next question"""
        nonlocal current_correct_answer, option_buttons

        # Clear previous buttons
        option_buttons = []

        if current_question >= QUESTION_COUNT:
            return False  # Game over

        # Select correct answer
        all_emotions = list(emotions.keys())
        current_correct_answer = random.choice(all_emotions)

        # Create options (1 correct + 2 random)
        options = [current_correct_answer]
        while len(options) < 3:
            option = random.choice(all_emotions)
            if option not in options:
                options.append(option)
        random.shuffle(options)

        # Create button rectangles
        button_width = 200
        button_height = 250
        total_width = len(options) * button_width + (len(options) - 1) * 50
        start_x = (WIDTH - total_width) // 2
        button_y = HEIGHT // 2

        for i, emotion in enumerate(options):
            button_x = start_x + i * (button_width + 50)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            option_buttons.append({
                'rect': button_rect,
                'emotion': emotion,
                'image': emotion_images[emotion],
                'hover': False
            })

        return True

    def check_answer(selected_emotion):
        """Check if selected answer is correct"""
        nonlocal score, feedback_text, feedback_color, show_feedback, feedback_pulse_time

        if selected_emotion == current_correct_answer:
            score += 1
            feedback_text = "🎉 ОДЛИЧНО!"
            feedback_color = colors['success']
            create_confetti()
        else:
            feedback_text = "❌ ОБИДИ СЕ ПОВТОРНО!"
            feedback_color = colors['error']

        show_feedback = True
        feedback_pulse_time = pygame.time.get_ticks()

        return selected_emotion == current_correct_answer

    def draw_final_score():
        """Draw final score screen"""
        percentage = round((score / QUESTION_COUNT) * 100)

        # Determine message and color
        if percentage >= 80:
            message = "🏆 ФАНТАСТИЧНО!"
            color = colors['success']
        elif percentage >= 60:
            message = "👏 ДОБРО!"
            color = colors['warning']
        else:
            message = "💪 ОБИДИ СЕ ПОВТОРНО!"
            color = colors['error']

        # Draw message
        lines = [
            message,
            f"Точно одговори на {score} од {QUESTION_COUNT} прашања",
            f"({percentage}%)"
        ]

        y_offset = HEIGHT // 3
        for line in lines:
            text_surf = question_font.render(line, True, color)
            text_rect = text_surf.get_rect()
            text_rect.centerx = WIDTH // 2
            text_rect.y = y_offset
            screen.blit(text_surf, text_rect)
            y_offset += text_surf.get_height() + 10

        # Draw restart button
        button_width = 250
        button_height = 60
        restart_rect = pygame.Rect((WIDTH - button_width) // 2, y_offset + 40, button_width, button_height)
        draw_rounded_rect(screen, restart_rect, colors['accent'], 15)

        restart_text = button_font.render("🔄 ИГРАЈ ПОВТОРНО", True, colors['text'])
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = restart_rect.center
        screen.blit(restart_text, restart_text_rect)

        # Draw next level button
        next_rect = pygame.Rect((WIDTH - button_width) // 2, restart_rect.bottom + 20, button_width, button_height)
        draw_rounded_rect(screen, next_rect, colors['success'], 15)

        next_text = button_font.render("➡️ Следен Левел", True, colors['text'])
        next_text_rect = next_text.get_rect()
        next_text_rect.center = next_rect.center
        screen.blit(next_text, next_text_rect)

        # Draw back button
        back_rect = pygame.Rect(20, 20, 120, 50)
        draw_rounded_rect(screen, back_rect, colors['error'], 10)
        back_text = button_font.render("НАЗАД", True, colors['text'])
        back_text_rect = back_text.get_rect()
        back_text_rect.center = back_rect.center
        screen.blit(back_text, back_text_rect)

        return restart_rect, next_rect, back_rect

    def restart_game():
        """Restart the game"""
        nonlocal current_question, score, show_feedback
        current_question = 0
        score = 0
        show_feedback = False
        confetti_pieces.clear()
        get_next_question()

    def launch_level2():
        """Launch Level 2"""
        try:
            from NIVO5.level2 import start_level2
            start_level2()
        except ImportError:
            print("Level 2 not found!")

    def return_to_main():
        """Return to main menu"""
        try:
            from main.cpc import main
            #pygame.quit()
            main()
        except ImportError:
            print("Main module not found!")
            pygame.quit()

    # Initialize first question
    get_next_question()

    # Game loop
    clock = pygame.time.Clock()
    running = True
    game_over = False
    waiting_for_next = False
    next_question_time = 0

    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if game_over:
                        restart_rect, next_rect, back_rect = draw_final_score()  # Get button rects
                        if restart_rect.collidepoint(mouse_pos):
                            game_over = False
                            restart_game()
                        elif next_rect.collidepoint(mouse_pos):
                            launch_level2()
                            running = False
                        elif back_rect.collidepoint(mouse_pos):
                            return_to_main()
                            running = False
                    else:
                        # Check back button (shown during gameplay)
                        back_rect = pygame.Rect(20, 20, 120, 50)
                        if back_rect.collidepoint(mouse_pos):
                            return_to_main()
                            running = False
                        elif not waiting_for_next:
                            # Check answer buttons
                            for button in option_buttons:
                                if button['rect'].collidepoint(mouse_pos):
                                    check_answer(button['emotion'])
                                    waiting_for_next = True
                                    next_question_time = current_time + 3000  # 3 seconds delay
                                    break

        # Update hover states
        for button in option_buttons:
            button['hover'] = button['rect'].collidepoint(mouse_pos)

        # Handle next question timing
        if waiting_for_next and current_time >= next_question_time:
            waiting_for_next = False
            show_feedback = False
            current_question += 1

            if current_question >= QUESTION_COUNT:
                game_over = True
                if score >= int(QUESTION_COUNT * 0.8):  # 80% or higher
                    create_confetti()
            else:
                get_next_question()

        # Update animations
        if random.random() < 0.3:
            create_particle()
        update_particles()
        update_confetti()

        # Clear screen
        screen.fill(colors['primary'])

        # Draw background particles
        draw_particles(screen)

        if not game_over:
            # Draw back button during gameplay
            back_rect = pygame.Rect(20, 20, 120, 50)
            draw_rounded_rect(screen, back_rect, colors['error'], 10)
            back_text = button_font.render("НАЗАД", True, colors['text'])
            back_text_rect = back_text.get_rect()
            back_text_rect.center = back_rect.center
            screen.blit(back_text, back_text_rect)

            # Draw title
            title_text = title_font.render("🎭 ПРЕПОЗНАЈ ЈА ЕМОЦИЈАТА", True, colors['glow'])
            title_rect = title_text.get_rect()
            title_rect.centerx = WIDTH // 2
            title_rect.y = 30
            screen.blit(title_text, title_rect)

            # Draw score
            score_text = score_font.render(f"РЕЗУЛТАТ: {score} / {QUESTION_COUNT}", True, colors['text'])
            score_bg_rect = pygame.Rect(0, 0, score_text.get_width() + 20, score_text.get_height() + 10)
            score_bg_rect.centerx = WIDTH // 2
            score_bg_rect.y = title_rect.bottom + 10
            draw_rounded_rect(screen, score_bg_rect, colors['secondary'], 10)

            score_rect = score_text.get_rect()
            score_rect.center = score_bg_rect.center
            screen.blit(score_text, score_rect)

            # Draw progress bar
            draw_progress_bar()

            # Draw question
            if current_correct_answer:
                question_text = f"Кликни на лицето што е: {current_correct_answer}"
                question_surf = question_font.render(question_text, True, colors['text'])
                question_bg_rect = pygame.Rect(0, 0, question_surf.get_width() + 40, question_surf.get_height() + 20)
                question_bg_rect.centerx = WIDTH // 2
                question_bg_rect.y = HEIGHT // 3 - 40
                draw_rounded_rect(screen, question_bg_rect, colors['secondary'], 15, colors['glow'], 2)

                question_rect = question_surf.get_rect()
                question_rect.center = question_bg_rect.center
                screen.blit(question_surf, question_rect)

            # Draw option buttons
            for button in option_buttons:
                draw_button(button['rect'], button['emotion'], button['emotion'],
                           button['image'], button['hover'])

            # Draw feedback
            if show_feedback:
                # Pulse effect
                pulse_scale = 1.0 + 0.3 * math.sin((current_time - feedback_pulse_time) * 0.01)
                feedback_font_scaled = pygame.font.Font(None, int(feedback_font.get_height() * pulse_scale))

                feedback_surf = feedback_font_scaled.render(feedback_text, True, feedback_color)
                feedback_rect = feedback_surf.get_rect()
                feedback_rect.centerx = WIDTH // 2
                feedback_rect.y = HEIGHT - 150
                screen.blit(feedback_surf, feedback_rect)
        else:
            # Draw final score screen
            restart_rect, next_rect, back_rect = draw_final_score()

        # Draw confetti
        draw_confetti(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    start_emotion_game()