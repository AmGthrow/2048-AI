from bs4 import BeautifulSoup
import re
import numpy as np


def get_tiles(browser):
    """
    Scrapes the webpage for raw data on the state of the board and generates a 4x4 matrix with tiles in the correct place
    """
    soup = BeautifulSoup(browser, 'lxml')

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

        if val > tile_info[y][x]:
            tile_info[y][x] = val

    return tile_info
