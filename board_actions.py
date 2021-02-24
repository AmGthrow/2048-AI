"""
Web scraping stuff that lets me clean the webpage data
from online 2048 websites like https://play2048.co/ and easily
interact with the board
"""

from selenium.webdriver.common.keys import Keys
import numpy as np
from bs4 import BeautifulSoup
import re
import AI

DEFAULT_NUM_MOVES = 4
DEFAULT_NUM_TRIALS = 100


class BoardDriver:
    """An interface between a selenium WebDriver for https://play2048.co/ and the AI 
    which retrieves a "best move", as well as some helper functions
    for scraping board information from the WebDriver
    """

    def __init__(self, browser):
        # a selenium WebDriver object that represents the actual page being controlled by selenium
        self.browser = browser
        # WebElement for all the HTML inside the browser WebDriver
        # I need the HTML because Keys need the WebElement, not the WebDriver. If I didn't get self.html up here,
        # I'd have to re-check it whenever any of the move_ functions are called
        self.html = browser.find_element_by_tag_name("html")

    def get_tiles(self) -> np.ndarray:
        """Scrapes the webpage for info on the board's tiles and generates a 4x4 matrix representation

        Returns:
            tile_info: a 4x4 np.ndarray matrix with all the board's current tiles
        """
        soup = BeautifulSoup(self.browser.page_source, "lxml")

        # A lot of this is really inelegant because I'm scraping off raw HTML. I could've done this more cleanly if I had a
        # numerical representation of the board from the actual JS code, but I don't know how to access that. Instead, I'm generating a new board
        # based off of the class names inside <div class="tile-container">, which just follows the HTML in the actual website.

        # This gives us the CSS class info of every tile on the board
        # e.g. a board with [['tile', 'tile-2', 'tile-position-1-3']] has a 2 tile at the position 1,3
        tiles = [tile["class"] for tile in soup.select(".tile")]

        # matrix representing the 4x4 grid from the board
        tile_info = np.zeros((4, 4), dtype=int)

        for tile in tiles:

            # extracts the value and position of every tile in tiles
            val = int(re.match(r"tile-(\d+)", tile[1]).group(1))

            # I don't need to use a regex like in val since the board is only 4x4, so I'm sure I'll never have 2 digits for x or y
            # need to use y-1 and x-1 since tile_info is 0-indexed but the actual xpos, ypos we scraped are 1-indexed
            x, y = int(tile[2][-3]) - 1, int(tile[2][-1]) - 1

            # the webpage actually keeps old tiles when merging, e.g. when you create a new 8 tile at (1,1), there are still two 4 tilse at (1,1)
            # So I need to get the biggest value that occupies that tile (i.e. the 8 tile in this example)
            if val > tile_info[y][x]:
                tile_info[y][x] = val

        return tile_info

    def get_new_tiles(self) -> [(int, int, int)]:
        """Scrapes the webpage for info on the board's  most recently-added tiles and returns their position and value

        Returns:
            tile_info: a list of tuples [(x, y, val)] representing each new tile in the board
        """
        soup = BeautifulSoup(self.browser.page_source, "lxml")

        # everything is the same as get_tiles() except now I only care about the tile with the .tile-new class
        tiles = [tile["class"] for tile in soup.select(".tile-new")]

        # matrix representing the 4x4 grid from the board
        tile_info = []

        for tile in tiles:

            # extracts the value and position of every tile in tiles
            val = int(re.match(r"tile-(\d+)", tile[1]).group(1))

            # I don't need to use a regex like in val since the board is only 4x4, so I'm sure I'll never have 2 digits for x or y
            # need to use y-1 and x-1 since tile_info is 0-indexed but the actual xpos, ypos we scraped are 1-indexed
            x, y = int(tile[2][-3]) - 1, int(tile[2][-1]) - 1

            # the webpage actually keeps old tiles when merging, e.g. when you create a new 8 tile at (1,1), there are still two 4 tilse at (1,1)
            # So I need to get the biggest value that occupies that tile (i.e. the 8 tile in this example)
            tile_info.append((x, y, val))

        return tile_info

    def move_left(self):
        self.html.send_keys(Keys.LEFT)

    def move_right(self):
        self.html.send_keys(Keys.RIGHT)

    def move_up(self):
        self.html.send_keys(Keys.UP)

    def move_down(self):
        self.html.send_keys(Keys.DOWN)

    def get_best_move(
        self, num_moves=DEFAULT_NUM_MOVES, num_trials=DEFAULT_NUM_TRIALS
    ):
        """Send the BoardDriver's current board configuration to the AI and get what
        the best move for the board would be    

        Args:
        num_moves (int, optional): The number of moves it looks ahead into the future for. Defaults to DEFAULT_NUM_MOVES.
        num_trials (int, optional): the number of trials for the AI to run. Defaults to DEFAULT_NUM_TRIALS.

        Returns:
            [type]: [description]
        """
        function_names = {
            "ai_up": self.move_up,
            "ai_down": self.move_down,
            "ai_left": self.move_left,
            "ai_right": self.move_right,
        }
        board = self.get_tiles()
        move = AI.get_best_move(board, num_moves, num_trials)
        return function_names[move.__name__]
