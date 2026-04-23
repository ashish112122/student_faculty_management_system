"""
Verify Credentials Script
Checks if the credentials from WORKING_LINKS.md exist in the database
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def verify_credentials():
    print("=" * 80)
    print("VERIFYING CREDENTIALS")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Credentials from WORKING_LINKS.md
    test_credentials = [
        {
            'email': 'rohan.sharma.2q34.3@thapar.edu',
            'password': 'pass123',
            'role': 'student',
            'name': 'Rohan Sharma'
        },
        {
            'email': 'dr.rajesh@thaparfac.edu',
            'password': 'pass123',
            'role': 'faculty',
            'name': 'Dr. Rajesh Kumar'
        }
    ]
    
    print("\n1. Checking test credentials...")
    all_valid = True
    
    for cred in test_credentials:
        print(f"\n   Testing: {cred['email']}")
        
        cursor.execute("""
            SELECT user_id, name, role, password
            FROM users
            WHERE email = :email
        """, {'email': cred['email']})
        
        user = cursor.fetchone()
        
        if not user:
            print(f"   ERROR: User not found!")
            all_valid = False
            continue
        
        user_id, name, role, password = user
        
        # Check password
        if password != cred['password']:
            print(f"   ERROR: Password mismatch!")
            print(f"   Expected: {cred['password']}")
            print(f"   Found: {password}")
            all_valid = False
            continue
        
        # Check role
        if role != cred['role']:
            print(f"   ERROR: Role mismatch!")
            print(f"   Expected: {cred['role']}")
            print(f"   Found: {role}")
            all_valid = False
            continue
        
        print(f"   OK - User ID: {user_id}, Name: {name}, Role: {role}")
        
        # Get additional info
        if role == 'student':
            cursor.execute("""
                SELECT student_id, class_name, roll_number, cgpa
                FROM students
                WHERE user_id = :user_id
            """, {'user_id': user_id})
            student = cursor.fetchone()
            if student:
                print(f"   Student ID: {student[0]}, Class: {student[1]}, Roll: {student[2]}, CGPA: {student[3]}")
            else:
                print(f"   WARNING: Student record not found!")
                all_valid = False
        
        elif role == 'faculty':
            cursor.execute("""
                SELECT faculty_id, department, faculty_code
                FROM faculty
                WHERE user_id = :user_id
            """, {'user_id': user_id})
            faculty = cursor.fetchone()
            if faculty:
                print(f"   Faculty ID: {faculty[0]}, Department: {faculty[1]}, Code: {faculty[2]}")
            else:
                print(f"   WARNING: Faculty record not found!")
                all_valid = False
    
    print("\n2. Checking total users...")
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    print(f"   Total users in database: {total_users}")
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    total_students = cursor.fetchone()[0]
    print(f"   Total students: {total_students}")
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'faculty'")
    total_faculty = cursor.fetchone()[0]
    print(f"   Total faculty: {total_faculty}")
    
    print("\n3. Sample users from each batch...")
    cursor.execute("""
        SELECT u.email, s.class_name, s.roll_number
        FROM users u
        JOIN students s ON u.user_id = s.user_id
        WHERE s.class_name IN ('2Q31', '2Q34', '2Q40')
        AND ROWNUM <= 3
        ORDER BY s.class_name, s.roll_number
    """)
    
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]} - Roll: {row[2]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    if all_valid:
        print("VERIFICATION SUCCESSFUL!")
        print("=" * 80)
        print("\nAll test credentials are valid and working.")
        print("\nYou can now login with:")
        print("  Student: rohan.sharma.2q34.3@thapar.edu / pass123")
        print("  Faculty: dr.rajesh@thaparfac.edu / pass123")
    else:
        print("VERIFICATION FAILED!")
        print("=" * 80)
        print("\nSome credentials are missing or invalid.")
        print("Please run: python backend/setup_complete_system.py")

if __name__ == '__main__':
    verify_credentials()
