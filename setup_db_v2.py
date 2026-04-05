import oracledb

DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}

def create_tables():
    """Create all required tables"""
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Drop existing tables (ignore errors)
    drop_tables = [
        'feedback', 'attendance', 'marks', 'subjects', 
        'faculty', 'students', 'batches', 'alerts', 'users', 'departments'
    ]
    
    for table in drop_tables:
        try:
            cursor.execute(f'DROP TABLE {table} CASCADE CONSTRAINTS')
            print(f"✓ Dropped table: {table}")
        except:
            pass
    
    conn.commit()
    
    # Drop existing sequences (ignore errors)
    drop_seqs = ['user_seq', 'student_seq', 'faculty_seq', 'subject_seq', 
                 'mark_seq', 'attendance_seq', 'alert_seq', 'feedback_seq', 'dept_seq', 'batch_seq']
    
    for seq in drop_seqs:
        try:
            cursor.execute(f'DROP SEQUENCE {seq}')
            print(f"✓ Dropped sequence: {seq}")
        except:
            pass
    
    conn.commit()
    
    #Create sequences
    sequences = [
        'CREATE SEQUENCE user_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE student_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE subject_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE mark_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE alert_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE feedback_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE dept_seq START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE batch_seq START WITH 1 INCREMENT BY 1',
    ]
    
    for seq_sql in sequences:
        try:
            cursor.execute(seq_sql)
            print(f"✓ Created sequence")
        except Exception as e:
            print(f"✗ Error creating sequence: {e}")
    
    conn.commit()
    
    # Create tables
    cursor.execute('''CREATE TABLE users (
        user_id NUMBER PRIMARY KEY,
        email VARCHAR2(100) UNIQUE NOT NULL,
        password VARCHAR2(255) NOT NULL,
        name VARCHAR2(100) NOT NULL,
        role VARCHAR2(20) CHECK (role IN ('student', 'faculty')) NOT NULL
    )''')
    print("✓ Created table: users")
    
    cursor.execute('''CREATE TABLE departments (
        department_id NUMBER PRIMARY KEY,
        name VARCHAR2(100) NOT NULL
    )''')
    print("✓ Created table: departments")
    
    cursor.execute('''CREATE TABLE batches (
        batch_id NUMBER PRIMARY KEY,
        name VARCHAR2(100) NOT NULL
    )''')
    print("✓ Created table: batches")
    
    cursor.execute('''CREATE TABLE students (
        student_id NUMBER PRIMARY KEY,
        user_id NUMBER UNIQUE REFERENCES users(user_id),
        batch_id NUMBER REFERENCES batches(batch_id),
        semester NUMBER,
        cgpa NUMBER(3,2),
        total_credits NUMBER
    )''')
    print("✓ Created table: students")
    
    cursor.execute('''CREATE TABLE faculty (
        faculty_id NUMBER PRIMARY KEY,
        user_id NUMBER UNIQUE REFERENCES users(user_id),
        department_id NUMBER REFERENCES departments(department_id)
    )''')
    print("✓ Created table: faculty")
    
    cursor.execute('''CREATE TABLE subjects (
        subject_id NUMBER PRIMARY KEY,
        name VARCHAR2(100) NOT NULL,
        batch_id NUMBER REFERENCES batches(batch_id),
        faculty_id NUMBER REFERENCES faculty(faculty_id)
    )''')
    print("✓ Created table: subjects")
    
    cursor.execute('''CREATE TABLE marks (
        mark_id NUMBER PRIMARY KEY,
        student_id NUMBER REFERENCES students(student_id),
        subject_id NUMBER REFERENCES subjects(subject_id),
        mst NUMBER,
        est NUMBER,
        quiz NUMBER,
        assignment NUMBER,
        total NUMBER,
        grade VARCHAR2(2)
    )''')
    print("✓ Created table: marks")
    
    cursor.execute('''CREATE TABLE attendance (
        attendance_id NUMBER PRIMARY KEY,
        student_id NUMBER REFERENCES students(student_id),
        subject_id NUMBER REFERENCES subjects(subject_id),
        att_date DATE NOT NULL,
        status VARCHAR2(10) CHECK (status IN ('present', 'absent')) NOT NULL
    )''')
    print("✓ Created table: attendance")
    
    cursor.execute('''CREATE TABLE alerts (
        alert_id NUMBER PRIMARY KEY,
        student_id NUMBER REFERENCES students(student_id),
        message VARCHAR2(500) NOT NULL,
        is_read NUMBER(1) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    print("✓ Created table: alerts")
    
    cursor.execute('''CREATE TABLE feedback (
        feedback_id NUMBER PRIMARY KEY,
        student_id NUMBER REFERENCES students(student_id),
        faculty_id NUMBER REFERENCES faculty(faculty_id),
        subject_id NUMBER REFERENCES subjects(subject_id),
        sender_type VARCHAR2(20) CHECK (sender_type IN ('student', 'faculty')) NOT NULL,
        message CLOB NOT NULL,
        is_read NUMBER(1) DEFAULT 0,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    print("✓ Created table: feedback")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("\n✓ Database setup complete!")

if __name__ == '__main__':
    create_tables()
