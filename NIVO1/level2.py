import pygame
import sys
import random
import subprocess  # За стартување на друг Python фајл

pygame.init()

# Земи резолуција на екранот
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h

# Постави fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Направи торта!")
font = pygame.font.SysFont(None, 40)

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
LIGHT_BROWN = (205, 133, 63)
DARK_BROWN = (101, 67, 33)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)


# Функција за кружна исечка на pygame.Surface
def crop_surface_to_circle(surface):
    size = surface.get_size()
    mask_surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.circle(mask_surf, (255, 255, 255, 255), (size[0] // 2, size[1] // 2), min(size) // 2)
    result = pygame.Surface(size, pygame.SRCALPHA)
    result.blit(surface, (0, 0))
    result.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return result


# Load images for ingredients
images = {
    "dough": pygame.image.load("cakedough.png"),
    "sauce": pygame.image.load("../pictures/pink.png"),
    "cheese": pygame.image.load("../pictures/strawberries.png"),
    "veggies": pygame.image.load("../pictures/candles.png")
}

# За fullscreen - задаваме ingredient_size пропорционално на висината на екранот
ingredient_size = (int(HEIGHT * 0.15), int(HEIGHT * 0.15))  # околу 15% од висината

for key in images:
    images[key] = pygame.transform.scale(images[key], ingredient_size)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

# После ова, скалирај ја сликата:
table_img = pygame.image.load("background.png").convert()
table_img = pygame.transform.smoothscale(table_img, (WIDTH, HEIGHT))

bg = pygame.image.load("background.png")
print("BG SIZE:", bg.get_width(), bg.get_height())

pizza_stages = [
    pygame.image.load("cakedough.png"),  # dough only
    pygame.image.load("cake_1.png"),  # dough + sauce
    pygame.image.load("cake_2.png"),  # dough + sauce + cheese
    pygame.image.load("cake_3.png")  # dough + sauce + cheese + veggies
]

# За pizza_stages - големина 25% од висината и ширината за одржување на квалитетот
pizza_size = (int(HEIGHT * 0.25), int(HEIGHT * 0.25))
pizza_stages = [pygame.transform.scale(img, pizza_size) for img in pizza_stages]
#pizza_stages = [crop_surface_to_circle(img) for img in pizza_stages]

# Load sounds
success_sound = pygame.mixer.Sound("../sounds/correct.wav")
error_sound = pygame.mixer.Sound("../sounds/wrong.mp3")

# Ingredient order
correct_order = ["dough", "sauce", "cheese", "veggies"]
current_index = 0

# Fixed brown squares positions under ingredients
square_size = int(ingredient_size[0] * 1.2)
top_y = int(HEIGHT * 0.1)
square_y = top_y + ingredient_size[1] + int(HEIGHT * 0.02)
start_x = (WIDTH - (len(correct_order) * (square_size + int(WIDTH * 0.05)) - int(WIDTH * 0.05))) // 2

brown_squares = []
for i in range(len(correct_order)):
    x = start_x + i * (square_size + int(WIDTH * 0.05))
    rect = pygame.Rect(x, square_y, square_size, square_size)
    brown_squares.append(rect)


# Измешај ги имињата на состојките за случаен редослед
def shuffle_ingredients():
    shuffled = correct_order.copy()
    random.shuffle(shuffled)
    return shuffled


shuffled_names = shuffle_ingredients()

# Нови позиции за состојките горе - ќе ги распоредиме во редица, центрирано
top_y = int(HEIGHT * 0.1)
start_x = (WIDTH - (len(shuffled_names) * (ingredient_size[0] + int(WIDTH * 0.05)) - int(WIDTH * 0.05))) // 2

ingredients = []
for i, name in enumerate(shuffled_names):
    x = start_x + i * (ingredient_size[0] + int(WIDTH * 0.05))
    y = top_y
    rect = pygame.Rect(x, y, *ingredient_size)
    ingredients.append({"name": name, "rect": rect, "dragging": False, "initial_pos": (x, y)})

# Pizza area - поместена погоре (од HEIGHT * 0.6 на HEIGHT * 0.5)
pizza_area_pos = (WIDTH // 2 - pizza_size[0] // 2, HEIGHT * 0.58 - pizza_size[1] // 2)

# List to store placed ingredients info (name and rect where to draw in brown square)
placed_positions = [None] * len(correct_order)

# Променети копчиња - обични правоаголни
button_width = 140
button_height = 50
button_padding = 10

restart_button_rect = pygame.Rect(WIDTH - button_width - 20, 20, button_width, button_height)
#next_button_rect = pygame.Rect(WIDTH - button_width - 20, 20 + button_height + button_padding, button_width,
 #                              button_height)


def draw_button(rect, text, color, font, screen):
    pygame.draw.rect(screen, color, rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=5)  # Црна граница
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (rect.centerx - text_surf.get_width() // 2,
                            rect.centery - text_surf.get_height() // 2))


def reset_game():
    global current_index, ingredients, placed_positions, shuffled_names, game_completed

    current_index = 0
    game_completed = False
    placed_positions = [None] * len(correct_order)
    shuffled_names = shuffle_ingredients()
    top_y = int(HEIGHT * 0.1)
    start_x = (WIDTH - (len(shuffled_names) * (ingredient_size[0] + int(WIDTH * 0.05)) - int(WIDTH * 0.05))) // 2

    ingredients.clear()
    for i, name in enumerate(shuffled_names):
        x = start_x + i * (ingredient_size[0] + int(WIDTH * 0.05))
        y = top_y
        rect = pygame.Rect(x, y, *ingredient_size)
        ingredients.append({"name": name, "rect": rect, "dragging": False, "initial_pos": (x, y)})


def draw_screen():
    screen.blit(table_img, (0, 0))  # Background на цел екран

    # Title - позициониран горе центрирано
    text = font.render("Ајде да направиме торта!", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, int(HEIGHT * 0.02)))

    # Draw brown squares
    for sq in brown_squares:
        pygame.draw.rect(screen, BROWN, sq, border_radius=10)

    # Draw placed ingredients normally (не кружни)
    for pos in placed_positions:
        if pos:
            img = images[pos["name"]]
            rect = img.get_rect(center=pos["rect"].center)
            screen.blit(img, rect.topleft)

    # Draw draggable ingredients normally
    for ing in ingredients:
        screen.blit(images[ing["name"]], ing["rect"].topleft)

    # Draw pizza stage below only if current_index > 0 (кај pizza_stages се кружни)
    if current_index > 0:
        screen.blit(pizza_stages[current_index - 1], pizza_area_pos)

    # Draw buttons - сега со новата функција за обични копчиња
    draw_button(restart_button_rect, "Restart", LIGHT_BROWN, font, screen)

    # Show "Следно" button only when game is completed
    #if game_completed:
     #   draw_button(next_button_rect, "Следно", BROWN, font, screen)

    # Show "Bravo!" message when game is completed
    if game_completed:
        text = font.render("Браво! Ја направи тортата!", True, GREEN)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 300))

    pygame.display.flip()


# Main loop
dragging_item = None
offset_x, offset_y = 0, 0
game_completed = False

clock = pygame.time.Clock()
running = True

while running:
    draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Додади ESC за излез од fullscreen
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Проверка дали кликнал на Restart копче
            if restart_button_rect.collidepoint(mouse_pos):
                reset_game()

            # Проверка дали кликнал на Следно копче само ако играта е завршена


            elif not game_completed:  # Дозволи drag само ако играта не е завршена
                for ing in reversed(ingredients):
                    if ing["rect"].collidepoint(event.pos):
                        ing["dragging"] = True
                        dragging_item = ing
                        offset_x = event.pos[0] - ing["rect"].x
                        offset_y = event.pos[1] - ing["rect"].y
                        # Bring dragged ingredient to top of list
                        ingredients.remove(ing)
                        ingredients.append(ing)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_item and not game_completed:  # Дозволи drop само ако играта не е завршена
                dragging_item["dragging"] = False

                # Проверка дали е пуштена во правилното кафено квадраче
                target_rect = brown_squares[current_index]
                if target_rect.colliderect(dragging_item["rect"]):
                    if dragging_item["name"] == correct_order[current_index]:
                        success_sound.play()

                        # Постави ја состојката во кафеното квадраче
                        placed_positions[current_index] = {
                            "name": dragging_item["name"],
                            "rect": target_rect.copy()
                        }
                        placed_positions[current_index]["rect"].center = target_rect.center

                        current_index += 1
                        ingredients.remove(dragging_item)

                        # Проверка дали играта е завршена
                        if current_index == len(correct_order):
                            game_completed = True
                    else:
                        error_sound.play()
                        dragging_item["rect"].topleft = dragging_item["initial_pos"]
                else:
                    # Ако не е пуштена во правилното квадраче врати назад
                    dragging_item["rect"].topleft = dragging_item["initial_pos"]

                dragging_item = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_item and dragging_item["dragging"] and not game_completed:
                dragging_item["rect"].x = event.pos[0] - offset_x
                dragging_item["rect"].y = event.pos[1] - offset_y

    clock.tick(60)

pygame.quit()
sys.exit()