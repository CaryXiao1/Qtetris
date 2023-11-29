import numpy as np
from .mini_tetromino_utils import *

class MiniBoard():
    def __init__(self):
        self.occupancy = np.zeros((8, 4), dtype=bool)
        self.cur_type = None
        self.piece_r = None
        self.piece_c = None
        self.piece_ori = None
        self.ori_number = 0

        self.gen_new_tetromino()

    def gen_new_tetromino(self):
        self.cur_type = np.random.choice(['L', 'I'])
        (self.piece_r, self.piece_c) = (0, 1)  # upper left corner of new piece

        self.piece_ori = get_start_ori(self.cur_type)
        self.ori_number = 0

    def get_input(self):
        ''' input options:
        0 : translate left
        1 : translate right
        2 : rotate counter-clockwise
        3 : rotate clockwise
        4 : do nothing '''

        return np.random.randint(5)

    def check_collision(self, mat, r, c, side_len):  # true if collision
        # 1. extract submatrix from occupancy with correct size
        submat = np.pad(self.occupancy, 2, 'constant', constant_values=False)[r+2:r+2+side_len, c+2:c+2+side_len]

        # 2. do or of elementwise and of mat and submatrix
        return np.any(np.logical_and(mat, submat))

    def check_OOB(self, mat, r, c, side_len):  # true if piece OOB
        # 1. generate submatrix where elements indicate OOB
        in_bounds = np.zeros((8, 4), dtype=bool)
        submat = np.pad(in_bounds, 2, 'constant', constant_values=True)[r+2:r+2+side_len, c+2:c+2+side_len]

        # 2. do or of elementwise and of mat and submatrix
        return np.any(np.logical_and(mat, submat))

    def freeze(self, mat, r, c, side_len):  # overwrite occupancy with positive values in mat
        OOB_buffer = np.pad(self.occupancy, 2, 'constant', constant_values=False)
        OOB_buffer[r+2:r+2+side_len, c+2:c+2+side_len] = np.logical_or(OOB_buffer[r+2:r+2+side_len, c+2:c+2+side_len], mat)
        self.occupancy = OOB_buffer[2:10, 2:6]

    def update_piece(self, player_input):
        new_c = self.piece_c
        new_ori = self.piece_ori

        if player_input == 0:
            new_c -= 1
        elif player_input == 1:
            new_c += 1
        elif player_input == 2:
            new_ori = rotate_left_ori(self.piece_ori)
        elif player_input == 3:
            new_ori = rotate_right_ori(self.piece_ori)

        # exit early if this input is invalid (ignore input)

        piece_width = len(self.piece_ori)
        if self.check_OOB(new_ori, self.piece_r, new_c, piece_width): return  # invalid
        if self.check_collision(new_ori, self.piece_r, new_c, piece_width): return  # invalid

        self.piece_c = new_c
        self.piece_ori = new_ori

        # bookkeeping for generating state number
        if player_input == 2: self.ori_number = (self.ori_number + 1) % 4
        elif player_input == 3: self.ori_number = (self.ori_number - 1) % 4

    def gravity_piece(self):
        new_r = self.piece_r + 1
        piece_width = len(self.piece_ori)

        if (self.check_OOB(self.piece_ori, new_r, self.piece_c, piece_width) or
                self.check_collision(self.piece_ori, new_r, self.piece_c, piece_width)):
            return True  # piece cannot fall any further

        self.piece_r = new_r
        return False

    def turn(self):
        filled_lines = 0

        # 1. get an input from user
        player_input = self.get_input()

        # 2. execute input if it is possible
        self.update_piece(player_input)

        # 3. move down if possible
        hit_bottom = self.gravity_piece()

        # 3.1 if not possible, freeze piece
        if hit_bottom:
            self.freeze(self.piece_ori, self.piece_r, self.piece_c, len(self.piece_ori))

            # 3.2 check if lines are cleared, and update occupancy accordingly
            for i in range(8):
                if np.all(self.occupancy[i - filled_lines, :]):
                    self.occupancy = np.delete(self.occupancy, i - filled_lines, 0)
                    filled_lines += 1

            for i in range(filled_lines):
                self.occupancy = np.vstack([np.zeros((4), dtype=bool), self.occupancy])

            # 3.3 generate a new piece, and check if it is obstructed
            self.gen_new_tetromino()
            if self.check_collision(self.piece_ori, self.piece_r, self.piece_c, len(self.piece_ori)):
                return -1  # game end

        return filled_lines ** 2  # score earned this move

    '''
    piece state is represented with
    5 bits per column * 10 columns
    4 + 5 bits for current piece column and row
    3 bits for current piece type
    2 bits for current piece orientation
    = 64 bits
    '''
    def get_state(self):
        out = 0
        bit = 0

        for c in range(4):
            for r in range(8):
                if self.occupancy[r, c]:
                    out += r << bit
                    break
                bit += 3

        out += self.piece_c << bit
        bit += 2

        out += self.piece_r << bit
        bit += 3

        out += int(self.cur_type == 'L') << bit
        bit += 1

        out += self.ori_number << bit
        return out

def main():
    b = Board()

if __name__ == '__main__':
    main()
