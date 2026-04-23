import oracledb
from config import Config

conn = oracledb.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=Config.DB_DSN)
cursor = conn.cursor()

for table in ['MARKS', 'ATTENDANCE', 'ALERTS', 'FACULTY_CLASSES']:
    cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table}'")
    print(f"\n{table} columns:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")

cursor.close()
conn.close()
