"""Insert data.
Colect the attendance of all matches and update table"""

import sqlite3
from decouple import config
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from splinter import Browser, exceptions

conn = sqlite3.connect('tmjournal_season60.db')
cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

"""Initialize the browser"""
user_agent = config('USER_AGENT')
executable_path = config('EXECUTABLE_PATH')
browser = Browser(headless=True, executable_path=executable_path, user_agent=user_agent)

url_base = config('URL_BASE')

browser.visit(url_base)
browser.fill('email', config('EMAIL'))
browser.fill('password', config('PASSWORD'))
browser.find_by_xpath('//*[@id="login_button"]').first.click()

def get_a(link):
    try:
        url_match = url_base + link
        browser.visit(url_match)

        while browser.is_element_not_present_by_xpath('/html/body/div[8]/div[1]/div[3]/div/div[1]/div[4]/div'):
            pass

        browser.find_by_xpath('/html/body/div[8]/div[1]/div[3]/div/div[1]/div[4]/div').first.click()
        attendance = browser.find_by_xpath('/html/body/div[8]/div[2]/div/div[10]/div/ul[2]/li[4]/span[2]').first
        attendance = attendance.text.strip()
        attendance = attendance.replace(',', '')
        return int(attendance)
    except (WebDriverException, NoSuchWindowException) as e:
        print(e)
        return 0


for table in tables.fetchall():
    query = """SELECT * FROM {};""".format(table[0])
    result = cursor.execute(query)
    for link in result.fetchall():
        if link[0] == 1:
            a = get_a(link[1])
            update = """UPDATE {}
SET attendance = {}
WHERE link = '{}'""".format(table[0], a, link[1])
            cursor.execute(update)

conn.commit()
conn.close()
browser.quit()
