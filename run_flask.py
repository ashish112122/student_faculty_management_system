from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import oracledb
import bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

SECRET_KEY = 'sfs-secret-key-2026'
DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}

def get_db_connection():
    return oracledb.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']
            current_role = data.get('role')
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, current_role, *args, **kwargs)
    return decorated

# ===== LOGIN & REGISTER =====
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'msg': 'Missing email/password'}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, password, role FROM users WHERE email = :1", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user:
            return jsonify({'msg': 'Invalid credentials'}), 401
        try:
            if not bcrypt.checkpw(password.encode(), user[1].encode()):
                return jsonify({'msg': 'Invalid credentials'}), 401
        except:
            if password != user[1]:
                return jsonify({'msg': 'Invalid credentials'}), 401
        token = jwt.encode({'user_id': user[0], 'role': user[2], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token, 'role': user[2]}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'msg': 'SFS Backend Running'}), 200

# ===== STUDENT API =====
@app.route('/api/student/info', methods=['GET'])
@token_required
def student_info(uid, role):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT u.name, s.student_id, s.batch_id, s.semester, s.cgpa FROM users u JOIN students s ON u.user_id = s.user_id WHERE u.user_id = :1", (uid,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if not res: return jsonify({'msg': 'Not found'}), 404
        return jsonify({'name': res[0], 'student_id': res[1], 'batch_id': res[2], 'semester': res[3], 'cgpa': float(res[4]) if res[4] else 0}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/student/subjects', methods=['GET'])
@token_required
def student_subjects(uid, role):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT s.subject_id, s.name, f.name as fname, f.faculty_id FROM subjects s JOIN faculty f ON s.faculty_id = f.faculty_id WHERE s.batch_id = (SELECT batch_id FROM students WHERE user_id = :1)", (uid,))
        res = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'sid': r[0], 'name': r[1], 'fname': r[2], 'fid': r[3]} for r in (res or [])]), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/student/marks/<sid>', methods=['GET'])
@token_required
def student_marks(uid, role, sid):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE user_id = :1", (uid,))
        stud = cur.fetchone()
        if not stud: return jsonify({'msg': 'Not found'}), 404
        sid_val = stud[0]
        cur.execute("SELECT mst, est, quiz, assignment, total, grade FROM marks WHERE student_id = :1 AND subject_id = :2", (sid_val, sid))
        marks = cur.fetchone()
        cur.execute("SELECT AVG(mst), AVG(est), AVG(quiz), AVG(assignment), AVG(total) FROM marks WHERE subject_id = :1", (sid,))
        avg = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({
            'student_marks': {'mst': float(marks[0]) if marks and marks[0] else None, 'est': float(marks[1]) if marks and marks[1] else None, 'quiz': float(marks[2]) if marks and marks[2] else None, 'assignment': float(marks[3]) if marks and marks[3] else None, 'total': float(marks[4]) if marks and marks[4] else None, 'grade': marks[5] if marks else None},
            'class_avg': {'mst': float(avg[0]) if avg[0] else 0, 'est': float(avg[1]) if avg[1] else 0, 'quiz': float(avg[2]) if avg[2] else 0, 'assignment': float(avg[3]) if avg[3] else 0, 'total': float(avg[4]) if avg[4] else 0}
        }), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/student/attendance/<sid>', methods=['GET'])
@token_required
def student_attendance(uid, role, sid):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE user_id = :1", (uid,))
        stud = cur.fetchone()
        if not stud: return jsonify({'msg': 'Not found'}), 404
        sid_val = stud[0]
        cur.execute("SELECT att_date, status FROM attendance WHERE student_id = :1 AND subject_id = :2 ORDER BY att_date", (sid_val, sid))
        recs = cur.fetchall()
        cur.close()
        conn.close()
        present = sum(1 for r in (recs or []) if r[1] == 'present')
        total = len(recs) if recs else 0
        pct = (present / total * 100) if total > 0 else 0
        return jsonify({'records': [{'date': str(r[0]), 'status': r[1]} for r in (recs or [])], 'percentage': round(pct, 2), 'total': total, 'present': present}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/student/alerts', methods=['GET'])
@token_required
def student_alerts(uid, role):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE user_id = :1", (uid,))
        stud = cur.fetchone()
        if not stud: return jsonify({'msg': 'Not found'}), 404
        sid_val = stud[0]
        cur.execute("SELECT alert_id, message, is_read FROM alerts WHERE student_id = :1 ORDER BY created_at DESC", (sid_val,))
        alts = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': a[0], 'msg': a[1], 'read': bool(a[2])} for a in (alts or [])]), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/student/feedback/<sid>', methods=['GET'])
@token_required
def student_feedback_get(uid, role, sid):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE user_id = :1", (uid,))
        stud = cur.fetchone()
        if not stud: return jsonify({'msg': 'Not found'}), 404
        sid_val = stud[0]
        cur.execute("SELECT DISTINCT f.faculty_id, u.name FROM faculty f JOIN users u ON u.user_id = f.user_id JOIN subjects s ON s.faculty_id = f.faculty_id WHERE s.subject_id = :1", (sid,))
        fac = cur.fetchone()
        if not fac: return jsonify({'msg': 'Faculty not found'}), 404
        cur.execute("SELECT feedback_id, sender_type, message FROM feedback WHERE student_id = :1 AND faculty_id = :2 AND subject_id = :3 ORDER BY sent_at ASC", (sid_val, fac[0], sid))
        msgs = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'faculty_name': fac[1], 'faculty_id': fac[0], 'messages': [{'id': m[0], 'type': m[1], 'text': m[2]} for m in (msgs or [])]}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/student/feedback/send', methods=['POST'])
@token_required
def student_feedback_send(uid, role):
    if role != 'student': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE user_id = :1", (uid,))
        stud = cur.fetchone()[0]
        cur.execute("INSERT INTO feedback (feedback_id, student_id, faculty_id, subject_id, sender_type, message, sent_at) VALUES (feedback_seq.NEXTVAL, :1, :2, :3, 'student', :4, SYSDATE)", (stud, data['fid'], data['sid'], data['msg']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'msg': 'Sent'}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

# ===== FACULTY API =====
@app.route('/api/faculty/info', methods=['GET'])
@token_required
def faculty_info(uid, role):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT u.name, d.name, f.faculty_id FROM users u JOIN faculty f ON u.user_id = f.user_id JOIN departments d ON f.department_id = d.department_id WHERE u.user_id = :1", (uid,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if not res: return jsonify({'msg': 'Not found'}), 404
        return jsonify({'name': res[0], 'dept': res[1], 'fid': res[2]}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/faculty/subjects', methods=['GET'])
@token_required
def faculty_subjects(uid, role):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT faculty_id FROM faculty WHERE user_id = :1", (uid,))
        fac = cur.fetchone()
        if not fac: return jsonify({'msg': 'Not found'}), 404
        cur.execute("SELECT subject_id, name FROM subjects WHERE faculty_id = :1", (fac[0],))
        res = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'sid': r[0], 'name': r[1]} for r in (res or [])]), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/faculty/batches', methods=['GET'])
@token_required
def faculty_batches(uid, role):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT b.batch_id, b.name FROM batches b JOIN subjects s ON s.batch_id = b.batch_id JOIN faculty f ON s.faculty_id = f.faculty_id WHERE f.user_id = :1", (uid,))
        res = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'bid': r[0], 'name': r[1]} for r in (res or [])]), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/faculty/students/<bid>', methods=['GET'])
@token_required
def faculty_students(uid, role, bid):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT s.student_id, u.name FROM students s JOIN users u ON u.user_id = s.user_id WHERE s.batch_id = :1", (bid,))
        res = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'stud_id': r[0], 'name': r[1]} for r in (res or [])]), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/faculty/update_marks', methods=['POST'])
@token_required
def faculty_update_marks(uid, role):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        data = request.get_json()
        mst, est, quiz, assignment = data.get('mst'), data.get('est'), data.get('quiz'), data.get('assignment')
        total = (mst + est + quiz + assignment) / 4 if all([mst, est, quiz, assignment]) else None
        grade = None
        if total:
            if total >= 90: grade = 'A'
            elif total >= 80: grade = 'B'
            elif total >= 70: grade = 'C'
            elif total >= 60: grade = 'D'
            else: grade = 'F'
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT mark_id FROM marks WHERE student_id = :1 AND subject_id = :2", (data['stud_id'], data['sid']))
        existing = cur.fetchone()
        if existing:
            cur.execute("UPDATE marks SET mst = :1, est = :2, quiz = :3, assignment = :4, total = :5, grade = :6 WHERE student_id = :7 AND subject_id = :8", (mst, est, quiz, assignment, total, grade, data['stud_id'], data['sid']))
        else:
            cur.execute("INSERT INTO marks (mark_id, student_id, subject_id, mst, est, quiz, assignment, total, grade) VALUES (marks_seq.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8)", (data['stud_id'], data['sid'], mst, est, quiz, assignment, total, grade))
        cur.execute("SELECT AVG(total) FROM marks WHERE student_id = :1", (data['stud_id'],))
        avg = cur.fetchone()[0]
        new_cgpa = avg / 10 if avg else 0
        cur.execute("UPDATE students SET cgpa = ROUND(:1, 2) WHERE student_id = :2", (new_cgpa, data['stud_id']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'msg': 'Updated'}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/faculty/update_attendance', methods=['POST'])
@token_required
def faculty_update_attendance(uid, role):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT attendance_id FROM attendance WHERE student_id = :1 AND subject_id = :2 AND TRUNC(att_date) = TRUNC(SYSDATE)", (data['stud_id'], data['sid']))
        existing = cur.fetchone()
        if existing:
            cur.execute("UPDATE attendance SET status = :1 WHERE student_id = :2 AND subject_id = :3 AND TRUNC(att_date) = TRUNC(SYSDATE)", (data['status'], data['stud_id'], data['sid']))
        else:
            cur.execute("INSERT INTO attendance (attendance_id, student_id, subject_id, att_date, status) VALUES (attendance_seq.NEXTVAL, :1, :2, SYSDATE, :3)", (data['stud_id'], data['sid'], data['status']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'msg': 'Updated'}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@app.route('/api/faculty/feedback/send', methods=['POST'])
@token_required
def faculty_feedback_send(uid, role):
    if role != 'faculty': return jsonify({'msg': 'Unauthorized'}), 403
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT faculty_id FROM faculty WHERE user_id = :1", (uid,))
        fac_id = cur.fetchone()[0]
        cur.execute("INSERT INTO feedback (feedback_id, student_id, faculty_id, subject_id, sender_type, message, sent_at) VALUES (feedback_seq.NEXTVAL, :1, :2, :3, 'faculty', :4, SYSDATE)", (data['stud_id'], fac_id, data['sid'], data['msg']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'msg': 'Sent'}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
