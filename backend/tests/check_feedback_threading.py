import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

conn = oracledb.connect(**DB_CONFIG)
cursor = conn.cursor()

print("FEEDBACK_THREADS TABLE STRUCTURE:")
print("=" * 60)
cursor.execute("""
    SELECT column_name, data_type, nullable
    FROM user_tab_columns 
    WHERE table_name = 'FEEDBACK_THREADS' 
    ORDER BY column_id
""")

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} - Nullable: {row[2]}")

print("\n" + "=" * 60)
print("FEEDBACK_MESSAGES TABLE STRUCTURE:")
print("=" * 60)
cursor.execute("""
    SELECT column_name, data_type, nullable
    FROM user_tab_columns 
    WHERE table_name = 'FEEDBACK_MESSAGES' 
    ORDER BY column_id
""")

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} - Nullable: {row[2]}")

print("\n" + "=" * 60)
print("SAMPLE DATA:")
cursor.execute("SELECT COUNT(*) FROM feedback_threads")
thread_count = cursor.fetchone()[0]
print(f"Total threads: {thread_count}")

cursor.execute("SELECT COUNT(*) FROM feedback_messages")
message_count = cursor.fetchone()[0]
print(f"Total messages: {message_count}")

cursor.close()
conn.close()
