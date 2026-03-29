def get_student_subjects(user_id, cursor):
    cursor.execute("""
        SELECT s.subject_id, s.subject_name, s.subject_code
        FROM student_subjects ss
        JOIN subjects s ON ss.subject_id = s.subject_id
        WHERE ss.student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
        ORDER BY s.subject_id
    """, {'user_id': user_id})
    rows = cursor.fetchall()
    return [
        {
            'subject_id': row[0],
            'subject_name': row[1],
            'subject_code': row[2]
        }
        for row in rows
    ]


def get_subject_details(subject_id, cursor):
    cursor.execute("""
        SELECT subject_id, subject_name, subject_code
        FROM subjects
        WHERE subject_id = :subject_id
    """, {'subject_id': subject_id})
    row = cursor.fetchone()
    if row:
        return {
            'subject_id': row[0],
            'subject_name': row[1],
            'subject_code': row[2]
        }
    return None
