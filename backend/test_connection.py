"""
Test Oracle Database Connection
Run this to verify your Oracle setup is working
"""

import oracledb

# Update these with your Oracle credentials
DB_USER = 'system'
DB_PASSWORD = 'Vanshi@Oracle1'
DB_DSN = 'localhost:1521/XE'

def test_connection():
    try:
        print("Attempting to connect to Oracle Database...")
        print(f"User: {DB_USER}")
        print(f"DSN: {DB_DSN}")
        print()
        
        # Try to connect
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        
        print("✓ Connection successful!")
        print()
        
        # Test query
        cursor = connection.cursor()
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name FROM user_tables 
            WHERE table_name IN ('USERS', 'STUDENTS', 'SUBJECTS')
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print("✓ Tables found:")
            for table in tables:
                print(f"  - {table[0]}")
            print()
            
            # Count records
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"✓ Users in database: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT name, email, role FROM users WHERE ROWNUM <= 5")
                print("\nSample users:")
                for row in cursor.fetchall():
                    print(f"  - {row[0]} ({row[1]}) - {row[2]}")
        else:
            print("⚠ No tables found. Please run schema.sql and demo_data.sql")
        
        cursor.close()
        connection.close()
        
        print()
        print("=" * 50)
        print("Database setup is working correctly!")
        print("You can now run: python app.py")
        print("=" * 50)
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print("✗ Database Error:")
        print(f"  Code: {error.code}")
        print(f"  Message: {error.message}")
        print()
        print("Common solutions:")
        print("1. Check if Oracle service is running (services.msc)")
        print("2. Verify username/password in this file")
        print("3. Ensure Oracle is installed and listening on port 1521")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print()
        print("Make sure you have:")
        print("1. Installed oracledb: pip install oracledb")
        print("2. Oracle Database XE installed and running")

if __name__ == '__main__':
    test_connection()
