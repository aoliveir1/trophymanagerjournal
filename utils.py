from decouple import config
from splinter import Browser

def create_brower():
    user_agent = config('USER_AGENT')
    '''Firefox'''
    # executable_path = config('EXECUTABLE_PATH')
    # browser = Browser(executable_path=executable_path, user_agent=user_agent)
    '''Chrome'''
    executable_path = config('EXECUTABLE_PATH2')
    browser = Browser('chrome', headless=True, executable_path=executable_path, user_agent=user_agent)
    return browser

def sign_in(browser, url_base):
    browser.visit(url_base)
    while browser.is_element_not_present_by_css('.cc-cookie-accept'):
        print('.', end='')
    browser.find_by_css('.cc-cookie-accept').first.click()
    browser.visit(url_base)
    browser.fill('email', config('EMAIL'))
    browser.fill('password', config('PASSWORD'))
    browser.find_by_css('.button').first.click()
    return True
