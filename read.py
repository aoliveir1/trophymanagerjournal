# 06_read_data.py
import sqlite3

conn = sqlite3.connect('tmjournal_season60.db')
cursor = conn.cursor()

# lendo os dados
cursor.execute("""
SELECT attendance, link FROM canada WHERE round = 1 ORDER BY attendance DESC;
""")

for linha in cursor.fetchall():
    print(linha)

conn.close()
