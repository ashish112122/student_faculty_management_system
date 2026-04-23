import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
import cx_Oracle

def check_columns():
    try:
        conn = cx_Oracle.connect(
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            dsn=Config.DB_DSN
        )
        cursor = conn.cursor()
        
        # Check if cleared_by_student and cleared_by_faculty columns exist
        cursor.execute("""
            SELECT column_name, data_type 
            FROM user_tab_columns 
            WHERE table_name = 'FEEDBACK_THREADS'
            AND column_name IN ('CLEARED_BY_STUDENT', 'CLEARED_BY_FACULTY')
            ORDER BY column_name
        """)
        
        columns = cursor.fetchall()
        
        if len(columns) == 2:
            print("Clear chat columns exist:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
            print("\nUser-specific clear chat feature is ready!")
            return True
        else:
            print("Clear chat columns NOT found!")
            print(f"  Found {len(columns)} columns instead of 2")
            if columns:
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            return False
            
    except Exception as e:
        print(f"Error checking columns: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    check_columns()
