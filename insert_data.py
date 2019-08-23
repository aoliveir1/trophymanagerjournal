"""Insert data.
Colect the attendance of all matches and update table"""

import sqlite3
from decouple import config
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from utils import create_brower, sign_in

conn = sqlite3.connect('tmjournal_season60.db')
cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

url_base = config('URL_BASE')

"""Initialize the browser"""
browser = create_brower()

"""Login"""
sign_in(browser, url_base)

def get_match_data(link):
    try:
        url_match = url_base + link
        browser.visit(url_match)

        """Click to see report"""
        while browser.is_element_not_present_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[1]/div[4]/div'):
            pass
        browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[1]/div[4]/div').first.click()

        """Get attendance"""
        attendance = browser.find_by_xpath('/html/body/div[9]/div[2]/div/div[10]/div/ul[2]/li[4]/span[2]').first
        attendance = attendance.text.strip()
        attendance = attendance.replace(',', '')
        attendance = int(attendance)

        """Get stadium name"""
        stadium = browser.find_by_xpath('/html/body/div[9]/div[2]/div/div[10]/div/ul[1]/li[1]').first
        stadium = stadium.text.strip()

        """Get home team"""
        home = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[2]/a').first
        home = home.text.strip()

        """Get away team"""
        away = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[4]/a').first
        away = away.text.strip()

        """Get scoreboard"""
        scoreboard = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[3]')
        scoreboard = scoreboard.text.strip()
        scoreboard = scoreboard.split('-')
        scoreboard = [s.strip() for s in scoreboard]

        return attendance, stadium, home, away, scoreboard
    except (WebDriverException, NoSuchWindowException) as e:
        print(e)
        return 0

for table in tables.fetchall():
    query = """SELECT * FROM {};""".format(table[0])
    result = cursor.execute(query)
    for link in result.fetchall():
        if link[0] == 1:
            match_data = get_match_data(link[1])
            attendance = match_data[0]
            stadium = match_data[1]
            home = match_data[2]
            away = match_data[3]
            scoreboard = match_data[4]
            update = """UPDATE {}
SET attendance = {}, stadium = '{}', home = '{}', away = '{}', scoreboard = '{}'
WHERE link = '{}'""".format(table[0], attendance, stadium, home, away, scoreboard, link[1])
            input(update)
            cursor.execute(update)

conn.commit()
conn.close()
browser.quit()
