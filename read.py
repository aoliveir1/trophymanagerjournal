import sqlite3
import time

conn = sqlite3.connect('tmjournal_season60.db')
cursor = conn.cursor()

tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = tables.fetchall()

def sortAttendance(val):
    return val[2]

while True:
    all_fixtures = []
    for table in tables:
        select1 = """SELECT tournment, '{}' as Source, attendance, stadium, home_team, home_team_score, away_team_score, 
        away_team FROM {} WHERE round = 2;""".format(table[0], table[0])
        select2 = """SELECT '{}' as Source, tournment, home_team, home_team_score, away_team_score, away_team, 
        ABS(home_team_score - away_team_score) FROM {} WHERE round = 1;""".format(table[0], table[0])
        cursor.execute(select1)
        for linha in cursor.fetchall():
            all_fixtures.append(linha)

    # all_fixtures.sort(key=sortAttendance, reverse=True)
    # all_fixtures = all_fixtures[:5]
    # for fixture in all_fixtures:
    #     print(fixture[0] + ' - ' + fixture[1].title())
    #     print('Stadium: ' + fixture[3])
    #     print('Attendance: ' + str(fixture[2]))
    #     print(fixture[4] + ' [' + str(fixture[5]) + ' x ' + str(fixture[6]) + '] ' + fixture[7])
    #     print()

    # all_fixtures.sort(key=lambda e: (e[6], e[3], e[4]), reverse=True)
    # all_fixtures = all_fixtures[:5]
    # for fixture in all_fixtures:
    #     print(fixture[1] + ' - ' + fixture[0].title())
    #     print(fixture[2] + ' [' + str(fixture[3]) + ' x ' + str(fixture[4]) + '] ' + fixture[5])
    #     print()

    time.sleep(60)

conn.close()
