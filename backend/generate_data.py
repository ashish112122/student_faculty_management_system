"""
Generate comprehensive demo data for the student-faculty portal
- 5 classes: 2Q11, 2Q12, 2Q13, 2Q14, 2Q15
- 30 students per class (150 total)
- 10 faculty members
- 5 subjects
- Complete marks, attendance (Jan 1, 2026 to today), and alerts
"""

import oracledb
from datetime import datetime, timedelta
import random
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

CLASSES = ['2Q11', '2Q12', '2Q13', '2Q14', '2Q15']
FIRST_NAMES = ['Rohan', 'Priya', 'Amit', 'Sneha', 'Rahul', 'Anjali', 'Vikram', 'Neha', 'Karan', 'Pooja',
               'Arjun', 'Divya', 'Sanjay', 'Kavya', 'Aditya', 'Ritu', 'Manish', 'Swati', 'Nikhil', 'Tanvi',
               'Harsh', 'Ishita', 'Varun', 'Megha', 'Rohit', 'Shruti', 'Akash', 'Nisha', 'Gaurav', 'Preeti']
LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Gupta', 'Verma', 'Singh', 'Reddy', 'Joshi', 'Mehta', 'Nair',
              'Das', 'Iyer', 'Rao', 'Menon', 'Shah', 'Bose', 'Jain', 'Pillai', 'Agarwal', 'Kapoor',
              'Bansal', 'Saxena', 'Chopra', 'Sinha', 'Bhatt', 'Pandey', 'Tiwari', 'Dubey', 'Mishra', 'Yadav']

def clear_data(conn):
    """Clear all existing data"""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM alerts")
        cursor.execute("DELETE FROM attendance")
        cursor.execute("DELETE FROM marks")
        cursor.execute("DELETE FROM feedback")
        cursor.execute("DELETE FROM student_subjects")
        cursor.execute("DELETE FROM faculty_classes")
        cursor.execute("DELETE FROM faculty")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM subjects")
        cursor.execute("DELETE FROM users")
        conn.commit()
        print("✓ Cleared existing data")
    finally:
        cursor.close()

def reset_sequences(conn):
    """Reset all sequences"""
    cursor = conn.cursor()
    sequences = ['users_seq', 'students_seq', 'faculty_seq', 'subjects_seq', 
                 'student_subjects_seq', 'faculty_classes_seq', 'marks_seq', 
                 'attendance_seq', 'alerts_seq', 'feedback_seq']
    try:
        for seq in sequences:
            cursor.execute(f"ALTER SEQUENCE {seq} RESTART START WITH 1")
        conn.commit()
        print("✓ Reset sequences")
    finally:
        cursor.close()

def create_faculty(conn):
    """Create 10 faculty members"""
    cursor = conn.cursor()
    faculty_data = [
        ('dr.rajesh@thapar.edu', 'Dr. Rajesh Kumar', 'Computer Science', 'Associate Professor'),
        ('prof.meena@thapar.edu', 'Prof. Meena Sharma', 'Mathematics', 'Professor'),
        ('dr.suresh@thapar.edu', 'Dr. Suresh Patel', 'Computer Science', 'Assistant Professor'),
        ('prof.kavita@thapar.edu', 'Prof. Kavita Singh', 'Electronics', 'Associate Professor'),
        ('dr.anil@thapar.edu', 'Dr. Anil Verma', 'Computer Science', 'Professor'),
        ('prof.deepak@thapar.edu', 'Prof. Deepak Gupta', 'Computer Science', 'Assistant Professor'),
        ('dr.priya@thapar.edu', 'Dr. Priya Malhotra', 'Mathematics', 'Associate Professor'),
        ('prof.vikram@thapar.edu', 'Prof. Vikram Reddy', 'Computer Science', 'Professor'),
        ('dr.anjali@thapar.edu', 'Dr. Anjali Desai', 'Electronics', 'Assistant Professor'),
        ('prof.rahul@thapar.edu', 'Prof. Rahul Joshi', 'Computer Science', 'Associate Professor'),
    ]
    
    try:
        for email, name, dept, designation in faculty_data:
            cursor.execute("""
                INSERT INTO users (user_id, email, password, name, role)
                VALUES (users_seq.NEXTVAL, :email, 'pass123', :name, 'faculty')
            """, {'email': email, 'name': name})
            
            cursor.execute("""
                INSERT INTO faculty (faculty_id, user_id, department, designation)
                VALUES (faculty_seq.NEXTVAL, users_seq.CURRVAL, :dept, :designation)
            """, {'dept': dept, 'designation': designation})
        
        conn.commit()
        print(f"✓ Created {len(faculty_data)} faculty members")
    finally:
        cursor.close()

def create_subjects(conn):
    """Create 5 subjects"""
    cursor = conn.cursor()
    subjects = [
        ('Database Management Systems', 'CS301'),
        ('Operating Systems', 'CS302'),
        ('Computer Networks', 'CS303'),
        ('Software Engineering', 'CS304'),
        ('Data Structures', 'CS305'),
    ]
    
    try:
        for name, code in subjects:
            cursor.execute("""
                INSERT INTO subjects (subject_id, subject_name, subject_code)
                VALUES (subjects_seq.NEXTVAL, :name, :code)
            """, {'name': name, 'code': code})
        
        conn.commit()
        print(f"✓ Created {len(subjects)} subjects")
    finally:
        cursor.close()

def create_faculty_classes(conn):
    """Assign faculty to classes"""
    cursor = conn.cursor()
    # faculty_id, class_name, subject_id
    assignments = [
        # Dr. Rajesh (1) - DBMS (1) - Classes 2Q11, 2Q12, 2Q13
        (1, '2Q11', 1), (1, '2Q12', 1), (1, '2Q13', 1),
        # Prof. Meena (2) - OS (2) - Classes 2Q11, 2Q14
        (2, '2Q11', 2), (2, '2Q14', 2),
        # Dr. Suresh (3) - Networks (3) - Classes 2Q12, 2Q13, 2Q15
        (3, '2Q12', 3), (3, '2Q13', 3), (3, '2Q15', 3),
        # Prof. Kavita (4) - Software Eng (4) - Classes 2Q14, 2Q15
        (4, '2Q14', 4), (4, '2Q15', 4),
        # Dr. Anil (5) - Data Structures (5) - All Classes
        (5, '2Q11', 5), (5, '2Q12', 5), (5, '2Q13', 5), (5, '2Q14', 5), (5, '2Q15', 5),
        # Prof. Deepak (6) - DBMS (1) - Classes 2Q14, 2Q15
        (6, '2Q14', 1), (6, '2Q15', 1),
        # Dr. Priya (7) - OS (2) - Classes 2Q12, 2Q13, 2Q15
        (7, '2Q12', 2), (7, '2Q13', 2), (7, '2Q15', 2),
        # Prof. Vikram (8) - Networks (3) - Classes 2Q11, 2Q14
        (8, '2Q11', 3), (8, '2Q14', 3),
        # Dr. Anjali (9) - Software Eng (4) - Classes 2Q11, 2Q12, 2Q13
        (9, '2Q11', 4), (9, '2Q12', 4), (9, '2Q13', 4),
    ]
    
    try:
        for fac_id, class_name, subj_id in assignments:
            cursor.execute("""
                INSERT INTO faculty_classes (faculty_class_id, faculty_id, class_name, subject_id)
                VALUES (faculty_classes_seq.NEXTVAL, :fac_id, :class_name, :subj_id)
            """, {'fac_id': fac_id, 'class_name': class_name, 'subj_id': subj_id})
        
        conn.commit()
        print(f"✓ Created {len(assignments)} faculty-class assignments")
    finally:
        cursor.close()

def create_students(conn):
    """Create 150 students (30 per class)"""
    cursor = conn.cursor()
    student_count = 0
    
    try:
        for class_name in CLASSES:
            for i in range(30):
                first_name = FIRST_NAMES[i]
                last_name = LAST_NAMES[i]
                full_name = f"{first_name} {last_name}"
                email = f"{first_name.lower()}.{last_name.lower()}.{class_name.lower()}@thapar.edu"
                cgpa = round(random.uniform(7.0, 9.5), 2)
                
                # Create user
                cursor.execute("""
                    INSERT INTO users (user_id, email, password, name, role)
                    VALUES (users_seq.NEXTVAL, :email, 'pass123', :name, 'student')
                """, {'email': email, 'name': full_name})
                
                # Create student
                cursor.execute("""
                    INSERT INTO students (student_id, user_id, branch, year_of_study, semester, class_name, cgpa)
                    VALUES (students_seq.NEXTVAL, users_seq.CURRVAL, 'Computer Engineering', 2, 4, :class_name, :cgpa)
                """, {'class_name': class_name, 'cgpa': cgpa})
                
                student_count += 1
        
        conn.commit()
        print(f"✓ Created {student_count} students across {len(CLASSES)} classes")
    finally:
        cursor.close()

def enroll_students_in_subjects(conn):
    """Enroll all students in all 5 subjects"""
    cursor = conn.cursor()
    enrollment_count = 0
    
    try:
        # Get all student IDs
        cursor.execute("SELECT student_id FROM students")
        student_ids = [row[0] for row in cursor.fetchall()]
        
        # Enroll each student in all 5 subjects
        for student_id in student_ids:
            for subject_id in range(1, 6):
                cursor.execute("""
                    INSERT INTO student_subjects (student_subject_id, student_id, subject_id)
                    VALUES (student_subjects_seq.NEXTVAL, :student_id, :subject_id)
                """, {'student_id': student_id, 'subject_id': subject_id})
                enrollment_count += 1
        
        conn.commit()
        print(f"✓ Created {enrollment_count} student-subject enrollments")
    finally:
        cursor.close()

def generate_marks(conn):
    """Generate marks for all students in all subjects"""
    cursor = conn.cursor()
    marks_count = 0
    assessment_types = ['MST', 'EST', 'Assignment', 'Quiz']
    max_marks_map = {'MST': 50, 'EST': 100, 'Assignment': 20, 'Quiz': 10}
    
    try:
        # Get all students with their class
        cursor.execute("SELECT student_id, class_name FROM students")
        students = cursor.fetchall()
        
        for student_id, class_name in students:
            for subject_id in range(1, 6):
                for assessment_type in assessment_types:
                    max_marks = max_marks_map[assessment_type]
                    # Generate marks between 60-95% of max
                    marks_obtained = random.randint(int(max_marks * 0.6), int(max_marks * 0.95))
                    
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
        print(f"✓ Generated {marks_count} marks records")
    finally:
        cursor.close()

def generate_attendance(conn):
    """Generate attendance from Jan 1, 2026 to today"""
    cursor = conn.cursor()
    attendance_count = 0
    start_date = datetime(2026, 1, 1)
    end_date = datetime.now()
    
    try:
        # Get all students with their class
        cursor.execute("SELECT student_id, class_name FROM students")
        students = cursor.fetchall()
        
        for student_id, class_name in students:
            # Random attendance percentage for this student (65-95%)
            attendance_rate = random.uniform(0.65, 0.95)
            
            current_date = start_date
            while current_date <= end_date:
                # Skip weekends
                if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                    for subject_id in range(1, 6):
                        # Randomly mark present/absent based on attendance rate
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
        print(f"✓ Generated {attendance_count} attendance records")
    finally:
        cursor.close()

def generate_alerts(conn):
    """Generate alerts for students with low attendance"""
    cursor = conn.cursor()
    alert_count = 0
    
    try:
        # Get students with low attendance in any subject
        cursor.execute("""
            SELECT s.student_id, s.class_name, a.subject_id, sub.subject_name,
                   COUNT(*) as total_classes,
                   SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present_count
            FROM students s
            JOIN attendance a ON s.student_id = a.student_id
            JOIN subjects sub ON a.subject_id = sub.subject_id
            GROUP BY s.student_id, s.class_name, a.subject_id, sub.subject_name
            HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
        """)
        
        low_attendance_students = cursor.fetchall()
        
        for student_id, class_name, subject_id, subject_name, total, present in low_attendance_students:
            percentage = round((present / total) * 100, 2)
            
            # Determine alert type
            if percentage < 60:
                alert_type = 'Critical'
            elif percentage < 70:
                alert_type = 'Alert'
            else:
                alert_type = 'Warning'
            
            message = f"Low attendance in {subject_name}: {percentage}% ({present}/{total} classes)"
            
            cursor.execute("""
                INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message)
                VALUES (alerts_seq.NEXTVAL, :student_id, :subject_id, :alert_type, :message)
            """, {
                'student_id': student_id,
                'subject_id': subject_id,
                'alert_type': alert_type,
                'message': message
            })
            alert_count += 1
        
        conn.commit()
        print(f"✓ Generated {alert_count} alerts for low attendance")
    finally:
        cursor.close()

def main():
    print("=" * 70)
    print("GENERATING COMPREHENSIVE DEMO DATA")
    print("=" * 70)
    
    try:
        conn = oracledb.connect(**DB_CONFIG)
        print("✓ Connected to database\n")
        
        clear_data(conn)
        reset_sequences(conn)
        create_faculty(conn)
        create_subjects(conn)
        create_faculty_classes(conn)
        create_students(conn)
        enroll_students_in_subjects(conn)
        generate_marks(conn)
        generate_attendance(conn)
        generate_alerts(conn)
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✓ DATA GENERATION COMPLETE!")
        print("=" * 70)
        print("\nSummary:")
        print("  • 10 Faculty members")
        print("  • 5 Subjects")
        print("  • 5 Classes (2Q11-2Q15)")
        print("  • 150 Students (30 per class)")
        print("  • Complete marks for all assessments")
        print("  • Attendance from Jan 1, 2026 to today")
        print("  • Automatic alerts for low attendance")
        print("\nTest Credentials:")
        print("  Faculty: dr.rajesh@thapar.edu / pass123")
        print("  Student: rohan.sharma.2q11@thapar.edu / pass123")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        raise

if __name__ == '__main__':
    main()
