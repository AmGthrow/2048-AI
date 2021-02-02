from selenium.webdriver.common.keys import Keys
import numpy as np
from bs4 import BeautifulSoup
import re


class BoardDriver:
    def __init__(self, browser):
        # a selenium WebDriver object that represents the actual page being controlled by selenium
        self.browser = browser
        # WebElement for all the HTML inside the browser WebDriver
        # I need the HTML because Keys need the WebElement, not the WebDriver. If I didn't get self.html up here,
        # I'd have to re-check it whenever any of the move_ functions are called
        self.html = browser.find_element_by_tag_name('html')

    def get_tiles(self) -> np.ndarray:
        """Scrapes the webpage for info on the board's tiles and generates a 4x4 matrix representation

        Returns:
            tile_info: a 4x4 nd.ndarray matrix with all the board's current tiles
        """
        soup = BeautifulSoup(self.browser.page_source, 'lxml')

        # A lot of this is really inelegant because I'm scraping off raw HTML. I could've done this more cleanly if I had a
        # numerical representation of the board from the actual JS code, but I don't know how to access that. Instead, I'm generating a new board
        # based off of the class names inside <div class="tile-container">, which just follows the HTML in the actual website.

        # This gives us the CSS class info of every tile on the board
        # e.g. a board with [['tile', 'tile-2', 'tile-position-1-3']] has a 2 tile at the position 1,3
        tiles = [tile['class'] for tile in soup.select('.tile')]

        # matrix representing the 4x4 grid from the board
        tile_info = np.zeros((4, 4), dtype=int)

        for tile in tiles:

            # extracts the value and position of every tile in tiles
            val = int(re.match(r'tile-(\d+)', tile[1]).group(1))

            # I don't need to use a regex like in val since the board is only 4x4, so I'm sure I'll never have 2 digits for x or y
            # need to use y-1 and x-1 since tile_info is 0-indexed but the actual xpos, ypos we scraped are 1-indexed
            x, y = int(tile[2][-3]) - 1, int(tile[2][-1]) - 1

            # the webpage actually keeps old tiles when merging, e.g. when you create a new 8 tile at (1,1), there are still two 4 tilse at (1,1)
            # So I need to get the biggest value that occupies that tile (i.e. the 8 tile in this example)
            if val > tile_info[y][x]:
                tile_info[y][x] = val

        return tile_info

    def move_left(self):
        self.html.send_keys(Keys.LEFT)

    def move_right(self):
        self.html.send_keys(Keys.RIGHT)

    def move_up(self):
        self.html.send_keys(Keys.UP)

    def move_down(self):
        self.html.send_keys(Keys.DOWN)
