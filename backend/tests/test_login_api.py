import oracledb
import sys

print("Testing Login API Components...")
print("=" * 50)

# Test 1: Database Connection
print("\n[1/3] Testing database connection...")
try:
    conn = oracledb.connect(
        user='system',
        password='Vanshi@Oracle1',
        dsn='localhost:1521/XE'
    )
    print("✓ Database connection successful")
    
    # Test 2: Check if users table exists
    print("\n[2/3] Checking if users table exists...")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"✓ Users table exists with {count} records")
    
    # Test 3: Try to fetch a user
    print("\n[3/3] Testing user query...")
    cursor.execute("""
        SELECT user_id, name, role, password
        FROM users
        WHERE email = :email
    """, {'email': 'rohan.sharma@thapar.edu'})
    
    user = cursor.fetchone()
    if user:
        print(f"✓ Found user: {user[1]} (Role: {user[2]})")
        print(f"  User ID: {user[0]}")
        print(f"  Password in DB: {user[3]}")
    else:
        print("✗ User not found in database")
        print("\nThis means database tables are not setup!")
        print("Run: SETUP_DATABASE_PYTHON.bat")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 50)
    print("All tests passed! Login should work.")
    print("\nIf login still fails, check backend terminal for errors.")
    
except oracledb.Error as e:
    error, = e.args
    print(f"\n✗ Database Error: {error.message}")
    print("\nPossible causes:")
    print("1. Oracle database is not running")
    print("   - Check services.msc for OracleServiceXE")
    print("2. Wrong credentials")
    print("   - Verify password in backend/config.py")
    print("3. Database tables not created")
    print("   - Run: SETUP_DATABASE_PYTHON.bat")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    sys.exit(1)
