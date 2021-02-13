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

    def shift_left(self):
        """Shifts every tile as far left as it could go without merging anything
        """
        for row in range(self.rows):
            move_to = 0  # tracks which col a tile to move should be moved to
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    # swap col and move_to
                    # You might be alarmed that we're swapping but since this only happens if col == 0, this is
                    # more like a "bubble sort" where 0s get bubbled up
                    self.board[row][move_to], self.board[row][col] self.board[row][col], self.board[row][move_to]
                    move_to += 1
if __name__ == "__main__":
    board = Board()
