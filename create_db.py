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

for td in tr[1:]:
    try:
        """Format fixtures page link"""
        league = str(td.a['href']).replace('national-teams', 'league')
        league = league + '/1/1'
        fixtures = '/fixtures' + league
        browser.visit(url_base + fixtures)
        soup = BeautifulSoup(browser.html, 'html.parser')
        soup = soup.findAll('a', {'class': 'match_link'})

        """Create Table"""
        table_name = td.a.text.lower().replace(' ', '_').replace('-', '_').replace('\'',   '_').replace('&', '_')
        print('Create table: ' + table_name)
        cursor.execute("""CREATE TABLE {} (
        round INTEGER NOT NULL, 
        link TEXT NOT NULL,
        stadium TEXT, 
        home TEXT, 
        away TEXT , 
        attendance INTEGER,
        scoreboard TEXT);""".format(table_name))

        """Insert data"""
        turn = 1
        for i, match in enumerate(soup, start=1):
            link = match['href']
            cursor.execute("""
            INSERT INTO {} (round, link) 
            VALUES ({}, '{}')
            """.format(table_name, turn, link))
            if i % 9 == 0:
                turn += 1
    except (WebDriverException, NoSuchWindowException) as e:
        print(e)

"""Commit and Close"""
conn.commit()
browser.quit()
conn.close()
