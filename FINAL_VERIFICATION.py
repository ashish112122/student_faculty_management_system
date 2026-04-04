import oracledb
from backend.config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def verify_system():
    print("=" * 70)
    print("FINAL SYSTEM VERIFICATION")
    print("=" * 70)
    
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check tables
        print("\n1. Checking tables...")
        tables = ['users', 'students', 'faculty', 'subjects', 'faculty_classes',
                 'student_subjects', 'marks', 'attendance', 'feedback', 'alerts']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✓ {table}: {count} records")
            except:
                print(f"   ✗ {table}: NOT FOUND")
        
        # Check faculty
        print("\n2. Faculty members:")
        cursor.execute("""
            SELECT u.email, u.name
            FROM users u
            JOIN faculty f ON u.user_id = f.user_id
            ORDER BY f.faculty_id
        """)
        for row in cursor.fetchall():
            print(f"   • {row[0]} - {row[1]}")
        
        # Check students
        print("\n3. Students:")
        cursor.execute("""
            SELECT u.email, u.name, s.class_name
            FROM users u
            JOIN students s ON u.user_id = s.user_id
            ORDER BY s.student_id
        """)
        for row in cursor.fetchall():
            print(f"   • {row[0]} - {row[1]} ({row[2]})")
        
        # Check faculty-class assignments
        print("\n4. Faculty-Class Assignments:")
        cursor.execute("""
            SELECT u.name, fc.class_name, sub.subject_name
            FROM faculty_classes fc
            JOIN faculty f ON fc.faculty_id = f.faculty_id
            JOIN users u ON f.user_id = u.user_id
            JOIN subjects sub ON fc.subject_id = sub.subject_id
            ORDER BY u.name, fc.class_name
        """)
        for row in cursor.fetchall():
            print(f"   • {row[0]} → {row[1]} → {row[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✓ VERIFICATION COMPLETE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == '__main__':
    verify_system()
