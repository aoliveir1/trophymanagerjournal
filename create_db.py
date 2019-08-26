"""
Create a database of fixtures for the current season.
Access all national top divisions pages and collect all links of all fixtures.
Create one table for each nation and insert the links for each of all fixtures and your respective round.
"""

import sqlite3

from decouple import config
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException, NoSuchWindowException

from utils import create_brower, sign_in

url_base = config('URL_BASE')
url_ranking = url_base + config('URL_RANKING')

"""Initialize the browser"""
browser = create_brower()

"""Login"""
sign_in(browser, url_base)

browser.visit(url_ranking)

"""Start scrape"""
soup = BeautifulSoup(browser.html, 'html.parser')
table = soup.find('table')
tr = table.findAll('tr')

"""Create Database"""
season = browser.find_link_by_partial_text('Season').first
season = season.text.lower().replace(' ', '')
conn = sqlite3.connect('tmjournal_' + season + '.db')
cursor = conn.cursor()

print('creating tables...')
for td in tr[1:]:
    try:
        """Format fixtures page link"""
        league = str(td.a['href']).replace('national-teams', 'league')
        league = league + '/1/1'
        fixtures = '/fixtures' + league
        browser.visit(url_base + fixtures)
        soup = BeautifulSoup(browser.html, 'html.parser')
        soup = soup.findAll('a', {'class': 'match_link'})

        while browser.is_element_not_present_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div[2]/span[2]'):
            browser.wait_time(1)

        league_name = browser.find_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div[2]/span[2]').first
        league_name = league_name.text.strip()

        """Create Table"""
        table_name = td.a.text.lower().replace(' ', '_').replace('-', '_').replace('\'',   '_').replace('&', '_')
        cursor.execute("""CREATE TABLE {} (
        round INTEGER NOT NULL, 
        match_link TEXT NOT NULL,
        attendance INTEGER NOT NULL,
        tournment TEXT,
        tournment_link TEXT,
        stadium TEXT, 
        home_team TEXT,
        home_team_score INTEGER, 
        home_team_link TEXT,
        away_team TEXT,
        away_team_score INTEGER,
        away_team_link TEXT);""".format(table_name))

        """Initialize"""
        turn = 1
        for i, match in enumerate(soup, start=1):
            match_link = match['href']
            cursor.execute("""
            INSERT INTO {} (round, match_link, attendance, tournment, tournment_link) 
            VALUES ({}, '{}', 0, '{}', '{}')
            """.format(table_name, turn, match_link, league_name, league))
            if i % 9 == 0:
                turn += 1
    except (WebDriverException, NoSuchWindowException) as e:
        print(e)

print('done.')
"""Commit and Close"""
conn.commit()
conn.close()
browser.quit()
