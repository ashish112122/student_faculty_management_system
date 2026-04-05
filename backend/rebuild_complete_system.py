"""
Complete system rebuild - 150 students with full data
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

DEPARTMENTS = ['Computer Science', 'Electronics', 'Mechanical', 'Civil']
BATCHES = ['2Q11', '2Q12', '2Q13', '2Q14', '2Q15']
SEMESTERS = [1, 2, 3, 4, 5, 6, 7, 8]

FIRST_NAMES = ['Rohan', 'Priya', 'Amit', 'Sneha', 'Rahul', 'Anjali', 'Vikram', 'Neha', 'Karan', 'Pooja',
               'Arjun', 'Divya', 'Sanjay', 'Kavya', 'Aditya', 'Ritu', 'Manish', 'Swati', 'Nikhil', 'Tanvi',
               'Harsh', 'Ishita', 'Varun', 'Megha', 'Rohit', 'Shruti', 'Akash', 'Nisha', 'Gaurav', 'Preeti']

LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Gupta', 'Verma', 'Singh', 'Reddy', 'Joshi', 'Mehta', 'Nair',
              'Das', 'Iyer', 'Rao', 'Menon', 'Shah', 'Bose', 'Jain', 'Pillai', 'Agarwal', 'Kapoor']

def rebuild_system():
    print("=" * 80)
    print("REBUILDING COMPLETE SYSTEM - 150 STUDENTS")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Clear all data in correct order
    print("\n1. Clearing existing data...")
    try:
        cursor.execute("DELETE FROM alerts")
        cursor.execute("DELETE FROM attendance")
        cursor.execute("DELETE FROM marks")
        cursor.execute("DELETE FROM feedback")
        cursor.execute("DELETE FROM student_subjects")
        cursor.execute("DELETE FROM faculty_classes")
        cursor.execute("DELETE FROM faculty_subjects")
    except:
        pass
    
    # Get user IDs before deleting
    try:
        cursor.execute("SELECT user_id FROM students")
        student_user_ids = [row[0] for row in cursor.fetchall()]
    except:
        student_user_ids = []
    
    try:
        cursor.execute("SELECT user_id FROM faculty")
        faculty_user_ids = [row[0] for row in cursor.fetchall()]
    except:
        faculty_user_ids = []
    
    try:
        cursor.execute("DELETE FROM students")
    except:
        pass
    
    try:
        cursor.execute("DELETE FROM faculty")
    except:
        pass
    
    try:
        cursor.execute("DELETE FROM subjects")
    except:
        pass
    
    # Delete users
    for uid in student_user_ids + faculty_user_ids:
        try:
            cursor.execute("DELETE FROM users WHERE user_id = :uid", {'uid': uid})
        except:
            pass
    
    conn.commit()
    print("   OK Data cleared")
    
    # Create 10 faculty
    print("\n2. Creating 10 faculty members...")
    faculty_data = [
        ('dr.rajesh@thaparfac.edu', 'Dr. Rajesh Kumar', 'Computer Science'),
        ('prof.meena@thaparfac.edu', 'Prof. Meena Sharma', 'Computer Science'),
        ('dr.suresh@thaparfac.edu', 'Dr. Suresh Patel', 'Electronics'),
        ('prof.kavita@thaparfac.edu', 'Prof. Kavita Singh', 'Electronics'),
        ('dr.anil@thaparfac.edu', 'Dr. Anil Verma', 'Mechanical'),
        ('prof.deepak@thaparfac.edu', 'Prof. Deepak Gupta', 'Mechanical'),
        ('dr.priya@thaparfac.edu', 'Dr. Priya Malhotra', 'Civil'),
        ('prof.vikram@thaparfac.edu', 'Prof. Vikram Reddy', 'Civil'),
        ('dr.anjali@thaparfac.edu', 'Dr. Anjali Desai', 'Computer Science'),
        ('prof.rahul@thaparfac.edu', 'Prof. Rahul Joshi', 'Electronics'),
    ]
    
    faculty_ids = []
    for email, name, dept in faculty_data:
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE email = :email", {'email': email})
        existing_user = cursor.fetchone()
        
        if existing_user:
            user_id = existing_user[0]
            # Check if faculty record exists
            cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': user_id})
            existing_faculty = cursor.fetchone()
            if existing_faculty:
                faculty_ids.append(existing_faculty[0])
                continue
        else:
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
    print(f"   OK Created {len(faculty_ids)} faculty")
    
    # Create subjects
    print("\n3. Creating subjects...")
    subjects_data = [
        ('Database Management Systems', 'CS301'),
        ('Operating Systems', 'CS302'),
        ('Computer Networks', 'CS303'),
        ('Software Engineering', 'CS304'),
        ('Data Structures', 'CS305'),
        ('Digital Electronics', 'EC301'),
        ('Microprocessors', 'EC302'),
        ('Thermodynamics', 'ME301'),
        ('Fluid Mechanics', 'ME302'),
        ('Structural Analysis', 'CE301'),
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
    print(f"   OK Created {len(subjects_data)} subjects")
    
    # Assign faculty to classes and subjects
    print("\n4. Creating faculty-class assignments...")
    assignment_count = 0
    for fac_id in faculty_ids:
        # Each faculty teaches 2-3 classes
        num_classes = random.randint(2, 3)
        assigned_classes = random.sample(BATCHES, num_classes)
        
        # Each faculty teaches 2-3 subjects
        num_subjects = random.randint(2, 3)
        assigned_subjects = random.sample(subject_ids, num_subjects)
        
        for class_name in assigned_classes:
            for subj_id in assigned_subjects:
                cursor.execute("""
                    INSERT INTO faculty_classes (faculty_class_id, faculty_id, class_name, subject_id)
                    VALUES (faculty_classes_seq.NEXTVAL, :fac_id, :class_name, :subj_id)
                """, {'fac_id': fac_id, 'class_name': class_name, 'subj_id': subj_id})
                assignment_count += 1
    
    conn.commit()
    print(f"   OK Created {assignment_count} faculty-class assignments")
    
    # Create 150 students
    print("\n5. Creating 150 students...")
    student_count = 0
    student_ids = []
    
    for batch in BATCHES:
        for i in range(30):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}.{batch.lower()}.{i}@thapar.edu"
            dept = random.choice(DEPARTMENTS)
            semester = random.choice(SEMESTERS)
            section = random.choice(['A', 'B', 'C'])
            cgpa = round(random.uniform(6.5, 9.5), 2)
            
            cursor.execute("""
                INSERT INTO users (user_id, email, password, name, role)
                VALUES (users_seq.NEXTVAL, :email, 'pass123', :name, 'student')
            """, {'email': email, 'name': full_name})
            
            cursor.execute("""
                INSERT INTO students (student_id, user_id, name, branch, year_of_study, semester, section, class_name, cgpa)
                VALUES (students_seq.NEXTVAL, users_seq.CURRVAL, :name, :branch, :year, :semester, :section, :class_name, :cgpa)
            """, {
                'name': full_name,
                'branch': dept,
                'year': (semester + 1) // 2,
                'semester': semester,
                'section': section,
                'class_name': batch,
                'cgpa': cgpa
            })
            
            cursor.execute("SELECT students_seq.CURRVAL FROM dual")
            student_ids.append(cursor.fetchone()[0])
            student_count += 1
    
    conn.commit()
    print(f"   OK Created {student_count} students")
    
    # Enroll students in subjects (skip if table doesn't exist)
    print("\n6. Enrolling students in subjects...")
    enrollment_count = 0
    try:
        for student_id in student_ids:
            # Each student enrolled in 5-6 subjects
            num_subjects = random.randint(5, 6)
            enrolled_subjects = random.sample(subject_ids, num_subjects)
            
            for subj_id in enrolled_subjects:
                cursor.execute("""
                    INSERT INTO student_subjects (student_subject_id, student_id, subject_id)
                    VALUES (student_subjects_seq.NEXTVAL, :student_id, :subject_id)
                """, {'student_id': student_id, 'subject_id': subj_id})
                enrollment_count += 1
        
        conn.commit()
        print(f"   OK Created {enrollment_count} enrollments")
    except Exception as e:
        print(f"   SKIP Table student_subjects not found or error: {str(e)[:50]}")
        conn.rollback()
    
    # Generate marks
    print("\n7. Generating marks...")
    marks_count = 0
    assessment_types = ['MST', 'EST', 'Assignment', 'Quiz']
    max_marks_map = {'MST': 50, 'EST': 100, 'Assignment': 20, 'Quiz': 10}
    
    cursor.execute("SELECT student_id, class_name FROM students")
    students = cursor.fetchall()
    
    for student_id, class_name in students:
        # Assign random subjects to each student (3-5 subjects)
        num_subjects = random.randint(3, 5)
        student_subjects = random.sample(subject_ids, num_subjects)
        
        for subj_id in student_subjects:
            for assessment_type in assessment_types:
                max_marks = max_marks_map[assessment_type]
                marks_obtained = random.randint(int(max_marks * 0.5), int(max_marks * 0.95))
                
                cursor.execute("""
                    INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
                    VALUES (marks_seq.NEXTVAL, :student_id, :subject_id, :class_name, :assessment_type, :marks_obtained, :max_marks)
                """, {
                    'student_id': student_id,
                    'subject_id': subj_id,
                    'class_name': class_name,
                    'assessment_type': assessment_type,
                    'marks_obtained': marks_obtained,
                    'max_marks': max_marks
                })
                marks_count += 1
    
    conn.commit()
    print(f"   OK Generated {marks_count} marks records")
    
    # Generate attendance
    print("\n8. Generating attendance...")
    attendance_count = 0
    start_date = datetime(2026, 1, 1)
    end_date = datetime.now()
    
    # Get student-subject mapping from marks
    cursor.execute("""
        SELECT DISTINCT student_id, subject_id, class_name FROM marks
    """)
    student_subject_map = cursor.fetchall()
    
    for student_id, subject_id, class_name in student_subject_map:
        attendance_rate = random.uniform(0.60, 0.95)
        
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:
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
    print("\n9. Generating alerts...")
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
    
    for student_id, subject_id, subject_name, total, present in cursor.fetchall():
        percentage = round((present / total) * 100, 2)
        
        if percentage < 50:
            alert_type = 'Critical'
        elif percentage < 60:
            alert_type = 'Alert'
        else:
            alert_type = 'Warning'
        
        message = f"Low attendance in {subject_name}: {percentage}% ({present}/{total} classes)"
        
        cursor.execute("""
            INSERT INTO alerts (alert_id, student_id, alert_type, message)
            VALUES (alerts_seq.NEXTVAL, :student_id, :alert_type, :message)
        """, {
            'student_id': student_id,
            'alert_type': alert_type,
            'message': message
        })
        alert_count += 1
    
    # Generate low marks alerts
    cursor.execute("""
        SELECT s.student_id, m.subject_id, sub.subject_name, m.assessment_type, m.marks_obtained, m.max_marks
        FROM students s
        JOIN marks m ON s.student_id = m.student_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE (m.marks_obtained / m.max_marks) < 0.50
    """)
    
    for student_id, subject_id, subject_name, assessment_type, marks_obtained, max_marks in cursor.fetchall():
        percentage = round((marks_obtained / max_marks) * 100, 2)
        message = f"Low marks in {subject_name} ({assessment_type}): {marks_obtained}/{max_marks} ({percentage}%)"
        
        cursor.execute("""
            INSERT INTO alerts (alert_id, student_id, alert_type, message)
            VALUES (alerts_seq.NEXTVAL, :student_id, 'Critical', :message)
        """, {
            'student_id': student_id,
            'message': message
        })
        alert_count += 1
    
    conn.commit()
    print(f"   OK Generated {alert_count} alerts")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("SYSTEM REBUILD COMPLETE!")
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Faculty: 10")
    print(f"  Students: {student_count}")
    print(f"  Subjects: {len(subjects_data)}")
    print(f"  Enrollments: {enrollment_count}")
    print(f"  Marks: {marks_count}")
    print(f"  Attendance: {attendance_count}")
    print(f"  Alerts: {alert_count}")

if __name__ == '__main__':
    rebuild_system()
