from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#import contextlib
import getpass
import os
import selenium

print('''Please choose a login option by specifying the number in parentheses:
(1) chess.com
(2) facebook''')
option = input('> ')

# load credentials into memory
username = input('username: ')
password = getpass.getpass('password for "{}": '.format(username))

# spin up chrome
path = os.path.dirname(os.path.realpath(__file__))
chrome = webdriver.Chrome(os.path.join(path, 'chromedriver'))
#with contextlib.closing(webdriver.Chrome(os.path.join(path, 'chromedriver'))) as chrome:

# navigate to login screen
login_url = 'https://www.chess.com/login'
chrome.get(login_url)

## go to chess.com v3
try:
    chrome.find_element_by_link_text('Try the new Chess.com!').click()
except selenium.common.exceptions.NoSuchElementException:
    pass

if option == '1':
    print('logging in with chess.com credentials')
    chrome.find_element_by_id('username').send_keys(username)
    chrome.find_element_by_id('password').send_keys(password)
    chrome.find_element_by_id('login').click()

elif option == '2':
    print('logging in with facebook credentials')
    chrome.find_element_by_xpath('//a[@title="Connect with Facebook"]').click()
    chrome.find_element_by_id('email').send_keys(username)
    chrome.find_element_by_id('pass').send_keys(password)
    chrome.find_element_by_id('loginbutton').click()

# navigate to games archive
chrome.get('https://www.chess.com/games/archive?gameOwner=my_game&gameType=live')

# hit "More" until all your games are loaded
games = 100
while True:
    print('loaded {} games'.format(games))
    try:
        WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '.load-more-container a')))
    except TimeoutException:
        print('could not find "More" on iteration', games // 100)
        break
    more = chrome.find_element_by_css_selector('.load-more-container a')
    more.click()
    games += 100

# select all games
chrome.find_element_by_css_selector('thead input').click()

# download selected game PGNs
chrome.find_element_by_xpath('//a[@title="Download"]').click()
print('Please allow Google Chrome time to complete download before quitting out of it.')

