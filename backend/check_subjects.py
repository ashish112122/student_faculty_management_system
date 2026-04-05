import oracledb
from config import Config

conn = oracledb.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=Config.DB_DSN)
cursor = conn.cursor()

cursor.execute("SELECT column_name FROM user_tab_columns WHERE table_name = 'SUBJECTS'")
print("SUBJECTS table columns:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.execute("SELECT column_name FROM user_tab_columns WHERE table_name = 'ALERTS'")
print("\nALERTS table columns:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.execute("SELECT column_name FROM user_tab_columns WHERE table_name = 'FEEDBACK'")
print("\nFEEDBACK table columns:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

cursor.close()
conn.close()
