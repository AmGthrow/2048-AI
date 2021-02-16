from board import Board
import keyboard

board = Board()

board.spawn_random_tile()
board.spawn_random_tile()
board.show_board()


def key_up():
    is_valid = board.move_up()
    if is_valid:
        board.spawn_random_tile()
    board.show_board()
    print("Score: " + str(board.score))


def key_down():
    is_valid = board.move_down()
    if is_valid:
        board.spawn_random_tile()
    board.show_board()
    print("Score: " + str(board.score))


def key_left():
    is_valid = board.move_left()
    if is_valid:
        board.spawn_random_tile()
    board.show_board()
    print("Score: " + str(board.score))


def key_right():
    is_valid = board.move_right()
    if is_valid:
        board.spawn_random_tile()
    board.show_board()
    print("Score: " + str(board.score))


def new_game():
    board.reset_board()
    board.spawn_random_tile()
    board.spawn_random_tile()
    board.show_board()


keyboard.add_hotkey("up", key_up)
keyboard.add_hotkey("down", key_down)
keyboard.add_hotkey("left", key_left)
keyboard.add_hotkey("right", key_right)
keyboard.add_hotkey("esc", new_game)
keyboard.wait()