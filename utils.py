"""Initialize the browser"""
from decouple import config
from splinter import Browser

def create_brower():
    user_agent = config('USER_AGENT')
    executable_path = config('EXECUTABLE_PATH')
    browser = Browser(headless=True, executable_path=executable_path, user_agent=user_agent)
    return browser

def sign_in(browser, url_base):
    browser.visit(url_base)
    browser.fill('email', config('EMAIL'))
    browser.fill('password', config('PASSWORD'))
    browser.find_by_xpath('//*[@id="login_button"]').first.click()
    return True