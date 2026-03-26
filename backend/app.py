from flask import Flask, request, jsonify
from flask_cors import CORS
import oracledb
import jwt
import datetime
from functools import wraps
import os
from config import Config

app = Flask(__name__)

# Enable CORS for all routes - simple and permissive for development
CORS(app)

app.config['SECRET_KEY'] = Config.SECRET_KEY

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

@app.route('/')
def home():
    return "Backend running successfully"

def get_db_connection():
    return oracledb.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data['user_id']
            request.role = data['role']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    
    return decorated
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT user_id, name, role, password
                FROM users
                WHERE email = :email
            """, {'email': email})
            
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'message': 'Invalid email or password'}), 401
            
            user_id, name, role, stored_password = user
            
            if password != stored_password:
                return jsonify({'message': 'Invalid email or password'}), 401
            
            token = jwt.encode({
                'user_id': user_id,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user_id': user_id,
                'name': name,
                'role': role,
                'message': 'Login successful'
            })
        
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Server error occurred'}), 500
@app.route('/api/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({'message': 'Logged out successfully'})
@app.route('/api/student/dashboard', methods=['GET'])
@token_required
def student_dashboard():
    if request.role != 'student':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT name, branch, year_of_study, semester, section, cgpa
            FROM students
            WHERE user_id = :user_id
        """, {'user_id': request.user_id})
        
        student = cursor.fetchone()
        
        cursor.execute("""
            SELECT s.subject_name
            FROM student_subjects ss
            JOIN subjects s ON ss.subject_id = s.subject_id
            WHERE ss.student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
        """, {'user_id': request.user_id})
        
        subjects = [row[0] for row in cursor.fetchall()]
        
        return jsonify({
            'name': student[0],
            'branch': student[1],
            'year': student[2],
            'semester': student[3],
            'section': student[4],
            'cgpa': float(student[5]),
            'subjects': subjects
        })
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/subjects', methods=['GET'])
@token_required
def get_student_subjects():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.subject_id, s.subject_name, s.subject_code
            FROM student_subjects ss
            JOIN subjects s ON ss.subject_id = s.subject_id
            WHERE ss.student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
            ORDER BY s.subject_id
        """, {'user_id': request.user_id})
        
        subjects = [{'subject_id': row[0], 'subject_name': row[1], 'subject_code': row[2]} for row in cursor.fetchall()]
        return jsonify(subjects)
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/marks', methods=['GET'])
@token_required
def get_student_marks():
    subject_id = request.args.get('subject_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT m.assessment_type, m.marks_obtained, m.max_marks,
                   (SELECT AVG(marks_obtained) FROM marks WHERE subject_id = m.subject_id 
                    AND assessment_type = m.assessment_type) as class_avg
            FROM marks m
            WHERE m.student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
            AND m.subject_id = :subject_id
        """, {'user_id': request.user_id, 'subject_id': subject_id})
        
        marks = []
        for row in cursor.fetchall():
            marks.append({
                'assessment_type': row[0],
                'marks_obtained': float(row[1]),
                'max_marks': float(row[2]),
                'class_average': round(float(row[3]), 2)
            })
        
        # Return empty array if no marks (faculty hasn't uploaded yet)
        return jsonify(marks)
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/attendance', methods=['GET'])
@token_required
def get_student_attendance():
    subject_id = request.args.get('subject_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT attendance_date, status
            FROM attendance
            WHERE student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
            AND subject_id = :subject_id
            ORDER BY attendance_date DESC
        """, {'user_id': request.user_id, 'subject_id': subject_id})
        
        records = []
        present_count = 0
        total_count = 0
        
        for row in cursor.fetchall():
            status = 'Present' if row[1] == 'P' else 'Absent'
            records.append({
                'date': row[0].strftime('%Y-%m-%d'),
                'status': status
            })
            total_count += 1
            if row[1] == 'P':
                present_count += 1
        
        percentage = round((present_count / total_count * 100), 2) if total_count > 0 else 0
        
        # Return empty state if no attendance records
        return jsonify({
            'percentage': percentage,
            'records': records
        })
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/alerts', methods=['GET'])
@token_required
def get_student_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT alert_type, message, created_at
            FROM alerts
            WHERE student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
            ORDER BY created_at DESC
        """, {'user_id': request.user_id})
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'alert_type': row[0],
                'message': row[1],
                'created_at': row[2].strftime('%Y-%m-%d %H:%M')
            })
        
        return jsonify(alerts)
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/faculty', methods=['GET'])
@token_required
def get_faculty_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT u.user_id, u.name
            FROM users u
            WHERE u.role = 'faculty'
            ORDER BY u.name
        """)
        
        faculty = [{'user_id': row[0], 'name': row[1]} for row in cursor.fetchall()]
        return jsonify(faculty)
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/feedback', methods=['GET', 'POST'])
@token_required
def feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            subject_id = request.args.get('subject_id')
            
            cursor.execute("""
                SELECT f.message, f.created_at, u.name, u.role
                FROM feedback f
                JOIN users u ON f.sender_id = u.user_id
                WHERE f.student_id = (SELECT student_id FROM students WHERE user_id = :user_id)
                AND f.subject_id = :subject_id
                ORDER BY f.created_at ASC
            """, {'user_id': request.user_id, 'subject_id': subject_id})
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'message': row[0],
                    'created_at': row[1].strftime('%Y-%m-%d %H:%M'),
                    'sender_name': row[2],
                    'sender_role': row[3]
                })
            
            return jsonify(messages)
        
        else:
            data = request.get_json()
            subject_id = data.get('subject_id')
            message = data.get('message')
            
            cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", 
                         {'user_id': request.user_id})
            student_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO feedback (student_id, subject_id, sender_id, message, created_at)
                VALUES (:student_id, :subject_id, :sender_id, :message, SYSDATE)
            """, {
                'student_id': student_id,
                'subject_id': subject_id,
                'sender_id': request.user_id,
                'message': message
            })
            
            conn.commit()
            return jsonify({'message': 'Message sent successfully'})
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)