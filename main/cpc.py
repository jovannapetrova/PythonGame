import pygame
import sys
import random
import math
from NIVO1.level1 import start_motorika_game
from NIVO2.game7 import start_spatial_game
from NIVO3.level1 import start_kolicina_game
from NIVO5.level1 import start_emotion_game
from NIVO6.level1 import start_colorsAndshapes_game
from NIVO7.level1 import start_social_skills_game
from NIVO8.level1 import start_drawing_game
from NIVO4.game4 import run_macedonian_game

pygame.init()

BACKGROUND_COLOR = (255, 255, 255)

# Enhanced button colors with gradients and better contrast
BUTTON_COLORS = [
    (255, 102, 102),  # Soft red
    (102, 255, 102),  # Soft green
    (102, 153, 255),  # Soft blue
    (255, 204, 102),  # Soft orange
    (255, 102, 255),  # Soft magenta
    (102, 255, 255),  # Soft cyan
    (255, 178, 102),  # Peach
    (204, 153, 255)  # Soft purple
]

# Darker colors for button borders and shadows
BUTTON_BORDER_COLORS = [
    (204, 51, 51),
    (51, 204, 51),
    (51, 102, 204),
    (204, 153, 51),
    (204, 51, 204),
    (51, 204, 204),
    (204, 127, 51),
    (153, 102, 204)
]

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Игра за Деца")

background_image = pygame.image.load("mainbackground.png")
background_image = pygame.transform.scale(background_image, screen.get_size())

game_parts = [
    "Моторика",
    "Просторен однос",
    "Количина",
    "Фонолошка свесност",
    "Емоционална интеракција",
    "Бои и форми",
    "Социјални вештини",
    "Креативност"
]


screen_width, screen_height = screen.get_size()
EXIT_BUTTON_SIZE = (50, 50)
EXIT_BUTTON_POSITION = (screen_width - EXIT_BUTTON_SIZE[0] - 20, 20)



# Improved button layout - two circles or flower pattern
def calculate_button_positions():
    positions = []




    if len(game_parts) == 8:
        # Create a flower-like pattern with one center and 7 around
        center_x, center_y = screen_width // 2, screen_height // 2 - 50

        # Center button
        positions.append((center_x - 140, center_y - 50))

        # Surrounding buttons in a circle
        radius = 280
        for i in range(1, len(game_parts)):
            angle = 2 * math.pi * (i - 1) / 7 - math.pi / 2  # Start from top
            x = center_x + int(radius * math.cos(angle)) - 140
            y = center_y + int(radius * math.sin(angle)) - 50
            positions.append((x, y))
    else:
        # Fallback to circular arrangement
        radius = 350
        center_x, center_y = screen_width // 2, screen_height // 2 - 50
        for i in range(len(game_parts)):
            angle = 2 * math.pi * i / len(game_parts) - math.pi / 2
            x = center_x + int(radius * math.cos(angle)) - 140
            y = center_y + int(radius * math.sin(angle)) - 50
            positions.append((x, y))

    return positions


button_positions = calculate_button_positions()

# Manually move "Бои и форми" (index 5) further down-right
if len(button_positions) > 5:
    x, y = button_positions[5]
    button_positions[5] = (x -100, y )  # adjust values to space it more


# Move "Фонолошка свесност" (index 3) slightly right
if len(button_positions) > 3:
    x, y = button_positions[3]
    button_positions[3] = (x + 60, y)

# Move "Социјални вештини" (index 6) slightly left
if len(button_positions) > 6:
    x, y = button_positions[6]
    button_positions[6] = (x - 60, y)

BACK_BUTTON_POSITION = (screen_width // 2 - 100, screen_height - 120)

# Enhanced fonts
font_large = pygame.font.Font(pygame.font.match_font("arial"), 24)
font_medium = pygame.font.Font(pygame.font.match_font("arial"), 20)


def draw_enhanced_button(surface, rect, color, border_color, text, font, hover=False):
    """Draw a button with shadow, gradient effect, and better styling"""
    x, y, width, height = rect

    # Draw shadow
    shadow_offset = 4
    shadow_rect = (x , y , width, height)
    pygame.draw.rect(surface, (0, 0, 0, 50), shadow_rect, border_radius=15)

    # Draw button background with slight gradient effect
    if hover:
        # Lighter color when hovered
        button_color = tuple(min(255, c + 30) for c in color)
    else:
        button_color = color

    # Main button
    pygame.draw.rect(surface, button_color, (x, y, width, height), border_radius=15)

    # Button border
    pygame.draw.rect(surface, border_color, (x, y, width, height), width=3, border_radius=15)

    # Inner highlight for 3D effect
    highlight_color = tuple(min(255, c + 40) for c in button_color)
    pygame.draw.rect(surface, highlight_color, (x + 3, y + 3, width - 6, 8), border_radius=10)

    # Text with shadow
    text_surface = font.render(text, True, (0, 0, 0))


    # Center the text
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    #shadow_rect = text_shadow.get_rect(center=(x + width // 2 + 2, y + height // 2 + 2))

    # Draw text shadow first, then main text

    surface.blit(text_surface, text_rect)


def draw_buttons():
    """Draw all main menu buttons with enhanced styling"""
    for i, position in enumerate(button_positions):
        color = BUTTON_COLORS[i % len(BUTTON_COLORS)]
        border_color = BUTTON_BORDER_COLORS[i % len(BUTTON_BORDER_COLORS)]

        # Use smaller font for longer text
        text = game_parts[i]
        if len(text) > 12:
            font_to_use = font_medium
        else:
            font_to_use = font_large

        draw_enhanced_button(
            screen,
            (*position, 280, 100),
            color,
            border_color,
            text,
            font_to_use
        )

    # Enhanced back button
    draw_enhanced_button(
        screen,
        (*BACK_BUTTON_POSITION, 200, 50),
        (220, 220, 220),
        (150, 150, 150),
        "Назад",
        font_large
    )

def draw_exit_button(surface):
        x, y = EXIT_BUTTON_POSITION
        width, height = EXIT_BUTTON_SIZE

        # Background
        pygame.draw.rect(surface, (255, 80, 80), (x, y, width, height), border_radius=10)

        # Border
        pygame.draw.rect(surface, (180, 0, 0), (x, y, width, height), width=3, border_radius=10)

        # Draw "X"
        font_exit = pygame.font.Font(pygame.font.match_font("arial"), 32)
        text_surface = font_exit.render("X", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(text_surface, text_rect)


def is_button_clicked(x, y, mouse_pos, width=280, height=100):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height


def is_back_button_clicked(mouse_pos):
    return BACK_BUTTON_POSITION[0] <= mouse_pos[0] <= BACK_BUTTON_POSITION[0] + 200 and BACK_BUTTON_POSITION[1] <= \
        mouse_pos[1] <= BACK_BUTTON_POSITION[1] + 50


def draw_emotion_images():
    images = ['angry.png', 'happy.png', 'sad.png', 'surprised.png']
    image_surfaces = []
    target_width = 250
    target_height = 250

    for image in images:
        try:
            image_surface = pygame.image.load(image)
            image_surface = pygame.transform.scale(image_surface, (target_width, target_height))
            image_surfaces.append(image_surface)
        except pygame.error as e:
            print(f"Грешка при учитавање на сликата {image}: {e}")
            # Create placeholder colored rectangle
            placeholder = pygame.Surface((target_width, target_height))
            placeholder.fill((200, 200, 200))
            image_surfaces.append(placeholder)

    return image_surfaces


RANDOM_BUTTON_POSITION = (screen_width // 2 - 125, screen_height // 2 + 120)


def draw_emotion_interaction_window():
    # Gradient background
    for y in range(screen_height):
        color_ratio = y / screen_height
        r = int(240 + (255 - 240) * color_ratio)
        g = int(248 + (255 - 248) * color_ratio)
        b = int(255)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen_width, y))

    image_surfaces = draw_emotion_images()

    # Title
    title_font = pygame.font.Font(pygame.font.match_font("arial"), 36)
    title_text = title_font.render("Емоционална интеракција", True, (50, 50, 100))
    title_rect = title_text.get_rect(center=(screen_width // 2, 80))
    screen.blit(title_text, title_rect)

    # Arrange emotion images in a 2x2 grid
    target_width = 250
    target_height = 250
    spacing = 50
    start_x = (screen_width - (2 * target_width + spacing)) // 2
    start_y = 150

    for i, image_surface in enumerate(image_surfaces):
        if image_surface:
            row = i // 2
            col = i % 2
            x = start_x + col * (target_width + spacing)
            y = start_y + row * (target_height + spacing)

            # Draw image with border
            border_rect = (x - 5, y - 5, target_width + 10, target_height + 10)
            pygame.draw.rect(screen, (100, 100, 100), border_rect, border_radius=15)

            image_rect = (x, y, target_width, target_height)
            pygame.draw.rect(screen, (255, 255, 255), image_rect, border_radius=10)

            image_center = (x + target_width // 2, y + target_height // 2)
            img_rect = image_surface.get_rect(center=image_center)
            screen.blit(image_surface, img_rect)

    # Enhanced random button
    draw_enhanced_button(
        screen,
        (*RANDOM_BUTTON_POSITION, 250, 60),
        (102, 255, 178),
        (51, 204, 127),
        "Генерирај емоција",
        font_large
    )

    # Enhanced back button
    draw_enhanced_button(
        screen,
        (*BACK_BUTTON_POSITION, 200, 50),
        (220, 220, 220),
        (150, 150, 150),
        "Назад",
        font_large
    )

    return image_surfaces


def display_random_emotion(image_surfaces):
    # Gradient background
    for y in range(screen_height):
        color_ratio = y / screen_height
        r = int(255 - 50 * color_ratio)
        g = int(255 - 30 * color_ratio)
        b = int(255)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen_width, y))

    random_emotion = random.choice([img for img in image_surfaces if img is not None])
    if random_emotion:
        # Draw image with decorative border
        img_size = 300
        x = (screen_width - img_size) // 2
        y = (screen_height - img_size) // 2 - 80

        # Decorative border
        border_size = img_size + 20
        border_x = x - 10
        border_y = y - 10

        pygame.draw.rect(screen, (100, 150, 200), (border_x, border_y, border_size, border_size), border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, img_size, img_size), border_radius=15)

        # Scale and center the image
        scaled_emotion = pygame.transform.scale(random_emotion, (img_size - 20, img_size - 20))
        image_rect = scaled_emotion.get_rect(center=(x + img_size // 2, y + img_size // 2))
        screen.blit(scaled_emotion, image_rect)

        # Question text with background
        question_font = pygame.font.Font(pygame.font.match_font("arial"), 32)
        text_surface = question_font.render("Која е оваа емоција?", True, (50, 50, 100))
        text_rect = text_surface.get_rect(center=(screen_width // 2, y + img_size + 80))

        # Text background
        text_bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(screen, (255, 255, 255, 200), text_bg_rect, border_radius=15)
        pygame.draw.rect(screen, (100, 150, 200), text_bg_rect, width=3, border_radius=15)

        screen.blit(text_surface, text_rect)

    # Enhanced back button
    draw_enhanced_button(
        screen,
        (*BACK_BUTTON_POSITION, 200, 50),
        (220, 220, 220),
        (150, 150, 150),
        "Назад",
        font_large
    )


def main():
    active_window = None
    image_surfaces = []
    random_emotion_display = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if Exit button clicked
                if EXIT_BUTTON_POSITION[0] <= mouse_pos[0] <= EXIT_BUTTON_POSITION[0] + EXIT_BUTTON_SIZE[0] and \
                        EXIT_BUTTON_POSITION[1] <= mouse_pos[1] <= EXIT_BUTTON_POSITION[1] + EXIT_BUTTON_SIZE[1]:
                    pygame.quit()
                    sys.exit()

                if is_back_button_clicked(mouse_pos):
                    active_window = None
                    random_emotion_display = False

                if active_window == 4 and is_button_clicked(RANDOM_BUTTON_POSITION[0], RANDOM_BUTTON_POSITION[1],
                                                            mouse_pos, 250, 60):
                    random_emotion_display = True

                for i, position in enumerate(button_positions):
                    if is_button_clicked(position[0], position[1], mouse_pos):
                        active_window = i
                        if i == 0:
                            start_motorika_game()
                        elif i == 1:
                            start_spatial_game()
                        elif i == 2:
                            start_kolicina_game()
                        elif i == 5:
                             start_colorsAndshapes_game()
                        elif i==7:
                            start_drawing_game()
                        elif i==6:
                            start_social_skills_game()
                        elif i == 4:
                            start_emotion_game()
                        elif i == 3:
                            run_macedonian_game()

        if active_window is not None:
            if active_window == 4:  # Emotional interaction
                if not random_emotion_display:
                    image_surfaces = draw_emotion_interaction_window()
            else:
                # Gradient background for other windows
                for y in range(screen_height):
                    color_ratio = y / screen_height
                    r = int(240 + (255 - 240) * color_ratio)
                    g = int(248 + (255 - 248) * color_ratio)
                    b = int(255)
                    pygame.draw.line(screen, (r, g, b), (0, y), (screen_width, y))

                # Window title
                title_font = pygame.font.Font(pygame.font.match_font("arial"), 48)
                text_surface = title_font.render(game_parts[active_window], True, (50, 50, 100))
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

                # Title background
                title_bg_rect = text_rect.inflate(60, 30)
                pygame.draw.rect(screen, (255, 255, 255, 200), title_bg_rect, border_radius=20)
                pygame.draw.rect(screen, (100, 150, 200), title_bg_rect, width=4, border_radius=20)

                screen.blit(text_surface, text_rect)

                # Enhanced back button
                draw_enhanced_button(
                    screen,
                    (*BACK_BUTTON_POSITION, 200, 50),
                    (220, 220, 220),
                    (150, 150, 150),
                    "Назад",
                    font_large
                )

        if random_emotion_display:
            display_random_emotion(image_surfaces)

        if active_window is None:
            screen.fill(BACKGROUND_COLOR)
            screen.blit(background_image, (0, 0))
            draw_buttons()

        draw_exit_button(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()