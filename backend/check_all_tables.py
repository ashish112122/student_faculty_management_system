import oracledb
from config import Config

conn = oracledb.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=Config.DB_DSN)
cursor = conn.cursor()

cursor.execute("SELECT table_name FROM user_tables ORDER BY table_name")
print("All tables:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.close()
conn.close()
