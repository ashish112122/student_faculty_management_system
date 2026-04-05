import oracledb

DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}

def insert_marks_attendance():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # Get all students
        cursor.execute("SELECT student_id FROM students WHERE ROWNUM <= 50")
        students = cursor.fetchall()
        
        # Get all subjects
        cursor.execute("SELECT subject_id FROM subjects")
        subjects = cursor.fetchall()
        
        for student_id_tuple in students:
            student_id = student_id_tuple[0]
            for subject_id_tuple in subjects:
                subject_id = subject_id_tuple[0]
                marks = 70 + (student_id % 30)
                grade = 'A' if marks >= 90 else 'B' if marks >= 80 else 'C' if marks >= 70 else 'D'
                cursor.execute("INSERT INTO marks (mark_id, student_id, subject_id, marks, grade) VALUES (marks_seq.NEXTVAL, :1, :2, :3, :4)", (student_id, subject_id, marks, grade))
                cursor.execute("INSERT INTO attendance (attendance_id, student_id, subject_id, attendance_date, status) VALUES (attendance_seq.NEXTVAL, :1, :2, SYSDATE, 'present')", (student_id, subject_id))
        
        conn.commit()
        print("Marks and attendance inserted")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_marks_attendance()