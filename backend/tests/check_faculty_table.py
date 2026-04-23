import oracledb
from config import Config

conn = oracledb.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=Config.DB_DSN)
cursor = conn.cursor()

cursor.execute("SELECT column_name FROM user_tab_columns WHERE table_name = 'FACULTY'")
print("Faculty table columns:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.close()
conn.close()
