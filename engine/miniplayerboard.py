from .miniboard import MiniBoard

class MiniPlayerBoard(MiniBoard):
    def __init__(self, *args):
        assert 0 <= len(args) < 2
        self.move = 4
        if len(args) == 0: super().__init__()
        else: super().__init__(args[0])

    ''' input options:
    0 : translate left
    1 : translate right
    2 : rotate counter-clockwise
    3 : rotate clockwise
    4 : do nothing '''

    def set_move(self, move: int):
        self.move = move

    # overwritten method
    def get_input(self):
        return self.move

    # call self.turn to make a turn given the input

    ''' 0 : unoccupied
        1 : frozen tile
        2 : current controlled piece occupies this tile '''

    def display_info(self):
        out = self.occupancy.astype(int)

        for r_off in range(len(self.piece_ori)):
            for c_off in range(len(self.piece_ori)):
                if self.piece_ori[r_off, c_off]:
                    out[self.piece_r + r_off, self.piece_c + c_off] = 2

        return out
