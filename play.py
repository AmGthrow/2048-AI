"""
Instantiates a new WebDriver for selenium to control and sends keystrokes to play the game and reset when it ends
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
from board_actions import BoardDriver
import logging

logging.basicConfig(filename='BoardDriver.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def play():
    # Takes the browser to play2048.co and starts a game
    browser = webdriver.Chrome()
    browser.get('https://play2048.co/')
    newGame = browser.find_element_by_class_name('restart-button')
    newGame.click()

    board = BoardDriver(browser)
    # sends keys in the sequence UP, DOWN, LEFT, RIGHT and restarts the game when the option appears
    while True:
        # TODO: Log the best move?
        board.perform_best_move(board.get_tiles())

        # it takes a while for the HTML to update with the board, so I need to wait a bit. Otherwise, get_tiles()
        # gives a wrong board, one where the move/s might not have been done yet
        time.sleep(0.1)
        logging.debug(f"New board: {board.get_tiles()}")

        # Try to click "Keep Going" if it shows up
        try:
            # Press the "Keep Going" button that shows up when we reach the 2048 tile
            continueGame = browser.find_element_by_class_name(
                'keep-playing-button')
            # Assuming we reached 2048, log the board's current state
            logging.info("REACHED 2048")
            logging.info(str(board.get_tiles()))
            continueGame.click()
        except:
            continue

        # If there's no "Keep Going" but retry-button shows up, press that instead
        # Since it means we lost and the board is currently in a Game Over state
        try:
            # Reset the game when we lose
            resetGame = browser.find_element_by_class_name('retry-button')
            # Assuming we found the resetGame button, log the board and score
            logging.info("GAME OVER")
            logging.info(str(board.get_tiles()))
            score = browser.find_element_by_class_name('score-container')
            # Reset the game
            logging.info(f"SCORE: {score.text}")
            resetGame.click()
        except:
            continue


if __name__ == "__main__":
    play()
