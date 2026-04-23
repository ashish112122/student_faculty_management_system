import oracledb


def calculate_percentage(student_id, subject_id, cursor):
    cursor.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) as present
        FROM attendance
        WHERE student_id = :student_id AND subject_id = :subject_id
    """, {'student_id': student_id, 'subject_id': subject_id})
    row = cursor.fetchone()
    total = row[0]
    present = row[1] if row[1] else 0
    if total == 0:
        return 0
    return round((present / total) * 100, 2)


def generate_alert(student_id, subject_id, percentage, conn, cursor):
    cursor.execute("""
        SELECT COUNT(*) FROM alerts WHERE student_id = :student_id
    """, {'student_id': student_id})
    count = cursor.fetchone()[0]

    if count == 0 and percentage < 75:
        cursor.execute("""
            SELECT subject_name FROM subjects WHERE subject_id = :subject_id
        """, {'subject_id': subject_id})
        subject_name = cursor.fetchone()[0]

        if percentage < 50:
            alert_type = 'Critical'
        elif percentage < 65:
            alert_type = 'Alert'
        else:
            alert_type = 'Warning'

        message = f"Your attendance in {subject_name} is below {percentage}%. Please improve."

        cursor.execute("""
            INSERT INTO alerts
            VALUES (alerts_seq.NEXTVAL, :student_id, :alert_type, :message, SYSDATE)
        """, {
            'student_id': student_id,
            'alert_type': alert_type,
            'message': message
        })
        conn.commit()
