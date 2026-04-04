import oracledb
from backend.config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def check_tables():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Checking tables...")
        
        tables = ['users', 'students', 'faculty', 'subjects', 'student_subjects', 
                 'marks', 'attendance', 'alerts', 'feedback', 'faculty_classes']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✓ {table}: {count} records")
            except Exception as e:
                print(f"✗ {table}: {str(e)}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    check_tables()
