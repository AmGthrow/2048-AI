"""
Instantiates a new WebDriver for selenium to control and sends keystrokes to play the game and reset when it ends
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
from board_actions import BoardDriver
import logging
import sqlite3
import re
import argparse
import os

parser = argparse.ArgumentParser(
    description="Run a 2048 AI to play 2048 while saving results."
)
parser.add_argument(
    "num_moves",
    type=int,
    default=3,
    help="Number of moves for the AI to look ahead into the future for",
)
parser.add_argument(
    "num_trials",
    type=int,
    default=200,
    help="Number of trials that the AI runs for every move to calculate a best score",
)
parser.add_argument(
    "num_runs",
    type=int,
    default=0,
    help="Number of games the AI will play. 0 means the AI will run until forcibly closed",
)

args = parser.parse_args()

# TODO: Use a logger instead of basicConfig
logging.basicConfig(
    filename="BoardDriver.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def play(num_moves=3, num_trials=200, runs_left=0):
    """Opens a selenium webdriver and plays 2048, logging results to a database

    Args:
        num_moves (int, optional): The number of moves it looks ahead into the future for. Defaults to 3.
        num_trials (int, optional): the number of trials for the AI to run. Defaults to 200.
        runs_left (int, optional): The number of games of 2048 to play. Runs indefinitely when
        set to 0 or less. Defaults to 0.
    """

    # Track wins/losses to get win rate
    wins = 0
    losses = 0
    # Track whether or not the AI reached 2048 (resets every run)
    did_win = False

    # Track how many runs we've finished
    runs_done = 0

    logging.info(
        f"Beginning new session.\nnum_moves: {num_moves}\nnum_trials: {num_trials}\nnum_runs: {runs_left}"
    )
    # Takes the browser to play2048.co and starts a game
    browser = webdriver.Chrome()
    browser.get("https://play2048.co/")
    newGame = browser.find_element_by_class_name("restart-button")
    newGame.click()

    board = BoardDriver(browser)
    # sends keys in the sequence UP, DOWN, LEFT, RIGHT and restarts the game when the option appears
    while runs_done < runs_left or runs_left == 0:
        print(f"New board: \n{board.get_tiles()}")
        # Retrieve the best move we can perform
        best_move = board.get_best_move(
            board.get_tiles(), num_moves, num_trials)
        print(f"Best move is {best_move.__name__}")
        # Execute the best move
        best_move()

        # it takes a while for the HTML to update with the board, so I need to wait a bit. Otherwise, get_tiles()
        # gives a wrong board, one where the move/s might not have been done yet

        # Try to click "Keep Going" if it shows up
        try:
            # Store the current board and score
            win_board = str(board.get_tiles())
            win_score = browser.find_element_by_class_name(
                "score-container").text
            # Sometimes, an extra "+ <score>" is left in the HTML from when the JS
            # Adds points after a merge, like +4 or +8. I only need to extract the first
            # set of numbers, which is my real score
            win_score = re.search(r"\d+", win_score).group()

            # Press the "Keep Going" button that shows up when we reach the 2048 tile
            continueGame = browser.find_element_by_class_name(
                "keep-playing-button")
            continueGame.click()  # Raises an exception if the button doesn't exist

            # Assuming we didn't fly into the 'except' yet, log the board's current state
            logging.info("REACHED 2048")
            logging.info("\n" + win_board)
            logging.info(f"SCORE: {win_score}")
            wins += 1
            did_win = True
        except:
            pass

        # If there's no "Keep Going" but retry-button shows up, press that instead
        # Since it means we lost and the board is currently in a Game Over state
        try:
            # Store the current board and score
            lose_board = str(board.get_tiles())
            lose_score = browser.find_element_by_class_name(
                "score-container").text
            # Sometimes, an extra "+ <score>" is left in the HTML from when the JS
            # Adds points after a merge, like +4 or +8. I only need to extract the first
            # set of numbers, which is my real score
            lose_score = re.search(r"\d+", lose_score).group()

            # Reset the game when we lose
            resetGame = browser.find_element_by_class_name("retry-button")
            resetGame.click()  # Raises an exception if the button doesn't exist

            # Assuming we didn't go into the 'except' yet, log the current board and score
            logging.info("GAME OVER")
            logging.info("\n" + lose_board)
            logging.info(f"SCORE: {lose_score}")
            losses += 1
            logging.info(f"Win rate: {round((100 * wins/losses), 2)}%")

            # Also, throw the results into the database

            # Connect to a database to store results from trials
            conn = sqlite3.connect("2048_AI_results.db")
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS results
                            (
                            attempt_no INTEGER PRIMARY KEY,
                            num_moves SMALLINT,
                            num_trials SMALLINT,
                            highest_score INT,
                            did_win BOOL
                            )
                            """
            )
            cursor.execute(
                "INSERT INTO results VALUES(NULL, ?, ?, ?, ?)",
                (num_moves, num_trials, lose_score, int(did_win)),
            )
            conn.commit()
            last_trial = cursor.execute(
                "SELECT MAX(attempt_no) FROM results").fetchone()[0]
            conn.close()

            # Declare this run as finished and start another one
            runs_done += 1
            did_win = False

            # TODO: Take a screenshot of the "Game Over" board
            # For now I guess a text version of the board will do
            if not os.path.exists('GameOvers'):
                os.makedirs('GameOvers')
            with open(f'GameOvers/{last_trial}.txt', 'w') as last_board:
                last_board.write(lose_board + f'\nSCORE: {lose_score}')
        except:
            pass
    logging.info("Finished session")
    browser.close()


if __name__ == "__main__":
    play(args.num_moves, args.num_trials, args.num_runs)
