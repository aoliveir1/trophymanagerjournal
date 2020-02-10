"""Collect matches data and update tables"""

import time
import sqlite3
from bs4 import BeautifulSoup
from decouple import config
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, InvalidSessionIdException
from splinter.exceptions import ElementDoesNotExist

from utils import create_brower, sign_in

conn = sqlite3.connect('tmjournal_season62.db')
cursor = conn.cursor()
conn_players = sqlite3.connect('rating_players_season62.db')
cursor_players = conn_players.cursor()


def get_table_list(index: int) -> list:
    """Returns a list containing table names.
    Index 0 for all tables. Index 1 to 14 for the tables contained in the list."""
    db_tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    all_tables = [table[0] for table in db_tables]

    # 00:00
    prev1 = ['fixtures_paraguay', 'fixtures_panama', 'fixtures_cuba', 'fixtures_venezuela', 'fixtures_ecuador',
             'fixtures_dominican_republic', 'fixtures_trinidad___tobago', 'fixtures_west_indies', 'fixtures_colombia']

    # 00:00, 01:00
    prev2 = ['fixtures_bolivia', 'fixtures_peru', 'fixtures_jamaica', 'fixtures_mexico', 'fixtures_puerto_rico',
             'fixtures_canada', 'fixtures_honduras', 'fixtures_belize', 'fixtures_el_salvador']

    # 01:00, 08:00, 10:00, 11:00
    prev3 = ['fixtures_united_states', 'fixtures_guatemala', 'fixtures_costa_rica', 'fixtures_new_zealand',
             'fixtures_fiji', 'fixtures_oceania', 'fixtures_australia', 'fixtures_hong_kong', 'fixtures_singapore']

    # 11:00, 12:00
    prev4 = ['fixtures_philippines', 'fixtures_brunei_darussalam', 'fixtures_taiwan', 'fixtures_chinese_beijing',
             'fixtures_malaysia', 'fixtures_japan', 'fixtures_south_korea', 'fixtures_indonesia', 'fixtures_thailand']

    # 12:00, 13:00, 14:00
    prev5 = ['fixtures_vietnam', 'fixtures_kazakhstan', 'fixtures_nepal', 'fixtures_india', 'fixtures_bangladesh',
             'fixtures_afghanistan', 'fixtures_pakistan', 'fixtures_united_arab_emirates', 'fixtures_azerbaijan']

    # 14:00, 15:00
    prev6 = ['fixtures_oman', 'fixtures_iran', 'fixtures_georgia', 'fixtures_armenia', 'fixtures_qatar',
             'fixtures_ukraine', 'fixtures_turkey', 'fixtures_palestine', 'fixtures_kuwait']

    # 15:00
    prev7 = ['fixtures_saudi_arabia', 'fixtures_lebanon', 'fixtures_jordan', 'fixtures_bahrain', 'fixtures_moldova',
             'fixtures_russia', 'fixtures_romania', 'fixtures_estonia', 'fixtures_bulgaria']

    # 15:00, 16:00
    prev8 = ['fixtures_iraq', 'fixtures_belarus', 'fixtures_lithuania', 'fixtures_syria', 'fixtures_latvia',
             'fixtures_bosnia_herzegovina', 'fixtures_croatia', 'fixtures_finland', 'fixtures_montenegro']

    # 16:00
    prev9 = ['fixtures_hungary', 'fixtures_czech_republic', 'fixtures_greece', 'fixtures_egypt', 'fixtures_poland',
             'fixtures_slovenia', 'fixtures_libya', 'fixtures_botswana', 'fixtures_cyprus', 'fixtures_slovakia']

    # 16:00, 18:00
    prev10 = ['fixtures_israel', 'fixtures_serbia', 'fixtures_north_macedonia', 'fixtures_albania', 'fixtures_cameroun',
              'fixtures_belgium', 'fixtures_south_africa', 'fixtures_switzerland', 'fixtures_norway']

    # 18:00
    prev11 = ['fixtures_malta', 'fixtures_denmark', 'fixtures_sweden', 'fixtures_austria', 'fixtures_spain',
              'fixtures_san_marino', 'fixtures_france', 'fixtures_germany', 'fixtures_andorra']

    # 18:00, 20:00
    prev12 = ['fixtures_italy', 'fixtures_netherlands', 'fixtures_luxembourg', 'fixtures_portugal', 'fixtures_ireland',
              'fixtures_algeria', 'fixtures_ghana', 'fixtures_cote_d_ivoire', 'fixtures_northern_ireland']

    # 20:00, 21:00
    prev13 = ['fixtures_nigeria', 'fixtures_angola', 'fixtures_iceland', 'fixtures_scotland', 'fixtures_faroe_islands',
              'fixtures_chad', 'fixtures_wales', 'fixtures_morocco', 'fixtures_senegal']

    # 20:00, 21:00
    prev14 = ['fixtures_england', 'fixtures_tunisia', 'fixtures_chile', 'fixtures_argentina', 'fixtures_brazil',
              'fixtures_uruguay']

    table_list = (all_tables, prev1, prev2, prev3, prev4, prev5, prev6, prev7, prev8, prev9, prev10, prev11, prev12,
                  prev13, prev14)

    return table_list[index]


def update_matches_table(fixture_data: list) -> str:
    """Formats a query."""
    table_name = fixture_data[0]
    attendance = fixture_data[1]
    stadium = fixture_data[2]
    home_team = fixture_data[3]
    home_team_score = fixture_data[4]
    home_team_link = fixture_data[5]
    away_team = fixture_data[6]
    away_team_score = fixture_data[7]
    away_team_link = fixture_data[8]
    match_link = fixture_data[9]
    update = """UPDATE {} SET 
    attendance = {}, stadium = "{}", home_team = "{}", home_team_score = {}, home_team_link = "{}", away_team = "{}", 
    away_team_score = {}, away_team_link = "{}" WHERE match_link = '{}'""". \
        format(table_name, attendance, stadium, home_team, home_team_score, home_team_link, away_team, away_team_score,
               away_team_link, match_link)
    return update


def create_players_table(table_name: str) -> str:
    """Formats a query."""
    create_table = '''CREATE TABLE IF NOT EXISTS {} (player_name TEXT, player_age TEXT, player_wage FLOAT, 
    player_position TEXT, player_nation TEXT, player_link TEXT, player_si INTEGER, player_rating FLOAT, player_goals 
    INTEGER, turn INTEGER, turn_link TEXT, team TEXT, team_link TEXT)'''.format(table_name)
    return create_table


def insert_players_data(players_data: list) -> str:
    """Formats a query."""
    table = players_data[0]
    name = players_data[1]
    age = players_data[2]
    wage = players_data[3]
    link = players_data[4]
    si = players_data[5]
    position = players_data[6]
    rating = players_data[7]
    goals = players_data[8]
    team = players_data[9]
    team_link = players_data[10]
    turn = players_data[11]
    nation = players_data[12]
    insert_players_data = '''INSERT INTO {} (player_name, player_age, player_wage, player_link, player_si, 
    player_position, player_rating, player_goals, team, team_link, turn, player_nation) VALUES ("{}", {}, {}, "{}", {}, 
    "{}", {}, {}, "{}", "{}", {}, "{}");'''.\
        format(table, name, age, wage, link, si, position, rating, goals, team, team_link, turn, nation)
    return insert_players_data


def get_match_data(link):
    """Receive the match link and scrape for the data."""
    # link = '/matches/148692932/'  #  Forfeit example
    # link = '/matches/148693198/'  #  April match
    try:
        players = []
        url_match = url_base + link
        browser.visit(url_match)
        browser.visit(url_match)

        # Go to report is a button that appears when the game ends
        while browser.is_element_not_present_by_css('.go_to_report'):
            time.sleep(3)
            if browser.is_element_not_present_by_css('.field > div:nth-child(1)'):
                attendance = -1
                stadium = ''
                print('Forfeit')
                break
            print('.', end='')

        """Get match data"""
        if browser.is_element_present_by_css('.go_to_report'):
            # Click to see report
            browser.find_by_css('.go_to_report').first.click()

            attendance = browser.find_by_css('.attendance').first
            attendance = attendance.text.strip()
            attendance = attendance.replace(',', '')

            stadium = browser.find_by_xpath('/html/body/div[8]/div[2]/div/div[10]/div/ul[1]/li[1]').first
            stadium = stadium.text.strip().replace('“', '\'').replace('"', '\'').replace('¨', '\'')

        while browser.is_element_not_present_by_css('div.score'):
            print('.', end='')
        scoreboard = browser.find_by_css('div.score').first
        scoreboard = scoreboard.text.strip()
        scoreboard = scoreboard.split('-')
        home_team_score, away_team_score = [s.strip() for s in scoreboard]

        try:
            home_team = browser.find_by_xpath('/html/body/div[8]/div[1]/div[3]/div/div[2]/div[2]/a').first
            home_team_link = browser.find_by_css('div.names:nth-child(2) > a:nth-child(1)').first
            home_team_link = home_team_link['href']

            away_team = browser.find_by_css('div.names:nth-child(4) > a:nth-child(1)').first
            away_team_link = browser.find_by_css('div.names:nth-child(4) > a:nth-child(1)').first
            away_team_link = away_team_link['href']
        except:
            home_team = browser.find_by_css(
                'body > div:nth-child(9) > div.box_body.mv_bottom > div > div:nth-child(6) > div > div.nameplate > div.overlay > div.home.name.bold').first
            home_team_link = 'https://trophymanager.com/club/' + home_team['club_link']
            away_team = browser.find_by_css(
                'body > div:nth-child(9) > div.box_body.mv_bottom > div > div:nth-child(6) > div > div.nameplate > div.overlay > div.away.name.bold')
            away_team_link = 'https://trophymanager.com/club/' + away_team['club_link']

        home_team = home_team.text.strip().replace('“', '\'').replace('"', '\'')
        away_team = away_team.text.strip().replace('“', '\'').replace('"', '\'')

        """Players stats"""
        soup = BeautifulSoup(browser.html, 'html.parser')
        soup = soup.findAll('ul', {'class': 'player_list underlined_slim tleft'})
        for i, team in enumerate(soup):
            if i == 0:
                team_name = home_team
                team_link = home_team_link

            if i == 1:
                team_name = away_team
                team_link = away_team_link

            player = team.findAll('li')
            for item in player:
                href = item.a['href']
                link = 'https://trophymanager.com' + href

                player_nation = ''
                age = 0
                wage = 0
                si = 0

                # '''Player SI'''
                browser.visit(link)
                try:
                    player_nation = BeautifulSoup(browser.html, 'html.parser')
                    player_nation = player_nation.find('div', {'class': 'large'})
                    player_nation = player_nation.find('a', {'class': 'country_link'})
                    player_nation = player_nation['href']
                    player_nation = player_nation.replace('/national-teams/', '').replace('/', '')
                except:
                    player_nation = ''
                try:
                    age = browser.find_by_css(
                        'body > div:nth-child(9) > div.column2_a > div > div.box_body > div:nth-child(4) > table > tbody > tr:nth-child(3) > td')
                    age = age.text
                    age = age.replace(' Years ', '.').replace('Months', '')
                except:
                    age = 0
                try:
                    wage = browser.find_by_css(
                        'body > div:nth-child(9) > div.column2_a > div > div.box_body > div:nth-child(4) > table > tbody > tr:nth-child(5) > td > span')
                    wage = wage.text
                    wage = wage.replace(',', '')
                    wage = int(wage)
                except:
                    wage = 0
                try:
                    si = browser.find_by_css('.float_left > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2)')
                    si = si.text
                    si = si.replace(',', '')
                    si = int(si)
                except:
                    si = 0
                # ''' End Player SI'''

                name = item.find('div', {'class': 'name'})
                name = name.text
                try:
                    rating = item.find('div', {'class': 'rating'})
                    rating = float(rating.text)
                except:
                    rating = 0
                position = item.find('div', {'class': 'position'})
                position = position.text
                goal = item.findAll('img', {'src': '/pics/icons/ball.gif'})

                player = [name, age, wage, link, si, position, rating, len(goal), team_name, team_link, player_nation]
                players.append(player)

        return attendance, stadium, home_team, home_team_score, home_team_link, away_team, away_team_score, away_team_link, players
    except (InvalidSessionIdException, NoSuchWindowException, WebDriverException) as e:
        print(e.msg)
        return None
    except ElementDoesNotExist as e:
        print(e)
        return None


url_base = config('URL_BASE')
"""Initialize the browser and log in"""
browser = create_brower()
browser.driver.maximize_window()
sign_in(browser, url_base)

tables = get_table_list(0)
tables_fails = []
for table in tables:
    turn = 7
    query = """SELECT round, match_link FROM {} WHERE round = {} and attendance = 0;""".format(table, turn)
    columns = cursor.execute(query).fetchall()
    for column in columns:
        if column[0] == turn:
            print(table, column[1])
            match_data = get_match_data(column[1])
            if match_data is not None:
                try:
                    attendance = match_data[0]
                    stadium = match_data[1]
                    home_team = match_data[2]
                    home_team_score = match_data[3]
                    home_team_link = match_data[4]
                    away_team = match_data[5]
                    away_team_score = match_data[6]
                    away_team_link = match_data[7]
                    data = [table, attendance, stadium, home_team, home_team_score, home_team_link, away_team,
                            away_team_score, away_team_link, column[1]]
                    for player in match_data[8]:
                        player_link = player[3]
                        table_name = player_link
                        table_name = table_name.lstrip('https://trophymanager.com/players/')
                        table_name = 't_' + table_name
                        table_name = table_name.replace('/', '')
                        create_table = create_players_table(table_name)
                        # print(create_table)
                        cursor_players.execute(create_table)
                        conn_players.commit()
                        players_data = [table_name, player[0], player[1], player[2], player[3], player[4], player[5],
                                        player[6], player[7], player[8], player[9], turn, player[10]]
                        insert_players_rating = insert_players_data(players_data)
                        print(insert_players_rating)
                        cursor_players.execute(insert_players_rating)
                        conn_players.commit()
                    update = update_matches_table(data)
                    print(update)
                    cursor.execute(update)
                    conn.commit()
                    print()
                except:
                    tables_fails.append((table, column[1]))

conn_players.close()
conn.close()
browser.quit()

if tables_fails:
    print(tables_fails)
