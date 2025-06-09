import pygame
import sys
import json

pygame.init()

# Прво постави го екранот - fullscreen со резолуција на моменталниот дисплеј
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Бојење по броеви со click и слободно цртање")

# Вчитај ја сликата и конвертирај ја
background_tmp = pygame.image.load("background.png")
background = background_tmp.convert()

clouds_tmp = pygame.image.load("../pictures/cloudsbackground.png")
clouds = pygame.transform.scale(clouds_tmp, (screen_width, screen_height))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Позиција за сликата за бојадисување - лево
bg_width, bg_height = background.get_size()
bg_x = 50  # лево маргина
bg_y = (screen_height - bg_height) // 2

palette_colors = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 165, 0),
    6: (128, 0, 128)
}

# Хоризонтален распоред на палетата долу централно
palette_radius = 25
palette_spacing = 20
num_colors = len(palette_colors)

start_x = (screen_width - (num_colors * (2*palette_radius + palette_spacing) - palette_spacing)) // 2
palette_y = screen_height - 80

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

final_image = pygame.image.load("final.png").convert_alpha()

# Намалување и нова позиција на финалната слика - долу десно
final_scale = 0.3
final_image = pygame.transform.smoothscale(
    final_image,
    (int(final_image.get_width() * final_scale), int(final_image.get_height() * final_scale))
)

final_x = screen_width - final_image.get_width() - 50
final_y = screen_height - final_image.get_height() - 50

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
        # Прикажи селектирана боја и бројка горе десно, поголемо и јасно
        sel_pos = (screen_width - 150, 50)
        # Полупрозрачна бела кутија
        s = pygame.Surface((140, 70), pygame.SRCALPHA)
        s.fill((255, 255, 255, 180))
        screen.blit(s, (sel_pos[0]-10, sel_pos[1]-40))
        pygame.draw.circle(screen, selected_color, (sel_pos[0]+30, sel_pos[1]), 30)
        pygame.draw.circle(screen, (0, 0, 0), (sel_pos[0]+30, sel_pos[1]), 30, 4)
        text = font.render(f"Селектирана боја: {selected_number}", True, (0,0,0))
        screen.blit(text, (sel_pos[0]+70, sel_pos[1]-15))

def all_colored():
    for a in areas:
        if not a["visited"]:
            return False
    return True

def show_congrats_screen():
    screen.fill((255, 255, 200))
    text1 = font.render("БРАВО! Сè е обоено точно!", True, (0, 150, 0))
    text2 = font.render("Кликни на 'Рестарт' за нов почеток.", True, (0, 100, 0))
    screen.blit(text1, ((screen_width - text1.get_width()) // 2, screen_height // 2 - 40))
    screen.blit(text2, ((screen_width - text2.get_width()) // 2, screen_height // 2))

def draw_restart_button():
    rect = pygame.Rect(screen_width//2 - 100, screen_height - 60, 200, 40)
    pygame.draw.rect(screen, (0, 120, 255), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3)
    text = font.render("Рестарт", True, (255, 255, 255))
    screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
    return rect

def main():
    global selected_color, selected_number
    running = True
    finished = False

    draw_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)

    while running:
        # Ново: Постави ја позадината clouds.png
        screen.blit(clouds, (0, 0))

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

        if finished:
            # Прикажи екран за честитка (префрлај на цел екран)
            show_congrats_screen()

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
                else:
                    # Проверка дали кликнал на палетата
                    if not finished:
                        for num, pos in palette_pos.items():
                            px, py = pos
                            if (mx - px)**2 + (my - py)**2 <= palette_radius**2:
                                selected_color = palette_colors[num]
                                selected_number = num
                                break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
