"""
Quick test to verify user-specific clear chat implementation
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def test_clear_chat():
    print("-" * 80)
    print("TESTING USER-SPECIFIC CLEAR CHAT FEATURE")
    print("-" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 1. Check if columns exist
        print("\n1. Checking database columns...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM user_tab_columns 
            WHERE table_name = 'FEEDBACK_THREADS'
            AND column_name IN ('CLEARED_BY_STUDENT', 'CLEARED_BY_FACULTY')
            ORDER BY column_name
        """)
        
        columns = cursor.fetchall()
        if len(columns) == 2:
            print("   Both columns exist:")
            for col in columns:
                print(f"     - {col[0]}: {col[1]}")
        else:
            print(f"   ERROR: Expected 2 columns, found {len(columns)}")
            return False
        
        # 2. Check if any threads have been cleared
        print("\n2. Checking for cleared threads...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM feedback_threads 
            WHERE cleared_by_student IS NOT NULL 
               OR cleared_by_faculty IS NOT NULL
        """)
        
        cleared_count = cursor.fetchone()[0]
        print(f"   Found {cleared_count} thread(s) with clear history")
        
        # 3. Show sample thread data
        print("\n3. Sample thread data (first 3 threads)...")
        cursor.execute("""
            SELECT thread_id, student_id, faculty_id, subject_id,
                   TO_CHAR(cleared_by_student, 'YYYY-MM-DD HH24:MI:SS') as student_cleared,
                   TO_CHAR(cleared_by_faculty, 'YYYY-MM-DD HH24:MI:SS') as faculty_cleared
            FROM feedback_threads
            WHERE ROWNUM <= 3
            ORDER BY thread_id
        """)
        
        threads = cursor.fetchall()
        if threads:
            for thread in threads:
                print(f"\n   Thread ID: {thread[0]}")
                print(f"   Student: {thread[1]}, Faculty: {thread[2]}, Subject: {thread[3]}")
                print(f"   Cleared by Student: {thread[4] or 'Never'}")
                print(f"   Cleared by Faculty: {thread[5] or 'Never'}")
        else:
            print("   No threads found")
        
        # 4. Count total messages
        print("\n4. Message statistics...")
        cursor.execute("SELECT COUNT(*) FROM feedback_messages")
        total_messages = cursor.fetchone()[0]
        print(f"   Total messages in database: {total_messages}")
        
        print("\n" + "-" * 80)
        print("DATABASE STRUCTURE: READY")
        print("-" * 80)
        print("\nNext Steps:")
        print("1. Start backend: python backend/app.py")
        print("2. Open two browsers (student + faculty)")
        print("3. Test clear chat functionality")
        print("4. Refer to TEST_CLEAR_CHAT.md for detailed testing steps")
        
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    test_clear_chat()
