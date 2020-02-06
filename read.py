import sqlite3
import time

turn1 = 1
turn2 = 5
turn_current = 7
conn_countries = sqlite3.connect('tmjournal_season62.db')
cursor = conn_countries.cursor()
conn_players = sqlite3.connect('rating_players_season62.db')
cursor_players = conn_players.cursor()


def get_all_countries_tables() -> list:
    """Returns a list containing all tables of countries."""
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    tables = [table[0] for table in tables]
    return tables


def get_all_players_tables() -> list:
    """Returns a list containing all tables of players."""
    tables = cursor_players.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    tables = [table[0] for table in tables]
    return tables


def get_attendance() -> list:
    """Perform queries on all countries tables and returns a list containing top highest attendances."""
    fixtures = []
    for table in get_all_countries_tables():
        select = """SELECT tournment, country, attendance, stadium, home_team, home_team_score, home_team_link, 
        away_team_link, away_team_score, away_team, match_link, round FROM {} WHERE round BETWEEN {} and {} ORDER BY 
        attendance DESC;""".format(table, turn1, turn2)
        attendance = cursor.execute(select).fetchall()
        for a in attendance:
            fixtures.append(a)
    fixtures.sort(key=lambda e: (e[2]), reverse=True)
    return fixtures[:5]


def set_attendance() -> bool:
    """Just prints on the screen."""
    attendances = get_attendance()
    for fixture in attendances:
        print('Attendance: ' + str(fixture[2]))
        print(fixture[4] + ' ' + str(fixture[5]) + ' x ' + str(fixture[8]) + ' ' + fixture[9] + ' at ' + str(fixture[3]))
        print(fixture[0] + ', ' + fixture[1].title() + '. Round ' + str(fixture[11]))
        print()
    return True


def get_scores() -> list:
    """Perform queries on all countries tables and returns a list containing top highest scores."""
    fixtures = []
    for table in get_all_countries_tables():
        select = """SELECT country, tournment, attendance, home_team, home_team_score, home_team_link, away_team_link, 
                away_team_score, away_team, ABS(home_team_score - away_team_score), match_link, round, stadium FROM {} 
                WHERE round BETWEEN {} and {};""".format(table, turn1, turn_current)
        score = cursor.execute(select).fetchall()
        for s in score:
            fixtures.append(s)
    fixtures.sort(key=lambda e: (e[9], e[4], e[3]), reverse=True)
    return fixtures[:5]


def set_scores() -> bool:
    """Just prints on the screen."""
    scores = get_scores()
    for fixture in scores:
        print(fixture[3] + ' ' + str(fixture[4]) + ' x ' + str(fixture[7]) + ' ' + fixture[8] + ' at ' + str(fixture[12]))
        print(fixture[1] + ', ' + fixture[0].title() + '. Round ' + str(fixture[11]))
        print()
    return True


def get_players_rating() -> list:
    """Perform queries on all players tables and returns a list containing top highest average ratings."""
    ratings = []
    for table in get_all_players_tables():
        select = '''SELECT player_name, player_position, player_age, player_rating, team FROM {} WHERE turn BETWEEN {} 
        AND {};'''.format(table, turn1, turn2)
        player = cursor_players.execute(select).fetchall()
        total_matches = 0
        total_rating = 0
        average_rating = 0
        name = ''
        position = ''
        age = ''
        team = ''
        for line in player:
            total_matches += 1
            name = line[0]
            position = line[1]
            age = line[2]
            rating = line[3]
            total_rating += rating
            total_rating = round(total_rating, 2)
            average_rating = total_rating / total_matches
            average_rating = round(average_rating, 2)
            team = line[4]
        if total_matches >= (turn_current / 2):
            ratings.append((name, position, age, average_rating, total_matches, team))
    ratings.sort(key=lambda e: (e[3]), reverse=True)
    return ratings[:4]


def set_players_rating() -> bool:
    """Just prints on the screen."""
    ratings = get_players_rating()
    for i, player in enumerate(ratings):
        print(str(i+1) + 'º - ' + player[0] + ' (' + player[5] + ')')
        print('Rating: ' + str(player[3]))
        print()
    return True


def get_players_scorers() -> list:
    """Perform queries on all players tables and returns a list containing top highest scorers."""
    scorers = []
    for table in get_all_players_tables():
        select = '''SELECT player_name, player_position, player_age, player_goals, team FROM {} WHERE turn BETWEEN 1 
        AND {};'''.format(table, turn_current)
        player = cursor_players.execute(select).fetchall()
        total_matches = 0
        total_goals = 0
        name = ''
        position = ''
        age = ''
        team = ''
        for line in player:
            total_matches += 1
            name = line[0]
            position = line[1]
            age = line[2]
            goals = line[3]
            total_goals += goals
            team = line[4]
        scorers.append((name, position, age, total_goals, total_matches, team))
    scorers.sort(key=lambda e: (e[3]), reverse=True)
    return scorers[:4]


def set_players_scorers() -> bool:
    """Just prints on the screen."""
    scorers = get_players_scorers()
    for i, player in enumerate(scorers):
        print(str(i+1) + 'º - ' + player[0] + ' (' + player[5] + ')')
        print('Goals: ' + str(player[3]))
        print()
    return True

print('[Attendance]')
set_attendance()
print('[Scores]')
set_scores()
print('[Best players]')
set_players_rating()
print('Top scorers')
set_players_scorers()
