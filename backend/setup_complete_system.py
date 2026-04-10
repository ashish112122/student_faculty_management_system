"""
Complete system setup matching exact requirements
"""
import oracledb
from config import Config
from datetime import datetime, timedelta
import random

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

BATCHES = ['2Q31', '2Q32', '2Q33', '2Q34', '2Q35', '2Q36', '2Q37', '2Q38', '2Q39', '2Q40']
SEMESTER = 4

FIRST_NAMES = ['Rohan', 'Priya', 'Amit', 'Sneha', 'Rahul', 'Anjali', 'Vikram', 'Neha', 'Karan', 'Pooja',
               'Arjun', 'Divya', 'Sanjay', 'Kavya', 'Aditya', 'Ritu', 'Manish', 'Swati', 'Nikhil', 'Tanvi',
               'Harsh', 'Ishita', 'Varun', 'Megha', 'Rohit', 'Shruti', 'Akash', 'Nisha', 'Gaurav', 'Preeti']

LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Gupta', 'Verma', 'Singh', 'Reddy', 'Joshi', 'Mehta', 'Nair']

def setup_system():
    print("=" * 80)
    print("SETTING UP COMPLETE SYSTEM")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Drop and recreate tables with correct schema
    print("\n1. Setting up database schema...")
    
    # Drop existing tables
    tables_to_drop = ['FEEDBACK', 'ALERTS', 'ATTENDANCE', 'MARKS', 'FACULTY_CLASSES', 
                      'STUDENTS', 'FACULTY', 'SUBJECTS', 'USERS']
    
    for table in tables_to_drop:
        try:
            cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
            print(f"   Dropped {table}")
        except:
            pass
    
    # Drop sequences
    sequences = ['users_seq', 'students_seq', 'faculty_seq', 'subjects_seq', 
                 'marks_seq', 'attendance_seq', 'alerts_seq', 'feedback_seq', 'faculty_classes_seq']
    for seq in sequences:
        try:
            cursor.execute(f"DROP SEQUENCE {seq}")
        except:
            pass
    
    # Create tables
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
    
    cursor.execute("""
        CREATE TABLE students (
            student_id NUMBER PRIMARY KEY,
            user_id NUMBER UNIQUE NOT NULL,
            name VARCHAR2(100) NOT NULL,
            branch VARCHAR2(50) NOT NULL,
            semester NUMBER NOT NULL,
            class_name VARCHAR2(10) NOT NULL,
            cgpa NUMBER(3,2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1")
    
    cursor.execute("""
        CREATE TABLE faculty (
            faculty_id NUMBER PRIMARY KEY,
            user_id NUMBER UNIQUE NOT NULL,
            name VARCHAR2(100) NOT NULL,
            department VARCHAR2(50) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1")
    
    cursor.execute("""
        CREATE TABLE subjects (
            subject_id NUMBER PRIMARY KEY,
            subject_name VARCHAR2(100) NOT NULL,
            subject_code VARCHAR2(20) UNIQUE NOT NULL
        )
    """)
    cursor.execute("CREATE SEQUENCE subjects_seq START WITH 1 INCREMENT BY 1")
    
    cursor.execute("""
        CREATE TABLE faculty_classes (
            faculty_class_id NUMBER PRIMARY KEY,
            faculty_id NUMBER NOT NULL,
            subject_id NUMBER NOT NULL,
            class_name VARCHAR2(10) NOT NULL,
            FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE faculty_classes_seq START WITH 1 INCREMENT BY 1")
    
    cursor.execute("""
        CREATE TABLE marks (
            mark_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            subject_id NUMBER NOT NULL,
            class_name VARCHAR2(10) NOT NULL,
            assessment_type VARCHAR2(20) NOT NULL CHECK (assessment_type IN ('MST', 'EST', 'Quiz', 'Assignment')),
            marks_obtained NUMBER NOT NULL,
            max_marks NUMBER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE marks_seq START WITH 1 INCREMENT BY 1")
    
    cursor.execute("""
        CREATE TABLE attendance (
            attendance_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            subject_id NUMBER NOT NULL,
            class_name VARCHAR2(10) NOT NULL,
            attendance_date DATE NOT NULL,
            status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1")
    
    cursor.execute("""
        CREATE TABLE alerts (
            alert_id NUMBER PRIMARY KEY,
            student_id NUMBER NOT NULL,
            subject_id NUMBER,
            alert_type VARCHAR2(20) NOT NULL,
            message VARCHAR2(500) NOT NULL,
            is_read NUMBER(1) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)
    cursor.execute("CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1")
    
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
    
    conn.commit()
    print("   OK Schema created")
    
    # Create 5 subjects
    print("\n2. Creating 5 subjects...")
    subjects_data = [
        ('Data Structures', 'CS401'),
        ('Algorithms', 'CS402'),
        ('Database Management', 'CS403'),
        ('Operating Systems', 'CS404'),
        ('Computer Networks', 'CS405')
    ]
    
    subject_ids = []
    for name, code in subjects_data:
        cursor.execute("""
            INSERT INTO subjects (subject_id, subject_name, subject_code)
            VALUES (subjects_seq.NEXTVAL, :name, :code)
        """, {'name': name, 'code': code})
        cursor.execute("SELECT subjects_seq.CURRVAL FROM dual")
        subject_ids.append(cursor.fetchone()[0])
    
    conn.commit()
    print(f"   OK Created 5 subjects")
    
    # Create 5 faculty
    print("\n3. Creating 5 faculty...")
    faculty_data = [
        ('dr.rajesh@thaparfac.edu', 'Dr. Rajesh Kumar', 'CSE'),
        ('prof.meena@thaparfac.edu', 'Prof. Meena Sharma', 'CSE'),
        ('dr.suresh@thaparfac.edu', 'Dr. Suresh Patel', 'CSE'),
        ('prof.kavita@thaparfac.edu', 'Prof. Kavita Singh', 'CSE'),
        ('dr.anil@thaparfac.edu', 'Dr. Anil Verma', 'CSE')
    ]
    
    faculty_ids = []
    for email, name, dept in faculty_data:
        cursor.execute("""
            INSERT INTO users (user_id, email, password, name, role)
            VALUES (users_seq.NEXTVAL, :email, 'pass123', :name, 'faculty')
        """, {'email': email, 'name': name})
        cursor.execute("SELECT users_seq.CURRVAL FROM dual")
        user_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO faculty (faculty_id, user_id, name, department)
            VALUES (faculty_seq.NEXTVAL, :user_id, :name, :dept)
        """, {'user_id': user_id, 'name': name, 'dept': dept})
        cursor.execute("SELECT faculty_seq.CURRVAL FROM dual")
        faculty_ids.append(cursor.fetchone()[0])
    
    conn.commit()
    print(f"   OK Created 5 faculty")
    
    # Assign faculty: each gets 1 subject and 3 batches
    print("\n4. Creating faculty assignments...")
    assignment_count = 0
    
    # Faculty 1: Batches 2Q31, 2Q32, 2Q33
    # Faculty 2: Batches 2Q33, 2Q34, 2Q35
    # Faculty 3: Batches 2Q35, 2Q36, 2Q37
    # Faculty 4: Batches 2Q37, 2Q38, 2Q39
    # Faculty 5: Batches 2Q39, 2Q40, 2Q31
    
    faculty_batch_assignments = [
        [0, 1, 2],   # Faculty 1: 2Q31, 2Q32, 2Q33
        [2, 3, 4],   # Faculty 2: 2Q33, 2Q34, 2Q35
        [4, 5, 6],   # Faculty 3: 2Q35, 2Q36, 2Q37
        [6, 7, 8],   # Faculty 4: 2Q37, 2Q38, 2Q39
        [8, 9, 0]    # Faculty 5: 2Q39, 2Q40, 2Q31
    ]
    
    for i, fac_id in enumerate(faculty_ids):
        subject_id = subject_ids[i]
        batch_indices = faculty_batch_assignments[i]
        assigned_batches = [BATCHES[idx] for idx in batch_indices]
        
        for batch in assigned_batches:
            cursor.execute("""
                INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
                VALUES (faculty_classes_seq.NEXTVAL, :fac_id, :subj_id, :class_name)
            """, {'fac_id': fac_id, 'subj_id': subject_id, 'class_name': batch})
            assignment_count += 1
    
    conn.commit()
    print(f"   OK Created {assignment_count} assignments")
    
    # Create 300 students
    print("\n5. Creating 300 students...")
    student_count = 0
    student_ids = []
    
    for batch in BATCHES:
        for i in range(30):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}.{batch.lower()}.{i}@thapar.edu"
            cgpa = round(random.uniform(6.5, 9.5), 2)
            
            cursor.execute("""
                INSERT INTO users (user_id, email, password, name, role)
                VALUES (users_seq.NEXTVAL, :email, 'pass123', :name, 'student')
            """, {'email': email, 'name': full_name})
            cursor.execute("SELECT users_seq.CURRVAL FROM dual")
            user_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
                VALUES (students_seq.NEXTVAL, :user_id, :name, 'CSE', :semester, :class_name, :cgpa)
            """, {
                'user_id': user_id,
                'name': full_name,
                'semester': SEMESTER,
                'class_name': batch,
                'cgpa': cgpa
            })
            cursor.execute("SELECT students_seq.CURRVAL FROM dual")
            student_ids.append(cursor.fetchone()[0])
            student_count += 1
    
    conn.commit()
    print(f"   OK Created 300 students")
    
    # Generate marks
    print("\n6. Generating marks...")
    marks_count = 0
    assessment_types = [('MST', 30), ('EST', 40), ('Quiz', 15), ('Assignment', 15)]
    
    for student_id in student_ids:
        cursor.execute("SELECT class_name FROM students WHERE student_id = :sid", {'sid': student_id})
        class_name = cursor.fetchone()[0]
        
        for subject_id in subject_ids:
            for assessment_type, max_marks in assessment_types:
                marks_obtained = random.randint(int(max_marks * 0.5), int(max_marks * 0.95))
                
                cursor.execute("""
                    INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
                    VALUES (marks_seq.NEXTVAL, :student_id, :subject_id, :class_name, :assessment_type, :marks_obtained, :max_marks)
                """, {
                    'student_id': student_id,
                    'subject_id': subject_id,
                    'class_name': class_name,
                    'assessment_type': assessment_type,
                    'marks_obtained': marks_obtained,
                    'max_marks': max_marks
                })
                marks_count += 1
    
    conn.commit()
    print(f"   OK Generated {marks_count} marks")
    
    # Generate attendance (1 Jan - 1 May 2026)
    print("\n7. Generating attendance...")
    attendance_count = 0
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 5, 1)
    
    for student_id in student_ids:
        cursor.execute("SELECT class_name FROM students WHERE student_id = :sid", {'sid': student_id})
        class_name = cursor.fetchone()[0]
        
        attendance_rate = random.uniform(0.60, 0.95)
        
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:
                for subject_id in subject_ids:
                    status = 'P' if random.random() < attendance_rate else 'A'
                    
                    cursor.execute("""
                        INSERT INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
                        VALUES (attendance_seq.NEXTVAL, :student_id, :subject_id, :class_name, :attendance_date, :status)
                    """, {
                        'student_id': student_id,
                        'subject_id': subject_id,
                        'class_name': class_name,
                        'attendance_date': current_date,
                        'status': status
                    })
                    attendance_count += 1
            
            current_date += timedelta(days=1)
    
    conn.commit()
    print(f"   OK Generated {attendance_count} attendance records")
    
    # Generate alerts
    print("\n8. Generating alerts...")
    alert_count = 0
    
    cursor.execute("""
        SELECT s.student_id, a.subject_id, sub.subject_name,
               COUNT(*) as total,
               SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        JOIN subjects sub ON a.subject_id = sub.subject_id
        GROUP BY s.student_id, a.subject_id, sub.subject_name
        HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
    """)
    
    alert_results = cursor.fetchall()
    for idx, (student_id, subject_id, subject_name, total, present) in enumerate(alert_results):
        percentage = round((present / total) * 100, 2)
        alert_type = 'Critical' if percentage < 50 else 'Warning'
        message = f"Low attendance in {subject_name}: {percentage}%"
        
        # Vary the alert creation date (spread over last 30 days)
        days_ago = idx % 30
        alert_date = datetime(2026, 4, 5) - timedelta(days=days_ago)
        
        cursor.execute("""
            INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message, is_read, created_at)
            VALUES (alerts_seq.NEXTVAL, :student_id, :subject_id, :alert_type, :message, 0, :created_at)
        """, {
            'student_id': student_id,
            'subject_id': subject_id,
            'alert_type': alert_type,
            'message': message,
            'created_at': alert_date
        })
        alert_count += 1
    
    conn.commit()
    print(f"   OK Generated {alert_count} alerts")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("SETUP COMPLETE!")
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Faculty: 5 (1 subject each, 3 batches each)")
    print(f"  Students: 300 (30 per batch, semester 4)")
    print(f"  Subjects: 5")
    print(f"  Batches: 10 (2Q31-2Q40)")
    print(f"  Marks: {marks_count}")
    print(f"  Attendance: {attendance_count}")
    print(f"  Alerts: {alert_count}")
    print(f"\nSample Student: rohan.sharma.2q31.0@thapar.edu / pass123")
    print(f"Sample Faculty: dr.rajesh@thaparfac.edu / pass123")

if __name__ == '__main__':
    setup_system()
