from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()

browser.get('https://play2048.co/')

newGame = browser.find_element_by_class_name('restart-button')

newGame.click()

html = browser.find_element_by_tag_name('html')
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
    
