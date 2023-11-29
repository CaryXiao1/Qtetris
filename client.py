"""
client.py

uses the functions and classes defined the engine folder to create a GUI that can be used
by a human player to record the number of points they have achieved versus the number of
moves they have made.
"""

import tkinter as tk
import numpy as np
from engine.playerboard import PlayerBoard

class TetrisCanvas(tk.Canvas):
    def __init__(self, root, w, h, score_str, moves_str):
        super().__init__(root, width=w, height=h, bg="black")
        # self.matrix = np.zeros((20, 10))
        self.board = PlayerBoard()
        self.score = 0
        self.num_moves = 0
        self.score_str = score_str
        self.moves_str = moves_str
        self.game_over = False

    def start_game(self):
        # draw line
        # render the starting pos of the
        self.board = PlayerBoard()
        self.score = 0
        self.num_moves = 0
        self.score_str.set("Score: 0")
        self.moves_str.set("# Moves: 0")
        self.update_game()
        self.game_over = False

    def do_move(self):
        if self.game_over: return
        points_added = self.board.turn()
        if points_added == -1:
            self.game_over = True
            return
        self.update_game()
        self.num_moves += 1
        self.moves_str.set("# Moves: " + str(self.num_moves))
        if points_added != 0:
            self.score += points_added
            self.score_str.set("Score: " + str(self.score))

    def left(self):
        self.board.set_move(0)
        self.do_move()

    def right(self):
        self.board.set_move(1)
        self.do_move()

    def rotate_left(self):
        self.board.set_move(2)
        self.do_move()

    def rotate_right(self):
        self.board.set_move(3)
        self.do_move()

    def do_nothing(self):
        self.board.set_move(4)
        self.do_move()

    # wrapper functions to eliminate event from keystrokes
    def left_keypress(self, _):
        self.left()
    def right_keypress(self, _):
        self.right()
    def do_nothing_keypress(self, _):
        self.do_nothing()
    def rotate_left_keypress(self, _):
        self.rotate_left()
    def rotate_right_keypress(self, _):
        self.rotate_right()

    def update_game(self):
        states = self.board.display_info() # TODO: replace that with Michael's function!
        self.delete("all")
        self.create_line(0, 120, 300, 120, fill="red")
        for i in range(20):
            for j in range(10):
                if states[i, j] != 0:
                    x1, x2 = 30 * j + 1, 30 * j + 30
                    y1, y2 = 30 * i + 1, 30 * i + 30
                    color = "gray" if states[i, j] == 1 else "red"
                    self.create_rectangle(x1, y1, x2, y2, fill=color)

class App:
    def print_click(self):
        print("Button clicked!")

    def __init__(self, root):
        self.root = root
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT)
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT)
        # create tracker for score
        score_str = tk.StringVar(right_frame, "Score: 0")
        score_label = tk.Label(right_frame, textvariable=score_str, height=2)
        score_label.pack()
        # create tracker for how many moves made
        moves_str = tk.StringVar(right_frame, "# Moves: 0")
        moves_label = tk.Label(right_frame, textvariable=moves_str, height=2)
        moves_label.pack()
        # create tetris board
        canvas = TetrisCanvas(left_frame, 300, 600, score_str, moves_str)
        canvas.pack()
        # movement buttons
        start = tk.Button(right_frame, text="Start Game!", command=canvas.start_game)
        left = tk.Button(right_frame, text="Left", command=canvas.left)
        right = tk.Button(right_frame, text="Right", command=canvas.right)
        do_nothing = tk.Button(right_frame, text="Pass", command=canvas.do_nothing)
        rotate_left = tk.Button(right_frame, text="Rotate Left", command=canvas.rotate_left)
        rotate_right = tk.Button(right_frame, text="Rotate Right", command=canvas.rotate_right)
        # add keybinds as well
        root.bind("a", canvas.left_keypress)
        root.bind("<Left>", canvas.left_keypress)
        root.bind("d", canvas.right_keypress)
        root.bind("<Right>", canvas.right_keypress)
        root.bind("s", canvas.do_nothing_keypress)
        root.bind("<Down>", canvas.do_nothing_keypress)
        root.bind("q", canvas.rotate_left_keypress)
        root.bind("e", canvas.rotate_right_keypress)
        # Add buttons below labels
        start.pack(pady=5, padx=5)
        left.pack(pady=5)
        right.pack(pady=5)
        do_nothing.pack(pady=5)
        rotate_left.pack(pady=5)
        rotate_right.pack(pady=5)


root = tk.Tk()
app = App(root)
root.geometry("435x700")
root.title("My Tkinter App")
root.mainloop()
