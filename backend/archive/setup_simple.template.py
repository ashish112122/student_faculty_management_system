"""
Simple Database Setup Template
Copy this file to setup_simple.py and update with your credentials
"""
import oracledb

# UPDATE THESE WITH YOUR CREDENTIALS
DB_USER = 'system'
DB_PASSWORD = 'YOUR_ORACLE_PASSWORD_HERE'
DB_DSN = 'localhost:1521/XE'

print("Connecting to Oracle...")
conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
cursor = conn.cursor()
print("✓ Connected!\n")

# Drop existing tables (ignore errors)
print("Cleaning up old tables...")
tables = ['FEEDBACK', 'ALERTS', 'ATTENDANCE', 'MARKS', 'STUDENT_SUBJECTS', 
          'STUDENTS', 'FACULTY', 'SUBJECTS', 'USERS']
for table in tables:
    try:
        cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
        print(f"  Dropped {table}")
    except:
        pass

print("\nCreating tables...")

# 1. Users table
cursor.execute("""
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) NOT NULL
)
""")
print("✓ USERS")

# 2. Students table
cursor.execute("""
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    name VARCHAR2(100) NOT NULL,
    branch VARCHAR2(50),
    year_of_study NUMBER,
    semester NUMBER,
    section VARCHAR2(10),
    cgpa NUMBER(3,2)
)
""")
print("✓ STUDENTS")

# 3. Faculty table
cursor.execute("""
CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    name VARCHAR2(100) NOT NULL,
    department VARCHAR2(50)
)
""")
print("✓ FACULTY")

# 4. Subjects table
cursor.execute("""
CREATE TABLE subjects (
    subject_id NUMBER PRIMARY KEY,
    subject_name VARCHAR2(100) NOT NULL,
    subject_code VARCHAR2(20)
)
""")
print("✓ SUBJECTS")

# 5. Student_Subjects table
cursor.execute("""
CREATE TABLE student_subjects (
    student_id NUMBER REFERENCES students(student_id),
    subject_id NUMBER REFERENCES subjects(subject_id),
    PRIMARY KEY (student_id, subject_id)
)
""")
print("✓ STUDENT_SUBJECTS")

# 6. Marks table
cursor.execute("""
CREATE TABLE marks (
    mark_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    subject_id NUMBER REFERENCES subjects(subject_id),
    assessment_type VARCHAR2(20),
    marks_obtained NUMBER(5,2),
    max_marks NUMBER(5,2)
)
""")
print("✓ MARKS")

# 7. Attendance table
cursor.execute("""
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    subject_id NUMBER REFERENCES subjects(subject_id),
    attendance_date DATE,
    status CHAR(1)
)
""")
print("✓ ATTENDANCE")

# 8. Alerts table
cursor.execute("""
CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    alert_type VARCHAR2(20),
    message VARCHAR2(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("✓ ALERTS")

# 9. Feedback table
cursor.execute("""
CREATE TABLE feedback (
    feedback_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    subject_id NUMBER REFERENCES subjects(subject_id),
    sender_id NUMBER,
    message VARCHAR2(1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("✓ FEEDBACK")

conn.commit()
print("\n✅ All tables created!")

print("\nInserting demo data...")

# Insert users
users_data = [
    (1, 'rohan.sharma@thapar.edu', 'password123', 'Rohan Sharma', 'student'),
    (2, 'rahul.verma@thapar.edu', 'password123', 'Rahul Verma', 'student'),
    (3, 'simran.kaur@thapar.edu', 'password123', 'Simran Kaur', 'student'),
    (4, 'aman.gupta@thapar.edu', 'password123', 'Aman Gupta', 'student'),
    (5, 'priya.singh@thapar.edu', 'password123', 'Priya Singh', 'student'),
    (51, 'rohan.sharma@thaparfac.edu', 'password123', 'Dr. Rohan Sharma', 'faculty'),
    (52, 'neha.verma@thaparfac.edu', 'password123', 'Dr. Neha Verma', 'faculty'),
    (53, 'amit.khanna@thaparfac.edu', 'password123', 'Dr. Amit Khanna', 'faculty'),
    (54, 'priya.mehta@thaparfac.edu', 'password123', 'Dr. Priya Mehta', 'faculty'),
]

cursor.executemany("""
    INSERT INTO users (user_id, email, password, name, role)
    VALUES (:1, :2, :3, :4, :5)
""", users_data)
print("✓ Users inserted")

# Insert students
students_data = [
    (1, 1, 'Rohan Sharma', 'CSE', 2, 4, '2Q31', 8.5),
    (2, 2, 'Rahul Verma', 'CSE', 2, 4, '2Q31', 7.8),
    (3, 3, 'Simran Kaur', 'CSE', 2, 4, '2Q32', 9.1),
    (4, 4, 'Aman Gupta', 'CSE', 2, 4, '2W31', 8.2),
    (5, 5, 'Priya Singh', 'CSE', 2, 4, '2W32', 8.9),
]

cursor.executemany("""
    INSERT INTO students (student_id, user_id, name, branch, year_of_study, semester, section, cgpa)
    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
""", students_data)
print("✓ Students inserted")

# Insert faculty
faculty_data = [
    (1, 51, 'Dr. Rohan Sharma', 'Computer Science'),
    (2, 52, 'Dr. Neha Verma', 'Computer Science'),
    (3, 53, 'Dr. Amit Khanna', 'Computer Science'),
    (4, 54, 'Dr. Priya Mehta', 'Computer Science'),
]

cursor.executemany("""
    INSERT INTO faculty (faculty_id, user_id, name, department)
    VALUES (:1, :2, :3, :4)
""", faculty_data)
print("✓ Faculty inserted")

# Insert subjects
subjects_data = [
    (1, 'Database Management Systems', 'DBMS'),
    (2, 'Operating Systems', 'OS'),
    (3, 'Computer Networks', 'CN'),
    (4, 'Data Structures and Algorithms', 'DSA'),
    (5, 'Software Engineering', 'SE'),
]

cursor.executemany("""
    INSERT INTO subjects (subject_id, subject_name, subject_code)
    VALUES (:1, :2, :3)
""", subjects_data)
print("✓ Subjects inserted")

# Insert student_subjects (each student enrolled in all 5 subjects)
student_subjects_data = []
for student_id in range(1, 6):
    for subject_id in range(1, 6):
        student_subjects_data.append((student_id, subject_id))

cursor.executemany("""
    INSERT INTO student_subjects (student_id, subject_id)
    VALUES (:1, :2)
""", student_subjects_data)
print("✓ Student-Subject mappings inserted")

# NOTE: No marks or attendance data inserted
# This ensures empty state is shown until faculty uploads data

conn.commit()

# Verify
print("\n" + "="*50)
print("Verification:")
print("="*50)
cursor.execute("SELECT COUNT(*) FROM users")
print(f"✓ USERS: {cursor.fetchone()[0]} records")

cursor.execute("SELECT COUNT(*) FROM students")
print(f"✓ STUDENTS: {cursor.fetchone()[0]} records")

cursor.execute("SELECT COUNT(*) FROM subjects")
print(f"✓ SUBJECTS: {cursor.fetchone()[0]} records")

cursor.execute("SELECT COUNT(*) FROM marks")
print(f"✓ MARKS: {cursor.fetchone()[0]} records (empty - as expected)")

cursor.execute("SELECT COUNT(*) FROM attendance")
print(f"✓ ATTENDANCE: {cursor.fetchone()[0]} records (empty - as expected)")

cursor.close()
conn.close()

print("\n" + "="*50)
print("✅ Database setup complete!")
print("="*50)
print("\nYou can now login with:")
print("  Email: rohan.sharma@thapar.edu")
print("  Password: password123")
