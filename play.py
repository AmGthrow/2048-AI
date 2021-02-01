"""
Instantiates a new WebDriver for selenium to control and sends keystrokes to play the game and reset when it ends
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def play():
    # Takes the browser to play2048.co and starts a game
    browser = webdriver.Chrome()
    browser.get('https://play2048.co/')
    newGame = browser.find_element_by_class_name('restart-button')
    newGame.click()

    html = browser.find_element_by_tag_name('html')
    # sends keys in the sequence UP, DOWN, LEFT, RIGHT and restarts the game when the option appears
    while True:
        html.send_keys(Keys.UP)
        html.send_keys(Keys.DOWN)
        html.send_keys(Keys.LEFT)
        html.send_keys(Keys.RIGHT)
        try:
            resetGame = browser.find_element_by_class_name('retry-button')
            resetGame.click()
        except:
            continue

if __name__ == "__main__":
    play()