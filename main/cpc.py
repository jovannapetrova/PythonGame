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
import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
pygame.init()

BACKGROUND_COLOR = (255, 255, 255)

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


if len(button_positions) > 5:
    x, y = button_positions[5]
    button_positions[5] = (x -100, y )


if len(button_positions) > 3:
    x, y = button_positions[3]
    button_positions[3] = (x + 60, y)

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

def start_spatial2_game():
    """
    Main function to start the spatial relationship game.
    Call this function to launch the game window.
    """

    pygame.mixer.init()

    # Load sounds
    def play_correct_sound():
        try:
            pygame.mixer.music.load("sounds/correct.mp3")
            pygame.mixer.music.play()
        except:
            pass

    def play_wrong_sound():
        try:
            pygame.mixer.music.load("sounds/incorrect.mp3")
            pygame.mixer.music.play()
        except:
            pass

    # --- Window setup ---
    root = tk.Tk()
    root.title("Просторен однос: Лева и десна рака - Три нивоа")

    # Set window size to screen size (not fullscreen mode)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.minsize(800, 600)

    # Canvas that fills the window
    canvas = tk.Canvas(root, highlightthickness=0, bg="#e6f7ff")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Styling
    TITLE_FONT = ("Arial", 32, "bold")
    FEEDBACK_FONT = ("Arial", 28, "bold")
    LEVEL_FONT = ("Arial", 24, "bold")
    TEXT_COLOR = "#2d3436"
    SUCCESS_COLOR = "#27ae60"
    ERROR_COLOR = "#e74c3c"
    PRIMARY_COLOR = "#3498db"
    HIGHLIGHT_COLOR = "#f1c40f"
    BG_COLOR = "#ecf0f1"

    # Game state
    class GameState:
        def __init__(self):
            self.current_level = None
            self.current_step = 0
            self.total_steps = 0
            self.monkeys = []
            self.hand_zones = []
            self.instructions = []
            self.banana = None
            self.bg_img = None
            self.monkey_img = None
            self.banana_img_small = None
            self.banana_img_large = None
            self.load_images()
            self.completed_levels = []  # Track completed levels

        def load_images(self):
            try:
                # Load background
                bg_img_raw = Image.open("../Pictures-Game2/background.jpg").resize((screen_width, screen_height))
                self.bg_img = ImageTk.PhotoImage(bg_img_raw)

                # load second background
                bg_img2_raw = Image.open("../Pictures-Game2/room-image.jpg").resize((screen_width, screen_height))
                self.bg_img2 = ImageTk.PhotoImage(bg_img2_raw)

                # Load monkey
                monkey_img_raw = Image.open("../Pictures-Game2/monkey-no background.png").resize((350, 350))
                self.monkey_img = ImageTk.PhotoImage(monkey_img_raw)

                # Load bananas
                banana_img_raw = Image.open("../Pictures-Game2/banana.png")
                self.banana_img_small = ImageTk.PhotoImage(banana_img_raw.resize((100, 100)))
                self.banana_img_large = ImageTk.PhotoImage(banana_img_raw.resize((120, 120)))
            except:
                # Create placeholder images if files don't exist
                self.create_placeholder_images()

        def create_placeholder_images(self):
            # Create simple colored rectangles as placeholders
            bg_placeholder = Image.new('RGB', (screen_width, screen_height), '#87CEEB')
            self.bg_img = ImageTk.PhotoImage(bg_placeholder)

            monkey_placeholder = Image.new('RGB', (350, 350), '#8B4513')
            self.monkey_img = ImageTk.PhotoImage(monkey_placeholder)

            banana_small = Image.new('RGB', (100, 100), '#FFD700')
            self.banana_img_small = ImageTk.PhotoImage(banana_small)

            banana_large = Image.new('RGB', (120, 120), '#FFD700')
            self.banana_img_large = ImageTk.PhotoImage(banana_large)

    game_state = GameState()

    # UI Elements
    instruction_label = None
    shadow_label = None
    level_label = None

    def create_ui_elements():
        nonlocal instruction_label, shadow_label, level_label

        # Clear canvas
        canvas.delete("all")

        # Background
        canvas.create_image(0, 0, image=game_state.bg_img, anchor="nw")

        # Level indicator
        if level_label:
            level_label.destroy()
        level_label = tk.Label(root, font=LEVEL_FONT, bg=HIGHLIGHT_COLOR, fg="black",
                               bd=3, relief="ridge", padx=20, pady=10)
        level_label.place(relx=0.5, rely=0.1, anchor="center")

        # Instruction labels
        if instruction_label:
            instruction_label.destroy()
        if shadow_label:
            shadow_label.destroy()

        instruction_label = tk.Label(root, font=TITLE_FONT, bg=PRIMARY_COLOR, fg="white",
                                     bd=4, relief="ridge", padx=20, pady=10,
                                     wraplength=screen_width - 200)
        shadow_label = tk.Label(root, font=TITLE_FONT, bg="black", fg="black",
                                bd=4, padx=20, pady=10, wraplength=screen_width - 200)

        instruction_label.place(relx=0.5, rely=0.3, anchor="center")
        shadow_label.place(relx=0.502, rely=0.302, anchor="center")
        instruction_label.lift()

    def set_instruction_text(text):
        if instruction_label and shadow_label:
            instruction_label.config(text=text)
            shadow_label.config(text=text)

    def set_level_text(text):
        if level_label:
            level_label.config(text=text)

    # Level definitions
    def setup_easy_level():
        # Clear all existing widgets first
        for widget in root.place_slaves():
            widget.destroy()

        game_state.current_level = "easy"
        game_state.current_step = 0
        game_state.total_steps = 2
        game_state.instructions = [
            "Земи ја бананата и стави ја во ЛЕВАТА рака на мајмунот",
            "Сега стави ја бананата во ДЕСНАТА рака на мајмунот"
        ]

        create_ui_elements()
        set_level_text("ЛЕСНО НИВО (1/3)")
        set_instruction_text(game_state.instructions[0])

        # Single monkey in center
        monkey_x = screen_width // 2
        monkey_y = screen_height // 2 + 50
        monkey = canvas.create_image(monkey_x, monkey_y, image=game_state.monkey_img)
        game_state.monkeys = [{"id": monkey, "x": monkey_x, "y": monkey_y}]

        # Hand zones for single monkey
        left_zone = canvas.create_rectangle(
            monkey_x - 200, monkey_y - 40,
            monkey_x - 100, monkey_y + 40,
            outline="", fill="", tags="left_hand_0")

        right_zone = canvas.create_rectangle(
            monkey_x + 100, monkey_y - 40,
            monkey_x + 200, monkey_y + 40,
            outline="", fill="", tags="right_hand_0")

        game_state.hand_zones = [
            {"left": left_zone, "right": right_zone, "monkey_index": 0}
        ]

        create_banana()
        # Add back button
        back_btn = tk.Button(root, text="Назад кон нивоа",
                             font=("Arial", 16), bg=PRIMARY_COLOR, fg="white",
                             padx=10, pady=5, command=show_level_selection)
        back_btn.place(relx=0.1, rely=0.1, anchor="center")

    def setup_medium_level():
        # Clear all existing widgets first
        for widget in root.place_slaves():
            widget.destroy()

        game_state.current_level = "medium"
        game_state.current_step = 0
        game_state.total_steps = 2
        game_state.instructions = [
            "Стави ја бананата во ЛЕВАТА рака на ЛЕВИОТ мајмун",
            "Сега стави ја бананата во ДЕСНАТА рака на ДЕСНИОТ мајмун"
        ]

        create_ui_elements()
        set_level_text("СРЕДНО НИВО (2/3)")
        set_instruction_text(game_state.instructions[0])

        # Two monkeys
        monkey1_x = screen_width // 3
        monkey2_x = (screen_width // 3) * 2
        monkey_y = screen_height // 2 + 50

        monkey1 = canvas.create_image(monkey1_x, monkey_y, image=game_state.monkey_img)
        monkey2 = canvas.create_image(monkey2_x, monkey_y, image=game_state.monkey_img)

        game_state.monkeys = [
            {"id": monkey1, "x": monkey1_x, "y": monkey_y},
            {"id": monkey2, "x": monkey2_x, "y": monkey_y}
        ]

        # Hand zones for both monkeys
        game_state.hand_zones = []
        for i, monkey in enumerate(game_state.monkeys):
            left_zone = canvas.create_rectangle(
                monkey["x"] - 200, monkey["y"] - 40,
                monkey["x"] - 100, monkey["y"] + 40,
                outline="", fill="", tags=f"left_hand_{i}")

            right_zone = canvas.create_rectangle(
                monkey["x"] + 100, monkey["y"] - 40,
                monkey["x"] + 200, monkey["y"] + 40,
                outline="", fill="", tags=f"right_hand_{i}")

            game_state.hand_zones.append({
                "left": left_zone,
                "right": right_zone,
                "monkey_index": i
            })

        create_banana()
        back_btn = tk.Button(root, text="Назад кон нивоа",
                             font=("Arial", 16), bg=PRIMARY_COLOR, fg="white",
                             padx=10, pady=5, command=show_level_selection)
        back_btn.place(relx=0.1, rely=0.1, anchor="center")

    def setup_hard_level():
        # Clear all existing widgets first
        for widget in root.place_slaves():
            widget.destroy()

        game_state.current_level = "hard"
        game_state.current_step = 0
        game_state.total_steps = 3
        game_state.instructions = [
            "Стави ја бананата во ЛЕВАТА рака на ВТОРИОТ мајмун (средниот)",
            "Сега стави ја бананата во ДЕСНАТА рака на ТРЕТИОТ мајмун (десниот)",
            "Конечно, стави ја бананата во ЛЕВАТА рака на ПРВИОТ мајмун (левиот)"
        ]

        create_ui_elements()
        set_level_text("ТЕШКО НИВО (3/3)")
        set_instruction_text(game_state.instructions[0])

        # Three monkeys
        monkey1_x = screen_width // 4
        monkey2_x = screen_width // 2
        monkey3_x = (screen_width // 4) * 3
        monkey_y = screen_height // 2 + 50

        monkey1 = canvas.create_image(monkey1_x, monkey_y, image=game_state.monkey_img)
        monkey2 = canvas.create_image(monkey2_x, monkey_y, image=game_state.monkey_img)
        monkey3 = canvas.create_image(monkey3_x, monkey_y, image=game_state.monkey_img)

        game_state.monkeys = [
            {"id": monkey1, "x": monkey1_x, "y": monkey_y},
            {"id": monkey2, "x": monkey2_x, "y": monkey_y},
            {"id": monkey3, "x": monkey3_x, "y": monkey_y}
        ]

        # Hand zones for all three monkeys
        game_state.hand_zones = []
        for i, monkey in enumerate(game_state.monkeys):
            left_zone = canvas.create_rectangle(
                monkey["x"] - 200, monkey["y"] - 40,
                monkey["x"] - 100, monkey["y"] + 40,
                outline="", fill="", tags=f"left_hand_{i}")

            right_zone = canvas.create_rectangle(
                monkey["x"] + 100, monkey["y"] - 40,
                monkey["x"] + 200, monkey["y"] + 40,
                outline="", fill="", tags=f"right_hand_{i}")

            game_state.hand_zones.append({
                "left": left_zone,
                "right": right_zone,
                "monkey_index": i
            })

        create_banana()
        # Add back button
        back_btn = tk.Button(root, text="Назад кон нивоа",
                             font=("Arial", 16), bg=PRIMARY_COLOR, fg="white",
                             padx=10, pady=5, command=show_level_selection)
        back_btn.place(relx=0.1, rely=0.1, anchor="center")

    def create_banana():
        banana_x = screen_width // 2
        banana_y = screen_height - 120
        game_state.banana = canvas.create_image(banana_x, banana_y,
                                                image=game_state.banana_img_small,
                                                tags="banana")

    # Drag and drop logic
    drag_data = {"x": 0, "y": 0, "item": None, "dragging": False}

    def on_start(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if "banana" in canvas.gettags(item):
            drag_data["item"] = item
            drag_data["x"] = event.x
            drag_data["y"] = event.y
            drag_data["dragging"] = True
            canvas.itemconfig(item, image=game_state.banana_img_large)

    def on_drag(event):
        if drag_data["item"] and drag_data["dragging"]:
            dx = event.x - drag_data["x"]
            dy = event.y - drag_data["y"]
            canvas.move(drag_data["item"], dx, dy)
            drag_data["x"] = event.x
            drag_data["y"] = event.y

    def on_drop(event):
        if drag_data["item"] and drag_data["dragging"]:
            canvas.itemconfig(drag_data["item"], image=game_state.banana_img_small)
            x, y = event.x, event.y

            correct_drop = check_correct_drop(x, y)

            if correct_drop:
                play_correct_sound()
                show_confetti()
                game_state.current_step += 1

                if game_state.current_step < game_state.total_steps:
                    show_message("Браво! Точно!", SUCCESS_COLOR)
                    set_instruction_text(game_state.instructions[game_state.current_step])
                    reset_banana()
                else:
                    show_message("Одлично! Го завршивте ова ниво!", SUCCESS_COLOR)
                    canvas.after(3000, show_next_level_or_restart)
            else:
                play_wrong_sound()
                show_message("Ова не е точната рака/мајмун. Обиди се повторно.", ERROR_COLOR)
                reset_banana()

    def check_correct_drop(x, y):
        if game_state.current_level == "easy":
            return check_easy_drop(x, y)
        elif game_state.current_level == "medium":
            return check_medium_drop(x, y)
        elif game_state.current_level == "hard":
            return check_hard_drop(x, y)
        return False

    def check_easy_drop(x, y):
        zone_data = game_state.hand_zones[0]
        if game_state.current_step == 0:  # Left hand
            zone = canvas.bbox(zone_data["left"])
        else:  # Right hand
            zone = canvas.bbox(zone_data["right"])

        return zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]

    def check_medium_drop(x, y):
        if game_state.current_step == 0:  # Left hand of left monkey
            zone = canvas.bbox(game_state.hand_zones[0]["left"])
        else:  # Right hand of right monkey
            zone = canvas.bbox(game_state.hand_zones[1]["right"])

        return zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]

    def check_hard_drop(x, y):
        if game_state.current_step == 0:  # Left hand of middle monkey
            zone = canvas.bbox(game_state.hand_zones[1]["left"])
        elif game_state.current_step == 1:  # Right hand of right monkey
            zone = canvas.bbox(game_state.hand_zones[2]["right"])
        else:  # Left hand of left monkey
            zone = canvas.bbox(game_state.hand_zones[0]["left"])

        return zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]

    def show_message(text, color=SUCCESS_COLOR):
        # Remove existing feedback messages
        for widget in root.place_slaves():
            if getattr(widget, "is_feedback", False):
                widget.destroy()

        message = tk.Label(root, text=text,
                           font=FEEDBACK_FONT,
                           fg="white",
                           bg=color,
                           bd=3,
                           relief="ridge",
                           padx=15, pady=10)
        message.is_feedback = True
        message.place(relx=0.5, rely=0.2, anchor="center")
        message.lift()

        root.after(3000, message.destroy)

    def reset_banana():
        banana_x = screen_width // 2
        banana_y = screen_height - 120
        canvas.coords(game_state.banana, banana_x, banana_y)
        canvas.itemconfig(game_state.banana, image=game_state.banana_img_small)

    def show_confetti():
        shapes = ["oval", "rectangle", "arc"]
        for _ in range(80):
            x = random.randint(100, screen_width - 100)
            y = random.randint(50, screen_height - 200)
            size = random.randint(8, 15)
            color = random.choice(["#e74c3c", "#2ecc71", "#3498db", "#f1c40f", "#9b59b6", "#e67e22"])
            shape = random.choice(shapes)

            if shape == "oval":
                confetti = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            elif shape == "rectangle":
                confetti = canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="")
            else:
                confetti = canvas.create_arc(x, y, x + size, y + size, fill=color, outline="",
                                             start=0, extent=120)

            for i in range(1, 25):
                canvas.after(i * 60, lambda c=confetti: canvas.move(c, 0, 5))
            canvas.after(2500, lambda c=confetti: canvas.delete(c))

    def show_next_level_or_restart():
        # Clear any existing buttons
        for widget in root.place_slaves():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Mark current level as completed if not already
        if game_state.current_level not in game_state.completed_levels:
            game_state.completed_levels.append(game_state.current_level)

        if game_state.current_level == "easy":
            btn = tk.Button(root, text="Следно ниво (Средно)", font=FEEDBACK_FONT,
                            bg=PRIMARY_COLOR, fg="white", padx=20, pady=10,
                            command=setup_medium_level)
            btn.place(relx=0.5, rely=0.75, anchor="center")
            btn.lift()
        elif game_state.current_level == "medium":
            btn = tk.Button(root, text="Следно ниво (Тешко)", font=FEEDBACK_FONT,
                            bg=PRIMARY_COLOR, fg="white", padx=20, pady=10,
                            command=setup_hard_level)
            btn.place(relx=0.5, rely=0.75, anchor="center")
            btn.lift()
        else:  # hard level completed
            # Show completion message with two options
            completion_label = tk.Label(root, text=f"🎉 Честитки! Го завршивте {game_state.current_level} нивото! 🎉",
                                        font=("Arial", 30, "bold"), bg=SUCCESS_COLOR, fg="white",
                                        bd=4, relief="ridge", padx=20, pady=15)
            completion_label.place(relx=0.5, rely=0.6, anchor="center")

            # Restart levels button
            restart_btn = tk.Button(root, text="🔄 Играј повторно\n(Лева-Десна рака)",
                                    font=FEEDBACK_FONT, bg=PRIMARY_COLOR, fg="white",
                                    padx=20, pady=10, command=show_level_selection)
            restart_btn.place(relx=0.3, rely=0.8, anchor="center")

            # Next game button
            next_game_btn = tk.Button(root, text="➡️ Следна игра\n(Локации)",
                                      font=FEEDBACK_FONT, bg=HIGHLIGHT_COLOR, fg="black",
                                      padx=20, pady=10, command=start_location_game)
            next_game_btn.place(relx=0.7, rely=0.8, anchor="center")

    def show_level_selection():
        # Clear everything
        canvas.delete("all")
        for widget in root.place_slaves():
            widget.destroy()

        # Background
        canvas.create_image(0, 0, image=game_state.bg_img, anchor="nw")

        # Title
        title = tk.Label(root, text="Избери ниво на тежина",
                         font=("Arial", 40, "bold"), bg=PRIMARY_COLOR, fg="white",
                         bd=5, relief="ridge", padx=30, pady=20)
        title.place(relx=0.5, rely=0.2, anchor="center")

        # Level buttons with completion indicators
        easy_text = "ЛЕСНО\n(1 мајмун, 2 чекори)"
        if "easy" in game_state.completed_levels:
            easy_text += " ✓"

        easy_btn = tk.Button(root, text=easy_text,
                             font=LEVEL_FONT, bg=SUCCESS_COLOR, fg="white",
                             padx=30, pady=20, command=setup_easy_level)
        easy_btn.place(relx=0.5, rely=0.4, anchor="center")

        medium_text = "СРЕДНО\n(2 мајмуни, 2 чекори)"
        if "medium" in game_state.completed_levels:
            medium_text += " ✓"

        medium_btn = tk.Button(root, text=medium_text,
                               font=LEVEL_FONT, bg=HIGHLIGHT_COLOR, fg="black",
                               padx=30, pady=20, command=setup_medium_level)
        medium_btn.place(relx=0.5, rely=0.55, anchor="center")

        hard_text = "ТЕШКО\n(3 мајмуни, 3 чекори)"
        if "hard" in game_state.completed_levels:
            hard_text += " ✓"

        hard_btn = tk.Button(root, text=hard_text,
                             font=LEVEL_FONT, bg=ERROR_COLOR, fg="white",
                             padx=30, pady=20, command=setup_hard_level)
        hard_btn.place(relx=0.5, rely=0.7, anchor="center")

        # Exit button
        exit_btn = tk.Button(root, text="Излез",
                             font=LEVEL_FONT, bg="#95a5a6", fg="white",
                             padx=20, pady=10, command=root.quit)
        exit_btn.place(relx=0.1, rely=0.1, anchor="center")

    def return_to_level_selection():
        show_level_selection()

    # Location Game Implementation
    class LocationGameState:
        def __init__(self):
            self.current_level = None
            self.current_step = 0
            self.total_steps = 0
            self.objects = []
            self.locations = []
            self.drop_zones = []
            self.instructions = []
            self.draggable_object = None
            self.object_images = {}
            self.location_images = {}
            self.load_location_images()

        def load_location_images(self):
            try:
                # Load object images with bigger sizes
                ball_img = Image.open("../Pictures-Game2/ball.png").resize((160, 160))  # was 80x80
                self.object_images['ball'] = ImageTk.PhotoImage(ball_img)

                book_img = Image.open("../Pictures-Game2/book.png").resize((160, 120))  # was 80x60
                self.object_images['book'] = ImageTk.PhotoImage(book_img)

                cup_img = Image.open("../Pictures-Game2/cup.png").resize((120, 160))  # was 60x80
                self.object_images['cup'] = ImageTk.PhotoImage(cup_img)

                # Load location images with bigger sizes
                table_img = Image.open("../Pictures-Game2/table.png").resize((400, 300))  # was 200x150
                self.location_images['table'] = ImageTk.PhotoImage(table_img)

                chair_img = Image.open("../Pictures-Game2/chair.png").resize((240, 360))  # was 120x180
                self.location_images['chair'] = ImageTk.PhotoImage(chair_img)

                box_img = Image.open("../Pictures-Game2/box.png").resize((300, 300))  # was 150x150
                self.location_images['box'] = ImageTk.PhotoImage(box_img)

            except:
                self.create_location_placeholders()

        def create_location_placeholders(self):
            # Create placeholder images with bigger sizes for objects
            ball_placeholder = Image.new('RGB', (160, 160), '#FF6B6B')  # was 80x80
            self.object_images['ball'] = ImageTk.PhotoImage(ball_placeholder)

            book_placeholder = Image.new('RGB', (160, 120), '#4ECDC4')  # was 80x60
            self.object_images['book'] = ImageTk.PhotoImage(book_placeholder)

            cup_placeholder = Image.new('RGB', (120, 160), '#45B7D1')  # was 60x80
            self.object_images['cup'] = ImageTk.PhotoImage(cup_placeholder)

            # Create placeholder images with bigger sizes for locations
            table_placeholder = Image.new('RGB', (400, 300), '#8B4513')  # was 200x150
            self.location_images['table'] = ImageTk.PhotoImage(table_placeholder)

            chair_placeholder = Image.new('RGB', (240, 360), '#654321')  # was 120x180
            self.location_images['chair'] = ImageTk.PhotoImage(chair_placeholder)

            box_placeholder = Image.new('RGB', (300, 300), '#D2691E')  # was 150x150
            self.location_images['box'] = ImageTk.PhotoImage(box_placeholder)

    location_game_state = LocationGameState()

    def start_location_game():
        """Initialize the location-based game"""
        # Switch to location game
        show_location_level_selection()

    def show_location_level_selection():
        # Clear everything
        canvas.delete("all")
        for widget in root.place_slaves():
            widget.destroy()

        # Background
        canvas.create_image(0, 0, image=game_state.bg_img2, anchor="nw")

        # Title
        title = tk.Label(root, text="Игра со локации - Избери ниво",
                         font=("Arial", 36, "bold"), bg="#9b59b6", fg="white",
                         bd=5, relief="ridge", padx=30, pady=20)
        title.place(relx=0.5, rely=0.15, anchor="center")

        # Subtitle
        subtitle = tk.Label(root, text="Стави го предметот на правилното место!",
                            font=("Arial", 24), bg="#ecf0f1", fg="#2c3e50",
                            padx=20, pady=10)
        subtitle.place(relx=0.5, rely=0.25, anchor="center")

        # Level buttons
        easy_btn = tk.Button(root, text="ЛЕСНО\n(1 предмет, 1 место)",
                             font=LEVEL_FONT, bg=SUCCESS_COLOR, fg="white",
                             padx=30, pady=20, command=setup_location_easy)
        easy_btn.place(relx=0.5, rely=0.4, anchor="center")

        medium_btn = tk.Button(root, text="СРЕДНО\n(2 предмети, 2 места)",
                               font=LEVEL_FONT, bg=HIGHLIGHT_COLOR, fg="black",
                               padx=30, pady=20, command=setup_location_medium)
        medium_btn.place(relx=0.5, rely=0.55, anchor="center")

        hard_btn = tk.Button(root, text="ТЕШКО\n(3 предмети, 3 места)",
                             font=LEVEL_FONT, bg=ERROR_COLOR, fg="white",
                             padx=30, pady=20, command=setup_location_hard)
        hard_btn.place(relx=0.5, rely=0.7, anchor="center")

        # Add a back button (if needed)
        back_btn = tk.Button(root, text="Назад",
                             font=LEVEL_FONT, bg=PRIMARY_COLOR, fg="white",
                             padx=20, pady=10, command=lambda: None)  # Replace with your back command
        back_btn.place(relx=0.1, rely=0.1, anchor="center")

    def return_to_level_selection():
        show_level_selection()

    # Location Game Implementation
    class LocationGameState:
        def __init__(self):
            self.current_level = None
            self.current_step = 0
            self.total_steps = 0
            self.objects = []
            self.locations = []
            self.drop_zones = []
            self.instructions = []
            self.draggable_object = None
            self.object_images = {}
            self.location_images = {}
            self.load_location_images()

        def load_location_images(self):
            try:
                # Load object images with bigger sizes
                ball_img = Image.open("photos/ball.png").resize((160, 160))  # was 80x80
                self.object_images['ball'] = ImageTk.PhotoImage(ball_img)

                book_img = Image.open("photos/book.png").resize((160, 120))  # was 80x60
                self.object_images['book'] = ImageTk.PhotoImage(book_img)

                cup_img = Image.open("photos/cup.png").resize((120, 160))  # was 60x80
                self.object_images['cup'] = ImageTk.PhotoImage(cup_img)

                # Load location images with bigger sizes
                table_img = Image.open("photos/table.png").resize((400, 300))  # was 200x150
                self.location_images['table'] = ImageTk.PhotoImage(table_img)

                chair_img = Image.open("photos/chair.png").resize((240, 360))  # was 120x180
                self.location_images['chair'] = ImageTk.PhotoImage(chair_img)

                box_img = Image.open("photos/box.png").resize((300, 300))  # was 150x150
                self.location_images['box'] = ImageTk.PhotoImage(box_img)

            except:
                self.create_location_placeholders()

        def create_location_placeholders(self):
            # Create placeholder images with bigger sizes for objects
            ball_placeholder = Image.new('RGB', (160, 160), '#FF6B6B')  # was 80x80
            self.object_images['ball'] = ImageTk.PhotoImage(ball_placeholder)

            book_placeholder = Image.new('RGB', (160, 120), '#4ECDC4')  # was 80x60
            self.object_images['book'] = ImageTk.PhotoImage(book_placeholder)

            cup_placeholder = Image.new('RGB', (120, 160), '#45B7D1')  # was 60x80
            self.object_images['cup'] = ImageTk.PhotoImage(cup_placeholder)

            # Create placeholder images with bigger sizes for locations
            table_placeholder = Image.new('RGB', (400, 300), '#8B4513')  # was 200x150
            self.location_images['table'] = ImageTk.PhotoImage(table_placeholder)

            chair_placeholder = Image.new('RGB', (240, 360), '#654321')  # was 120x180
            self.location_images['chair'] = ImageTk.PhotoImage(chair_placeholder)

            box_placeholder = Image.new('RGB', (300, 300), '#D2691E')  # was 150x150
            self.location_images['box'] = ImageTk.PhotoImage(box_placeholder)

    location_game_state = LocationGameState()

    def start_location_game():
        """Initialize the location-based game"""
        global game_state
        # Switch to location game
        show_location_level_selection()

    def show_location_level_selection():
        # Clear everything
        canvas.delete("all")
        for widget in root.place_slaves():
            widget.destroy()

        # Background
        canvas.create_image(0, 0, image=game_state.bg_img2, anchor="nw")

        # Title
        title = tk.Label(root, text="Игра со локации - Избери ниво",
                         font=("Arial", 36, "bold"), bg="#9b59b6", fg="white",
                         bd=5, relief="ridge", padx=30, pady=20)
        title.place(relx=0.5, rely=0.15, anchor="center")

        # Subtitle
        subtitle = tk.Label(root, text="Стави го предметот на правилното место!",
                            font=("Arial", 24), bg="#ecf0f1", fg="#2c3e50",
                            padx=20, pady=10)
        subtitle.place(relx=0.5, rely=0.25, anchor="center")

        # Level buttons
        easy_btn = tk.Button(root, text="ЛЕСНО\n(1 предмет, 1 место)",
                             font=LEVEL_FONT, bg=SUCCESS_COLOR, fg="white",
                             padx=30, pady=20, command=setup_location_easy)
        easy_btn.place(relx=0.5, rely=0.4, anchor="center")

        medium_btn = tk.Button(root, text="СРЕДНО\n(2 предмети, 2 места)",
                               font=LEVEL_FONT, bg=HIGHLIGHT_COLOR, fg="black",
                               padx=30, pady=20, command=setup_location_medium)
        medium_btn.place(relx=0.5, rely=0.55, anchor="center")

        hard_btn = tk.Button(root, text="ТЕШКО\n(3 предмети, 3 места)",
                             font=LEVEL_FONT, bg=ERROR_COLOR, fg="white",
                             padx=30, pady=20, command=setup_location_hard)
        hard_btn.place(relx=0.5, rely=0.7, anchor="center")

        # Back button
        back_btn = tk.Button(root, text="⬅️ Назад кон прва игра",
                             font=("Arial", 18), bg="#95a5a6", fg="white",
                             padx=20, pady=10, command=show_level_selection)
        back_btn.place(relx=0.08, rely=0.05, anchor="center")
    def create_location_ui():
        global instruction_label, shadow_label, level_label

        # Clear canvas
        canvas.delete("all")

        # Background
        canvas.create_image(0, 0, image=game_state.bg_img2, anchor="nw")

        # Level indicator
        if level_label:
            level_label.destroy()
        level_label = tk.Label(root, font=LEVEL_FONT, bg="#9b59b6", fg="white",
                               bd=3, relief="ridge", padx=20, pady=10)
        level_label.place(relx=0.1, rely=0.05, anchor="center")

        # Instruction labels
        if instruction_label:
            instruction_label.destroy()
        if shadow_label:
            shadow_label.destroy()

        instruction_label = tk.Label(root, font=TITLE_FONT, bg="#9b59b6", fg="white",
                                     bd=4, relief="ridge", padx=20, pady=10,
                                     wraplength=screen_width - 200)
        shadow_label = tk.Label(root, font=TITLE_FONT, bg="black", fg="black",
                                bd=4, padx=20, pady=10, wraplength=screen_width - 200)

        instruction_label.place(relx=0.5, rely=0.2, anchor="center")
        shadow_label.place(relx=0.502, rely=0.202, anchor="center")
        instruction_label.lift()

    def setup_location_easy():
        # Clear all existing widgets
        for widget in root.place_slaves():
            widget.destroy()

        location_game_state.current_level = "easy"
        location_game_state.current_step = 0
        location_game_state.total_steps = 1
        location_game_state.instructions = [
            "Стави ја топката ПОД масата"
        ]

        create_location_ui()
        set_level_text("ЛЕСНО НИВО - Локации (1/3)")
        set_instruction_text(location_game_state.instructions[0])

        # Create table in center
        table_x = screen_width // 2
        table_y = screen_height // 2 - 50
        table = canvas.create_image(table_x, table_y, image=location_game_state.location_images['table'])

        # Create drop zone under table
        drop_zone = canvas.create_rectangle(
            table_x - 150, table_y + 30,  # was -100, +75
            table_x + 150, table_y + 160,  # was +100, +140
            outline="", width=2, fill="", tags="under_table")

        location_game_state.drop_zones = [{"zone": drop_zone, "type": "under_table"}]

        # Create ball
        ball_x = screen_width // 2
        ball_y = screen_height - 100
        ball = canvas.create_image(ball_x, ball_y, image=location_game_state.object_images['ball'],
                                   tags="draggable_ball")
        location_game_state.draggable_object = ball

        # Bind drag events
        canvas.tag_bind("draggable_ball", "<ButtonPress-1>", location_on_start)
        canvas.tag_bind("draggable_ball", "<B1-Motion>", location_on_drag)
        canvas.tag_bind("draggable_ball", "<ButtonRelease-1>", location_on_drop)

    def setup_location_medium():
        # Clear all existing widgets
        for widget in root.place_slaves():
            widget.destroy()

        location_game_state.current_level = "medium"
        location_game_state.current_step = 0
        location_game_state.total_steps = 2
        location_game_state.instructions = [
            "Стави ја топката ПОД масата",
            "Сега стави ја книгата НА столот"
        ]

        create_location_ui()
        set_level_text("СРЕДНО НИВО - Локации (2/3)")
        set_instruction_text(location_game_state.instructions[0])

        # Create table and chair
        table_x = screen_width // 3
        table_y = screen_height // 2 - 50
        table = canvas.create_image(table_x, table_y, image=location_game_state.location_images['table'])

        chair_x = (screen_width // 3) * 2
        chair_y = screen_height // 2
        chair = canvas.create_image(chair_x, chair_y, image=location_game_state.location_images['chair'])

        # Create drop zones
        under_table_zone = canvas.create_rectangle(
            table_x - 120, table_y + 50,  # moved 25 px up, widened 20 px left
            table_x + 120, table_y + 115,  # moved 25 px up, widened 20 px right
            outline="", width=2, fill="", tags="under_table")

        on_chair_zone = canvas.create_rectangle(
            chair_x - 80, chair_y - 60,  # wider by 20 px on left, moved down by 20 px
            chair_x + 80, chair_y,  # wider by 20 px on right, moved down by 20 px
            outline="", width=2, fill="", tags="on_chair")

        location_game_state.drop_zones = [
            {"zone": under_table_zone, "type": "under_table"},
            {"zone": on_chair_zone, "type": "on_chair"}
        ]

        # Create objects
        ball_x = screen_width // 4
        ball_y = screen_height - 100
        ball = canvas.create_image(ball_x, ball_y, image=location_game_state.object_images['ball'],
                                   tags="draggable_ball")

        book_x = (screen_width // 4) * 3
        book_y = screen_height - 100
        book = canvas.create_image(book_x, book_y, image=location_game_state.object_images['book'],
                                   tags="draggable_book")

        location_game_state.objects = [ball, book]
        location_game_state.draggable_object = ball  # Start with ball

        # Bind drag events
        canvas.tag_bind("draggable_ball", "<ButtonPress-1>", location_on_start)
        canvas.tag_bind("draggable_ball", "<B1-Motion>", location_on_drag)
        canvas.tag_bind("draggable_ball", "<ButtonRelease-1>", location_on_drop)

        canvas.tag_bind("draggable_book", "<ButtonPress-1>", location_on_start)
        canvas.tag_bind("draggable_book", "<B1-Motion>", location_on_drag)
        canvas.tag_bind("draggable_book", "<ButtonRelease-1>", location_on_drop)

    def setup_location_hard():
        # Clear all existing widgets
        for widget in root.place_slaves():
            widget.destroy()

        location_game_state.current_level = "hard"
        location_game_state.current_step = 0
        location_game_state.total_steps = 3
        location_game_state.instructions = [
            "Стави ја топката ПОД масата",
            "Стави ја книгата НА столот",
            "Стави ја чашата ВО кутијата"
        ]

        create_location_ui()
        set_level_text("ТЕШКО НИВО - Локации (3/3)")
        set_instruction_text(location_game_state.instructions[0])

        # Create locations
        table_x = screen_width // 4
        table_y = screen_height // 2 - 50
        table = canvas.create_image(table_x, table_y, image=location_game_state.location_images['table'])

        chair_x = screen_width // 2
        chair_y = screen_height // 2
        chair = canvas.create_image(chair_x, chair_y, image=location_game_state.location_images['chair'])

        box_x = (screen_width // 4) * 3
        box_y = screen_height // 2
        box = canvas.create_image(box_x, box_y, image=location_game_state.location_images['box'])

        # Under the table zone - move up and bigger
        under_table_zone = canvas.create_rectangle(
            table_x - 110, table_y + 60,  # moved 15 px up and wider by 10 px on left
            table_x + 110, table_y + 150,  # moved 10 px down and wider by 10 px on right, bigger height
            outline="", width=2, fill="", tags="under_table")

        # On the chair zone - move down and taller
        on_chair_zone = canvas.create_rectangle(
            chair_x - 60, chair_y - 70,  # moved 10 px down (y increased from -80 to -70)
            chair_x + 60, chair_y - 10,  # moved 10 px down and taller (from -20 to -10)
            outline="", width=2, fill="", tags="on_chair")

        # In the box zone - move up and shorter from bottom
        in_box_zone = canvas.create_rectangle(
            box_x - 75, box_y - 90,  # moved 15 px up (from -75 to -90)
            box_x + 75, box_y + 50,  # shorter from bottom (from +75 to +50)
            outline="", width=2, fill="", tags="in_box")

        location_game_state.drop_zones = [
            {"zone": under_table_zone, "type": "under_table"},
            {"zone": on_chair_zone, "type": "on_chair"},
            {"zone": in_box_zone, "type": "in_box"}
        ]

        # Create objects
        ball_x = screen_width // 5
        ball_y = screen_height - 100
        ball = canvas.create_image(ball_x, ball_y, image=location_game_state.object_images['ball'],
                                   tags="draggable_ball")

        book_x = screen_width // 2
        book_y = screen_height - 100
        book = canvas.create_image(book_x, book_y, image=location_game_state.object_images['book'],
                                   tags="draggable_book")

        cup_x = (screen_width // 5) * 4
        cup_y = screen_height - 100
        cup = canvas.create_image(cup_x, cup_y, image=location_game_state.object_images['cup'],
                                  tags="draggable_cup")

        location_game_state.objects = [ball, book, cup]

        # Bind drag events
        for tag in ["draggable_ball", "draggable_book", "draggable_cup"]:
            canvas.tag_bind(tag, "<ButtonPress-1>", location_on_start)
            canvas.tag_bind(tag, "<B1-Motion>", location_on_drag)
            canvas.tag_bind(tag, "<ButtonRelease-1>", location_on_drop)

    # Location game drag and drop
    location_drag_data = {"x": 0, "y": 0, "item": None, "dragging": False}

    def location_on_start(event):
        item = canvas.find_closest(event.x, event.y)[0]
        location_drag_data["item"] = item
        location_drag_data["x"] = event.x
        location_drag_data["y"] = event.y
        location_drag_data["dragging"] = True

    def location_on_drag(event):
        if location_drag_data["item"] and location_drag_data["dragging"]:
            dx = event.x - location_drag_data["x"]
            dy = event.y - location_drag_data["y"]
            canvas.move(location_drag_data["item"], dx, dy)
            location_drag_data["x"] = event.x
            location_drag_data["y"] = event.y

    def location_on_drop(event):
        if location_drag_data["item"] and location_drag_data["dragging"]:
            x, y = event.x, event.y

            correct_drop = check_location_drop(x, y)

            if correct_drop:
                play_correct_sound()
                show_confetti()
                location_game_state.current_step += 1

                if location_game_state.current_step < location_game_state.total_steps:
                    show_message("Браво! Точно место!", SUCCESS_COLOR)
                    set_instruction_text(location_game_state.instructions[location_game_state.current_step])
                else:
                    show_message("Одлично! Го завршивте ова ниво!", SUCCESS_COLOR)
                    canvas.after(3000, show_location_next_level)
            else:
                play_wrong_sound()
                show_message("Ова не е точното место. Обиди се повторно.", ERROR_COLOR)

    def check_location_drop(x, y):
        current_instruction = location_game_state.instructions[location_game_state.current_step]

        # Check which zone the drop occurred in
        for zone_data in location_game_state.drop_zones:
            zone_bbox = canvas.bbox(zone_data["zone"])
            if zone_bbox[0] <= x <= zone_bbox[2] and zone_bbox[1] <= y <= zone_bbox[3]:
                # Check if this matches the current instruction
                if location_game_state.current_step == 0 and zone_data["type"] == "under_table":
                    return True
                elif location_game_state.current_step == 1 and zone_data["type"] == "on_chair":
                    return True
                elif location_game_state.current_step == 2 and zone_data["type"] == "in_box":
                    return True

        return False

    def show_location_next_level():
        # Clear any existing buttons
        for widget in root.place_slaves():
            if isinstance(widget, tk.Button):
                widget.destroy()

        if location_game_state.current_level == "easy":
            btn = tk.Button(root, text="Следно ниво (Средно)", font=FEEDBACK_FONT,
                            bg="#9b59b6", fg="white", padx=20, pady=10,
                            command=setup_location_medium)
        elif location_game_state.current_level == "medium":
            btn = tk.Button(root, text="Следно ниво (Тешко)", font=FEEDBACK_FONT,
                            bg="#9b59b6", fg="white", padx=20, pady=10,
                            command=setup_location_hard)
        else:  # hard level completed
            completion_label = tk.Label(root, text=" Браво! Ги завршивте сите игри!",
                                        font=("Arial", 30, "bold"), bg=SUCCESS_COLOR, fg="white",
                                        bd=4, relief="ridge", padx=20, pady=15)
            completion_label.place(relx=0.5, rely=0.6, anchor="center")

            # Restart location game
            restart_btn = tk.Button(root, text=" Играј локации повторно",
                                    font=FEEDBACK_FONT, bg="#9b59b6", fg="white",
                                    padx=20, pady=10, command=show_location_level_selection)
            restart_btn.place(relx=0.3, rely=0.8, anchor="center")

            # Back to first game
            back_btn = tk.Button(root, text="Назад кон прва игра",
                                 font=FEEDBACK_FONT, bg=PRIMARY_COLOR, fg="white",
                                 padx=20, pady=10, command=show_level_selection)
            back_btn.place(relx=0.7, rely=0.8, anchor="center")
            return

        btn.place(relx=0.5, rely=0.75, anchor="center")
        btn.lift()

    # Bind events
    canvas.tag_bind("banana", "<ButtonPress-1>", on_start)
    canvas.tag_bind("banana", "<B1-Motion>", on_drag)
    canvas.tag_bind("banana", "<ButtonRelease-1>", on_drop)

    # Start the game
    show_level_selection()
    root.mainloop()




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
                            start_spatial2_game()
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