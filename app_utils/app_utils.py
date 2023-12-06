"""
app_utils.py

Implements a class that given a file, will run games of miniTetris by extracting features from
the board, generating the proper number for the given state, looks at the given line in the policy
file and then picks that given state. 
"""
QL_FILENAME = 'app_utils/ql.policy'
RAND_FILENAME = 'app_utils/rand.policy'

BOT_TIMESTEP = 10 # milliseconds to wait before each next move is performed by bots

# constants for gathering data
RAND_POINTS_OUT = 'result/random_total_score.csv'
RAND_RATIO_OUT = 'result/random_score_ratio.csv'

QL_POINTS_OUT = 'result/ql_total_score.csv'
QL_RATIO_OUT = 'result/ql_score_ratio.csv'

import numpy as np
import tkinter as tk
from engine.miniplayerboard import MiniPlayerBoard


class TetrisCanvas(tk.Canvas):
    def __init__(self, root, w, h, score_str, moves_str, rand_bot_str, ql_bot_str):
        super().__init__(root, width=w, height=h, bg="black")
        self.board = MiniPlayerBoard()
        self.root = root
        self.score = 0
        self.num_moves = 0
        self.score_str = score_str
        self.moves_str = moves_str
        self.rand_bot_str = rand_bot_str
        self.ql_bot_str = ql_bot_str
        self.bot_running = 0 # set to 0 for player control, 1 for random bot and 2 for ql bot
        self.game_over = False
        self.ql_bot = Bot(QL_FILENAME)
        self.rand_bot = Bot(RAND_FILENAME)

    # def __init__(self, bot_filename):
    #     self.board = MiniPlayerBoard()
    #     self.score = 0
    #     self.num_moves = 0
    #     self.score_str = None
    #     self.bot_running = 0 # set to 0 for player control, 1 for random bot and 2 for ql bot
    #     self.game_over = False
    #     self.rand_bot = Bot(bot_filename)

    def start_game(self):
        # (for storing the total score from a bot)
        if self.bot_running == 1:
            score = self.score
            moves = self.num_moves
            f_score = open(RAND_POINTS_OUT, "a")  # append mode
            f_moves = open(RAND_RATIO_OUT, "a")
            f_score.write(score + ',')
            f_moves.write(str(float(score) / float(moves)) + ',') 
            f_score.close()
            f_moves.close()
        if self.bot_running == 2:
            score = self.score_str.get()[self.score_str.get().find(' ') + 1:]
            moves = self.moves_str.get()[self.moves_str.get().find(':') + 2:]
            f_score = open(QL_POINTS_OUT, "a")  # append mode
            f_moves = open(QL_RATIO_OUT, "a")
            f_score.write(score + ',')
            f_moves.write(str(float(score) / float(moves)) + ',') 
            f_score.close()
            f_moves.close()

        self.board = MiniPlayerBoard()
        self.score = 0
        self.num_moves = 0
        self.score_str.set("Score: 0")
        self.moves_str.set("# Moves: 0")
        self.update_game()
        self.game_over = False

    def do_move(self):
        if self.game_over: return
        points_added = self.board.turn()
        if points_added == -100:
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
        return self.do_move()

    def right(self):
        self.board.set_move(1)
        return self.do_move()

    def rotate_left(self):
        self.board.set_move(2)
        return self.do_move()

    def rotate_right(self):
        self.board.set_move(3)
        return self.do_move()

    def do_nothing(self):
        self.board.set_move(4)
        return self.do_move()

    # wrapper functions to eliminate event from keystrokes
    def left_keypress(self, _):
        if self.bot_running != 0: return
        self.left()
    def right_keypress(self, _):
        if self.bot_running != 0: return
        self.right()
    def do_nothing_keypress(self, _):
        if self.bot_running != 0: return
        self.do_nothing()
    def rotate_left_keypress(self, _):
        if self.bot_running != 0: return
        self.rotate_left()
    def rotate_right_keypress(self, _):
        if self.bot_running != 0: return
        self.rotate_right()

    def update_game(self):
        states = self.board.display_info()
        self.delete("all")
        self.create_line(0, 100, 200, 100, fill="red")
        for i in range(8):
            for j in range(4):
                if states[i, j] != 0:
                    x1, x2 = 50 * j + 1, 50 * j + 50
                    y1, y2 = 50 * i + 1, 50 * i + 50
                    color = "gray" if states[i, j] == 1 else "red"
                    self.create_rectangle(x1, y1, x2, y2, fill=color)

    # toggles for bots
    def toggle_rand(self):
        if self.bot_running == 2: return
        elif self.bot_running == 0:
            self.bot_running = 1
            self.rand_bot_str.set("Stop Rand Bot")
            self.run_rand()
        elif self.bot_running == 1:
            self.bot_running = 0
            self.rand_bot_str.set("Start Rand Bot")
        
    def toggle_ql(self):
        if self.bot_running == 1: return
        elif self.bot_running == 0:
            self.bot_running = 2
            self.ql_bot_str.set("Stop QL Bot")
            self.run_ql()
        elif self.bot_running == 2:
            self.bot_running = 0
            self.ql_bot_str.set("Start QL Bot")

    def run_rand(self):
        if self.bot_running != 1: return
        self.rand_bot.perform_action(self)
        self.root.after(BOT_TIMESTEP, self.run_rand)

    def run_ql(self):
        if self.bot_running != 2: return
        self.ql_bot.perform_action(self)
        self.after(BOT_TIMESTEP, self.run_ql)

    

class Bot:
    def __init__(self, filename):
        f = open(filename)
        self.lines = f.readlines()
    
    def perform_action(self, canvas: TetrisCanvas):
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
