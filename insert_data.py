"""Insert data.
Colect the attendance of all matches and update table"""

import sqlite3
from decouple import config
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, InvalidSessionIdException
import unidecode

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

        while browser.is_element_not_present_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[3]'):
            pass

        if browser.is_element_not_present_by_xpath('/html/body/div[9]/div[2]/div[1]/div/div[1]/div'):
            attendance = -1
            stadium = ''
        else:
            """Click to see report"""
            while browser.is_element_not_present_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[1]/div[4]/div'):
                pass
            browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[1]/div[4]/div').first.click()

            """Get match data"""
            attendance = browser.find_by_xpath('/html/body/div[9]/div[2]/div/div[10]/div/ul[2]/li[4]/span[2]').first
            attendance = attendance.text.strip()
            attendance = attendance.replace(',', '')

            stadium = browser.find_by_xpath('/html/body/div[9]/div[2]/div/div[10]/div/ul[1]/li[1]').first
            stadium = stadium.text.strip().replace('“',   '\'').replace('"', '\'')

        scoreboard = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[3]').first
        scoreboard = scoreboard.text.strip()
        scoreboard = scoreboard.split('-')
        scoreboard = [s.strip() for s in scoreboard]

        home_team = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[2]/a').first
        home_team = home_team.text.strip().replace('“',   '\'').replace('"', '\'')
        home_team_score = scoreboard[0]
        home_team_link = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[2]/a').first
        home_team_link = home_team_link['href']

        away_team = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[4]/a').first
        away_team = away_team.text.strip().replace('“',   '\'').replace('"', '\'')
        away_team_score = scoreboard[1]
        away_team_link = browser.find_by_xpath('/html/body/div[9]/div[1]/div[3]/div/div[2]/div[4]/a').first
        away_team_link = away_team_link['href']

        return attendance, stadium, home_team, home_team_score, home_team_link, away_team, away_team_score, away_team_link
    except (InvalidSessionIdException, NoSuchWindowException, WebDriverException) as e:
        print(e.msg)
        browser.quit()
        return None

for table in tables.fetchall():
    turn = 2
    query = """SELECT * FROM {} WHERE round = {} and attendance = 0;""".format(table[0], turn)
    columns = cursor.execute(query)
    for column in columns.fetchall():
        if column[0] == turn:
            match_data = get_match_data(column[1])
            if match_data is not None:
                attendance = match_data[0]
                stadium = match_data[1]
                home_team = match_data[2]
                home_team_score = match_data[3]
                home_team_link = match_data[4]
                away_team = match_data[5]
                away_team_score = match_data[6]
                away_team_link = match_data[7]
                update = """
UPDATE {}
SET attendance = {}, stadium = "{}", home_team = "{}", home_team_score = {}, home_team_link = "{}",
away_team = "{}", away_team_score = {}, away_team_link = "{}"
WHERE match_link = '{}'""".format(table[0], attendance, stadium, home_team, home_team_score, home_team_link,
                                away_team, away_team_score, away_team_link, column[1])
                update = unidecode.unidecode(update)
                print(update)
                cursor.execute(update)
                conn.commit()

conn.close()
browser.quit()
