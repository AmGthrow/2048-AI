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

    def test_new_tile(self):
        start = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [0, 4, 4, 0]],
            dtype=int)

        end = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [5, 4, 4, 0]],
            dtype=int)

        board = Board(start)
        board.new_tile(3, 0, 5)
        np.testing.assert_equal(board.board, end)

        end = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [10, 4, 4, 0]],
            dtype=int)
        board.new_tile(3,0,10)
        np.testing.assert_equal(board.board, end)

    def test_spawn_random_tile(self):
        start = np.array([
            [2, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 4, 4, 4],
            [0, 4, 4, 0]],
            dtype=int)

        # Repeat the test 100 times
        for _ in range(100):
            # initialize a new board
            board = Board(start.copy())
            # add a random tile 8 times
            for i in range(1, 9):
                # add one random tile
                board.spawn_random_tile()
                # get the indices of tiles which are different from start 
                newvals = np.argwhere(board.board != start)
                # Make sure only one is added each time
                self.assertEqual(len(newvals), i)
                y, x = newvals[-1]
                # Make sure the most recently added one was either 2 or 4
                self.assertTrue(board.board[y][x] in {2, 4})
            # assert that the board is full after occupying the 8 available "slots" for a new tile
            self.assertFalse(board.spawn_random_tile())
                


if __name__ == "__main__":
    unittest.main()
