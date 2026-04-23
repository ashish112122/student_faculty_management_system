import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

conn = oracledb.connect(**DB_CONFIG)
cursor = conn.cursor()

print("FEEDBACK TABLE STRUCTURE:")
print("=" * 60)
cursor.execute("""
    SELECT column_name, data_type, data_length, nullable
    FROM user_tab_columns 
    WHERE table_name = 'FEEDBACK' 
    ORDER BY column_id
""")

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}({row[2]}) - Nullable: {row[3]}")

print("\n" + "=" * 60)
print("SAMPLE FEEDBACK RECORDS:")
cursor.execute("SELECT * FROM feedback WHERE ROWNUM <= 3")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
