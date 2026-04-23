"""
Check if the database is set up correctly
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def check_setup():
    print("=" * 70)
    print("CHECKING DATABASE SETUP")
    print("=" * 70)
    
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if new schema exists
        print("\n1. Checking if tables exist...")
        tables_to_check = ['users', 'students', 'faculty', 'subjects', 
                          'faculty_classes', 'marks', 'attendance', 'feedback', 'alerts']
        
        existing_tables = []
        missing_tables = []
        
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                existing_tables.append(table)
                print(f"   ✓ {table}: {count} records")
            except:
                missing_tables.append(table)
                print(f"   ✗ {table}: NOT FOUND")
        
        if missing_tables:
            print("\n" + "=" * 70)
            print("⚠ DATABASE NOT SET UP!")
            print("=" * 70)
            print("\nMissing tables:", ", ".join(missing_tables))
            print("\nYou need to run the setup script:")
            print("  1. Run: SETUP_V2.bat")
            print("  2. Or manually: cd backend && python setup_v2.py")
            return False
        
        # Check faculty users
        print("\n2. Checking faculty users...")
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='faculty'")
        faculty_count = cursor.fetchone()[0]
        
        if faculty_count == 0:
            print("   ✗ No faculty users found!")
            print("\n" + "=" * 70)
            print("⚠ DATA NOT GENERATED!")
            print("=" * 70)
            print("\nYou need to run the setup script:")
            print("  1. Run: SETUP_V2.bat")
            print("  2. Or manually: cd backend && python setup_v2.py")
            return False
        else:
            print(f"   ✓ Found {faculty_count} faculty users")
        
        # Check student users
        print("\n3. Checking student users...")
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
        student_count = cursor.fetchone()[0]
        print(f"   ✓ Found {student_count} student users")
        
        # Show sample credentials
        print("\n4. Sample credentials:")
        
        cursor.execute("""
            SELECT u.email, u.name 
            FROM users u 
            JOIN faculty f ON u.user_id = f.user_id 
            WHERE ROWNUM <= 3
            ORDER BY u.user_id
        """)
        
        print("\n   Faculty:")
        for row in cursor.fetchall():
            print(f"   • {row[0]} / pass123 ({row[1]})")
        
        cursor.execute("""
            SELECT u.email, u.name, s.class_name
            FROM users u 
            JOIN students s ON u.user_id = s.user_id 
            WHERE ROWNUM <= 3
            ORDER BY u.user_id
        """)
        
        print("\n   Students:")
        for row in cursor.fetchall():
            print(f"   • {row[0]} / pass123 ({row[1]} - {row[2]})")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✓ DATABASE IS SET UP CORRECTLY!")
        print("=" * 70)
        print("\nYou can now start the server:")
        print("  • Run: START_SERVER_V2.bat")
        print("  • Or manually: cd backend && python app_v2.py")
        
        return True
        
    except oracledb.Error as e:
        print(f"\n✗ Database connection error: {str(e)}")
        print("\nPlease check:")
        print("  1. Oracle service is running")
        print("  2. Credentials in backend/config.py are correct")
        print("  3. Database connection string is correct")
        return False
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False

if __name__ == '__main__':
    check_setup()
