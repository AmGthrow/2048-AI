"""
My internal representation for a 2048 board,
with moves, merging, and tile spawning. Basically 
all of the 2048 goodness except in numpy arrays instead of 
javascript.
"""

import numpy as np
import random

DEFAULT_ROWS = 4
DEFAULT_COLS = 4


class Board:
    """Object representing a board you can play 2048 on"""

    def __init__(self, board=np.zeros((DEFAULT_ROWS, DEFAULT_COLS), dtype=int)):
        self.new_board(board)

    def new_board(self, new_board):
        self.board = new_board
        self.score = 0
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def reset_board(self, new_board=None):
        """Sets everything on the board back to 0"""
        if new_board.all() == None:
            new_board = np.zeros((4, 4), dtype=int).copy()
        self.new_board(new_board)

    def reset_score(self, score=0):
        self.score = score

    def show_board(self):
        print(self.board)
        print(f"Score: {self.score}")

    def is_valid(self):
        board_copy = Board(self.board.copy())
        return (
            board_copy.move_up()
            or board_copy.move_down()
            or board_copy.move_left()
            or board_copy.move_right()
        )

    def new_tile(self, y, x, val):
        """Replaces the value of the specified tile in the board

        Args:
            y (int): the row of the tile whose value is to be changed
            x (int): the column of the tile whose value is to be changed
            val (int): The new value for the specified tile
        """
        self.board[y][x] = val

    def spawn_random_tile(self):
        """Spawns a new tile (either 2 or 4) in one of the tiles on the board which currently has
        a value of 0

        Returns:
            bool: Whether or not a new tile was spawned (i.e. whether or not there were any 0s left on the board)
        """
        # Get an np.ndarray with the indices where self.board has 0s
        zeros = np.argwhere(self.board == 0)
        if len(zeros) == 0:
            return False
        # pick a random index and record the x,y values
        y, x = random.choice(zeros)
        self.new_tile(y, x, np.random.choice([2, 4], p=[0.9, 0.1]))
        return True

    def random_move(self):
        """Selects a random move (up, down, left, or right) and performs it on the board

        Returns:
            bool: Whether or not the move actually changed anything on the board
        """
        moves = (self.move_up, self.move_down, self.move_left, self.move_right)
        selected_move = random.choice(moves)
        return selected_move()

    def move_up(self):
        """Shoves all tiles upward and merges similar tiles where applicable

        Returns:
            bool: Whether or not the move actually changed anything on the board
        """
        # Rotate the matrix so that "up" is at the left
        self.board = np.rot90(self.board, 1)
        # perform a regular move_left()
        is_valid = self.move_left()
        # reset the board to its original orientation
        self.board = np.rot90(self.board, -1)
        # return whether or not the move actually changed anything
        return is_valid

    def move_down(self):
        """Shoves all tiles downward and merges similar tiles where applicable

        Returns:
            bool: Whether or not the move actually changed anything on the board
        """
        # Rotate the matrix so that "down" is at the left
        self.board = np.rot90(self.board, -1)
        # perform a regular move_left()
        is_valid = self.move_left()
        # reset the board to its original orientation
        self.board = np.rot90(self.board, 1)
        # return whether or not the move actually changed anything
        return is_valid

    def move_right(self):
        """Shoves all tiles to the right and merges similar tiles where applicable

        Returns:
            bool: Whether or not the move actually changed anything on the board
        """
        # Rotate the matrix so that "right" is at the left
        self.board = np.fliplr(self.board)
        # perform a regular move_left()
        is_valid = self.move_left()
        # reset the board to its original orientation
        self.board = np.fliplr(self.board)
        # return whether or not the move actually changed anything
        return is_valid

    def move_left(self):
        """Shoves all tiles to the left and merges similar tiles where applicable

        Returns:
            bool: Whether or not the move actually changed anything on the board
        """
        old = self.board.copy()
        # combine tiles that would be combined after the left swipe
        self.merge_left()
        # push every tile to the left
        self.shift_left()
        # if any of the tiles merged/moved, the move is valid
        # otherwise, the move didn't change anything and the move is invalid
        is_valid = (old != self.board).any()
        return is_valid

    def shift_left(self):
        """Shifts every tile as far left as it could go without merging anything"""
        for row in range(self.rows):
            move_to = 0  # tracks which col a tile to move should be moved to
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    # swap col and move_to
                    # You might be alarmed that we're swapping but since this only happens if col == 0, this is
                    # more like a "bubble sort" where 0s get bubbled up
                    self.board[row][move_to], self.board[row][col] = (
                        self.board[row][col],
                        self.board[row][move_to],
                    )
                    move_to += 1

    def merge_left(self):
        """Merges similar tiles to the left if they're the same value

        Returns:
            int: the score we get from performing the merges
        """
        score_add = 0
        for row in range(self.rows):
            to_merge = 0  # tracks which tile should be "merged into"
            # skip the 1st column since it's what's being merged into
            for col in range(1, self.cols):
                # skip to the next one if current is 0
                if self.board[row][col] == 0:
                    continue
                # merge if current one matches 'to_merge'
                elif self.board[row][col] == self.board[row][to_merge]:
                    self.board[row][to_merge] *= 2
                    score_add += self.board[row][to_merge]
                    self.board[row][col] = 0
                # move 'to_merge' to the current tile if it wasn't a 0
                to_merge = col
        # take the score we added from performing the merges and add them to the board's score
        self.score += score_add
        return score_add


if __name__ == "__main__":
    board = Board()
    board.spawn_random_tile()
    board.spawn_random_tile()
    for _ in range(10):
        board.show_board()
        print(board.random_move())
        board.spawn_random_tile()
