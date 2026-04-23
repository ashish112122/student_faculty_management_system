"""
Migration script to v2.0
"""
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def migrate():
    print("Migrating to v2.0...")
    
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create faculty_classes table
        try:
            cursor.execute("""
                CREATE TABLE faculty_classes (
                    faculty_class_id NUMBER PRIMARY KEY,
                    faculty_id NUMBER NOT NULL,
                    class_name VARCHAR2(10) NOT NULL,
                    subject_id NUMBER NOT NULL,
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
                )
            """)
            print("✓ Created faculty_classes table")
        except:
            print("ℹ faculty_classes table already exists")
        
        # Create sequence
        try:
            cursor.execute("CREATE SEQUENCE faculty_classes_seq START WITH 1")
            print("✓ Created sequence")
        except:
            print("ℹ Sequence already exists")
        
        # Add class_name to students
        try:
            cursor.execute("ALTER TABLE students ADD class_name VARCHAR2(10)")
            print("✓ Added class_name to students")
        except:
            print("ℹ class_name already exists")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Migration complete")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    migrate()
