"""
Migration script to update feedback system to thread-based system
Run this to create new tables and migrate existing data
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def migrate_feedback_system():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        print("Starting feedback system migration...")
        
        # Step 1: Create new tables
        print("\n1. Creating feedback_threads table...")
        cursor.execute("""
            CREATE TABLE feedback_threads (
                thread_id NUMBER PRIMARY KEY,
                student_id NUMBER NOT NULL,
                faculty_id NUMBER NOT NULL,
                subject_id NUMBER NOT NULL,
                thread_title VARCHAR2(200),
                initiated_by VARCHAR2(20) NOT NULL CHECK (initiated_by IN ('student', 'faculty')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            )
        """)
        print("✓ feedback_threads table created")
        
        print("\n2. Creating feedback_threads sequence...")
        cursor.execute("CREATE SEQUENCE feedback_threads_seq START WITH 1 INCREMENT BY 1")
        print("✓ feedback_threads_seq created")
        
        print("\n3. Creating feedback_messages table...")
        cursor.execute("""
            CREATE TABLE feedback_messages (
                message_id NUMBER PRIMARY KEY,
                thread_id NUMBER NOT NULL,
                sender_id NUMBER NOT NULL,
                sender_role VARCHAR2(20) NOT NULL CHECK (sender_role IN ('student', 'faculty')),
                message CLOB NOT NULL,
                is_read NUMBER(1) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                attachment_path VARCHAR2(500),
                attachment_name VARCHAR2(200),
                attachment_type VARCHAR2(50),
                FOREIGN KEY (thread_id) REFERENCES feedback_threads(thread_id) ON DELETE CASCADE,
                FOREIGN KEY (sender_id) REFERENCES users(user_id)
            )
        """)
        print("✓ feedback_messages table created")
        
        print("\n4. Creating feedback_messages sequence...")
        cursor.execute("CREATE SEQUENCE feedback_messages_seq START WITH 1 INCREMENT BY 1")
        print("✓ feedback_messages_seq created")
        
        print("\n5. Creating indexes...")
        cursor.execute("CREATE INDEX idx_feedback_threads_student ON feedback_threads(student_id)")
        cursor.execute("CREATE INDEX idx_feedback_threads_faculty ON feedback_threads(faculty_id)")
        cursor.execute("CREATE INDEX idx_feedback_threads_subject ON feedback_threads(subject_id)")
        cursor.execute("CREATE INDEX idx_feedback_messages_thread ON feedback_messages(thread_id)")
        cursor.execute("CREATE INDEX idx_feedback_messages_sender ON feedback_messages(sender_id)")
        print("✓ Indexes created")
        
        print("\n6. Creating trigger for last_message_at...")
        cursor.execute("""
            CREATE OR REPLACE TRIGGER update_thread_timestamp
            AFTER INSERT ON feedback_messages
            FOR EACH ROW
            BEGIN
                UPDATE feedback_threads
                SET last_message_at = CURRENT_TIMESTAMP
                WHERE thread_id = :NEW.thread_id;
            END;
        """)
        print("✓ Trigger created")
        
        # Step 2: Migrate existing data (if old feedback table exists)
        print("\n7. Checking for existing feedback data...")
        try:
            cursor.execute("SELECT COUNT(*) FROM feedback")
            old_count = cursor.fetchone()[0]
            
            if old_count > 0:
                print(f"   Found {old_count} old feedback records")
                print("   Migrating to new structure...")
                
                # Group old feedback by student-faculty-subject and create threads
                cursor.execute("""
                    SELECT DISTINCT student_id, faculty_id, subject_id
                    FROM feedback
                    ORDER BY student_id, faculty_id, subject_id
                """)
                
                for student_id, faculty_id, subject_id in cursor.fetchall():
                    # Create thread
                    cursor.execute("""
                        INSERT INTO feedback_threads 
                        (thread_id, student_id, faculty_id, subject_id, thread_title, initiated_by)
                        VALUES (feedback_threads_seq.NEXTVAL, :1, :2, :3, 'Migrated Conversation', 'student')
                    """, (student_id, faculty_id, subject_id))
                    
                    # Get thread_id
                    cursor.execute("SELECT feedback_threads_seq.CURRVAL FROM DUAL")
                    thread_id = cursor.fetchone()[0]
                    
                    # Migrate messages
                    cursor.execute("""
                        SELECT feedback_id, sender_role, message, is_read, created_at,
                               attachment_path, attachment_name, attachment_type
                        FROM feedback
                        WHERE student_id = :1 AND faculty_id = :2 AND subject_id = :3
                        ORDER BY created_at
                    """, (student_id, faculty_id, subject_id))
                    
                    for row in cursor.fetchall():
                        # Get sender_id based on role
                        if row[1] == 'student':
                            cursor.execute("SELECT user_id FROM students WHERE student_id = :1", (student_id,))
                        else:
                            cursor.execute("SELECT user_id FROM faculty WHERE faculty_id = :1", (faculty_id,))
                        sender_id = cursor.fetchone()[0]
                        
                        cursor.execute("""
                            INSERT INTO feedback_messages
                            (message_id, thread_id, sender_id, sender_role, message, is_read, created_at,
                             attachment_path, attachment_name, attachment_type)
                            VALUES (feedback_messages_seq.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8, :9)
                        """, (thread_id, sender_id, row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                
                print(f"✓ Migrated {old_count} messages to new structure")
                
                # Optionally rename old table
                print("\n8. Renaming old feedback table to feedback_old...")
                cursor.execute("ALTER TABLE feedback RENAME TO feedback_old")
                print("✓ Old table renamed (you can drop it later)")
            else:
                print("   No existing data to migrate")
        except Exception as e:
            print(f"   No old feedback table found or error: {e}")
            print("   Continuing with fresh installation...")
        
        conn.commit()
        print("\n" + "="*50)
        print("✅ Migration completed successfully!")
        print("="*50)
        print("\nNew tables created:")
        print("  - feedback_threads")
        print("  - feedback_messages")
        print("\nYou can now use the new threading system!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during migration: {e}")
        print("\nIf tables already exist, you can:")
        print("1. Drop them: DROP TABLE feedback_messages CASCADE CONSTRAINTS;")
        print("2. Drop them: DROP TABLE feedback_threads CASCADE CONSTRAINTS;")
        print("3. Run this script again")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("="*50)
    print("FEEDBACK SYSTEM MIGRATION")
    print("="*50)
    print("\nThis will:")
    print("1. Create new feedback_threads table")
    print("2. Create new feedback_messages table")
    print("3. Migrate existing data (if any)")
    print("4. Rename old feedback table to feedback_old")
    print("\n" + "="*50)
    
    response = input("\nProceed with migration? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        migrate_feedback_system()
    else:
        print("Migration cancelled.")
