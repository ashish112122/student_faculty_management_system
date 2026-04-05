import oracledb
import random
from datetime import datetime, timedelta

DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}

def insert_students():
    """Insert 150 students across 5 batches (30 per batch)"""
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        student_count = 0
        for batch in range(1, 6):
            for i in range(1, 31):
                student_count += 1
                email = f'student{student_count}@univ.edu'
                password = 'pass123'
                name = f'Student {student_count}'
                
                try:
                    cursor.execute(
                        "INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, :1, :2, :3, 'student')",
                        (email, password, name)
                    )
                    cursor.execute(
                        "INSERT INTO students (student_id, user_id, batch_id, semester, cgpa, total_credits) VALUES (students_seq.NEXTVAL, users_seq.CURRVAL, :1, 4, 0.0, 0)",
                        (batch,)
                    )
                except oracledb.IntegrityError:
                    pass
                
                if student_count % 25 == 0:
                    print(f"Inserted {student_count} students...")
        
        conn.commit()
        print(f"Total {student_count} students inserted successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    """Insert sample marks and attendance for some students"""
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # Get first 50 students
        cursor.execute("SELECT student_id FROM (SELECT student_id FROM students ORDER BY student_id) WHERE ROWNUM <= 50")
        students = cursor.fetchall()
        
        # Get all subjects
        cursor.execute("SELECT subject_id FROM subjects")
        subjects = cursor.fetchall()
        
        for stud in students:
            student_id = stud[0]
            # Randomly select 5 subjects for this student
            selected_subjs = random.sample(subjects, min(5, len(subjects)))
            
            for subj in selected_subjs:
                subject_id = subj[0]
                
                # Insert marks
                mst = random.randint(15, 30)
                est = random.randint(15, 30)
                quiz = random.randint(10, 20)
                assignment = random.randint(10, 20)
                total = (mst + est + quiz + assignment) / 4
                grade = 'A' if total >= 90 else 'B' if total >= 80 else 'C' if total >= 70 else 'D'
                
                try:
                    cursor.execute(
                        "INSERT INTO marks (mark_id, student_id, subject_id, mst, est, quiz, assignment, total, grade) VALUES (marks_seq.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8)",
                        (student_id, subject_id, mst, est, quiz, assignment, total, grade)
                    )
                except:
                    pass
                
                # Insert attendance (Jan 1 - May 1, 2026)
                start_date = datetime(2026, 1, 1)
                for day in range(120):
                    current_date = start_date + timedelta(days=day)
                    status = 'present' if random.random() > 0.15 else 'absent'
                    
                    try:
                        cursor.execute(
                            "INSERT INTO attendance (attendance_id, student_id, subject_id, att_date, status) VALUES (attendance_seq.NEXTVAL, :1, :2, :3, :4)",
                            (student_id, subject_id, current_date, status)
                        )
                    except:
                        pass
        
        conn.commit()
        print("Sample data inserted!")
    except Exception as e:
        print(f"Error in sample data: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_students()
    insert_sample_data()