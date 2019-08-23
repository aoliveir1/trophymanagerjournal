"""
Create a database of fixtures for the current season.
Access all national top divisions pages and collect all links of all fixtures.
Create one table for each nation and insert the links for each of all fixtures and your respective round.
"""

import sqlite3

from decouple import config
from bs4 import BeautifulSoup

from utils import create_brower, sign_in

url_base = config('URL_BASE')
url_ranking = url_base + config('URL_RANKING')

"""Initialize the browser"""
browser = create_brower()

"""Login"""
sign_in(browser, url_base)

browser.visit(url_ranking)

"""Wait page load"""
while browser.is_element_not_present_by_xpath('/html/body/div[8]/div[2]/div/div[2]/div[3]/div/div[1]/div'):
    pass

"""Start scrape"""
soup = BeautifulSoup(browser.html, 'html.parser')
table = soup.find('table')
tr = table.findAll('tr')

"""Create Database"""
season = browser.find_link_by_partial_text('Season').first
season = season.text.lower().replace(' ', '')
conn = sqlite3.connect('tmjournal_' + season + '.db')
cursor = conn.cursor()

for i, td in enumerate(tr):
    if i > 0:
        """Format fixtures page link"""
        league = str(td.a['href']).replace('national-teams', 'league')
        league = league + '/1/1'
        fixtures = '/fixtures' + league
        browser.visit(url_base + fixtures)
        soup = BeautifulSoup(browser.html, 'html.parser')
        soup = soup.findAll('a', {'class': 'match_link'})

        """Create Table"""
        table_name = td.a.text.lower().replace(' ', '_').replace('-', '_').replace('\'',   '_').replace('&', '_')
        cursor.execute("""CREATE TABLE {} (
        turn INTEGER NOT NULL, 
        link TEXT NOT NULL, 
        attendance INTEGER);""".format(table_name))

        """Insert data"""
        turn = 1
        for j, match in enumerate(soup, start=1):
            link = match['href']
            cursor.execute("""
            INSERT INTO {} (turn, link, attendance) VALUES ({}, '{}', 0)
            """.format(table_name, turn, link))
            if j % 9 == 0:
                turn += 1

"""Commit and Close"""
conn.commit()
browser.quit()
conn.close()
