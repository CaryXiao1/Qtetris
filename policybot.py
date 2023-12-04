"""
policybot.py

Implements a class that given a file, will run games of miniTetris by extracting features from
the board, generating the proper number for the given state, looks at the given line in the policy
file and then picks that given state. 
"""
import numpy as np
from client import TetrisCanvas
# from engine import 

class Bot:
    def __init__(self, filename):
        f = open(filename)
        self.lines = f.readlines()
    
    def perform_action(self, canvas: TetrisCanvas):
        # pseudocode:
        #   1. get action 
        state = canvas.board.get_state()
        action = self.lines[state].strip()
        if action == '0':
            canvas.left()
        if action == '1':
            canvas.right()
        if action == '2':
            canvas.rotate_left()
        if action == '3':
            canvas.rotate_right()
        if action == '4':
            canvas.do_nothing()