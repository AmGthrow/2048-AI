import unittest
from board import Board
import numpy as np


class TestBoard(unittest.TestCase):

    def test_left(self):
        """Test to make sure move_left() both shifts all elements and merges similar values
        """
        start = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [0, 4, 4, 0]],
            dtype=int)

        end = np.array([
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [8, 4, 0, 0],
            [8, 0, 0, 0]],
            dtype=int)

        left_board = Board(start)
        score = left_board.move_left()
        self.assertEqual(score, 20)
        np.testing.assert_equal(left_board.board, end)

    def test_right(self):
        start = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [0, 4, 4, 0]],
            dtype=int)

        end = np.array([
            [0, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 4, 8],
            [0, 0, 0, 8]],
            dtype=int)

        right_board = Board(start)
        score = right_board.move_right()
        self.assertEqual(score, 20)
        np.testing.assert_equal(right_board.board, end)

    def test_up(self):
        start = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [0, 4, 4, 0]],
            dtype=int)

        end = np.array([
            [4, 2, 8, 4],
            [0, 8, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            dtype=int)

        up_board = Board(start)
        score = up_board.move_up()
        self.assertEqual(score, 20)
        np.testing.assert_equal(up_board.board, end)

    def test_down(self):
        start = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [0, 4, 4, 0]],
            dtype=int)

        end = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [4, 8, 8, 4]],
            dtype=int)

        down_board = Board(start)
        score = down_board.move_down()
        self.assertEqual(score, 20)
        np.testing.assert_equal(down_board.board, end)


if __name__ == "__main__":
    unittest.main()