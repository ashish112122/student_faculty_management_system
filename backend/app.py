from flask import Flask, request, jsonify
from flask_cors import CORS
import oracledb
import jwt
import datetime
from functools import wraps
from config import Config

app = Flask(__name__)
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

# STUDENT APIs
@app.route('/api/student/dashboard', methods=['GET'])
@token_required
def student_dashboard():
    if request.role != 'student':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.student_id, s.name, s.branch, s.year_of_study, s.semester, s.section, s.cgpa, s.class_name
            FROM students s
            WHERE s.user_id = :user_id
        """, {'user_id': request.user_id})
        
        student = cursor.fetchone()
        
        if not student:
            return jsonify({'message': 'Student not found'}), 404
        
        student_id, name, branch, year, semester, section, cgpa, class_name = student
        
        cursor.execute("""
            SELECT DISTINCT s.subject_id, s.subject_name, s.subject_code
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            WHERE m.student_id = :student_id
            ORDER BY s.subject_name
        """, {'student_id': student_id})
        
        subjects = [{'subject_id': row[0], 'subject_name': row[1], 'subject_code': row[2]} for row in cursor.fetchall()]
        total_credits = len(subjects) * 4
        
        # Get marks with detailed breakdown
        cursor.execute("""
            SELECT s.subject_id, s.subject_name, s.subject_code, 
                   f.name as faculty_name,
                   MAX(CASE WHEN m.assessment_type = 'MST' THEN m.marks_obtained END) as mid,
                   MAX(CASE WHEN m.assessment_type = 'MST' THEN m.max_marks END) as mid_max,
                   MAX(CASE WHEN m.assessment_type = 'EST' THEN m.marks_obtained END) as final,
                   MAX(CASE WHEN m.assessment_type = 'EST' THEN m.max_marks END) as final_max,
                   MAX(CASE WHEN m.assessment_type = 'Quiz' THEN m.marks_obtained END) as quiz,
                   MAX(CASE WHEN m.assessment_type = 'Quiz' THEN m.max_marks END) as quiz_max,
                   MAX(CASE WHEN m.assessment_type = 'Assignment' THEN m.marks_obtained END) as assignment,
                   MAX(CASE WHEN m.assessment_type = 'Assignment' THEN m.max_marks END) as assignment_max
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            LEFT JOIN faculty_classes fc ON fc.subject_id = s.subject_id AND fc.class_name = m.class_name
            LEFT JOIN faculty f ON f.faculty_id = fc.faculty_id
            WHERE m.student_id = :student_id
            GROUP BY s.subject_id, s.subject_name, s.subject_code, f.name
            ORDER BY s.subject_name
        """, {'student_id': student_id})
        
        marks = []
        for row in cursor.fetchall():
            mid = float(row[4]) if row[4] else 0
            mid_max = float(row[5]) if row[5] else 50
            final = float(row[6]) if row[6] else 0
            final_max = float(row[7]) if row[7] else 100
            quiz = float(row[8]) if row[8] else 0
            quiz_max = float(row[9]) if row[9] else 10
            assignment = float(row[10]) if row[10] else 0
            assignment_max = float(row[11]) if row[11] else 20
            
            total = mid + final + quiz + assignment
            total_max = mid_max + final_max + quiz_max + assignment_max
            percentage = round((total / total_max) * 100, 2) if total_max > 0 else 0
            grade = 'A+' if percentage >= 90 else 'A' if percentage >= 80 else 'B+' if percentage >= 70 else 'B' if percentage >= 60 else 'C' if percentage >= 50 else 'F'
            
            marks.append({
                'subject_id': row[0],
                'subject': row[1],
                'subject_code': row[2],
                'faculty': row[3] or 'N/A',
                'mid': mid,
                'final': final,
                'quiz': quiz,
                'assignment': assignment,
                'total': total,
                'grade': grade
            })
        
        # Get class averages
        cursor.execute("""
            SELECT s.subject_id, s.subject_name,
                   AVG(CASE WHEN m.assessment_type = 'MST' THEN m.marks_obtained END) as mid_avg,
                   AVG(CASE WHEN m.assessment_type = 'EST' THEN m.marks_obtained END) as final_avg,
                   AVG(CASE WHEN m.assessment_type = 'Quiz' THEN m.marks_obtained END) as quiz_avg,
                   AVG(CASE WHEN m.assessment_type = 'Assignment' THEN m.marks_obtained END) as assignment_avg
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            WHERE s.subject_id IN (
                SELECT DISTINCT subject_id FROM marks WHERE student_id = :student_id
            )
            GROUP BY s.subject_id, s.subject_name
            ORDER BY s.subject_name
        """, {'student_id': student_id})
        
        class_average = []
        for row in cursor.fetchall():
            class_average.append({
                'subject_id': row[0],
                'subject': row[1],
                'mid': round(float(row[2]), 2) if row[2] else 0,
                'final': round(float(row[3]), 2) if row[3] else 0,
                'quiz': round(float(row[4]), 2) if row[4] else 0,
                'assignment': round(float(row[5]), 2) if row[5] else 0
            })
        
        # Get attendance
        cursor.execute("""
            SELECT s.subject_name, s.subject_code,
                   COUNT(*) as total,
                   SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.subject_id
            WHERE a.student_id = :student_id
            GROUP BY s.subject_name, s.subject_code
            ORDER BY s.subject_name
        """, {'student_id': student_id})
        
        attendance = []
        for row in cursor.fetchall():
            total = row[2] if row[2] else 0
            present = row[3] if row[3] else 0
            percentage = round((present / total) * 100, 2) if total > 0 else 0
            
            attendance.append({
                'subject': row[0],
                'total_classes': total,
                'present': present,
                'percentage': percentage
            })
        
        # Get alerts
        cursor.execute("""
            SELECT alert_type, message, created_at
            FROM alerts
            WHERE student_id = :student_id
            ORDER BY created_at DESC
        """, {'student_id': student_id})
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'type': row[0],
                'message': row[1],
                'is_read': False
            })
        
        return jsonify({
            'student_id': student_id,
            'name': name,
            'semester': semester,
            'cgpa': float(cgpa),
            'total_credits': total_credits,
            'branch': branch,
            'class_name': class_name,
            'marks': marks,
            'class_average': class_average,
            'attendance': attendance,
            'alerts': alerts
        })
    finally:
        cursor.close()
        conn.close()

# FACULTY APIs
@app.route('/api/faculty/dashboard', methods=['GET'])
@token_required
def faculty_dashboard():
    if request.role != 'faculty':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT f.faculty_id, f.name, f.department
            FROM faculty f
            WHERE f.user_id = :user_id
        """, {'user_id': request.user_id})
        
        faculty = cursor.fetchone()
        if not faculty:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id, name, department = faculty
        
        cursor.execute("""
            SELECT DISTINCT s.subject_id, s.subject_name, s.subject_code, fc.class_name
            FROM faculty_classes fc
            JOIN subjects s ON fc.subject_id = s.subject_id
            WHERE fc.faculty_id = :faculty_id
            ORDER BY s.subject_name, fc.class_name
        """, {'faculty_id': faculty_id})
        
        subjects = []
        for row in cursor.fetchall():
            subjects.append({
                'subject_id': row[0],
                'subject_name': row[1],
                'subject_code': row[2],
                'class_name': row[3]
            })
        
        return jsonify({
            'faculty_id': faculty_id,
            'name': name,
            'department': department,
            'subjects': subjects
        })
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/marks/<int:subject_id>/<class_name>', methods=['GET'])
@token_required
def get_faculty_marks(subject_id, class_name):
    if request.role != 'faculty':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.student_id, s.name,
                   MAX(CASE WHEN m.assessment_type = 'MST' THEN m.marks_obtained END) as mid,
                   MAX(CASE WHEN m.assessment_type = 'EST' THEN m.marks_obtained END) as final,
                   MAX(CASE WHEN m.assessment_type = 'Quiz' THEN m.marks_obtained END) as quiz,
                   MAX(CASE WHEN m.assessment_type = 'Assignment' THEN m.marks_obtained END) as assignment
            FROM students s
            LEFT JOIN marks m ON s.student_id = m.student_id AND m.subject_id = :subject_id
            WHERE s.class_name = :class_name
            GROUP BY s.student_id, s.name
            ORDER BY s.name
        """, {'subject_id': subject_id, 'class_name': class_name})
        
        students = []
        for row in cursor.fetchall():
            mid = float(row[2]) if row[2] else 0
            final = float(row[3]) if row[3] else 0
            quiz = float(row[4]) if row[4] else 0
            assignment = float(row[5]) if row[5] else 0
            total = mid + final + quiz + assignment
            
            students.append({
                'student_id': row[0],
                'name': row[1],
                'mid': mid,
                'final': final,
                'quiz': quiz,
                'assignment': assignment,
                'total': total
            })
        
        return jsonify(students)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/add_marks', methods=['POST'])
@token_required
def add_marks():
    if request.role != 'faculty':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        class_name = data.get('class_name')
        marks_data = data.get('marks')
        
        cursor.execute("""
            DELETE FROM marks 
            WHERE student_id = :student_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'subject_id': subject_id})
        
        assessment_map = {
            'mid': ('MST', 50),
            'final': ('EST', 100),
            'quiz': ('Quiz', 10),
            'assignment': ('Assignment', 20)
        }
        
        for key, (assessment_type, max_marks) in assessment_map.items():
            if key in marks_data and marks_data[key] is not None and marks_data[key] != '':
                cursor.execute("""
                    INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
                    VALUES (marks_seq.NEXTVAL, :student_id, :subject_id, :class_name, :assessment_type, :marks_obtained, :max_marks)
                """, {
                    'student_id': student_id,
                    'subject_id': subject_id,
                    'class_name': class_name,
                    'assessment_type': assessment_type,
                    'marks_obtained': float(marks_data[key]),
                    'max_marks': max_marks
                })
        
        conn.commit()
        return jsonify({'message': 'Marks updated successfully'})
    except Exception as e:
        conn.rollback()
        print(f"Error adding marks: {str(e)}")
        return jsonify({'message': f'Error updating marks: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/marks_report/<int:subject_id>/<class_name>', methods=['GET'])
@token_required
def get_marks_report(subject_id, class_name):
    if request.role != 'faculty':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                AVG(CASE WHEN assessment_type = 'MST' THEN marks_obtained END) as mid_avg,
                AVG(CASE WHEN assessment_type = 'EST' THEN marks_obtained END) as final_avg,
                AVG(CASE WHEN assessment_type = 'Quiz' THEN marks_obtained END) as quiz_avg,
                AVG(CASE WHEN assessment_type = 'Assignment' THEN marks_obtained END) as assignment_avg
            FROM marks
            WHERE subject_id = :subject_id AND class_name = :class_name
        """, {'subject_id': subject_id, 'class_name': class_name})
        
        avg_row = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN percentage >= 90 THEN 'A+'
                    WHEN percentage >= 80 THEN 'A'
                    WHEN percentage >= 70 THEN 'B+'
                    WHEN percentage >= 60 THEN 'B'
                    WHEN percentage >= 50 THEN 'C'
                    ELSE 'F'
                END as grade,
                COUNT(*) as count
            FROM (
                SELECT student_id,
                    (SUM(marks_obtained) / SUM(max_marks)) * 100 as percentage
                FROM marks
                WHERE subject_id = :subject_id AND class_name = :class_name
                GROUP BY student_id
            )
            GROUP BY 
                CASE 
                    WHEN percentage >= 90 THEN 'A+'
                    WHEN percentage >= 80 THEN 'A'
                    WHEN percentage >= 70 THEN 'B+'
                    WHEN percentage >= 60 THEN 'B'
                    WHEN percentage >= 50 THEN 'C'
                    ELSE 'F'
                END
            ORDER BY grade
        """, {'subject_id': subject_id, 'class_name': class_name})
        
        grade_distribution = []
        for row in cursor.fetchall():
            grade_distribution.append({
                'grade': row[0],
                'count': row[1]
            })
        
        return jsonify({
            'class_average': {
                'mid': round(float(avg_row[0]), 2) if avg_row[0] else 0,
                'final': round(float(avg_row[1]), 2) if avg_row[1] else 0,
                'quiz': round(float(avg_row[2]), 2) if avg_row[2] else 0,
                'assignment': round(float(avg_row[3]), 2) if avg_row[3] else 0
            },
            'grade_distribution': grade_distribution
        })
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
