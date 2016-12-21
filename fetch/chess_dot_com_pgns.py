from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
import contextlib
import datetime
import getpass
import glob
import os
import selenium
import sys
import time

# TODO by default last 1000 blitz games, else provide custom url
# TODO download each page separately

chromedriver_path = sys.argv[1]
pgns_dir = sys.argv[2]

print('''Please choose a login option by specifying the number in parentheses:
(1) chess.com
(2) facebook''')
option = int(input('> '))
if option not in {1, 2}:
    print('Invalid option "{}"'.format(option))
    sys.exit(3)

# load credentials into memory
username = input('username: ')
password = getpass.getpass('password for "{}": '.format(username))

# spin up chrome
if not os.path.exists(chromedriver_path):
    chromedriver_url = 'https://sites.google.com/a/chromium.org/chromedriver/'
    raise FileNotFoundError('Chromedriver not found. Please install from', chromedriver_url)

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory' : pgns_dir})
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
        sys.exit(3)

    # navigate to games archive
    chrome.get('https://www.chess.com/games/archive?gameOwner=my_game&gameType=live')


    # hit "More" until all your games are loaded
    for _ in tqdm(range(20)):
        # select all games
        chrome.find_element_by_css_selector('thead input').click()
        chrome.find_element_by_xpath('//a[@title="Download"]').click()

        # download selected game PGNs
        pgns = glob.glob(os.path.join(pgns_dir, '*'))

        timeout = datetime.datetime.now() + datetime.timedelta(minutes=5)
        download_success = False
        while datetime.datetime.now() < timeout:
            if glob.glob(os.path.join(pgns_dir, '*')) != pgns:
                download_success = True
                break
            time.sleep(1)
        # TODO maybe we can get rid of webdriverwait now
        try:
            WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, '.next a')))
        except TimeoutException:
            break
        more = chrome.find_element_by_css_selector('.next a')
        more.click()


    # timeout = datetime.datetime.now() + datetime.timedelta(minutes=5)
    # download_success = False
    # while datetime.datetime.now() < timeout:
    #     if glob.glob(os.path.join(pgns_dir, '*')) != pgns:
    #         download_success = True
    #         break
    #     time.sleep(1)

    # if not download_success:
    #     print('Chrome failed to download chess.com PGNs after 5 minutes')
    #     sys.exit(3)

    # filepath = max(
    #     glob.glob(os.path.join(pgns_dir, '*')),
    #     key=os.path.getctime)

    # os.rename(filepath, os.path.join(pgns_dir, 'chess_dot_com.pgn'))

