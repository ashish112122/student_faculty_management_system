import oracledb
import jwt
from flask import Blueprint, request, jsonify
from functools import wraps

DB_CONFIG = {
    'user': 'system',
    'password': 'gur2005',
    'dsn': 'localhost:1521/XE'
}

SECRET_KEY = 'your-secret-key-change-in-production'

attendance_bp = Blueprint('attendance_bp', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token missing'}), 401
        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = decoded.get('user_id')
            request.role = decoded.get('role')
        except Exception:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated


@attendance_bp.route('/api/attendance/report', methods=['GET'])
@token_required
def attendance_report():
    conn = None
    cursor = None
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT student_id FROM students WHERE user_id = :user_id",
            {'user_id': request.user_id}
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Student not found'}), 404
        student_id = row[0]

        cursor.execute("""
            SELECT s.subject_id, s.subject_name, s.subject_code
            FROM student_subjects ss
            JOIN subjects s ON ss.subject_id = s.subject_id
            WHERE ss.student_id = :student_id
            ORDER BY s.subject_id
        """, {'student_id': student_id})
        subjects = cursor.fetchall()

        report = []
        for subject in subjects:
            subject_id, subject_name, subject_code = subject

            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) as present
                FROM attendance
                WHERE student_id = :student_id AND subject_id = :subject_id
            """, {'student_id': student_id, 'subject_id': subject_id})
            att_row = cursor.fetchone()
            total = att_row[0]
            present = att_row[1] if att_row[1] else 0
            percentage = round((present / total) * 100, 2) if total > 0 else 0

            report.append({
                'subject_id': subject_id,
                'subject_name': subject_name,
                'subject_code': subject_code,
                'total_classes': total,
                'present': present,
                'percentage': percentage
            })

        return jsonify(report), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@attendance_bp.route('/api/attendance/mark', methods=['POST'])
@token_required
def mark_attendance():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        attendance_date = data.get('attendance_date')
        status = data.get('status')

        if status not in ('P', 'A'):
            return jsonify({'error': "Status must be 'P' or 'A'"}), 400

        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attendance
            VALUES (attendance_seq.NEXTVAL, :student_id, :subject_id,
                    TO_DATE(:attendance_date, 'YYYY-MM-DD'), :status)
        """, {
            'student_id': student_id,
            'subject_id': subject_id,
            'attendance_date': attendance_date,
            'status': status
        })

        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) as present
            FROM attendance
            WHERE student_id = :student_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'subject_id': subject_id})
        att_row = cursor.fetchone()
        total = att_row[0]
        present = att_row[1] if att_row[1] else 0
        percentage = round((present / total) * 100, 2) if total > 0 else 0

        if percentage < 75:
            cursor.execute(
                "SELECT COUNT(*) FROM alerts WHERE student_id = :student_id",
                {'student_id': student_id}
            )
            alert_count = cursor.fetchone()[0]

            if alert_count == 0:
                cursor.execute(
                    "SELECT subject_name FROM subjects WHERE subject_id = :subject_id",
                    {'subject_id': subject_id}
                )
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
        return jsonify({'message': 'Attendance marked successfully', 'percentage': percentage}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
