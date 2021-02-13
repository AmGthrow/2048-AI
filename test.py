import unittest
from board import Board
import numpy as np

class TestBoard(unittest.TestCase):

    def test_left(self):
        """Test to make sure move_left() both shifts all elements and merges similar values
        """
        start = np.array([
        [2,0,0,0],
        [2,0,0,0],
        [0,0,0,0],
        [0,4,4,0]], 
        dtype=int)

        end = np.array([
        [2,0,0,0],
        [2,0,0,0],
        [0,0,0,0],
        [8,0,0,0]], 
        dtype=int)

        left_board = Board(start)
        left_board.move_left()
        np.testing.assert_equal(left_board.board, end)


if __name__ == "__main__":
    unittest.main()