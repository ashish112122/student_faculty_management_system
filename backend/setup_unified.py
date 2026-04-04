# Unified setup script - old version
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def setup_unified():
    print("Setting up unified system...")
    try:
        conn = oracledb.connect(**DB_CONFIG)
        print("✓ Connected to database")
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    setup_unified()
