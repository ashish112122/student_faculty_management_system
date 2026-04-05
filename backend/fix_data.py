"""
Fix data to match requirements:
- 10 batches: 2Q31 to 2Q40
- 30 students per batch = 300 students
- 5 subjects
- Each faculty teaches 1 subject to 3 batches
- Semester 4 for all students
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
DEPARTMENTS = ['CSE']
SEMESTER = 4

FIRST_NAMES = ['Rohan', 'Priya', 'Amit', 'Sneha', 'Rahul', 'Anjali', 'Vikram', 'Neha', 'Karan', 'Pooja',
               'Arjun', 'Divya', 'Sanjay', 'Kavya', 'Aditya', 'Ritu', 'Manish', 'Swati', 'Nikhil', 'Tanvi',
               'Harsh', 'Ishita', 'Varun', 'Megha', 'Rohit', 'Shruti', 'Akash', 'Nisha', 'Gaurav', 'Preeti']

LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Gupta', 'Verma', 'Singh', 'Reddy', 'Joshi', 'Mehta', 'Nair']

def fix_data():
    print("=" * 80)
    print("FIXING DATA TO MATCH REQUIREMENTS")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Clear existing data
    print("\n1. Clearing existing data...")
    try:
        cursor.execute("DELETE FROM feedback")
        cursor.execute("DELETE FROM alerts")
        cursor.execute("DELETE FROM attendance")
        cursor.execute("DELETE FROM marks")
        cursor.execute("DELETE FROM faculty_classes")
        
        cursor.execute("SELECT user_id FROM students")
        student_user_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT user_id FROM faculty")
        faculty_user_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM faculty")
        cursor.execute("DELETE FROM subjects")
        
        for uid in student_user_ids + faculty_user_ids:
            cursor.execute("DELETE FROM users WHERE user_id = :uid", {'uid': uid})
        
        conn.commit()
        print("   OK Data cleared")
    except Exception as e:
        print(f"   Error clearing: {e}")
        conn.rollback()
    
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
    print(f"   OK Created {len(subjects_data)} subjects")
    
    # Create 5 faculty (one per subject)
    print("\n3. Creating 5 faculty members...")
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
    print(f"   OK Created {len(faculty_ids)} faculty")
    
    # Assign each faculty to 1 subject and 3 batches
    print("\n4. Creating faculty-subject-batch assignments...")
    assignment_count = 0
    for i, fac_id in enumerate(faculty_ids):
        subject_id = subject_ids[i]  # Each faculty gets one subject
        assigned_batches = BATCHES[i*2:(i*2)+3]  # Each faculty gets 3 consecutive batches
        
        for batch in assigned_batches:
            cursor.execute("""
                INSERT INTO faculty_classes (faculty_class_id, faculty_id, class_name, subject_id)
                VALUES (faculty_classes_seq.NEXTVAL, :fac_id, :class_name, :subj_id)
            """, {'fac_id': fac_id, 'class_name': batch, 'subj_id': subject_id})
            assignment_count += 1
    
    conn.commit()
    print(f"   OK Created {assignment_count} faculty-class assignments")
    
    # Create 300 students (30 per batch, semester 4)
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
                INSERT INTO students (student_id, user_id, name, branch, year_of_study, semester, section, class_name, cgpa)
                VALUES (students_seq.NEXTVAL, :user_id, :name, 'CSE', 2, :semester, 'A', :class_name, :cgpa)
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
    print(f"   OK Created {student_count} students")
    
    # Generate marks for all students in all 5 subjects
    print("\n6. Generating marks...")
    marks_count = 0
    assessment_types = [('MST', 50), ('EST', 100), ('Quiz', 10), ('Assignment', 20)]
    
    for student_id in student_ids:
        cursor.execute("SELECT class_name FROM students WHERE student_id = :sid", {'sid': student_id})
        class_name = cursor.fetchone()[0]
        
        # Each student gets marks in all 5 subjects
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
    print(f"   OK Generated {marks_count} marks records")
    
    # Generate attendance from 1 Jan 2026 to 1 May 2026
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
            if current_date.weekday() < 5:  # Monday to Friday
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
    
    # Generate alerts based on attendance < 75%
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
    
    for student_id, subject_id, subject_name, total, present in cursor.fetchall():
        percentage = round((present / total) * 100, 2)
        alert_type = 'Critical' if percentage < 50 else 'Warning'
        message = f"Low attendance in {subject_name}: {percentage}% ({present}/{total} classes)"
        
        cursor.execute("""
            INSERT INTO alerts (alert_id, student_id, alert_type, message, is_read)
            VALUES (alerts_seq.NEXTVAL, :student_id, :alert_type, :message, 0)
        """, {
            'student_id': student_id,
            'alert_type': alert_type,
            'message': message
        })
        alert_count += 1
    
    conn.commit()
    print(f"   OK Generated {alert_count} alerts")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("DATA FIX COMPLETE!")
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Faculty: 5 (1 subject each, 3 batches each)")
    print(f"  Students: {student_count} (30 per batch, semester 4)")
    print(f"  Subjects: 5")
    print(f"  Batches: 10 (2Q31-2Q40)")
    print(f"  Marks: {marks_count}")
    print(f"  Attendance: {attendance_count} (1 Jan - 1 May 2026)")
    print(f"  Alerts: {alert_count}")

if __name__ == '__main__':
    fix_data()
