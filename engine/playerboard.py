from board import Board

class PlayerBoard(Board):
    def __init__(self):
        self.move = 4
        super().__init__()

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
