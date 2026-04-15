import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

conn = oracledb.connect(**DB_CONFIG)
cursor = conn.cursor()

print("ALL TABLES IN DATABASE:")
print("=" * 60)
cursor.execute("""
    SELECT table_name 
    FROM user_tables 
    ORDER BY table_name
""")

for row in cursor.fetchall():
    print(f"- {row[0]}")

cursor.close()
conn.close()
