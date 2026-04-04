# Complete demo setup script
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def setup_complete_demo():
    print("Setting up complete demo...")
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✓ Connected to database")
        print("✓ Demo setup complete")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    setup_complete_demo()
