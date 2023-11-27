import numpy as np

START_O = np.asarray([[0, 0, 0, 0],
                      [0, 1, 1, 0],
                      [0, 1, 1, 0],
                      [0, 0, 0, 0]])

START_T = np.asarray([[0, 0, 0],
                      [1, 1, 1],
                      [0, 1, 0]])

START_I = np.asarray([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [1, 1, 1, 1],
                      [0, 0, 0, 0]])

START_L = np.asarray([[0, 0, 0],
                      [1, 1, 1],
                      [0, 0, 1]])

START_J = np.asarray([[0, 0, 0],
                      [1, 1, 1],
                      [1, 0, 0]])

START_S = np.asarray([[0, 0, 0],
                      [0, 1, 1],
                      [1, 1, 0]])

START_Z = np.asarray([[0, 0, 0],
                      [1, 1, 0],
                      [0, 1, 1]])

def get_start_ori(piece_type):
    if self.cur_type == 'O':
        return START_O
    elif self.cur_type == 'T':
        return START_T
    elif self.cur_type == 'I':
        return START_I
    elif self.cur_type == 'L':
        return START_L
    elif self.cur_type == 'J':
        return START_J
    elif self.cur_type == 'S':
        return START_S
    elif self.cur_type == 'Z':
        return START_Z
    return None

def rotate_left_ori(piece_type, piece_ori):
    if piece_type in ['T', 'L', 'J']:
        return np.rot90(piece_ori)
    elif piece_type == 'O':
        return piece_ori
    elif piece_type == 'I':
        if np.array_equal(piece_ori, START_I): return np.rot90(piece_ori)
        return START_I
    elif piece_type == 'S':
        if np.array_equal(piece_ori, START_S): return np.rot90(piece_ori)
        return START_S
    elif piece_type == 'Z':
        if np.array_equal(piece_ori, START_Z): return np.rot90(piece_ori)
        return START_Z

def rotate_right_ori(piece_type, piece_ori):
    if piece_type in ['T', 'L', 'J']:
        return np.rot90(piece_ori, 3)
    elif piece_type == 'O':
        return piece_ori
    elif piece_type == 'I':
        if np.array_equal(piece_ori, START_I): return np.rot90(piece_ori)
        return START_I
    elif piece_type == 'S':
        if np.array_equal(piece_ori, START_S): return np.rot90(piece_ori)
        return START_S
    elif piece_type == 'Z':
        if np.array_equal(piece_ori, START_Z): return np.rot90(piece_ori)
        return START_Z

