import numpy as np

DEFAULT_ROWS = 4
DEFAULT_COLS = 4


class Board:
    """Object representing a board you can play 2048 on
    """

    def __init__(self, board=np.zeros((DEFAULT_ROWS, DEFAULT_COLS), dtype=int)):
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def show_board(self):
        print(self.board)

    def new_tile(self, x, y, val):
        self.board[y][x] = val

    def move_up(self):
        """Shoves all tiles upward and merges similar tiles where applicable

        Returns:
            bool: Whether or not the move actually changed the board
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
            bool: Whether or not the move actually changed the board
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
            bool: Whether or not the move actually changed the board
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
            bool: Whether or not the move actually changed the board
        """
        old = self.board
        # combine tiles that would be combined after the left swipe
        self.merge_left()
        # push every tile to the left
        self.shift_left()
        # Check if the move we made actually changed anything
        if old.all() == self.board.all():
            return False
        return True

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
                    self.board[row][move_to], self.board[row][col] = self.board[row][col], self.board[row][move_to]
                    move_to += 1

    def merge_left(self):
        """Merges similar tiles to the left if they're the same value
        """
        for row in range(self.rows):
            to_merge = 0    # tracks which tile should be "merged into"
            # skip the 1st column since it's what's being merged into
            for col in range(1, self.cols):
                # skip to the next one if current is 0
                if self.board[row][col] == 0:
                    continue
                # merge if current one matches 'to_merge'
                elif self.board[row][col] == self.board[row][to_merge]:
                    self.board[row][to_merge] *= 2
                    self.board[row][col] = 0
                # move 'to_merge' to the current tile if it wasn't a 0
                to_merge = col


if __name__ == "__main__":
    board = Board()
