import pygame
import sys
import json
import pygame.mixer
pygame.mixer.init()
pygame.init()

def scale_to_cover(image, target_width, target_height):
    img_w, img_h = image.get_size()
    scale = max(target_width / img_w, target_height / img_h)  # скалирање за да покрие цел екран
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    scaled_img = pygame.transform.smoothscale(image, (new_w, new_h))
    return scaled_img

# Прво постави го екранот - fullscreen со резолуција на моменталниот дисплеј
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Бојење по броеви со click и слободно цртање")

# Вчитај ја сликата и конвертирај ја
background_tmp = pygame.image.load("house.png")
background = background_tmp.convert()

clouds_tmp = pygame.image.load("backg.png").convert()
clouds = scale_to_cover(clouds_tmp, screen_width, screen_height)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Позиција за сликата за бојадисување - лево
# Позиција за сликата за бојадисување - центрирана во левиот дел од екранот
bg_width, bg_height = background.get_size()
bg_x = (screen_width // 2 - bg_width) // 2
bg_y = (screen_height - bg_height) // 2


palette_colors = {
    1: (255, 0, 0),       # црвена
    2: (255, 165, 0),     # портокалова
    3: (255, 255, 0),     # жолта
    4: (0, 255, 0),       # зелена
    5: (0, 0, 255) ,     # виолетова
    6: (128, 0, 128)       # сина (ако ја користиш и 6-та боја)
}


# Хоризонтален распоред на палетата долу централно
palette_radius = 25
palette_spacing = 20
num_colors = len(palette_colors)

start_x = (screen_width - (num_colors * (2*palette_radius + palette_spacing) - palette_spacing)) // 2
palette_y = 80

palette_pos = {}
for i, num in enumerate(sorted(palette_colors.keys())):
    palette_pos[num] = (start_x + i * (2*palette_radius + palette_spacing) + palette_radius, palette_y)

selected_color = None
selected_number = None

# Вчитување области од areas.json
with open("areas.json", "r") as f:
    areas = json.load(f)

for a in areas:
    a["color"] = None
    a["visited"] = False  # ново: за проверка дали е боено правилно

final_image = pygame.image.load("finalhouse.png").convert_alpha()

# Намалување и позиционирање на финалната слика - централно во десниот дел
# Скалирање на финалната слика - околу 30% од ширината на екранот
target_width = int(screen_width * 0.2)
scale_factor = target_width / final_image.get_width()
target_height = int(final_image.get_height() * scale_factor)

final_image = pygame.transform.smoothscale(final_image, (target_width, target_height))

# Позиционирање горе десно со малку внатрешен одмак
padding = 30
final_x = screen_width - target_width - padding
final_y = padding

def draw_areas():
    for a in areas:
        x, y, w, h = a["rect"]
        x += bg_x
        y += bg_y
        if a["color"]:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((*a["color"], 150))
            screen.blit(s, (x, y))
        pygame.draw.rect(screen, (0,0,0), (x, y, w, h), 2)
        text = font.render(str(a["number"]), True, (0,0,0))
        tx = x + w//2 - text.get_width()//2
        ty = y + h//2 - text.get_height()//2
        screen.blit(text, (tx, ty))

def draw_palette():
    for num, pos in palette_pos.items():
        color = palette_colors[num]
        pygame.draw.circle(screen, color, pos, palette_radius)
        pygame.draw.circle(screen, (0,0,0), pos, palette_radius, 3)
        text = font.render(str(num), True, (0,0,0))
        screen.blit(text, (pos[0] - text.get_width()//2, pos[1] - text.get_height()//2))
    if selected_color:
        # Прикажи селектирана боја долу централно
        sel_x = screen_width // 2
        sel_y = screen_height - 60  # Претходно беше под финалната слика

        pygame.draw.circle(screen, selected_color, (sel_x - 60, sel_y), 25)
        pygame.draw.circle(screen, (0, 0, 0), (sel_x - 60, sel_y), 25, 3)

        text = font.render(f"Селектирана боја: {selected_number}", True, (0, 0, 0))
        screen.blit(text, (sel_x - 10, sel_y - 10))


def all_colored():
    for a in areas:
        if not a["visited"]:
            return False
    return True


def show_congrats_screen():
    # Вчитај confetti позадина
    confetti_img = pygame.image.load("confetti.png")
    confetti_bg = pygame.transform.scale(confetti_img, (screen_width, screen_height))
    screen.blit(confetti_bg, (0, 0))

    text1 = font.render("БРАВО! Сè е обоено точно!", True, (255, 255, 255))
    text2 = font.render("Кликни на 'Следна слика' за да продолжиш.", True, (255, 255, 255))
    screen.blit(text1, ((screen_width - text1.get_width()) // 2, screen_height // 2 - 40))
    screen.blit(text2, ((screen_width - text2.get_width()) // 2, screen_height // 2))
def draw_next_button():
    rect = pygame.Rect(final_x + (target_width - 200) // 2, final_y + target_height + 80, 200, 50)
    pygame.draw.rect(screen, (0, 200, 0), rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)
    text = font.render("Следна слика", True, (255, 255, 255))
    screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
    return rect


def draw_restart_button():
    rect = pygame.Rect(final_x + (target_width - 200) // 2, final_y + target_height + 20, 200, 50)
    pygame.draw.rect(screen, (0, 120, 255), rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)
    text = font.render("Рестарт", True, (255, 255, 255))
    screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
    return rect


def main():
    global selected_color, selected_number
    running = True
    finished = False

    draw_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)

    while running:
        # Ново: Постави ја позадината clouds.png целосно покриена
        offset_x = (clouds.get_width() - screen_width) // 2
        offset_y = (clouds.get_height() - screen_height) // 2
        screen.blit(clouds, (-offset_x, -offset_y))

        # Слика за боење лево
        screen.blit(background, (bg_x, bg_y))
        screen.blit(draw_surface, (bg_x, bg_y))

        # Прикажи областите и бројките
        draw_areas()

        # Палета боја долу централно
        draw_palette()

        # Прикажи моделот (финалната слика) долу десно
        screen.blit(final_image, (final_x, final_y))

        # Копче за рестарт долу централно
        restart_btn = draw_restart_button()
        next_btn = draw_next_button()
        # Ако е завршено, прикажи копче за следна слика
        if finished:
            next_btn = draw_next_button()

        mouse_pressed = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        local_x = mx - bg_x
        local_y = my - bg_y

        if mouse_pressed[0] and not finished and selected_color is not None:
            painted = False
            for a in areas:
                x, y, w, h = a["rect"]
                abs_x = x + bg_x
                abs_y = y + bg_y
                if abs_x <= mx <= abs_x + w and abs_y <= my <= abs_y + h:
                    if a["number"] == selected_number:
                        pygame.draw.circle(draw_surface, selected_color + (255,), (local_x, local_y), 10)
                        a["visited"] = True
                        a["color"] = selected_color
                    painted = True
                    break
            if not painted:
                pygame.draw.circle(draw_surface, selected_color + (255,), (local_x, local_y), 10)

            if all_colored():
                if not finished:
                    pygame.mixer.Sound("correct.wav").play()
                finished = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


            elif event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos

                # Проверка дали кликнал на копчето Рестарт

                if restart_btn.collidepoint(mx, my):

                    for a in areas:
                        a["color"] = None
                        a["visited"] = False

                    draw_surface.fill((0, 0, 0, 0))

                    finished = False

                    selected_color = None
                    selected_number = None

                # Проверка дали кликнал на копчето Следна слика

                elif finished and next_btn and next_btn.collidepoint(mx, my):

                    pygame.quit()

                    import subprocess

                    subprocess.run([sys.executable, "level3.py"])

                    sys.exit()

                else:

                    # Проверка дали кликнал на палетата

                    if not finished:

                        for num, pos in palette_pos.items():

                            px, py = pos

                            if (mx - px) ** 2 + (my - py) ** 2 <= palette_radius ** 2:
                                selected_color = palette_colors[num]

                                selected_number = num

                                break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
