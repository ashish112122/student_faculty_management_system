"""
System Test After Cleanup
Tests all major functionality to ensure nothing is broken
"""
import oracledb
from config import Config
import requests
import json

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

BACKEND_URL = 'http://localhost:5000'

def test_database_tables():
    """Test that all required tables exist"""
    print("\n1. Testing Database Tables...")
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    required_tables = [
        'USERS', 'STUDENTS', 'FACULTY', 'SUBJECTS', 'MARKS',
        'ATTENDANCE', 'ALERTS', 'FACULTY_CLASSES',
        'FEEDBACK_THREADS', 'FEEDBACK_MESSAGES'
    ]
    
    cursor.execute("""
        SELECT table_name FROM user_tables 
        WHERE table_name IN ('USERS', 'STUDENTS', 'FACULTY', 'SUBJECTS', 'MARKS', 
                             'ATTENDANCE', 'ALERTS', 'FACULTY_CLASSES', 
                             'FEEDBACK_THREADS', 'FEEDBACK_MESSAGES')
        ORDER BY table_name
    """)
    
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    all_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"   OK - {table} exists")
        else:
            print(f"   ERROR - {table} missing!")
            all_exist = False
    
    # Check for old tables that should be removed
    cursor.execute("""
        SELECT table_name FROM user_tables 
        WHERE table_name IN ('FEEDBACK', 'STUDENT_SUBJECTS')
    """)
    
    old_tables = cursor.fetchall()
    if old_tables:
        print(f"\n   WARNING - Old tables still exist:")
        for table in old_tables:
            print(f"   - {table[0]} (should be removed)")
    
    cursor.close()
    conn.close()
    
    return all_exist

def test_credentials():
    """Test that credentials exist and are valid"""
    print("\n2. Testing Credentials...")
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    test_users = [
        ('rohan.sharma.2q34.3@thapar.edu', 'pass123', 'student'),
        ('dr.rajesh@thaparfac.edu', 'pass123', 'faculty')
    ]
    
    all_valid = True
    for email, password, role in test_users:
        cursor.execute("""
            SELECT user_id, name, role, password
            FROM users
            WHERE email = :email
        """, {'email': email})
        
        user = cursor.fetchone()
        if user and user[3] == password and user[2] == role:
            print(f"   OK - {email} ({role})")
        else:
            print(f"   ERROR - {email} invalid!")
            all_valid = False
    
    cursor.close()
    conn.close()
    
    return all_valid

def test_data_counts():
    """Test that data is populated"""
    print("\n3. Testing Data Counts...")
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    tables_to_check = [
        ('users', 305),  # 300 students + 5 faculty
        ('students', 300),
        ('faculty', 5),
        ('subjects', 5),
        ('marks', 6000),  # 300 students × 5 subjects × 4 assessments
        ('attendance', 100000),  # Approximate
        ('faculty_classes', 15)  # 5 faculty × 3 batches each
    ]
    
    all_ok = True
    for table, expected_min in tables_to_check:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        
        if count >= expected_min:
            print(f"   OK - {table}: {count} records")
        else:
            print(f"   WARNING - {table}: {count} records (expected >= {expected_min})")
            all_ok = False
    
    cursor.close()
    conn.close()
    
    return all_ok

def test_backend_running():
    """Test if backend is running"""
    print("\n4. Testing Backend Server...")
    try:
        response = requests.get(BACKEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"   OK - Backend running at {BACKEND_URL}")
            return True
        else:
            print(f"   ERROR - Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   WARNING - Backend not running at {BACKEND_URL}")
        print(f"   Start backend with: python backend/app.py")
        return False
    except Exception as e:
        print(f"   ERROR - {str(e)}")
        return False

def test_login_api():
    """Test login API"""
    print("\n5. Testing Login API...")
    
    if not test_backend_running():
        print("   SKIPPED - Backend not running")
        return False
    
    try:
        # Test student login
        response = requests.post(
            f'{BACKEND_URL}/api/login',
            json={
                'email': 'rohan.sharma.2q34.3@thapar.edu',
                'password': 'pass123'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data and data['role'] == 'student':
                print(f"   OK - Student login successful")
                student_token = data['token']
            else:
                print(f"   ERROR - Invalid response: {data}")
                return False
        else:
            print(f"   ERROR - Login failed: {response.status_code}")
            return False
        
        # Test faculty login
        response = requests.post(
            f'{BACKEND_URL}/api/login',
            json={
                'email': 'dr.rajesh@thaparfac.edu',
                'password': 'pass123'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data and data['role'] == 'faculty':
                print(f"   OK - Faculty login successful")
                return True
            else:
                print(f"   ERROR - Invalid response: {data}")
                return False
        else:
            print(f"   ERROR - Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ERROR - {str(e)}")
        return False

def main():
    print("=" * 80)
    print("SYSTEM TEST AFTER CLEANUP")
    print("=" * 80)
    
    results = {
        'Database Tables': test_database_tables(),
        'Credentials': test_credentials(),
        'Data Counts': test_data_counts(),
        'Backend Server': test_backend_running(),
        'Login API': test_login_api()
    }
    
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    
    all_passed = True
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("=" * 80)
        print("\nSystem is ready to use!")
        print("\nNext steps:")
        print("  1. Open: frontend/login_test.html")
        print("  2. Login with: rohan.sharma.2q34.3@thapar.edu / pass123")
        print("  3. Test all features")
    else:
        print("SOME TESTS FAILED!")
        print("=" * 80)
        print("\nPlease fix the issues above before using the system.")
        print("\nCommon fixes:")
        print("  - Run: python backend/setup_complete_system.py")
        print("  - Start backend: python backend/app.py")
        print("  - Check database connection in backend/config.py")

if __name__ == '__main__':
    main()
