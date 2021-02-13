import numpy as np

DEFAULT_ROWS = 4
DEFAULT_COLS = 4

class Board:
    def __init__(self, board=np.zeros((DEFAULT_ROWS, DEFAULT_COLS), dtype=int)):
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def show_board(self):
        print(self.board)

    def new_tile(self, x, y, val):
        self.board[y][x] = val

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

if __name__ == "__main__":
    board = Board()
