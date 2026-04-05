import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def recreate_schema():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("Dropping existing tables...")
    
    tables = ['FEEDBACK', 'ALERTS', 'ATTENDANCE', 'MARKS', 'FACULTY_CLASSES', 'SUBJECTS', 'STUDENTS', 'FACULTY', 'USERS']
    
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
            print(f"  Dropped {table}")
        except:
            print(f"  {table} doesn't exist")
    
    print("\nDropping sequences...")
    sequences = ['users_seq', 'students_seq', 'faculty_seq', 'subjects_seq', 'faculty_classes_seq', 
                 'marks_seq', 'attendance_seq', 'alerts_seq', 'feedback_seq']
    
    for seq in sequences:
        try:
            cursor.execute(f"DROP SEQUENCE {seq}")
            print(f"  Dropped {seq}")
        except:
            print(f"  {seq} doesn't exist")
    
    conn.commit()
    
    print("\nCreating new schema...")
    
    # Users table
    cursor.execute("""
        CREATE TABLE users (
            user_id NUMBER PRIMARY KEY,
            email VARCHAR2(100) UNIQUE NOT NULL,
            password VARCHAR2(100) NOT NULL,
            name VARCHAR2(100) NOT NULL,
            role VARCHAR2(20) NOT NULL CHECK (role IN ('student', 'faculty'))
        )
    """)
    cursor.execute("CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1")
    print("  Created users")
    
    # Students table
    cursor.execute("""
        CREATE TABLE students (
            student_id NUMBER PRIMARY KEY,
            user_id NUMBER UNIQUE NOT NULL,
            name VARCHAR2(100) NOT NULL,
            branch VARCHAR2(50) NOT NULL,
            year_of_study NUMBER NOT NULL,
            semester NUMBER NOT NULL,
            section VARCHAR2(10) NOT NULL,
            class_name VARCHAR2(20) NOT NULL,
            cgpa NUMBER(3,2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1")
    print("  Created students")
    
    # Faculty table
    cursor.execute("""
        CREATE TABLE faculty (
            faculty_id NUMBER PRIMARY KEY,
            user_id NUMBER UNIQUE NOT NULL,
            name VARCHAR2(100) NOT NULL,
            department VARCHAR2(100) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1")
    print("  Created faculty")
    
    # Subjects table
    cursor.execute("""
        CREATE TABLE subjects (
            subject_id NUMBER PRIMARY KEY,
            subject_name VARCHAR2(100) NOT NULL,
            subject_code VARCHAR2(20) UNIQUE NOT NULL
        )
    """)
    cursor.execute("CREATE SEQUENCE subjects_seq START WITH 1 INCREMENT BY 1")
    print("  Created subjects")
    
    # Faculty Classes
    cursor.execute("""
        CREATE TABLE faculty_classes (
            faculty_class_id NUMBER PRIMARY KEY,
            faculty_id NUMBER NOT NULL,
            class_name VARCHAR2(20) NOT NULL,
            subject_id NUMBER NOT NULL,
            FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE faculty_classes_seq START WITH 1 INCREMENT BY 1")
    print("  Created faculty_classes")
    
    # Marks table
    cursor.execute("""
        CREATE TABLE marks (
            mark_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            subject_id NUMBER NOT NULL,
            class_name VARCHAR2(20) NOT NULL,
            assessment_type VARCHAR2(20) NOT NULL CHECK (assessment_type IN ('MST', 'EST', 'Quiz', 'Assignment')),
            marks_obtained NUMBER NOT NULL,
            max_marks NUMBER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE marks_seq START WITH 1 INCREMENT BY 1")
    print("  Created marks")
    
    # Attendance table
    cursor.execute("""
        CREATE TABLE attendance (
            attendance_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            subject_id NUMBER NOT NULL,
            class_name VARCHAR2(20) NOT NULL,
            attendance_date DATE NOT NULL,
            status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1")
    print("  Created attendance")
    
    # Alerts table
    cursor.execute("""
        CREATE TABLE alerts (
            alert_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            subject_id NUMBER,
            alert_type VARCHAR2(20) NOT NULL CHECK (alert_type IN ('Warning', 'Critical')),
            message VARCHAR2(500) NOT NULL,
            is_read NUMBER(1) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1")
    print("  Created alerts")
    
    # Feedback table
    cursor.execute("""
        CREATE TABLE feedback (
            feedback_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            faculty_id NUMBER NOT NULL,
            subject_id NUMBER NOT NULL,
            sender_role VARCHAR2(20) NOT NULL CHECK (sender_role IN ('student', 'faculty')),
            message CLOB NOT NULL,
            is_read NUMBER(1) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE feedback_seq START WITH 1 INCREMENT BY 1")
    print("  Created feedback")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\nSchema recreation complete!")

if __name__ == '__main__':
    recreate_schema()
