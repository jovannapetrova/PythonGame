# spatial_game.py
import math
import random
import pygame
import sys
import os


def start_spatial2_game():

    screen = pygame.display.get_surface()
    if screen is None:
        print("No display surface found!")
        return

    # Game state
    class GameState:
        def __init__(self):
            self.current_level = None
            self.current_step = 0
            self.total_steps = 0
            self.completed_levels = []
            self.instructions = []
            self.banana_pos = [0, 0]
            self.dragging = False
            self.banana_size = "small"
            self.level_selection = True
            self.game_active = True
            self.load_images()
            self.back_button_rect = None
            self.confetti_particles = []
            self.show_confetti = False
            self.confetti_timer = 0

        def load_images(self):
            try:

                self.monkey_img = pygame.image.load("../Pictures-Game2/monkey-no background.png")
                self.monkey_img = pygame.transform.scale(self.monkey_img, (350, 350))
                banana_img = pygame.image.load("../Pictures-Game2/banana.png")
                self.banana_img_small = pygame.transform.scale(banana_img, (100, 100))
                self.banana_img_large = pygame.transform.scale(banana_img, (120, 120))
                self.background = pygame.image.load("../Pictures-Game2/background.jpg")
                self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
            except:
                try:

                    self.monkey_img = pygame.image.load("../Pictures-Game2/monkey-no background.png")
                    self.monkey_img = pygame.transform.scale(self.monkey_img, (350, 350))
                    banana_img = pygame.image.load("../Pictures-Game2/banana.png")
                    self.banana_img_small = pygame.transform.scale(banana_img, (100, 100))
                    self.banana_img_large = pygame.transform.scale(banana_img, (120, 120))
                    self.background = pygame.image.load("background.jpg")
                    self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
                except:
                    # Create placeholders if images not found
                    self.monkey_img = pygame.Surface((350, 350))
                    self.monkey_img.fill((139, 69, 19))  # Brown
                    self.banana_img_small = pygame.Surface((100, 100))
                    self.banana_img_small.fill((255, 215, 0))  # Gold
                    self.banana_img_large = pygame.Surface((120, 120))
                    self.banana_img_large.fill((255, 215, 0))
                    self.background = pygame.Surface((screen.get_width(), screen.get_height()))
                    self.background.fill((240, 248, 255))  # Light blue

    # Initialize game state
    game_state = GameState()
    game_state.banana_pos = [screen.get_width() // 2, screen.get_height() - 120]


    try:
        font_title = pygame.font.Font(None, 48)
        font_large = pygame.font.Font(None, 36)
        font_medium = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 24)
    except:
        font_title = pygame.font.Font(None, 48)
        font_large = pygame.font.Font(None, 36)
        font_medium = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 24)

    # Enhanced colors for better visibility
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)  # Steel blue
    GREEN = (34, 139, 34)  # Forest green
    YELLOW = (255, 215, 0)  # Gold
    RED = (220, 20, 60)  # Crimson
    PURPLE = (138, 43, 226)  # Blue violet
    LIGHT_BLUE = (173, 216, 230)  # Light blue
    DARK_GREEN = (0, 100, 0)  # Dark green
    SHADOW_COLOR = (128, 128, 128, 128)  # Semi-transparent gray

    def draw_text_with_shadow(text, font, color, x, y, shadow_offset=2):

        # Create shadow
        shadow_text = font.render(text, True, (0, 0, 0))
        screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))


        main_text = font.render(text, True, color)
        screen.blit(main_text, (x, y))

        return main_text.get_rect(x=x, y=y)

    def draw_text_with_background(text, font, text_color, bg_color, x, y, padding=10, border_radius=10):

        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()


        bg_rect = pygame.Rect(x - padding, y - padding,
                              text_rect.width + 2 * padding,
                              text_rect.height + 2 * padding)


        pygame.draw.rect(screen, bg_color, bg_rect, border_radius=border_radius)
        pygame.draw.rect(screen, BLACK, bg_rect, 3, border_radius=border_radius)


        screen.blit(text_surface, (x, y))

        return bg_rect

    def draw_back_button():
        """Draws the universal 'Back to Main Menu' button with enhanced styling."""
        game_state.back_button_rect = pygame.Rect(40, 40, 220, 60)


        pygame.draw.rect(screen, BLUE, game_state.back_button_rect, border_radius=15)
        pygame.draw.rect(screen, (50, 100, 150), game_state.back_button_rect, 3, border_radius=15)


        back_button_text = font_medium.render(" Назад кон мени", True, WHITE)
        text_x = game_state.back_button_rect.centerx - back_button_text.get_width() // 2
        text_y = game_state.back_button_rect.centery - back_button_text.get_height() // 2
        screen.blit(back_button_text, (text_x, text_y))

    def handle_back_button_click(pos):
        """Handles back button click."""
        if game_state.back_button_rect and game_state.back_button_rect.collidepoint(pos):
            from main.cpc import main
            main()
            return True
        return False

    # def create_confetti():
    #     """Create confetti particles with improved physics"""
    #     game_state.confetti_particles = []
    #     colors = [
    #         (255, 99, 71), (255, 215, 0), (50, 205, 50), (30, 144, 255),
    #         (255, 20, 147), (255, 165, 0), (138, 43, 226), (0, 255, 255),
    #         (255, 192, 203), (124, 252, 0), (255, 69, 0), (75, 0, 130)
    #     ]
    #
    #     # Create particles from multiple points for better effect
    #     spawn_points = [
    #         (screen.get_width() // 4, 100),
    #         (screen.get_width() // 2, 100),
    #         (3 * screen.get_width() // 4, 100)
    #     ]
    #
    #     for spawn_x, spawn_y in spawn_points:
    #         for _ in range(40):  # 40 particles per spawn point
    #             angle = random.uniform(0, 2 * math.pi)
    #             speed = random.uniform(3, 8)
    #             particle = {
    #                 'x': float(spawn_x + random.uniform(-50, 50)),
    #                 'y': float(spawn_y),
    #                 'dx': math.cos(angle) * speed,
    #                 'dy': math.sin(angle) * speed - random.uniform(2, 5),  # Initial upward velocity
    #                 'size': random.randint(6, 12),
    #                 'color': random.choice(colors),
    #                 'life': random.randint(60, 120),  # Longer life
    #                 'rotation': random.uniform(0, 360),
    #                 'rotation_speed': random.uniform(-10, 10)
    #             }
    #             game_state.confetti_particles.append(particle)
    #
    #     game_state.show_confetti = True
    #     game_state.confetti_timer = 180  # 3 seconds at 60 FPS
    #
    # def update_confetti():
    #     """Update confetti physics with improved animation"""
    #     if not game_state.show_confetti:
    #         return
    #
    #     game_state.confetti_timer -= 1
    #     if game_state.confetti_timer <= 0:
    #         game_state.show_confetti = False
    #         game_state.confetti_particles = []
    #         return
    #
    #     for particle in game_state.confetti_particles[:]:
    #         # Update physics
    #         particle['x'] += particle['dx']
    #         particle['y'] += particle['dy']
    #         particle['dy'] += 0.15  # Gravity
    #         particle['dx'] *= 0.99  # Air resistance
    #         particle['rotation'] += particle['rotation_speed']
    #         particle['life'] -= 1
    #
    #         # Remove particles that are off screen or dead
    #         if (particle['life'] <= 0 or
    #                 particle['x'] < -20 or particle['x'] > screen.get_width() + 20 or
    #                 particle['y'] > screen.get_height() + 20):
    #             try:
    #                 game_state.confetti_particles.remove(particle)
    #             except ValueError:
    #                 pass  # Particle already removed
    #
    # def draw_confetti():
    #     """Draw confetti with rotation and fade effect"""
    #     if not game_state.show_confetti:
    #         return
    #
    #     for particle in game_state.confetti_particles:
    #         # Calculate alpha based on remaining life
    #         alpha = min(255, max(0, int(255 * particle['life'] / 60)))
    #
    #         # Create a surface for the particle with alpha
    #         particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
    #         color_with_alpha = (*particle['color'], alpha)
    #
    #         # Draw rotated rectangle
    #         points = []
    #         half_size = particle['size'] // 2
    #         for dx, dy in [(-half_size, -half_size), (half_size, -half_size),
    #                        (half_size, half_size), (-half_size, half_size)]:
    #             # Rotate point
    #             angle_rad = math.radians(particle['rotation'])
    #             rotated_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    #             rotated_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    #             points.append((particle['x'] + rotated_x, particle['y'] + rotated_y))
    #
    #         # Draw the particle
    #         try:
    #             pygame.draw.polygon(screen, particle['color'], points)
    #         except:
    #             # Fallback to simple circle if polygon fails
    #             pygame.draw.circle(screen, particle['color'],
    #                                (int(particle['x']), int(particle['y'])),
    #                                particle['size'] // 2)

    def setup_easy_level():
        game_state.current_level = "easy"
        game_state.current_step = 0
        game_state.total_steps = 2
        game_state.instructions = [
            " Земи ја бананата и стави ја во ЛЕВАТА рака на мајмунот",
            " Сега стави ја бананата во ДЕСНАТА рака на мајмунот"
        ]
        game_state.banana_pos = [screen.get_width() // 2, screen.get_height() - 120]
        game_state.level_selection = False

    def setup_medium_level():
        game_state.current_level = "medium"
        game_state.current_step = 0
        game_state.total_steps = 2
        game_state.instructions = [
            " Стави ја бананата во ЛЕВАТА рака на ЛЕВИОТ мајмун",
            " Сега стави ја бананата во ДЕСНАТА рака на ДЕСНИОТ мајмун"
        ]
        game_state.banana_pos = [screen.get_width() // 2, screen.get_height() - 120]
        game_state.level_selection = False

    def setup_hard_level():
        game_state.current_level = "hard"
        game_state.current_step = 0
        game_state.total_steps = 3
        game_state.instructions = [
            " Стави ја бананата во ЛЕВАТА рака на ВТОРИОТ мајмун (средниот)",
            " Сега стави ја бананата во ДЕСНАТА рака на ТРЕТИОТ мајмун (десниот)",
            " Конечно, стави ја бананата во ЛЕВАТА рака на ПРВИОТ мајмун (левиот)"
        ]
        game_state.banana_pos = [screen.get_width() // 2, screen.get_height() - 120]
        game_state.level_selection = False

    def start_location_game():
        """Start the location game (level 2)"""
        from NIVO2.level2 import LocationGame
        location_game = LocationGame(screen)
        result = location_game.run()

        if result == "menu":
            return "level_select"
        return result

    def check_easy_drop(pos):
        monkey_x = screen.get_width() // 2
        monkey_y = screen.get_height() // 2 + 50

        if game_state.current_step == 0:  # Left hand
            zone = pygame.Rect(monkey_x - 200, monkey_y - 40, 100, 80)
        else:  # Right hand
            zone = pygame.Rect(monkey_x + 100, monkey_y - 40, 100, 80)

        return zone.collidepoint(pos)

    def check_medium_drop(pos):
        monkey1_x = screen.get_width() // 3
        monkey2_x = (screen.get_width() // 3) * 2
        monkey_y = screen.get_height() // 2 + 50

        if game_state.current_step == 0:  # Left hand of left monkey
            zone = pygame.Rect(monkey1_x - 200, monkey_y - 40, 100, 80)
        else:  # Right hand of right monkey
            zone = pygame.Rect(monkey2_x + 100, monkey_y - 40, 100, 80)

        return zone.collidepoint(pos)

    def check_hard_drop(pos):
        monkey1_x = screen.get_width() // 4
        monkey2_x = screen.get_width() // 2
        monkey3_x = (screen.get_width() // 4) * 3
        monkey_y = screen.get_height() // 2 + 50

        if game_state.current_step == 0:  # Left hand of middle monkey
            zone = pygame.Rect(monkey2_x - 200, monkey_y - 40, 100, 80)
        elif game_state.current_step == 1:  # Right hand of right monkey
            zone = pygame.Rect(monkey3_x + 100, monkey_y - 40, 100, 80)
        else:  # Left hand of left monkey
            zone = pygame.Rect(monkey1_x - 200, monkey_y - 40, 100, 80)

        return zone.collidepoint(pos)

    def show_message(text, color=BLUE, duration=2500):
        """Show enhanced message with better styling"""

        message_y = 200

        # Draw semi-transparent background
        overlay = pygame.Surface((screen.get_width(), 120), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, message_y - 20))

        # Draw message background
        msg_rect = draw_text_with_background(
            text, font_large, WHITE, color,
            screen.get_width() // 2 - font_large.size(text)[0] // 2,
            message_y,
            padding=20, border_radius=15
        )

        # Add sparkle effect for success messages
        if color == GREEN:
            for _ in range(10):
                star_x = random.randint(msg_rect.left - 50, msg_rect.right + 50)
                star_y = random.randint(msg_rect.top - 30, msg_rect.bottom + 30)
                pygame.draw.circle(screen, YELLOW, (star_x, star_y), 3)

        pygame.display.flip()
        pygame.time.delay(duration)

    def show_level_selection():
        """Enhanced level selection screen"""
        game_state.level_selection = True
        game_state.current_level = None

        # Clear screen
        screen.blit(game_state.background, (0, 0))

        # Enhanced title with shadow
        title_text = " Просторен однос: Избери ниво "
        title_x = screen.get_width() // 2 - font_title.size(title_text)[0] // 2
        draw_text_with_shadow(title_text, font_title, DARK_GREEN, title_x, 80, 3)

        # Level buttons with enhanced styling
        button_width = 400
        button_height = 70
        button_x = screen.get_width() // 2 - button_width // 2

        # Easy level button
        easy_rect = pygame.Rect(button_x, 180, button_width, button_height)
        pygame.draw.rect(screen, GREEN, easy_rect, border_radius=15)
        pygame.draw.rect(screen, DARK_GREEN, easy_rect, 4, border_radius=15)
        easy_text = " ЛЕСНО (1 мајмун, 2 чекори)"
        text_x = easy_rect.centerx - font_medium.size(easy_text)[0] // 2
        text_y = easy_rect.centery - font_medium.size(easy_text)[1] // 2
        screen.blit(font_medium.render(easy_text, True, WHITE), (text_x, text_y))

        # Medium level button
        medium_rect = pygame.Rect(button_x, 270, button_width, button_height)
        pygame.draw.rect(screen, YELLOW, medium_rect, border_radius=15)
        pygame.draw.rect(screen, (200, 150, 0), medium_rect, 4, border_radius=15)
        medium_text = " СРЕДНО (2 мајмуни, 2 чекори)"
        text_x = medium_rect.centerx - font_medium.size(medium_text)[0] // 2
        text_y = medium_rect.centery - font_medium.size(medium_text)[1] // 2
        screen.blit(font_medium.render(medium_text, True, BLACK), (text_x, text_y))

        # Hard level button
        hard_rect = pygame.Rect(button_x, 360, button_width, button_height)
        pygame.draw.rect(screen, RED, hard_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 0, 0), hard_rect, 4, border_radius=15)
        hard_text = " ТЕШКО (3 мајмуни, 3 чекори)"
        text_x = hard_rect.centerx - font_medium.size(hard_text)[0] // 2
        text_y = hard_rect.centery - font_medium.size(hard_text)[1] // 2
        screen.blit(font_medium.render(hard_text, True, WHITE), (text_x, text_y))

        # Location Game button
        location_rect = pygame.Rect(button_x, 450, button_width, button_height)
        pygame.draw.rect(screen, PURPLE, location_rect, border_radius=15)
        pygame.draw.rect(screen, (100, 0, 150), location_rect, 4, border_radius=15)
        location_text = " ИГРА СО ЛОКАЦИИ (Ниво 2)"
        text_x = location_rect.centerx - font_medium.size(location_text)[0] // 2
        text_y = location_rect.centery - font_medium.size(location_text)[1] // 2
        screen.blit(font_medium.render(location_text, True, WHITE), (text_x, text_y))

        # Enhanced back button
        back_rect = pygame.Rect(40, screen.get_height() - 90, 250, 60)
        pygame.draw.rect(screen, BLUE, back_rect, border_radius=15)
        pygame.draw.rect(screen, (50, 100, 150), back_rect, 4, border_radius=15)
        back_text = "Назад кон главно мени"
        text_x = back_rect.centerx - font_medium.size(back_text)[0] // 2
        text_y = back_rect.centery - font_medium.size(back_text)[1] // 2
        screen.blit(font_medium.render(back_text, True, WHITE), (text_x, text_y))

        pygame.display.flip()
        return easy_rect, medium_rect, hard_rect, location_rect, back_rect

    def draw_level():
        """Enhanced level drawing"""
        level_translations = {
            "easy": " ЛЕСНО",
            "medium": " СРЕДНО",
            "hard": " ТЕШКО"
        }

        # Clear screen
        screen.blit(game_state.background, (0, 0))

        draw_back_button()

        # Enhanced level title
        level_name = level_translations.get(game_state.current_level, game_state.current_level.upper())
        level_text = f"Ниво: {level_name}"
        draw_text_with_shadow(level_text, font_large, DARK_GREEN, 300, 50, 2)

        # Enhanced instruction with background
        instruction = game_state.instructions[game_state.current_step]
        instr_x = screen.get_width() // 2 - font_large.size(instruction)[0] // 2
        draw_text_with_background(instruction, font_large, WHITE, LIGHT_BLUE, instr_x, 120, 15, 10)

        # Progress indicator
        progress_text = f"Чекор {game_state.current_step + 1} од {game_state.total_steps}"
        progress_x = screen.get_width() - 300
        draw_text_with_background(progress_text, font_medium, BLACK, YELLOW, progress_x, 50, 10, 8)

        # Draw monkey(s)
        if game_state.current_level == "easy":
            monkey_x = screen.get_width() // 2
            monkey_y = screen.get_height() // 2 + 50
            screen.blit(game_state.monkey_img, (monkey_x - game_state.monkey_img.get_width() // 2,
                                                monkey_y - game_state.monkey_img.get_height() // 2))
        elif game_state.current_level == "medium":
            monkey1_x = screen.get_width() // 3
            monkey2_x = (screen.get_width() // 3) * 2
            monkey_y = screen.get_height() // 2 + 50
            screen.blit(game_state.monkey_img, (monkey1_x - game_state.monkey_img.get_width() // 2,
                                                monkey_y - game_state.monkey_img.get_height() // 2))
            screen.blit(game_state.monkey_img, (monkey2_x - game_state.monkey_img.get_width() // 2,
                                                monkey_y - game_state.monkey_img.get_height() // 2))
        elif game_state.current_level == "hard":
            monkey1_x = screen.get_width() // 4
            monkey2_x = screen.get_width() // 2
            monkey3_x = (screen.get_width() // 4) * 3
            monkey_y = screen.get_height() // 2 + 50
            screen.blit(game_state.monkey_img, (monkey1_x - game_state.monkey_img.get_width() // 2,
                                                monkey_y - game_state.monkey_img.get_height() // 2))
            screen.blit(game_state.monkey_img, (monkey2_x - game_state.monkey_img.get_width() // 2,
                                                monkey_y - game_state.monkey_img.get_height() // 2))
            screen.blit(game_state.monkey_img, (monkey3_x - game_state.monkey_img.get_width() // 2,
                                                monkey_y - game_state.monkey_img.get_height() // 2))

        # Draw banana with glow effect when dragging
        banana_img = game_state.banana_img_small if game_state.banana_size == "small" else game_state.banana_img_large

        if game_state.dragging:
            # Add glow effect
            glow_surface = pygame.Surface((banana_img.get_width() + 20, banana_img.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 0, 50),
                               (glow_surface.get_width() // 2, glow_surface.get_height() // 2),
                               max(banana_img.get_width(), banana_img.get_height()) // 2 + 10)
            screen.blit(glow_surface, (game_state.banana_pos[0] - glow_surface.get_width() // 2,
                                       game_state.banana_pos[1] - glow_surface.get_height() // 2))

        screen.blit(banana_img, (game_state.banana_pos[0] - banana_img.get_width() // 2,
                                 game_state.banana_pos[1] - banana_img.get_height() // 2))

        # Enhanced back to levels button
        back_rect = pygame.Rect(40, screen.get_height() - 90, 250, 60)
        pygame.draw.rect(screen, BLUE, back_rect, border_radius=15)
        pygame.draw.rect(screen, (50, 100, 150), back_rect, 4, border_radius=15)
        back_text = " Назад кон нивоа"
        text_x = back_rect.centerx - font_medium.size(back_text)[0] // 2
        text_y = back_rect.centery - font_medium.size(back_text)[1] // 2
        screen.blit(font_medium.render(back_text, True, WHITE), (text_x, text_y))

        # Draw confetti
       # draw_confetti()
        pygame.display.flip()
        return back_rect

    # Main game loop
    clock = pygame.time.Clock()
    easy_rect, medium_rect, hard_rect, location_rect, back_rect = show_level_selection()

    while game_state.game_active:
        #update_confetti()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.game_active = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.game_active = False
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if handle_back_button_click(pos):
                    return

                if game_state.level_selection:
                    # Level selection screen
                    if easy_rect.collidepoint(pos):
                        setup_easy_level()
                        back_rect = draw_level()
                    elif medium_rect.collidepoint(pos):
                        setup_medium_level()
                        back_rect = draw_level()
                    elif hard_rect.collidepoint(pos):
                        setup_hard_level()
                        back_rect = draw_level()
                    elif location_rect.collidepoint(pos):
                        result = start_location_game()
                        if result == "level_select":
                            easy_rect, medium_rect, hard_rect, location_rect, back_rect = show_level_selection()
                        elif result == "quit":
                            game_state.game_active = False
                            return
                    elif back_rect.collidepoint(pos):
                        from main.cpc import main
                        main()

                else:
                    # Game level screen
                    if back_rect.collidepoint(pos):
                        easy_rect, medium_rect, hard_rect, location_rect, back_rect = show_level_selection()
                    else:
                        # Check if clicked on banana
                        banana_img = game_state.banana_img_small if game_state.banana_size == "small" else game_state.banana_img_large
                        banana_rect = pygame.Rect(
                            game_state.banana_pos[0] - banana_img.get_width() // 2,
                            game_state.banana_pos[1] - banana_img.get_height() // 2,
                            banana_img.get_width(),
                            banana_img.get_height()
                        )
                        if banana_rect.collidepoint(pos):
                            game_state.dragging = True
                            game_state.banana_size = "large"
                            draw_level()

            if event.type == pygame.MOUSEBUTTONUP and game_state.dragging:
                game_state.dragging = False
                game_state.banana_size = "small"
                pos = pygame.mouse.get_pos()

                # Check if dropped in correct zone
                correct_drop = False
                if game_state.current_level == "easy":
                    correct_drop = check_easy_drop(pos)
                elif game_state.current_level == "medium":
                    correct_drop = check_medium_drop(pos)
                elif game_state.current_level == "hard":
                    correct_drop = check_hard_drop(pos)

                if correct_drop:
                    #create_confetti()
                    game_state.current_step += 1
                    if game_state.current_step >= game_state.total_steps:
                        # Level completed
                        show_message("Браво! Го завршивте нивото!", GREEN)
                        game_state.completed_levels.append(game_state.current_level)
                        easy_rect, medium_rect, hard_rect, location_rect, back_rect = show_level_selection()
                    else:
                        show_message("Точно! Продолжете со следниот чекор.", GREEN)
                        game_state.banana_pos = [screen.get_width() // 2, screen.get_height() - 120]
                        back_rect = draw_level()
                else:
                    show_message("Погрешно место. Обидете се повторно.", RED)
                    game_state.banana_pos = [screen.get_width() // 2, screen.get_height() - 120]
                    back_rect = draw_level()

            if event.type == pygame.MOUSEMOTION and game_state.dragging:
                game_state.banana_pos = list(event.pos)
                draw_level()

        clock.tick(60)

    return


# For testing purposes - can be removed
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Spatial Game Test")
    start_spatial2_game()
    pygame.quit()