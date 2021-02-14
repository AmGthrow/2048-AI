import numpy as np
from board import Board

board = Board()
board.spawn_random_tile()
board.spawn_random_tile()

def get_best_move(original_board, num_moves, num_trials):
    # Instantiate a Board
    ai_board = Board()
    # List down all possible first moves we could make
    fm_candidates = [ai_up, ai_down, ai_left, ai_right]
    # Make an array to keep track of scores
    fm_scores = np.zeros(len(fm_candidates), dtype=int)
    for fm_index in range(len(fm_candidates)):
        # "Reset" the values on ai_board to match original_board
        ai_board.reset_board(original_board.copy())
        # Select a "first move" to execute on ai_board
        first_move = fm_candidates[fm_index]

        # Skip this first move if it's invalid
        if not first_move(ai_board):
            continue
        
        # Do a bunch of trials using the "post-first move" board
        trials_score = ai_trials(ai_board.board.copy(), num_moves, num_trials)
        # Put the trials_score into fm_scores
        fm_scores[fm_index] = trials_score

    # get the index which got the highest score
    max_score_index = np.argmax(fm_scores)
    #return the corresponding move
    return fm_candidates[max_score_index]

def ai_trials(trial_board, num_moves, num_trials):
    """performs <num_moves> random moves <num_trials> times on a given board, resetting the board to original between every trial,
    and returns the total score we get from all the trials

    Args:
        trial_board (np.ndarray): The starting configuration of the board
        num_moves (int): the "depth" of the number of moves that each trial expects to investigate
        num_trials (int): the number of iterations for the AI to run

    Returns:
        int: The score we get as a result of all the trials
    """
    # Keep track of the total "score" of these trials
    trials_score = 0
    # Do a bunch of trials with random moves after the first move
    for num_trial in range(num_trials):
        # Make a new board that starts off with the ai_board's first move
        search_board = Board(trial_board.copy())
        search_board.spawn_random_tile()
        
        moves_done = 0
        # Do <num_moves> number of random moves
        while moves_done < num_moves and search_board.is_valid():
            # Proceed to the next random move if we hit a dead end
            if not search_board.random_move():
                continue
            search_board.spawn_random_tile()
            moves_done += 1
        # Add the board's score after <num_moves> moves to trials_score
        trials_score += search_board.score
    return trials_score



def ai_up(board):
    return board.move_up()
def ai_down(board):
    return board.move_down()
def ai_left(board):
    return board.move_left()
def ai_right(board):
    return board.move_right()

            
while board.is_valid():
    board.show_board()
    best_move = get_best_move(board.board, 4, 500)
    print(best_move)
    best_move(board)
    board.spawn_random_tile()
board.show_board()