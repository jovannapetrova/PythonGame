import pygame
import sys
import random


pygame.init()


BACKGROUND_COLOR = (255, 255, 255)

BUTTON_COLORS = [
    (255, 128, 128),
    (128, 255, 128),
    (128, 128, 255),
    (255, 255, 128),
    (255, 128, 255),
    (128, 255, 255),  
    (255, 192, 128),
    (192, 192, 192)
]


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Игра за Деца")


background_image = pygame.image.load("background.jpg")
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
button_positions = [
    (screen_width // 6 - 100, screen_height // 5),
    (screen_width // 2 - 100, screen_height // 5),
    (5 * screen_width // 6 - 100, screen_height // 5),
    (screen_width // 6 - 100, 2 * screen_height // 5),
    (screen_width // 2 - 100, 2 * screen_height // 5),
    (5 * screen_width // 6 - 100, 2 * screen_height // 5),
    (screen_width // 6 - 100, 3 * screen_height // 5),
    (screen_width // 2 - 100, 3 * screen_height // 5)
]

#kopce za nazad
BACK_BUTTON_POSITION = (screen_width // 2 - 100, screen_height - 150)

# tekst na kvadratcinjata
font = pygame.font.Font(pygame.font.match_font("arial"), 28)

#prikaz na kocinjata
def draw_buttons():
    for i, position in enumerate(button_positions):
        color = BUTTON_COLORS[i % len(BUTTON_COLORS)]
        pygame.draw.rect(screen, color, (*position, 300, 120), border_radius=10)  # Заоблени рабови
        text_surface = font.render(game_parts[i], True, (0, 0, 0))  # Текст со црна боја
        text_rect = text_surface.get_rect(center=(position[0] + 150, position[1] + 60))  # Центрирање на текстот
        screen.blit(text_surface, text_rect)

    # kopce za nazad
    pygame.draw.rect(screen, (200, 200, 200), (*BACK_BUTTON_POSITION, 200, 50), border_radius=10)
    back_text = font.render("Назад", True, (0, 0, 0))
    back_text_rect = back_text.get_rect(center=(BACK_BUTTON_POSITION[0] + 100, BACK_BUTTON_POSITION[1] + 25))
    screen.blit(back_text, back_text_rect)

# dali e kliknato kopceto
def is_button_clicked(x, y, mouse_pos, width=300, height=120):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

# kliknato kopceto za nazad?
def is_back_button_clicked(mouse_pos):
    return BACK_BUTTON_POSITION[0] <= mouse_pos[0] <= BACK_BUTTON_POSITION[0] + 200 and BACK_BUTTON_POSITION[1] <= \
        mouse_pos[1] <= BACK_BUTTON_POSITION[1] + 50

# prikaz na slikite
def draw_emotion_images():
    images = ['angry.png', 'happy.png', 'sad.png', 'surprised.png']
    image_surfaces = []
    target_width = 300
    target_height = 300

    for image in images:
        try:
            # vcituvanje na slikite
            image_surface = pygame.image.load(image)

            # promena na golemina
            image_surface = pygame.transform.scale(image_surface, (target_width, target_height))

            image_surfaces.append(image_surface)
        except pygame.error as e:
            print(f"Грешка при учитавање на сликата {image}: {e}")
            image_surfaces.append(None)

    return image_surfaces

RANDOM_BUTTON_POSITION = (screen_width // 2 - 100, screen_height // 2 + 100)

# EMOCIONALNA INTERAKCIJA
def draw_emotion_interaction_window():
    screen.fill((255, 255, 255))
    # sliki za emociite
    image_surfaces = draw_emotion_images()


    target_width = 300
    target_height = 300

    #pozicija
    x_offset = screen_width // 6  # pocetna poz po horizontala
    y_offset = screen_height // 5  # pocetna poz po vertikala

    #slikite gore
    for i, image_surface in enumerate(image_surfaces):
        if image_surface:  #dali e uspesno loadirana
            # pozicija za goren del
            image_rect = image_surface.get_rect(center=(x_offset + i * target_width, y_offset))
            screen.blit(image_surface, image_rect)

    # RANDOM GENERIRANJE emocija
    pygame.draw.rect(screen, (200, 200, 200), (*RANDOM_BUTTON_POSITION, 200, 50), border_radius=10)
    random_text = font.render("Генерирај емоција", True, (0, 0, 0))
    random_text_rect = random_text.get_rect(center=(RANDOM_BUTTON_POSITION[0] + 100, RANDOM_BUTTON_POSITION[1] + 25))
    screen.blit(random_text, random_text_rect)

    # kopce za nazad
    pygame.draw.rect(screen, (200, 200, 200), (*BACK_BUTTON_POSITION, 200, 50), border_radius=10)
    back_text = font.render("Назад", True, (0, 0, 0))
    back_text_rect = back_text.get_rect(center=(BACK_BUTTON_POSITION[0] + 100, BACK_BUTTON_POSITION[1] + 25))
    screen.blit(back_text, back_text_rect)

    return image_surfaces

# PRIKAZ NA SLUCAJNA EMOCIJA
def display_random_emotion(image_surfaces):
    random_emotion = random.choice(image_surfaces)  # slucaen izbor na slikata
    if random_emotion:
        screen.fill((255, 255, 255))
        image_rect = random_emotion.get_rect(center=(screen_width // 2, screen_height // 2 - 100))  # poz na sliakta
        screen.blit(random_emotion, image_rect)


        text_surface = font.render("Која е оваа емоција?", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(text_surface, text_rect)


        pygame.draw.rect(screen, (200, 200, 200), (*BACK_BUTTON_POSITION, 200, 50), border_radius=10)
        back_text = font.render("Назад", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=(BACK_BUTTON_POSITION[0] + 100, BACK_BUTTON_POSITION[1] + 25))
        screen.blit(back_text, back_text_rect)


def main():
    active_window = None  # nema aktiven prozorec na pocetok
    image_surfaces = []  #prazen spisok na slikite
    random_emotion_display = False  #dali se prikaz slucajna emocija

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # izlez od igrata so escape
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # klik  na kopceto naazad
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # proverka za nazad
                if is_back_button_clicked(mouse_pos):
                    active_window = None  # nazad kon poceten prozor
                    random_emotion_display = False  #reset na random

                # proverka za klik za random
                if active_window == 4 and is_button_clicked(RANDOM_BUTTON_POSITION[0], RANDOM_BUTTON_POSITION[1], mouse_pos, 200, 50):
                    random_emotion_display = True  # aktiviraj prikaz na slucajna

                for i, position in enumerate(button_positions):
                    if is_button_clicked(position[0], position[1], mouse_pos):
                        active_window = i  # aktiviranje na prozorecot

        # Акako ima nekoj aktiven prozorec
        if active_window is not None:
            screen.fill((255, 255, 255))
            if active_window == 4:  # dali EMOCIONALNA INT e aktiven prozorec
                image_surfaces = draw_emotion_interaction_window()
            else:
                text_surface = font.render("Нов Прозорец: " + game_parts[active_window], True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(text_surface, text_rect)

            # samo kopceto za nazad
            pygame.draw.rect(screen, (200, 200, 200), (*BACK_BUTTON_POSITION, 200, 50), border_radius=10)
            back_text = font.render("Назад", True, (0, 0, 0))
            back_text_rect = back_text.get_rect(center=(BACK_BUTTON_POSITION[0] + 100, BACK_BUTTON_POSITION[1] + 25))
            screen.blit(back_text, back_text_rect)

        # ako se prikazuva slucajna random
        if random_emotion_display:
            display_random_emotion(image_surfaces)

        # ako nema aktiven prozorec togas osnovniot
        if active_window is None:
            screen.fill(BACKGROUND_COLOR)
            screen.blit(background_image, (0, 0))  # pozadinska slika
            draw_buttons()

        pygame.display.update()


if __name__ == "__main__":
    main()