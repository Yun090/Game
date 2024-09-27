 import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title('2048')
        self.board = [[0] * 4 for i in range(4)]
        self.score = 0
        self.high_score = 0
        self.high_score_label = tk.Label(master, text="High Score: 0")
        self.high_score_label.grid(row=0, column=0, columnspan=2)
        self.score_label = tk.Label(master, text="Score: 0")
        self.score_label.grid(row=0, column=2, columnspan=2)
        self.restart_button = None  # Define restart_button initially as None
        self.initialize_game()
        self.master.bind("<Key>", self.key_down)

    def initialize_game(self):
        self.board = [[0] * 4 for i in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.draw_board()

        if self.restart_button:
            self.restart_button.grid_forget()  # Hide the restart button if it's already there

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if not empty_cells:
            return
        i, j = random.choice(empty_cells)
        self.board[i][j] = 2 if random.random() < 0.9 else 4

    def draw_board(self):
        for i in range(4):
            for j in range(4):
                tile_value = self.board[i][j]
                color = self.get_color(tile_value)
                tile = tk.Label(self.master, text=str(tile_value) if tile_value != 0 else '', 
                                width=4, height=2, padx=10, pady=10, 
                                font=("Helvetica", 24, "bold"), 
                                bg=color, fg="black" if tile_value <= 4 else "white")
                tile.grid(row=i + 1, column=j, padx=5, pady=5)
        self.update_score_labels()

    def get_color(self, value):
        colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")

    def update_score_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def key_down(self, event):
        key_action = {
            'w': self.move_up,
            's': self.move_down,
            'a': self.move_left,
            'd': self.move_right,
            'Up': self.move_up,
            'Down': self.move_down,
            'Left': self.move_left,
            'Right': self.move_right,
        }

        if event.keysym in key_action:
            prev_board = [row[:] for row in self.board]
            key_action[event.keysym]()
            if self.board != prev_board:
                self.add_new_tile()
                self.update_score()
                self.draw_board()
                if self.check_game_over():
                    self.game_over()

    def move_left(self):
        for i in range(4):
            self.board[i] = self.merge(self.board[i])

    def move_right(self):
        for i in range(4):
            self.board[i] = self.merge(self.board[i][::-1])[::-1]

    def move_up(self):
        self.board = [list(row) for row in zip(*self.board)]
        self.move_left()
        self.board = [list(row) for row in zip(*self.board)]

    def move_down(self):
        self.board = [list(row) for row in zip(*self.board)]
        self.move_right()
        self.board = [list(row) for row in zip(*self.board)]

    def merge(self, row):
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row[i + 1] = 0
        new_row = [i for i in new_row if i != 0]
        return new_row + [0] * (4 - len(new_row))

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or \
                   (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        return True

    def game_over(self):
        game_over_label = tk.Label(self.master, text="Game Over!", bg="#ff0000", fg="#ffffff", font=("Helvetica", 48, "bold"))
        game_over_label.grid(row=2, column=0, columnspan=4)
        self.master.unbind("<Key>")  # Disable further key presses

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=4, pady=20)

    def restart_game(self):
        # Remove game over label
        for widget in self.master.grid_slaves():
            if int(widget.grid_info()["row"]) == 2 and int(widget.grid_info()["column"]) == 0:
                widget.grid_forget()

        self.master.bind("<Key>", self.key_down)
        self.initialize_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
