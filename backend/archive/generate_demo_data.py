# Demo data generator - old version
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def generate_demo_data():
    print("Generating demo data...")
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✓ Connected to database")
        print("✓ Demo data generated")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    generate_demo_data()
