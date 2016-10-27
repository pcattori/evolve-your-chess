import selenium
from selenium import webdriver
import getpass
import os
import time

username = input('chess.com username: ')
password = getpass.getpass('password for chess.com user "{}": '.format(username))

path = os.path.dirname(os.path.realpath(__file__))
chrome = webdriver.Chrome(os.path.join(path, 'chromedriver'))
time.sleep(1)

login_url = 'https://www.chess.com/login'
chrome.get(login_url)

try:
    chrome.find_element_by_link_text('Try the new Chess.com!').click()
except selenium.common.exceptions.NoSuchElementException:
    pass

chrome.find_element_by_id('username').send_keys(username)
chrome.find_element_by_id('password').send_keys(password)
chrome.find_element_by_id('login').click()

chrome.get('https://www.chess.com/games/archive')

while True:
    try:
        more = chrome.find_element_by_css_selector('.load-more-container a')
        more.click()
    except selenium.common.exceptions.NoSuchElementException:
        break

print(chrome.title)
