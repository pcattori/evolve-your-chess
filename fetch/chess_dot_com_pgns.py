from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import contextlib
import datetime
import getpass
import glob
import os
import selenium
import sh
import time
from tqdm import tqdm

from require import require
config = require('../config.py')

print('''Please choose a login option by specifying the number in parentheses:
(1) chess.com
(2) facebook''')
option = int(input('> '))
if option not in {1, 2}:
    print('Invalid option "{}"'.format(option))
    import sys; sys.exit(3)

# load credentials into memory
username = input('username: ')
password = getpass.getpass('password for "{}": '.format(username))

# spin up chrome
chromedriver_path = os.path.join(config.BIN, 'chromedriver')
if not os.path.exists(chromedriver_path):
    chromedriver_url = 'https://sites.google.com/a/chromium.org/chromedriver/'
    print('Please install the chromedriver binary ({}) to {}'.format(
        chromedriver_url, config.BIN))
    import sys; sys.exit(3)

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory' : os.path.join(
        config.DATA, 'pgn')})
with contextlib.closing(webdriver.Chrome(
        chromedriver_path, chrome_options=options)) as chrome:

    # navigate to login screen
    login_url = 'https://www.chess.com/login'
    chrome.get(login_url)

    ## go to chess.com v3
    try:
        chrome.find_element_by_link_text('Try the new Chess.com!').click()
    except selenium.common.exceptions.NoSuchElementException:
        pass


    if option == 1:
        print('logging in with chess.com credentials')
        chrome.find_element_by_id('username').send_keys(username)
        chrome.find_element_by_id('password').send_keys(password)
        chrome.find_element_by_id('login').click()
    elif option == 2:
        print('logging in with facebook credentials')
        chrome.find_element_by_xpath('//a[@title="Connect with Facebook"]').click()
        chrome.find_element_by_id('email').send_keys(username)
        chrome.find_element_by_id('pass').send_keys(password)
        chrome.find_element_by_id('loginbutton').click()

    # check that login succeeded
    if not chrome.current_url == 'https://www.chess.com/home':
        print('Incorrect password for user "{}"'.format(username))
        import sys; sys.exit(3)

    # navigate to games archive
    chrome.get('https://www.chess.com/games/archive?gameOwner=my_game&gameType=live')

    # hit "More" until all your games are loaded
    for i in tqdm(range(9)):
        try:
            WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, '.load-more-container a')))
        except TimeoutException:
            break
        more = chrome.find_element_by_css_selector('.load-more-container a')
        more.click()

    # select all games
    chrome.find_element_by_css_selector('thead input').click()

    # download selected game PGNs
    sh.mkdir('-p', os.path.join(config.DATA, 'pgn'))
    pgns = glob.glob(os.path.join(config.DATA, 'pgn', '*'))
    chrome.find_element_by_xpath('//a[@title="Download"]').click()

    timeout = datetime.datetime.now() + datetime.timedelta(minutes=5)
    download_success = False
    while datetime.datetime.now() < timeout:
        if glob.glob(os.path.join(config.DATA, 'pgn', '*')) != pgns:
            download_success = True
            break
        time.sleep(1)

    if not download_success:
        print('Chrome failed to download chess.com PGNs after 5 minutes')
        import sys; sys.exit(3)

    filepath = max(
        glob.glob(os.path.join(config.DATA, 'pgn', '*')),
        key=os.path.getctime)

    os.rename(filepath, os.path.join(config.DATA, 'pgn', 'chess_dot_com.pgn'))

