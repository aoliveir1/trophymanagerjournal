import sqlite3

conn = sqlite3.connect('tmjournal_season60.db')
cursor = conn.cursor()

tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = tables.fetchall()

all_fixtures = []
for table in tables:
    # lendo os dados
    cursor.execute("""
    SELECT attendance, round, link FROM {} WHERE round = 1;
    """.format(table[0]))

    for linha in cursor.fetchall():
        all_fixtures.append(linha)

all_fixtures.sort(reverse=True)

all_fixtures = all_fixtures[:100]

for fixture in all_fixtures:
    print(fixture)


conn.close()
