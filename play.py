"""
Instantiates a new WebDriver for selenium to control and sends keystrokes to play the game and reset when it ends
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
from board_actions import BoardDriver
from board import Board

def play():
    # Takes the browser to play2048.co and starts a game
    browser = webdriver.Chrome()
    browser.get('https://play2048.co/')
    newGame = browser.find_element_by_class_name('restart-button')
    newGame.click()

    board = BoardDriver(browser)
    # sends keys in the sequence UP, DOWN, LEFT, RIGHT and restarts the game when the option appears
    while True:
        print("found board")
        board.perform_best_move(board.get_tiles())
        print("DID BEST MOVE")
        
        # it takes a while for the HTML to update with the board, so I need to wait a bit. Otherwise, get_tiles() 
        # gives a wrong board, one where the move/s might not have been done yet
        time.sleep(0.1)
        print(board.get_tiles())
        try:
            resetGame = browser.find_element_by_class_name('retry-button')
            if not Board(board).is_valid():
                x = input("Game over: ")
                resetGame.click()
        except:
            continue


if __name__ == "__main__":
    play()
