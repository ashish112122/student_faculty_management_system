"""
Setup script for Student-Faculty Portal v2.0
- Applies new schema with class-based structure
- Generates comprehensive demo data
"""

import oracledb
import sys
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def execute_sql_file(conn, filename):
    """Execute SQL commands from a file"""
    print(f"\nExecuting {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        cursor = conn.cursor()
        
        # Split by semicolon and execute each statement
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    # Some statements might fail (like DROP if table doesn't exist)
                    if 'ORA-00942' not in str(e) and 'ORA-02289' not in str(e):
                        print(f"Warning: {str(e)}")
        
        conn.commit()
        cursor.close()
        print(f"✓ {filename} executed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error executing {filename}: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("STUDENT-FACULTY PORTAL v2.0 SETUP")
    print("=" * 70)
    
    try:
        # Connect to database
        print("\nConnecting to database...")
        conn = oracledb.connect(**DB_CONFIG)
        print("✓ Connected successfully")
        
        # Apply new schema
        if not execute_sql_file(conn, 'database/schema.sql'):
            print("\n✗ Schema setup failed!")
            sys.exit(1)
        
        conn.close()
        
        # Generate demo data using Python script
        print("\n" + "=" * 70)
        print("GENERATING DEMO DATA")
        print("=" * 70)
        
        from generate_data import main as generate_data
        generate_data()
        
        print("\n" + "=" * 70)
        print("✓ SETUP COMPLETE!")
        print("=" * 70)
        print("\nYour portal is ready with:")
        print("  • 5 Classes: 2Q11, 2Q12, 2Q13, 2Q14, 2Q15")
        print("  • 150 Students (30 per class)")
        print("  • 10 Faculty members")
        print("  • 5 Subjects")
        print("  • Complete marks and attendance data")
        print("  • Automatic alerts for low attendance")
        print("\nTest Credentials:")
        print("  Faculty: dr.rajesh@thapar.edu / pass123")
        print("  Student: rohan.sharma.2q11@thapar.edu / pass123")
        print("\nStart the backend:")
        print("  python app_v2.py")
        
    except oracledb.Error as e:
        print(f"\n✗ Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
