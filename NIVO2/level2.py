# location_game.py
import pygame
import random
import sys
from pygame.locals import *


class LocationGame:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = None
        self.current_step = 0
        self.total_steps = 0
        self.instructions = []
        self.objects = []
        self.locations = []
        self.drop_zones = []
        self.dragging = False
        self.dragged_obj = None
        self.drag_offset = (0, 0)  # Store offset from mouse to object center
        self.load_images()
        self.initial_positions = {}

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 100, 255)
        self.GREEN = (0, 200, 0)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.PURPLE = (155, 89, 182)

        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)

        # Game state
        self.state = "level_select"  # 'level_select', 'playing', 'completed'

    def load_images(self):
        try:

            self.ball_img = pygame.image.load("../Pictures-Game2/ball.png")
            self.ball_img = pygame.transform.scale(self.ball_img, (160, 160))

            self.book_img = pygame.image.load("../Pictures-Game2/book.png")
            self.book_img = pygame.transform.scale(self.book_img, (160, 120))

            self.cup_img = pygame.image.load("../Pictures-Game2/cup.png")
            self.cup_img = pygame.transform.scale(self.cup_img, (120, 160))


            self.table_img = pygame.image.load("../Pictures-Game2/table.png")
            self.table_img = pygame.transform.scale(self.table_img, (400, 300))

            self.chair_img = pygame.image.load("../Pictures-Game2/chair.png")
            self.chair_img = pygame.transform.scale(self.chair_img, (240, 360))

            self.box_img = pygame.image.load("../Pictures-Game2/box.png")
            self.box_img = pygame.transform.scale(self.box_img, (300, 300))

            # Background
            self.bg_img = pygame.image.load("../Pictures-Game2/room-image.jpg")
            self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))
        except:
            # Create placeholders if images not found
            self.create_placeholders()

    def create_placeholders(self):
        self.ball_img = pygame.Surface((160, 160))
        self.ball_img.fill((255, 107, 107))  # Light red

        self.book_img = pygame.Surface((160, 120))
        self.book_img.fill((78, 205, 196))  # Teal

        self.cup_img = pygame.Surface((120, 160))
        self.cup_img.fill((69, 183, 209))  # Light blue

        self.table_img = pygame.Surface((400, 300))
        self.table_img.fill((139, 69, 19))  # Brown

        self.chair_img = pygame.Surface((240, 360))
        self.chair_img.fill((101, 67, 33))  # Dark brown

        self.box_img = pygame.Surface((300, 300))
        self.box_img.fill((210, 105, 30))  # Chocolate

        self.bg_img = pygame.Surface((self.width, self.height))
        self.bg_img.fill((230, 230, 250))  # Lavender

    def setup_easy_level(self):
        self.current_level = "easy"
        self.current_step = 0
        self.total_steps = 1
        self.instructions = ["Стави ја топката ПОД масата"]

        # Clear existing objects
        self.objects = []
        self.locations = []
        self.drop_zones = []

        # Create table
        table_x = self.width // 2
        table_y = self.height // 2 - 50
        table_rect = pygame.Rect(table_x - 200, table_y - 150, 400, 300)
        self.locations.append(("table", table_rect, self.table_img))

        # Create drop zone under table
        drop_rect = pygame.Rect(table_x - 150, table_y + 30, 300, 130)
        self.drop_zones.append(("under_table", drop_rect))

        # Create ball
        ball_rect = pygame.Rect(self.width // 2 - 80, self.height - 150, 160, 160)
        self.objects.append(("ball", ball_rect, self.ball_img))
        self.initial_positions["ball"] = ball_rect.copy()

        self.state = "playing"

    def setup_medium_level(self):
        self.current_level = "medium"
        self.current_step = 0
        self.total_steps = 2
        self.instructions = [
            "Стави ја топката ПОД масата",
            "Стави ја книгата НА столот"
        ]

        # Clear existing objects
        self.objects = []
        self.locations = []
        self.drop_zones = []

        # Create table
        table_x = self.width // 3
        table_y = self.height // 2 - 50
        table_rect = pygame.Rect(table_x - 200, table_y - 150, 400, 300)
        self.locations.append(("table", table_rect, self.table_img))

        # Create chair
        chair_x = (self.width // 3) * 2
        chair_y = self.height // 2
        chair_rect = pygame.Rect(chair_x - 120, chair_y - 180, 240, 360)
        self.locations.append(("chair", chair_rect, self.chair_img))

        # Create drop zones
        drop_rect1 = pygame.Rect(table_x - 120, table_y + 50, 240, 65)  # Under table
        drop_rect2 = pygame.Rect(chair_x - 80, chair_y - 70, 160, 60)  # On chair
        self.drop_zones.append(("under_table", drop_rect1))
        self.drop_zones.append(("on_chair", drop_rect2))

        # Create objects
        ball_rect = pygame.Rect(self.width // 4 - 80, self.height - 150, 160, 160)
        book_rect = pygame.Rect((self.width // 4) * 3 - 80, self.height - 130, 160, 120)
        self.objects.append(("ball", ball_rect, self.ball_img))
        self.objects.append(("book", book_rect, self.book_img))

        # Store initial positions
        self.initial_positions["ball"] = ball_rect.copy()
        self.initial_positions["book"] = book_rect.copy()

        self.state = "playing"

    def setup_hard_level(self):
        self.current_level = "hard"
        self.current_step = 0
        self.total_steps = 3
        self.instructions = [
            "Стави ја топката ПОД масата",
            "Стави ја книгата НА столот",
            "Стави ја чашата ВО кутијата"
        ]

        # Clear existing objects
        self.objects = []
        self.locations = []
        self.drop_zones = []

        # Create table
        table_x = self.width // 4
        table_y = self.height // 2 - 50
        table_rect = pygame.Rect(table_x - 200, table_y - 150, 400, 300)
        self.locations.append(("table", table_rect, self.table_img))

        # Create chair
        chair_x = self.width // 2
        chair_y = self.height // 2
        chair_rect = pygame.Rect(chair_x - 120, chair_y - 180, 240, 360)
        self.locations.append(("chair", chair_rect, self.chair_img))

        # Create box
        box_x = (self.width // 4) * 3
        box_y = self.height // 2
        box_rect = pygame.Rect(box_x - 150, box_y - 150, 300, 300)
        self.locations.append(("box", box_rect, self.box_img))

        # Create drop zones
        drop_rect1 = pygame.Rect(table_x - 110, table_y + 60, 220, 90)  # Under table
        drop_rect2 = pygame.Rect(chair_x - 60, chair_y - 70, 120, 60)  # On chair
        drop_rect3 = pygame.Rect(box_x - 75, box_y - 90, 150, 140)  # In box
        self.drop_zones.append(("under_table", drop_rect1))
        self.drop_zones.append(("on_chair", drop_rect2))
        self.drop_zones.append(("in_box", drop_rect3))

        # Create objects
        ball_rect = pygame.Rect(self.width // 5 - 80, self.height - 150, 160, 160)
        book_rect = pygame.Rect(self.width // 2 - 80, self.height - 130, 160, 120)
        cup_rect = pygame.Rect((self.width // 5) * 4 - 60, self.height - 150, 120, 160)
        self.objects.append(("ball", ball_rect, self.ball_img))
        self.objects.append(("book", book_rect, self.book_img))
        self.objects.append(("cup", cup_rect, self.cup_img))

        # Store initial positions
        self.initial_positions["ball"] = ball_rect.copy()
        self.initial_positions["book"] = book_rect.copy()
        self.initial_positions["cup"] = cup_rect.copy()

        self.state = "playing"

    def get_target_object_for_step(self):
        """Returns the object name that should be moved in the current step"""
        if self.current_step == 0:
            return "ball"
        elif self.current_step == 1:
            return "book"
        elif self.current_step == 2:
            return "cup"
        return None

    def check_drop(self, pos, dragged_object):
        """Check if the dragged object is dropped in the correct zone for current step"""
        target_object = self.get_target_object_for_step()

        # Only allow correct object for current step
        if dragged_object != target_object:
            return False

        if self.current_level == "easy":
            if self.current_step == 0:  # Ball under table
                for zone in self.drop_zones:
                    if zone[0] == "under_table" and zone[1].collidepoint(pos):
                        return True

        elif self.current_level == "medium":
            if self.current_step == 0:  # Ball under table
                for zone in self.drop_zones:
                    if zone[0] == "under_table" and zone[1].collidepoint(pos):
                        return True
            elif self.current_step == 1:  # Book on chair
                for zone in self.drop_zones:
                    if zone[0] == "on_chair" and zone[1].collidepoint(pos):
                        return True

        elif self.current_level == "hard":
            if self.current_step == 0:  # Ball under table
                for zone in self.drop_zones:
                    if zone[0] == "under_table" and zone[1].collidepoint(pos):
                        return True
            elif self.current_step == 1:  # Book on chair
                for zone in self.drop_zones:
                    if zone[0] == "on_chair" and zone[1].collidepoint(pos):
                        return True
            elif self.current_step == 2:  # Cup in box
                for zone in self.drop_zones:
                    if zone[0] == "in_box" and zone[1].collidepoint(pos):
                        return True

        return False

    def show_message(self, text, color):
        msg_surface = self.font_medium.render(text, True, self.BLACK)
        msg_rect = msg_surface.get_rect(center=(self.width // 2, 150))

        # Draw background
        bg_rect = msg_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, color, bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, bg_rect, 2, border_radius=10)

        self.screen.blit(msg_surface, msg_rect)
        pygame.display.flip()
        pygame.time.delay(1500)  # Show message for 1.5 seconds

    def reset_object_position(self, obj_name):
        """Reset object to its initial or current valid position"""
        for i, obj in enumerate(self.objects):
            if obj[0] == obj_name:
                # Reset to initial position
                self.objects[i] = (obj[0], self.initial_positions[obj[0]].copy(), obj[2])
                break

    def draw_level_selection(self):
        self.screen.blit(self.bg_img, (0, 0))

        # Title
        title = self.font_large.render("Игра со локации - Избери ниво", True, self.BLACK)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))

        # Level buttons
        easy_rect = pygame.Rect(self.width // 2 - 150, 200, 300, 60)
        pygame.draw.rect(self.screen, self.GREEN, easy_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, easy_rect, 2, border_radius=10)
        easy_text = self.font_medium.render("ЛЕСНО (1 предмет, 1 место)", True, self.WHITE)
        self.screen.blit(easy_text, (easy_rect.centerx - easy_text.get_width() // 2,
                                     easy_rect.centery - easy_text.get_height() // 2))

        medium_rect = pygame.Rect(self.width // 2 - 150, 280, 300, 60)
        pygame.draw.rect(self.screen, self.YELLOW, medium_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, medium_rect, 2, border_radius=10)
        medium_text = self.font_medium.render("СРЕДНО (2 предмети, 2 места)", True, self.BLACK)
        self.screen.blit(medium_text, (medium_rect.centerx - medium_text.get_width() // 2,
                                       medium_rect.centery - medium_text.get_height() // 2))

        hard_rect = pygame.Rect(self.width // 2 - 150, 360, 300, 60)
        pygame.draw.rect(self.screen, self.RED, hard_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, hard_rect, 2, border_radius=10)
        hard_text = self.font_medium.render("ТЕШКО (3 предмети, 3 места)", True, self.WHITE)
        self.screen.blit(hard_text, (hard_rect.centerx - hard_text.get_width() // 2,
                                     hard_rect.centery - hard_text.get_height() // 2))

        # Back button
        back_rect = pygame.Rect(20, self.height - 70, 200, 50)
        pygame.draw.rect(self.screen, self.BLUE, back_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, back_rect, 2, border_radius=10)
        back_text = self.font_medium.render("Назад кон мени", True, self.WHITE)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))



        pygame.display.flip()
        return easy_rect, medium_rect, hard_rect, back_rect

    def draw_game(self):
        self.screen.blit(self.bg_img, (0, 0))

        # Level title
        level_names = {"easy": "ЛЕСНО", "medium": "СРЕДНО", "hard": "ТЕШКО"}
        level_display = level_names.get(self.current_level, "").upper()
        level_text = self.font_large.render(f"Ниво: {level_display}", True, self.BLACK)

        self.screen.blit(level_text, (20, 20))

        # Instruction
        instr_text = self.font_medium.render(self.instructions[self.current_step], True, self.BLACK)
        self.screen.blit(instr_text, (self.width // 2 - instr_text.get_width() // 2, 100))

        # Draw locations
        for loc in self.locations:
            self.screen.blit(loc[2], loc[1])

        # Draw all objects
        for obj in self.objects:
            self.screen.blit(obj[2], obj[1])

        # Back button
        back_rect = pygame.Rect(20, self.height - 70, 200, 50)
        pygame.draw.rect(self.screen, self.BLUE, back_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, back_rect, 2, border_radius=10)
        back_text = self.font_medium.render("Назад кон нивоа", True, self.WHITE)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))

        # Главно мени копче


        pygame.display.flip()
        return back_rect

    def draw_completed(self):
        self.screen.blit(self.bg_img, (0, 0))

        # Completion message
        complete_text = self.font_large.render("Браво! Го завршивте нивото!", True, self.BLACK)
        self.screen.blit(complete_text, (self.width // 2 - complete_text.get_width() // 2,
                                         self.height // 2 - 50))

        # Next level button
        if self.current_level == "easy":
            btn_text = "Следно ниво (Средно)"
        elif self.current_level == "medium":
            btn_text = "Следно ниво (Тешко)"

        else:
            btn_text = "Заврши"

        next_rect = pygame.Rect(self.width // 2 - 150, self.height // 2 + 50, 300, 60)
        pygame.draw.rect(self.screen, self.PURPLE, next_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, next_rect, 2, border_radius=10)
        next_text = self.font_medium.render(btn_text, True, self.WHITE)
        self.screen.blit(next_text, (next_rect.centerx - next_text.get_width() // 2,
                                     next_rect.centery - next_text.get_height() // 2))

        # Back to levels button
        back_rect = pygame.Rect(self.width // 2 - 150, self.height // 2 + 130, 300, 60)
        pygame.draw.rect(self.screen, self.BLUE, back_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, back_rect, 2, border_radius=10)
        back_text = self.font_medium.render("Назад кон нивоа", True, self.WHITE)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2,
                                     back_rect.centery - back_text.get_height() // 2))

        pygame.display.flip()
        return next_rect, back_rect

    def run(self):
        easy_rect, medium_rect, hard_rect, back_rect = self.draw_level_selection()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return "quit"

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                        return "menu"

                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.state == "level_select":
                        if easy_rect.collidepoint(pos):
                            self.setup_easy_level()
                            back_rect = self.draw_game()
                        elif medium_rect.collidepoint(pos):
                            self.setup_medium_level()
                            back_rect = self.draw_game()
                        elif hard_rect.collidepoint(pos):
                            self.setup_hard_level()
                            back_rect = self.draw_game()
                        elif back_rect.collidepoint(pos):
                            self.running = False
                            return "menu"


                    elif self.state == "playing":
                        if back_rect.collidepoint(pos):
                            self.state = "level_select"
                            easy_rect, medium_rect, hard_rect, back_rect = self.draw_level_selection()
                        else:
                            # Check if clicked on an object
                            for obj in self.objects:
                                if obj[1].collidepoint(pos):
                                    self.dragging = True
                                    self.dragged_obj = obj[0]
                                    # Calculate offset from mouse to object center
                                    self.drag_offset = (obj[1].centerx - pos[0], obj[1].centery - pos[1])
                                    break

                    elif self.state == "completed":
                        if next_rect.collidepoint(pos):
                            if self.current_level == "easy":
                                self.setup_medium_level()
                                back_rect = self.draw_game()
                            elif self.current_level == "medium":
                                self.setup_hard_level()
                                back_rect = self.draw_game()
                            else:
                                self.state = "level_select"
                                easy_rect, medium_rect, hard_rect, back_rect = self.draw_level_selection()
                        elif back_rect.collidepoint(pos):
                            self.state = "level_select"
                            easy_rect, medium_rect, hard_rect, back_rect = self.draw_level_selection()

                elif event.type == MOUSEBUTTONUP and self.dragging:
                    self.dragging = False
                    pos = pygame.mouse.get_pos()

                    if self.check_drop(pos, self.dragged_obj):
                        # Correct drop - move to correct position
                        for zone in self.drop_zones:
                            if ((self.current_step == 0 and zone[0] == "under_table") or
                                    (self.current_step == 1 and zone[0] == "on_chair") or
                                    (self.current_step == 2 and zone[0] == "in_box")):
                                if zone[1].collidepoint(pos):
                                    # Update object position to drop zone center
                                    for i, obj in enumerate(self.objects):
                                        if obj[0] == self.dragged_obj:
                                            new_rect = obj[1].copy()
                                            new_rect.center = zone[1].center
                                            self.objects[i] = (obj[0], new_rect, obj[2])
                                            # Update initial position so it stays there
                                            self.initial_positions[obj[0]] = new_rect.copy()
                                            break
                                    break

                        self.current_step += 1
                        if self.current_step >= self.total_steps:
                            self.state = "completed"
                            next_rect, back_rect = self.draw_completed()
                        else:
                            self.show_message("Точно! Продолжете со следниот чекор.", self.GREEN)
                            back_rect = self.draw_game()
                    else:
                        # Wrong drop - reset to original position
                        self.show_message("Погрешно место. Обидете се повторно.", self.RED)
                        self.reset_object_position(self.dragged_obj)
                        back_rect = self.draw_game()

                    self.dragged_obj = None

                elif event.type == MOUSEMOTION and self.dragging:
                    # Update the dragged object's position smoothly
                    for i, obj in enumerate(self.objects):
                        if obj[0] == self.dragged_obj:
                            new_rect = obj[1].copy()
                            # Use offset to maintain grab point
                            new_rect.centerx = event.pos[0] + self.drag_offset[0]
                            new_rect.centery = event.pos[1] + self.drag_offset[1]
                            self.objects[i] = (obj[0], new_rect, obj[2])
                            break
                    back_rect = self.draw_game()

            self.clock.tick(60)

        return "menu"