import numpy as np


class Board:
    def __init__(self, board = np.zeros((4,4), dtype=int)):
        self.board = board
    
    def show_board(self):
        print(self.board)

    def new_tile(self, x, y, val):
        self.board[y][x] = val

if __name__ == "__main__":
    board = Board()
