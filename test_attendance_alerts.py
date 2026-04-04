import oracledb
from backend.config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def test_alerts():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Testing attendance alerts...")
        
        cursor.execute("""
            SELECT s.student_id, u.name, sub.subject_name,
                   COUNT(*) as total,
                   SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
            FROM students s
            JOIN users u ON s.user_id = u.user_id
            JOIN attendance a ON s.student_id = a.student_id
            JOIN subjects sub ON a.subject_id = sub.subject_id
            GROUP BY s.student_id, u.name, sub.subject_name
            HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
        """)
        
        print("\nStudents with low attendance:")
        for row in cursor.fetchall():
            percentage = (row[4] / row[3]) * 100
            print(f"{row[1]} - {row[2]}: {percentage:.1f}% ({row[4]}/{row[3]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    test_alerts()
