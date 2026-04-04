import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def check_schema():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Checking database schema...")
        
        cursor.execute("""
            SELECT table_name FROM user_tables
            ORDER BY table_name
        """)
        
        print("\nTables:")
        for row in cursor.fetchall():
            print(f"  • {row[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    check_schema()
