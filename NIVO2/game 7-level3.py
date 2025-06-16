import tkinter as tk
import random

# Maze levels: 0 = path, 1 = wall, 2 = goal
MAZES = [
    [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 2, 1],
        [1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 2, 1],
        [1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
]

CELL_SIZE = 80
PLAYER_COLOR = "#3498db"
GOAL_COLOR = "#2ecc71"
WALL_COLOR = "#34495e"
PATH_COLOR = "#ecf0f1"
MESSAGE_BG = "#1abc9c"
MESSAGE_FG = "white"
CONFETTI_COLORS = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]


class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.title("Maze Game - Просторен Однос")

        # Frame for message display
        self.message_frame = tk.Frame(root, bg=MESSAGE_BG)
        self.message_frame.pack(fill=tk.X)

        self.message_label = tk.Label(
            self.message_frame, text="Добредојде! Користи ги стрелките за движење.",
            font=("Arial", 18, "bold"), bg=MESSAGE_BG, fg=MESSAGE_FG, pady=10
        )
        self.message_label.pack()

        # Canvas for the maze
        self.canvas = tk.Canvas(root, bg=PATH_COLOR)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.level = 0
        self.player_pos = [1, 1]

        self.start_level()

        # Bind keyboard controls
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    def start_level(self):
        self.canvas.delete("all")
        self.player_pos = [1, 1]
        self.maze = MAZES[self.level]

        # Adjust canvas size based on maze dimensions
        self.canvas_width = CELL_SIZE * len(self.maze[0])
        self.canvas_height = CELL_SIZE * len(self.maze)
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

        # Center the maze on the screen
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.create_maze()
        self.draw_player()
        self.update_message(f"Ниво {self.level + 1}: Користи ги стрелките за движење!")

    def create_maze(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                if self.maze[row][col] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, outline="white")
                elif self.maze[row][col] == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=GOAL_COLOR, outline="white")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=PATH_COLOR, outline="white")

    def draw_player(self):
        x, y = self.player_pos
        x1, y1 = x * CELL_SIZE + 10, y * CELL_SIZE + 10
        x2, y2 = x1 + CELL_SIZE - 20, y1 + CELL_SIZE - 20
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill=PLAYER_COLOR)

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        # Check boundaries and walls
        if self.maze[new_y][new_x] != 1:
            self.player_pos = [new_x, new_y]
            self.canvas.move(self.player, dx * CELL_SIZE, dy * CELL_SIZE)

        # Check if reached the goal
        if self.maze[new_y][new_x] == 2:
            self.level_up()

    def level_up(self):
        if self.level < len(MAZES) - 1:
            self.show_confetti()
            self.level += 1
            self.root.after(2000, self.start_level)
        else:
            self.show_confetti()
            self.update_message("Честитки! Ги заврши сите нивоа!")
            self.root.after(3000, self.root.destroy)

    def move_up(self, event):
        self.move_player(0, -1)

    def move_down(self, event):
        self.move_player(0, 1)

    def move_left(self, event):
        self.move_player(-1, 0)

    def move_right(self, event):
        self.move_player(1, 0)

    def update_message(self, text):
        self.message_label.config(text=text)

    def show_confetti(self):
        for _ in range(50):
            x = random.randint(0, self.canvas_width)
            y = random.randint(0, self.canvas_height)
            size = random.randint(5, 15)
            color = random.choice(CONFETTI_COLORS)
            self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color, outline=""
            )


if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
