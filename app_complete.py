from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import oracledb
import bcrypt
import jwt
import datetime
from functools import wraps
from datetime import timedelta

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
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    name = data['name']
    role = data['role']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, :1, :2, :3, :4)", (email, password, name, role))
        if role == 'student':
            cursor.execute("INSERT INTO students (student_id, user_id, department_id, semester) VALUES (students_seq.NEXTVAL, users_seq.CURRVAL, :1, 1)", (data['department_id'],))
        elif role == 'faculty':
            cursor.execute("INSERT INTO faculty (faculty_id, user_id, department_id) VALUES (faculty_seq.NEXTVAL, users_seq.CURRVAL, :1)", (data['department_id'],))
        conn.commit()
        return jsonify({'message': 'User registered'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id, password, role FROM users WHERE email = :1", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")
            return jsonify({'token': token, 'role': user[2]})
        return jsonify({'message': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logged out'})

@app.route('/student/dashboard', methods=['GET'])
@token_required
def student_dashboard(current_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT semester, cgpa, total_credits FROM students WHERE user_id = :1", (current_user,))
        student = cursor.fetchone()
        cursor.execute("SELECT s.name, m.marks, m.grade FROM marks m JOIN subjects s ON m.subject_id = s.subject_id WHERE m.student_id = (SELECT student_id FROM students WHERE user_id = :1)", (current_user,))
        marks = cursor.fetchall()
        cursor.execute("SELECT s.name, ROUND(COUNT(CASE WHEN a.status = 'present' THEN 1 END) * 100.0 / COUNT(*), 2) as percentage FROM attendance a JOIN subjects s ON a.subject_id = s.subject_id WHERE a.student_id = (SELECT student_id FROM students WHERE user_id = :1) GROUP BY s.name", (current_user,))
        attendance = cursor.fetchall()
        cursor.execute("SELECT message, is_read FROM alerts WHERE student_id = (SELECT student_id FROM students WHERE user_id = :1) ORDER BY created_at DESC", (current_user,))
        alerts = cursor.fetchall()
        return jsonify({'semester': student[0], 'cgpa': student[1], 'credits': student[2], 'marks': marks, 'attendance': attendance, 'alerts': alerts})
    finally:
        cursor.close()
        conn.close()

@app.route('/faculty/dashboard', methods=['GET'])
@token_required
def faculty_dashboard(current_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT d.name FROM departments d JOIN faculty f ON d.department_id = f.department_id WHERE f.user_id = :1", (current_user,))
        dept = cursor.fetchone()
        cursor.execute("SELECT name FROM subjects WHERE faculty_id = (SELECT faculty_id FROM faculty WHERE user_id = :1)", (current_user,))
        subjects = cursor.fetchall()
        return jsonify({'department': dept[0], 'subjects': subjects})
    finally:
        cursor.close()
        conn.close()

@app.route('/faculty/add_marks', methods=['POST'])
@token_required
def add_marks(current_user):
    data = request.get_json()
    student_id = data['student_id']
    subject_id = data['subject_id']
    marks = data['marks']
    grade = calculate_grade(marks)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO marks (mark_id, student_id, subject_id, marks, grade) VALUES (marks_seq.NEXTVAL, :1, :2, :3, :4)", (student_id, subject_id, marks, grade))
        # Update CGPA
        update_cgpa(student_id)
        # Alert student
        cursor.execute("INSERT INTO alerts (alert_id, student_id, message) VALUES (alerts_seq.NEXTVAL, :1, 'Your marks have been updated')", (student_id,))
        conn.commit()
        return jsonify({'message': 'Marks added'})
    finally:
        cursor.close()
        conn.close()

def calculate_grade(marks):
    if marks >= 90: return 'A'
    elif marks >= 80: return 'B'
    elif marks >= 70: return 'C'
    elif marks >= 60: return 'D'
    else: return 'F'

def update_cgpa(student_id):
    # Simple CGPA calculation
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT AVG(marks) FROM marks WHERE student_id = :1", (student_id,))
        avg = cursor.fetchone()[0]
        cgpa = avg / 10  # Assuming 100 scale to 10
        cursor.execute("UPDATE students SET cgpa = :1 WHERE student_id = :2", (cgpa, student_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Add more routes for attendance, reports, feedback, alerts

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)