import numpy as np
import tetromino_utils

class Board():
    def __init__(self):
        self.occupancy = np.zeros((20, 10), dtype=bool)
        self.cur_type = None
        self.next_type = None
        self.piece_r = None
        self.piece_c = None
        self.piece_ori = None

        self.gen_new_tetromino()
        self.gen_new_tetromino()

    def gen_new_tetromino(self):
        self.cur_type = self.next_type
        self.next_type = np.random.choice(['O', 'T', 'I', 'L', 'J', 'S', 'Z'])
        (self.piece_r, self.piece_c) = (0, 3)  # upper left corner of new piece

        self.piece_ori = get_start_ori(self.cur_type)

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
        submat = self.occupancy[r:r+side_len, c:c+side_len]

        # 2. do or of elementwise and of mat and submatrix
        return np.any(np.logical_and(mat, submat))

    def check_OOB(self, mat, r, c, side_len):  # true if piece OOB
        # TODO: implement me!

    def update_piece(self, player_input):
        new_c = self.piece_c
        new_ori = self.piece_ori

        if player_input == 0:
            new_c -= 1
        elif player_input == 1:
            new_c += 1
        elif player_input == 2:
            new_ori = rotate_left_ori(self.cur_type, self.piece_ori)
        elif player_input == 3:
            new_ori = rotate_right_ori(self.cur_type, self.piece_ori)

        # exit early if this input is invalid (ignore input)

        piece_width = len(self.piece_ori)
        if self.check_OOB(new_ori, self.piece_r, new_c, piece_width): return  # invalid
        if self.check_collision(new_ori, self.piece_r, new_c, piece_width): return  # invalid

        self.piece_c = new_c
        self.piece_ori = new_ori

    def gravity_piece(self):
        new_r = self.piece_r + 1
        piece_width = 3 + int(self.cur_type in ['I', 'O'])

        if (self.check_OOB(self.piece_ori, new_r, self.piece_c, piece_width) or
                self.check_collision(self.piece_ori, new_r, self.piece_c, piece_width)):
            return True  # piece cannot fall any further

        self.piece_r = new_r
        return False

    def turn(self):
        # 1. get an input from user
        player_input = self.get_input()

        # 2. execute input if it is possible
        self.update_piece(player_input)

        # 3. move down if possible
        hit_bottom = self.gravity_piece()

        # 3.1 if not possible, freeze piece
        if hit_bottom:
        # TODO: implement me!

        # 3.2 check if lines are cleared, and update occupancy accordingly
        # TODO: implement me!

        # 3.3 generate a new piece, and check if it is obstructed
        self.gen_new_tetromino()
        # TODO: implement me!

def main():
    b = Board()

if __name__ == '__main__':
    main()
