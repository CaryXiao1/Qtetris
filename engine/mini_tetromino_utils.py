import numpy as np

START_I = np.asarray([[0, 0, 0],
                      [1, 1, 1],
                      [0, 0, 0]])

START_L = np.asarray([[0, 1],
                      [1, 1]])

def get_start_ori(piece_type):
    if piece_type == 'I':
        return START_I
    elif piece_type == 'L':
        return START_L
    return None

def rotate_left_ori(piece_ori):
    return np.rot90(piece_ori)

def rotate_right_ori(piece_ori):
    return np.rot90(piece_ori, 3)
