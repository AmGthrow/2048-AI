import unittest
from board import Board
import numpy as np

class TestBoard(unittest.TestCase):

    def test_right(self):
        """Test to make sure move_right() both shifts all elements and merges similar values
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

        right_board = Board(start)
        right_board.move_right()
        np.testing.assert_equal(right_board.board, end)


if __name__ == "__main__":
    unittest.main()