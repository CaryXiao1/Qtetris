#!/usr/bin/env python3

"""
client.py

uses the functions and classes defined the engine folder to create a GUI that can be used
by a human player to record the number of points they have achieved versus the number of
moves they have made.
"""

import tkinter as tk
import numpy as np
from engine.miniplayerboard import MiniPlayerBoard
from app_utils.app_utils import TetrisCanvas

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
        # bot button labels
        rand_str = tk.StringVar(right_frame, "Start Rand Bot")
        ql_str = tk.StringVar(right_frame, "Start QL Bot")
        # create tetris board
        canvas = TetrisCanvas(left_frame, 200, 400, score_str, moves_str, rand_str, ql_str)
        canvas.pack()
        # movement and bot buttons
        start = tk.Button(right_frame, text="Start Game!", command=canvas.start_game)
        left = tk.Button(right_frame, text="Left", command=canvas.left)
        right = tk.Button(right_frame, text="Right", command=canvas.right)
        do_nothing = tk.Button(right_frame, text="Pass", command=canvas.do_nothing)
        rotate_left = tk.Button(right_frame, text="Rotate Left", command=canvas.rotate_left)
        rotate_right = tk.Button(right_frame, text="Rotate Right", command=canvas.rotate_right)
        rand = tk.Button(right_frame, textvariable=rand_str, command=canvas.toggle_rand)
        ql = tk.Button(right_frame, textvariable=ql_str, command=canvas.toggle_ql)

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
        rand.pack(pady=5)
        ql.pack(pady=5)


root = tk.Tk()
app = App(root)
root.geometry("435x500")
root.title("My Tkinter App")
root.mainloop()
