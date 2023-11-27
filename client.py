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
    def __init__(self, root, w, h):
        super().__init__(root, width=w, height=h, bg="black")
        # self.matrix = np.zeros((20, 10))
        self.board = PlayerBoard()

    def start_game(self):
        # TODO: add stuff like including buttons for move left and right and stuff
        pass
    
    def left(self):
        self.board.set_move(0)
        self.board.turn()

    def right(self):
        self.board.set_move(1)
        self.board.turn()
        self.update_game()
    
    def rotate_left(self):
        self.board.set_move(2)
        self.board.turn()
        self.update_game()

    def rotate_right(self):
        self.board.set_move(3)
        self.board.turn()
        self.update_game()

    def do_nothing(self):
        self.board.set_move(4)
        self.board.turn()
        self.update_game()

    def update_game(self):
        states = self.board.display_info() # TODO: replace that with Michael's function!
        self.delete("all")
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

        canvas = TetrisCanvas(left_frame, w=300, h=600)
        canvas.pack()

        # Create a button and place it in the window
        start = tk.Button(right_frame, text="Start Game!", command=canvas.start_game)
        left = tk.Button(right_frame, text="Left", command=canvas.left)
        right = tk.Button(right_frame, text="Right", command=canvas.right)
        do_nothing = tk.Button(right_frame, text="Pass", command=canvas.do_nothing)
        rotate_left = tk.Button(right_frame, text="Rotate Left", command=canvas.rotate_left)
        rotate_right = tk.Button(right_frame, text="Rotate Right", command=canvas.rotate_right)

        string_variable = tk.StringVar(right_frame, "# Moves: 0")
        
        label = tk.Label(right_frame, textvariable=string_variable, height=10)
        label.pack()

        start.pack(pady=5, padx=5)  # pady adds some vertical space around the button
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