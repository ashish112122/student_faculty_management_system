"""
Database Cleanup Script
Removes unused/temporary tables that were created during development
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def cleanup_database():
    print("=" * 80)
    print("DATABASE CLEANUP")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Tables to drop (unused/old tables)
    tables_to_drop = [
        'FEEDBACK',  # Old feedback table (replaced by feedback_threads + feedback_messages)
        'STUDENT_SUBJECTS',  # Not used in app.py
    ]
    
    # Sequences to drop
    sequences_to_drop = [
        'feedback_seq',
        'student_subjects_seq'
    ]
    
    print("\n1. Dropping unused tables...")
    for table in tables_to_drop:
        try:
            cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
            print(f"   Dropped {table}")
        except Exception as e:
            if "ORA-00942" in str(e):  # Table does not exist
                print(f"   {table} does not exist (already clean)")
            else:
                print(f"   Error dropping {table}: {str(e)}")
    
    print("\n2. Dropping unused sequences...")
    for seq in sequences_to_drop:
        try:
            cursor.execute(f"DROP SEQUENCE {seq}")
            print(f"   Dropped {seq}")
        except Exception as e:
            if "ORA-02289" in str(e):  # Sequence does not exist
                print(f"   {seq} does not exist (already clean)")
            else:
                print(f"   Error dropping {seq}: {str(e)}")
    
    conn.commit()
    
    print("\n3. Verifying remaining tables...")
    cursor.execute("""
        SELECT table_name FROM user_tables 
        WHERE table_name IN ('USERS', 'STUDENTS', 'FACULTY', 'SUBJECTS', 'MARKS', 
                             'ATTENDANCE', 'ALERTS', 'FACULTY_CLASSES', 
                             'FEEDBACK_THREADS', 'FEEDBACK_MESSAGES')
        ORDER BY table_name
    """)
    
    tables = cursor.fetchall()
    print(f"   Active tables: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("CLEANUP COMPLETE!")
    print("=" * 80)
    print("\nSummary:")
    print("  - Removed unused tables")
    print("  - Removed unused sequences")
    print("  - Verified active tables")
    print("\nNext steps:")
    print("  1. Run setup_complete_system.py to populate data")
    print("  2. Test login with credentials from WORKING_LINKS.md")

if __name__ == '__main__':
    cleanup_database()
