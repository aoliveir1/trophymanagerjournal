"""Collect matches data and update tables"""

import time
import sqlite3
from bs4 import BeautifulSoup
from decouple import config
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, InvalidSessionIdException
from splinter.exceptions import ElementDoesNotExist

from utils import create_brower, sign_in

conn = sqlite3.connect('tmjournal_season64.db')
cursor = conn.cursor()
conn_players = sqlite3.connect('rating_players_season64.db')
cursor_players = conn_players.cursor()


def get_table_list(index: int) -> list:
    """Returns a list containing table names.
    Index 0 for all tables. Index 1 to 14 for the tables contained in the list."""
    db_tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    all_tables = [table[0] for table in db_tables]
    all_tables.remove('brazil_2_1')
    all_tables.remove('brazil_2_2')
    all_tables.remove('brazil_2_3')
    all_tables.remove('brazil_2_4')

    # 00:00
    prev1 = ['paraguay', 'panama', 'cuba', 'venezuela', 'ecuador', 'dominican_republic', 'trinidad___tobago',
             'west_indies', 'colombia']

    # 00:00, 01:00
    prev2 = ['bolivia', 'peru', 'jamaica', 'mexico', 'puerto_rico', 'canada', 'honduras', 'belize', 'el_salvador']

    # 01:00, 08:00, 10:00, 11:00
    prev3 = ['united_states', 'guatemala', 'costa_rica', 'new_zealand', 'fiji', 'oceania', 'australia', 'hong_kong',
             'singapore']

    # 11:00, 12:00
    prev4 = ['philippines', 'brunei_darussalam', 'taiwan', 'chinese_beijing', 'malaysia', 'japan', 'south_korea',
             'indonesia', 'thailand']

    # 12:00, 13:00, 14:00
    prev5 = ['vietnam', 'kazakhstan', 'nepal', 'india', 'bangladesh', 'afghanistan', 'pakistan', 'united_arab_emirates',
             'azerbaijan']

    # 14:00, 15:00
    prev6 = ['oman', 'iran', 'georgia', 'armenia', 'qatar', 'ukraine', 'turkey', 'palestine', 'kuwait']

    # 15:00
    prev7 = ['saudi_arabia', 'lebanon', 'jordan', 'bahrain', 'moldova', 'russia', 'romania', 'estonia', 'bulgaria']

    # 15:00, 16:00
    prev8 = ['iraq', 'belarus', 'lithuania', 'syria', 'latvia', 'bosnia_herzegovina', 'croatia', 'finland',
             'montenegro']

    # 16:00
    prev9 = ['hungary', 'czech_republic', 'greece', 'egypt', 'poland', 'slovenia', 'libya', 'botswana', 'cyprus']

    # 16:00, 18:00
    prev10 = ['slovakia', 'israel', 'serbia', 'north_macedonia', 'albania', 'cameroun', 'belgium', 'south_africa',
              'switzerland']

    # 18:00
    prev11 = ['malta', 'denmark', 'sweden', 'austria', 'spain', 'san_marino', 'france', 'germany', 'andorra']

    # 18:00, 20:00
    prev12 = ['norway', 'italy', 'netherlands', 'luxembourg', 'portugal', 'ireland', 'algeria', 'ghana',
              'cote_d_ivoire']

    # 20:00
    prev13 = ['northern_ireland', 'nigeria', 'angola', 'iceland', 'scotland', 'faroe_islands', 'chad', 'wales',
              'morocco']

    # 20:00, 21:00
    prev14 = ['senegal', 'england', 'tunisia', 'chile', 'argentina', 'brazil', 'uruguay']

    table_list = (all_tables, prev1, prev2, prev3, prev4, prev5, prev6, prev7, prev8, prev9, prev10, prev11, prev12,
                  prev13, prev14)

    return table_list[index]


def update_matches_table(fixture_data: list) -> str:
    """Formats a query for update matches tables."""
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
    """Formats a query for create table if not exists."""
    create_table = '''CREATE TABLE IF NOT EXISTS {} (player_name TEXT, player_age TEXT, player_wage FLOAT, 
    player_position TEXT, player_nation TEXT, player_link TEXT, player_si INTEGER, player_rating FLOAT, player_goals 
    INTEGER, turn INTEGER, turn_link TEXT, team TEXT, team_link TEXT, team_nation TEXT)'''.format(table_name)
    return create_table


def insert_players_data(players_data: list) -> str:
    """Formats a query for insert."""
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
    player_nation = players_data[12]
    team_nation = players_data[13]
    insert_players_data = '''INSERT INTO {} (player_name, player_age, player_wage, player_link, player_si, 
    player_position, player_rating, player_goals, team, team_link, turn, player_nation, team_nation) VALUES 
    ("{}", "{}", {}, "{}", {}, "{}", {}, {}, "{}", "{}", {}, "{}", "{}");'''.\
        format(table, name, age, wage, link, si, position, rating, goals, team, team_link, turn, player_nation, team_nation)
    return insert_players_data


def get_match_data(link):
    """Receive the match link and scrape for the data."""
    try:
        players = []
        url_match = url_base + link
        browser.visit(url_match)
        browser.visit(url_match)

        # base_xpath = '/html/body/div[8]/div[2]'  # non pro
        base_xpath = '/html/body/div[5]/div[2]'  # with pro

        # Go to report is a button that appears when the game ends
        while browser.is_element_not_present_by_css('.go_to_report'):
            time.sleep(5)
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

            # '/html/body/div[8]/div[2]/div/div[10]/div/ul[1]/li[1]'
            stadium = browser.find_by_xpath(base_xpath + '/div/div[10]/div/ul[1]/li[1]').first
            stadium = stadium.text.strip().replace('“', '\'').replace('"', '\'').replace('¨', '\'')
        try:
            while browser.is_element_not_present_by_css('div.score'):
                print('.', end='')
            scoreboard = browser.find_by_css('div.score').first
            scoreboard = scoreboard.text.strip()
            scoreboard = scoreboard.split('-')
            home_team_score, away_team_score = [s.strip() for s in scoreboard]
        except:
            return None
        try:
            home_team = browser.find_by_xpath('/html/body/div[5]/div/div[3]/div/div[2]/div[2]/a').first
            home_team_link = browser.find_by_css('div.names:nth-child(2) > a:nth-child(1)').first
            home_team_link = home_team_link['href']

            away_team = browser.find_by_css('div.names:nth-child(4) > a:nth-child(1)').first
            away_team_link = browser.find_by_css('div.names:nth-child(4) > a:nth-child(1)').first
            away_team_link = away_team_link['href']
        except:
            home_team = browser.find_by_xpath(base_xpath + '/div/div[6]/div/div[1]/div[3]/div[3]').first
            id = home_team['club_link']
            home_team_link = 'https://trophymanager.com/club/' + id
            away_team = browser.find_by_xpath(base_xpath + '/div/div[6]/div/div[1]/div[3]/div[2]').first
            id = away_team['club_link']
            away_team_link = 'https://trophymanager.com/club/' + id

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
                t_name = href.replace('/players/', 't_')
                name = item.find('div', {'class': 'name'})
                name = name.text
                position = item.find('div', {'class': 'position'})
                position = position.text
                try:
                    rating = item.find('div', {'class': 'rating'})
                    rating = float(rating.text)
                except:
                    rating = 0
                goal = item.findAll('img', {'src': '/pics/icons/ball.gif'})

                player_nation = ''
                team_nation = ''
                age = 0
                wage = 0
                si = 0

                '''Player SI'''
                '/html/body/div[8]/div[2]/div/div[2]/div[2]/div/strong'
                if t_name in set_tables():
                    print('player in set tables')
                    try:
                        browser.visit(link)
                        name = browser.find_by_xpath(base_xpath + '/div/div[2]/div[2]/div/strong').first
                        name = name.text
                        p = name.find('.')
                        name = name[p+2:]
                    except:
                        # print('não peguei o nome no try')
                        pass
                    try:
                        position = browser.find_by_xpath(base_xpath + '/div[2]/div/div[2]/div[2]/div/span[2]/strong/span/span').first
                        position = position['class']
                    except:
                        # print('não peguei a posição no try')
                        pass
                    try:
                        position2 = browser.find_by_xpath(
                            base_xpath + '/div/div[2]/div[2]/div/span[2]/strong/span/span[3]').first
                        position2 = position2['class']
                        if position2 != 'split':
                            position = position + '/' + position2
                    except:
                        pass
                    try:
                        player_nation = BeautifulSoup(browser.html, 'html.parser')
                        player_nation = player_nation.find('div', {'class': 'large'})
                        player_nation = player_nation.find('a', {'class': 'country_link'})
                        player_nation = player_nation['href']
                        player_nation = player_nation.replace('/national-teams/', '').replace('/', '')
                    except:
                        player_nation = ''
                    try:
                        team_nation = browser.find_by_xpath(base_xpath + '/div/div[2]/div[4]/table/tbody/tr[2]/td/a[2]').first
                        team_nation = team_nation['href']
                        team_nation = team_nation[-3:-1]
                    except:
                        team_nation = ''
                        # input('cant find team nation, ' + str(item))
                    try:
                        age = browser.find_by_xpath(base_xpath + '/div/div[2]/div[4]/table/tbody/tr[3]/td')
                        age = age.text
                        age = age.replace(' Years ', '.').replace('Months', '')
                        age = age.replace(' Anos ', '.').replace('Meses', '')
                    except:
                        age = 0
                    try:
                        wage = browser.find_by_xpath(base_xpath + '/div/div[2]/div[4]/table/tbody/tr[5]/td/span')
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
                ''' End Player SI'''

                player = [name, age, wage, link, si, position, rating, len(goal), team_name, team_link, player_nation, team_nation]
                players.append(player)

        return [attendance, stadium, home_team, home_team_score, home_team_link, away_team, away_team_score,
                away_team_link, players]
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
