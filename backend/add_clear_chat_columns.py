"""
Add columns for user-specific clear chat functionality
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def add_clear_chat_columns():
    print("-" * 80)
    print("ADDING CLEAR CHAT COLUMNS")
    print("-" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Add cleared_by_student column to feedback_threads
        print("\n1. Adding cleared_by_student column...")
        try:
            cursor.execute("""
                ALTER TABLE feedback_threads 
                ADD cleared_by_student TIMESTAMP DEFAULT NULL
            """)
            print("   Added cleared_by_student column")
        except Exception as e:
            if "ORA-01430" in str(e):
                print("   Column already exists")
            else:
                print(f"   Error: {str(e)}")
        
        # Add cleared_by_faculty column to feedback_threads
        print("\n2. Adding cleared_by_faculty column...")
        try:
            cursor.execute("""
                ALTER TABLE feedback_threads 
                ADD cleared_by_faculty TIMESTAMP DEFAULT NULL
            """)
            print("   Added cleared_by_faculty column")
        except Exception as e:
            if "ORA-01430" in str(e):
                print("   Column already exists")
            else:
                print(f"   Error: {str(e)}")
        
        conn.commit()
        
        # Verify columns were added
        print("\n3. Verifying columns...")
        cursor.execute("""
            SELECT column_name 
            FROM user_tab_columns 
            WHERE table_name = 'FEEDBACK_THREADS' 
            AND column_name IN ('CLEARED_BY_STUDENT', 'CLEARED_BY_FACULTY')
            ORDER BY column_name
        """)
        
        columns = cursor.fetchall()
        for col in columns:
            print(f"   {col[0]}")
        
        print("\n" + "-" * 80)
        print("COLUMNS ADDED SUCCESSFULLY!")
        print("-" * 80)
        print("\nNew columns:")
        print("  - cleared_by_student: Timestamp when student cleared chat")
        print("  - cleared_by_faculty: Timestamp when faculty cleared chat")
        print("\nMessages before these timestamps will be hidden for that user.")
        
    except Exception as e:
        conn.rollback()
        print(f"\nError: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_clear_chat_columns()
