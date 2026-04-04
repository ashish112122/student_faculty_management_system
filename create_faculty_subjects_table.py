import oracledb
from backend.config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def create_faculty_subjects_table():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Creating faculty_subjects table...")
        
        cursor.execute("""
            CREATE TABLE faculty_subjects (
                faculty_subject_id NUMBER PRIMARY KEY,
                faculty_id NUMBER NOT NULL,
                subject_id NUMBER NOT NULL,
                FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                UNIQUE (faculty_id, subject_id)
            )
        """)
        
        cursor.execute("CREATE SEQUENCE faculty_subjects_seq START WITH 1 INCREMENT BY 1")
        
        conn.commit()
        print("✓ Table created successfully")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    create_faculty_subjects_table()
