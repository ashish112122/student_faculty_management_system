from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import oracledb
import jwt
import datetime
import os
from functools import wraps
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'uploads/feedback_attachments'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
    def debug_log(message):
        print(message)
        try:
            with open(os.path.join('backend', 'login_debug.log'), 'a', encoding='utf-8') as log_file:
                log_file.write(message + '\n')
        except Exception:
            pass

    try:
        data = request.get_json(silent=True)
        if data is None:
            data = request.form.to_dict() if request.form else {}

        debug_log(f'Login route called with data: {data}')

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            print('Login validation failed: missing email or password')
            return jsonify({'message': 'Email and password required'}), 400

        print('Connecting to database for login:', email)
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

            if isinstance(token, bytes):
                token = token.decode('utf-8')

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
        import traceback
        traceback.print_exc()
        app.logger.error('Login error: %s', e)
        try:
            with open(os.path.join('backend', 'login_debug.log'), 'a', encoding='utf-8') as log_file:
                log_file.write('Login exception: ' + str(e) + '\n')
                log_file.write(traceback.format_exc() + '\n')
        except Exception:
            pass
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
            SELECT s.student_id, s.name, s.branch, s.semester, s.class_name, s.cgpa, s.roll_number
            FROM students s
            WHERE s.user_id = :user_id
        """, {'user_id': request.user_id})
        
        student = cursor.fetchone()
        
        if not student:
            return jsonify({'message': 'Student not found'}), 404
        
        student_id, name, branch, semester, class_name, cgpa, roll_number = student
        
        cursor.execute("""
            SELECT DISTINCT s.subject_id, s.subject_name, s.subject_code, f.name as faculty_name, f.faculty_code
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN faculty_classes fc ON fc.subject_id = s.subject_id AND fc.class_name = m.class_name
            JOIN faculty f ON f.faculty_id = fc.faculty_id
            WHERE m.student_id = :student_id
            ORDER BY s.subject_name
        """, {'student_id': student_id})
        
        subjects = [{'subject_id': row[0], 'subject_name': row[1], 'subject_code': row[2], 'faculty_name': row[3], 'faculty_code': row[4]} for row in cursor.fetchall()]
        total_credits = len(subjects) * 4
        
        return jsonify({
            'student_id': student_id,
            'name': name,
            'semester': semester,
            'cgpa': float(cgpa),
            'total_credits': total_credits,
            'branch': branch,
            'class_name': class_name,
            'roll_number': roll_number,
            'subjects': subjects
        })
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/marks/<int:subject_id>', methods=['GET'])
@token_required
def get_student_subject_marks(subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({})
        
        student_id = result[0]
        
        cursor.execute("""
            SELECT assessment_type, marks_obtained, max_marks
            FROM marks
            WHERE student_id = :student_id AND subject_id = :subject_id
            ORDER BY assessment_type
        """, {'student_id': student_id, 'subject_id': subject_id})
        
        marks = {}
        for row in cursor.fetchall():
            marks[row[0]] = {'obtained': float(row[1]), 'max': float(row[2])}
        
        # Get class average
        cursor.execute("""
            SELECT assessment_type, AVG(marks_obtained) as avg_marks
            FROM marks
            WHERE subject_id = :subject_id
            GROUP BY assessment_type
        """, {'subject_id': subject_id})
        
        class_avg = {}
        for row in cursor.fetchall():
            class_avg[row[0]] = round(float(row[1]), 2)
        
        return jsonify({'marks': marks, 'class_average': class_avg})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/attendance/<int:subject_id>', methods=['GET'])
@token_required
def get_student_subject_attendance(subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        student_id = result[0]
        
        cursor.execute("""
            SELECT attendance_date, status
            FROM attendance
            WHERE student_id = :student_id AND subject_id = :subject_id
            ORDER BY attendance_date ASC
        """, {'student_id': student_id, 'subject_id': subject_id})
        
        records = []
        present = 0
        total = 0
        
        for row in cursor.fetchall():
            records.append({
                'date': row[0].strftime('%Y-%m-%d'),
                'status': 'Present' if row[1] == 'P' else 'Absent'
            })
            total += 1
            if row[1] == 'P':
                present += 1
        
        percentage = round((present / total) * 100, 2) if total > 0 else 0
        
        return jsonify({
            'records': records,
            'present': present,
            'total': total,
            'percentage': percentage
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
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        student_id = result[0]
        
        cursor.execute("""
            SELECT alert_id, alert_type, message, is_read, created_at
            FROM alerts
            WHERE student_id = :student_id
            ORDER BY created_at DESC
        """, {'student_id': student_id})
        
        alerts = []
        for row in cursor.fetchall():
            # Format timestamp as "03 Apr 2026 — 10:45 AM"
            created_at = row[4]
            formatted_time = created_at.strftime('%d %b %Y — %I:%M %p')
            
            alerts.append({
                'alert_id': row[0],
                'type': row[1],
                'message': row[2],
                'is_read': row[3],
                'created_at': formatted_time
            })
        
        return jsonify(alerts)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/alerts/mark_read/<int:alert_id>', methods=['POST'])
@token_required
def mark_alert_read(alert_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE alerts SET is_read = 1 WHERE alert_id = :alert_id", {'alert_id': alert_id})
        conn.commit()
        return jsonify({'message': 'Alert marked as read'})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/feedback/subjects', methods=['GET'])
@token_required
def get_student_feedback_subjects():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        student_id = result[0]
        
        cursor.execute("""
            SELECT DISTINCT s.subject_id, s.subject_name, s.subject_code, f.faculty_id, f.name as faculty_name, f.faculty_code
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN faculty_classes fc ON fc.subject_id = s.subject_id AND fc.class_name = m.class_name
            JOIN faculty f ON f.faculty_id = fc.faculty_id
            WHERE m.student_id = :student_id
            ORDER BY s.subject_name
        """, {'student_id': student_id})
        
        subjects = []
        for row in cursor.fetchall():
            subjects.append({
                'subject_id': row[0],
                'subject_name': row[1],
                'subject_code': row[2],
                'faculty_id': row[3],
                'faculty_name': row[4],
                'faculty_code': row[5]
            })
        
        return jsonify(subjects)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/feedback/<int:faculty_id>/<int:subject_id>', methods=['GET'])
@token_required
def get_student_feedback_thread(faculty_id, subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        student_id = result[0]
        
        # Get thread with clear timestamps
        cursor.execute("""
            SELECT thread_id, cleared_by_student, cleared_by_faculty
            FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if not thread:
            return jsonify([])
        
        thread_id = thread[0]
        cleared_by_student = thread[1]
        
        # Get messages created after student cleared chat (or all if never cleared)
        if cleared_by_student:
            cursor.execute("""
                SELECT message_id, sender_role, message, is_read, created_at, 
                       attachment_path, attachment_name, attachment_type
                FROM feedback_messages
                WHERE thread_id = :thread_id AND created_at > :cleared_time
                ORDER BY created_at ASC
            """, {'thread_id': thread_id, 'cleared_time': cleared_by_student})
        else:
            cursor.execute("""
                SELECT message_id, sender_role, message, is_read, created_at, 
                       attachment_path, attachment_name, attachment_type
                FROM feedback_messages
                WHERE thread_id = :thread_id
                ORDER BY created_at ASC
            """, {'thread_id': thread_id})
        
        messages = []
        for row in cursor.fetchall():
            message_text = row[2].read() if hasattr(row[2], 'read') else str(row[2])
            messages.append({
                'feedback_id': row[0],
                'sender_role': row[1],
                'message': message_text,
                'is_read': row[3],
                'created_at': row[4].strftime('%Y-%m-%d %H:%M'),
                'attachment_name': row[6],
                'attachment_type': row[7],
                'has_attachment': row[6] is not None
            })
        
        # Mark as read
        cursor.execute("""
            UPDATE feedback_messages SET is_read = 1
            WHERE thread_id = :thread_id AND sender_role = 'faculty' AND is_read = 0
        """, {'thread_id': thread_id})
        conn.commit()
        
        return jsonify(messages)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/student/feedback/send', methods=['POST'])
@token_required
def send_student_feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if request has file
        if 'attachment' in request.files:
            file = request.files['attachment']
            faculty_id = int(request.form.get('faculty_id'))
            subject_id = int(request.form.get('subject_id'))
            message = request.form.get('message', '').strip()
            
            # If no message but has attachment, use default message
            if not message and file and file.filename:
                message = '[Attachment]'
            
            attachment_path = None
            attachment_name = None
            attachment_type = None
            
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                attachment_path = filepath
                attachment_name = filename
                attachment_type = filename.rsplit('.', 1)[1].lower()
        else:
            data = request.get_json()
            faculty_id = data.get('faculty_id')
            subject_id = data.get('subject_id')
            message = data.get('message', '').strip()
            attachment_path = None
            attachment_name = None
            attachment_type = None
        
        # Ensure message is not empty or None
        if not message:
            message = '[No message]'
        
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Student not found'}), 404
        
        student_id = result[0]
        
        # Get or create thread
        cursor.execute("""
            SELECT thread_id FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if thread:
            thread_id = thread[0]
        else:
            # Create new thread
            cursor.execute("""
                INSERT INTO feedback_threads (thread_id, student_id, faculty_id, subject_id, initiated_by, created_at, last_message_at)
                VALUES (feedback_threads_seq.NEXTVAL, :student_id, :faculty_id, :subject_id, 'student', SYSDATE, SYSDATE)
            """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
            cursor.execute("SELECT feedback_threads_seq.CURRVAL FROM dual")
            thread_id = cursor.fetchone()[0]
        
        # Insert message
        cursor.execute("""
            INSERT INTO feedback_messages (message_id, thread_id, sender_id, sender_role, message, is_read, created_at,
                                          attachment_path, attachment_name, attachment_type)
            VALUES (feedback_messages_seq.NEXTVAL, :thread_id, :sender_id, 'student', :message, 0, SYSDATE,
                   :attachment_path, :attachment_name, :attachment_type)
        """, {
            'thread_id': thread_id,
            'sender_id': request.user_id,
            'message': message,
            'attachment_path': attachment_path,
            'attachment_name': attachment_name,
            'attachment_type': attachment_type
        })
        
        # Update thread
        cursor.execute("""
            UPDATE feedback_threads SET last_message_at = SYSDATE WHERE thread_id = :thread_id
        """, {'thread_id': thread_id})
        
        conn.commit()
        return jsonify({'message': 'Message sent successfully'})
    except Exception as e:
        conn.rollback()
        print(f"Error sending feedback: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error sending message: {str(e)}'}), 500
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
            SELECT f.faculty_id, f.name, f.department, f.faculty_code
            FROM faculty f
            WHERE f.user_id = :user_id
        """, {'user_id': request.user_id})
        
        faculty = cursor.fetchone()
        if not faculty:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id, name, department, faculty_code = faculty
        
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
        
        # Get unread feedback count
        cursor.execute("""
            SELECT COUNT(*)
            FROM feedback_messages fm
            JOIN feedback_threads ft ON fm.thread_id = ft.thread_id
            WHERE ft.faculty_id = :faculty_id 
            AND fm.sender_role = 'student' 
            AND fm.is_read = 0
        """, {'faculty_id': faculty_id})
        
        unread_count = cursor.fetchone()[0]
        
        return jsonify({
            'faculty_id': faculty_id,
            'name': name,
            'department': department,
            'faculty_code': faculty_code,
            'subjects': subjects,
            'unread_feedback_count': unread_count
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
        # Verify faculty is assigned to this subject and class
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id = result[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM faculty_classes 
            WHERE faculty_id = :faculty_id AND subject_id = :subject_id AND class_name = :class_name
        """, {'faculty_id': faculty_id, 'subject_id': subject_id, 'class_name': class_name})
        
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'You are not assigned to this subject and class'}), 403
        
        cursor.execute("""
            SELECT s.student_id, s.name, s.roll_number,
                   MAX(CASE WHEN m.assessment_type = 'MST' THEN m.marks_obtained END) as mid,
                   MAX(CASE WHEN m.assessment_type = 'EST' THEN m.marks_obtained END) as final,
                   MAX(CASE WHEN m.assessment_type = 'Quiz' THEN m.marks_obtained END) as quiz,
                   MAX(CASE WHEN m.assessment_type = 'Assignment' THEN m.marks_obtained END) as assignment
            FROM students s
            LEFT JOIN marks m ON s.student_id = m.student_id AND m.subject_id = :subject_id
            WHERE s.class_name = :class_name
            GROUP BY s.student_id, s.name, s.roll_number
            ORDER BY s.roll_number
        """, {'subject_id': subject_id, 'class_name': class_name})
        
        students = []
        for row in cursor.fetchall():
            mid = float(row[3]) if row[3] else 0
            final = float(row[4]) if row[4] else 0
            quiz = float(row[5]) if row[5] else 0
            assignment = float(row[6]) if row[6] else 0
            total = mid + final + quiz + assignment
            
            students.append({
                'student_id': row[0],
                'name': row[1],
                'roll_number': row[2],
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
        
        # Verify faculty is assigned to this subject and class
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id = result[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM faculty_classes 
            WHERE faculty_id = :faculty_id AND subject_id = :subject_id AND class_name = :class_name
        """, {'faculty_id': faculty_id, 'subject_id': subject_id, 'class_name': class_name})
        
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'You are not assigned to this subject and class'}), 403
        
        # Verify student is in this class
        cursor.execute("""
            SELECT COUNT(*) FROM students WHERE student_id = :student_id AND class_name = :class_name
        """, {'student_id': student_id, 'class_name': class_name})
        
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'Student not found in this class'}), 404
        
        cursor.execute("""
            DELETE FROM marks 
            WHERE student_id = :student_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'subject_id': subject_id})
        
        assessment_map = {
            'mid': ('MST', 30),
            'final': ('EST', 40),
            'quiz': ('Quiz', 15),
            'assignment': ('Assignment', 15)
        }
        
        for key, (assessment_type, max_marks) in assessment_map.items():
            if key in marks_data and marks_data[key] is not None and marks_data[key] != '':
                marks_value = float(marks_data[key])
                
                # Validate marks don't exceed max
                if marks_value > max_marks:
                    return jsonify({'message': f'{assessment_type} marks cannot exceed {max_marks}'}), 400
                
                if marks_value < 0:
                    return jsonify({'message': f'{assessment_type} marks cannot be negative'}), 400
                
                cursor.execute("""
                    INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
                    VALUES (marks_seq.NEXTVAL, :student_id, :subject_id, :class_name, :assessment_type, :marks_obtained, :max_marks)
                """, {
                    'student_id': student_id,
                    'subject_id': subject_id,
                    'class_name': class_name,
                    'assessment_type': assessment_type,
                    'marks_obtained': marks_value,
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

@app.route('/api/faculty/feedback/unread', methods=['GET'])
@token_required
def get_faculty_unread_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        faculty_id = result[0]
        
        cursor.execute("""
            SELECT DISTINCT 
                s.student_id, 
                s.name as student_name, 
                s.roll_number,
                s.class_name,
                sub.subject_id, 
                sub.subject_name,
                (SELECT COUNT(*) FROM feedback_messages fm2 
                 WHERE fm2.thread_id = ft.thread_id 
                 AND fm2.sender_role = 'student' 
                 AND fm2.is_read = 0) as unread_count,
                (SELECT message FROM feedback_messages fm3 
                 WHERE fm3.thread_id = ft.thread_id 
                 AND fm3.sender_role = 'student'
                 ORDER BY fm3.created_at DESC 
                 FETCH FIRST 1 ROW ONLY) as last_message,
                (SELECT TO_CHAR(created_at, 'DD Mon YYYY HH24:MI') FROM feedback_messages fm4 
                 WHERE fm4.thread_id = ft.thread_id 
                 ORDER BY fm4.created_at DESC 
                 FETCH FIRST 1 ROW ONLY) as last_message_time
            FROM feedback_threads ft
            JOIN students s ON ft.student_id = s.student_id
            JOIN subjects sub ON ft.subject_id = sub.subject_id
            WHERE ft.faculty_id = :faculty_id
            AND EXISTS (
                SELECT 1 FROM feedback_messages fm 
                WHERE fm.thread_id = ft.thread_id 
                AND fm.sender_role = 'student' 
                AND fm.is_read = 0
            )
            ORDER BY last_message_time DESC
        """, {'faculty_id': faculty_id})
        
        unread = []
        for row in cursor.fetchall():
            # Handle CLOB for last_message
            last_msg = row[7]
            if hasattr(last_msg, 'read'):
                last_msg = last_msg.read()
            else:
                last_msg = str(last_msg) if last_msg else ""
            
            # Truncate message if too long
            if len(last_msg) > 100:
                last_msg = last_msg[:100] + "..."
            
            unread.append({
                'student_id': row[0],
                'student_name': row[1],
                'roll_number': row[2],
                'class_name': row[3],
                'subject_id': row[4],
                'subject_name': row[5],
                'unread_count': row[6],
                'last_message': last_msg,
                'last_message_time': row[8]
            })
        
        return jsonify(unread)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/feedback/threads', methods=['GET'])
@token_required
def get_faculty_feedback_threads():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        faculty_id = result[0]
        
        cursor.execute("""
            SELECT DISTINCT s.student_id, s.name, s.roll_number, s.class_name, sub.subject_id, sub.subject_name,
                   (SELECT COUNT(*) FROM feedback_messages fm 
                    JOIN feedback_threads ft ON fm.thread_id = ft.thread_id
                    WHERE ft.student_id = s.student_id AND ft.faculty_id = :faculty_id 
                    AND ft.subject_id = sub.subject_id AND fm.sender_role = 'student' AND fm.is_read = 0) as unread_count
            FROM feedback_threads ft
            JOIN students s ON ft.student_id = s.student_id
            JOIN subjects sub ON ft.subject_id = sub.subject_id
            WHERE ft.faculty_id = :faculty_id
            ORDER BY s.name
        """, {'faculty_id': faculty_id})
        
        threads = []
        for row in cursor.fetchall():
            threads.append({
                'student_id': row[0],
                'student_name': row[1],
                'roll_number': row[2],
                'class_name': row[3],
                'subject_id': row[4],
                'subject_name': row[5],
                'unread_count': row[6]
            })
        
        return jsonify(threads)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/feedback/<int:student_id>/<int:subject_id>', methods=['GET'])
@token_required
def get_faculty_feedback_thread(student_id, subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify([])
        
        faculty_id = result[0]
        
        # Get thread with clear timestamps
        cursor.execute("""
            SELECT thread_id, cleared_by_student, cleared_by_faculty
            FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if not thread:
            return jsonify([])
        
        thread_id = thread[0]
        cleared_by_faculty = thread[2]
        
        # Get messages created after faculty cleared chat (or all if never cleared)
        if cleared_by_faculty:
            cursor.execute("""
                SELECT message_id, sender_role, message, is_read, created_at, 
                       attachment_path, attachment_name, attachment_type
                FROM feedback_messages
                WHERE thread_id = :thread_id AND created_at > :cleared_time
                ORDER BY created_at ASC
            """, {'thread_id': thread_id, 'cleared_time': cleared_by_faculty})
        else:
            cursor.execute("""
                SELECT message_id, sender_role, message, is_read, created_at, 
                       attachment_path, attachment_name, attachment_type
                FROM feedback_messages
                WHERE thread_id = :thread_id
                ORDER BY created_at ASC
            """, {'thread_id': thread_id})
        
        messages = []
        for row in cursor.fetchall():
            message_text = row[2].read() if hasattr(row[2], 'read') else str(row[2])
            messages.append({
                'feedback_id': row[0],
                'sender_role': row[1],
                'message': message_text,
                'is_read': row[3],
                'created_at': row[4].strftime('%Y-%m-%d %H:%M'),
                'attachment_name': row[6],
                'attachment_type': row[7],
                'has_attachment': row[6] is not None
            })
        
        # Mark as read
        cursor.execute("""
            UPDATE feedback_messages SET is_read = 1
            WHERE thread_id = :thread_id AND sender_role = 'student' AND is_read = 0
        """, {'thread_id': thread_id})
        conn.commit()
        
        return jsonify(messages)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/feedback/send', methods=['POST'])
@token_required
def send_faculty_feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if request has file
        if 'attachment' in request.files:
            file = request.files['attachment']
            student_id = int(request.form.get('student_id'))
            subject_id = int(request.form.get('subject_id'))
            message = request.form.get('message', '').strip()
            
            # If no message but has attachment, use default message
            if not message and file and file.filename:
                message = '[Attachment]'
            
            attachment_path = None
            attachment_name = None
            attachment_type = None
            
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                attachment_path = filepath
                attachment_name = filename
                attachment_type = filename.rsplit('.', 1)[1].lower()
        else:
            data = request.get_json()
            student_id = data.get('student_id')
            subject_id = data.get('subject_id')
            message = data.get('message', '').strip()
            attachment_path = None
            attachment_name = None
            attachment_type = None
        
        # Ensure message is not empty or None
        if not message:
            message = '[No message]'
        
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id = result[0]
        
        # Get or create thread
        cursor.execute("""
            SELECT thread_id FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if thread:
            thread_id = thread[0]
        else:
            # Create new thread
            cursor.execute("""
                INSERT INTO feedback_threads (thread_id, student_id, faculty_id, subject_id, initiated_by, created_at, last_message_at)
                VALUES (feedback_threads_seq.NEXTVAL, :student_id, :faculty_id, :subject_id, 'faculty', SYSDATE, SYSDATE)
            """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
            cursor.execute("SELECT feedback_threads_seq.CURRVAL FROM dual")
            thread_id = cursor.fetchone()[0]
        
        # Insert message
        cursor.execute("""
            INSERT INTO feedback_messages (message_id, thread_id, sender_id, sender_role, message, is_read, created_at,
                                          attachment_path, attachment_name, attachment_type)
            VALUES (feedback_messages_seq.NEXTVAL, :thread_id, :sender_id, 'faculty', :message, 0, SYSDATE,
                   :attachment_path, :attachment_name, :attachment_type)
        """, {
            'thread_id': thread_id,
            'sender_id': request.user_id,
            'message': message,
            'attachment_path': attachment_path,
            'attachment_name': attachment_name,
            'attachment_type': attachment_type
        })
        
        # Update thread
        cursor.execute("""
            UPDATE feedback_threads SET last_message_at = SYSDATE WHERE thread_id = :thread_id
        """, {'thread_id': thread_id})
        
        conn.commit()
        return jsonify({'message': 'Message sent successfully'})
    except Exception as e:
        conn.rollback()
        print(f"Error sending feedback: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error sending message: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/attendance/<int:subject_id>/<class_name>', methods=['GET'])
@token_required
def get_faculty_attendance(subject_id, class_name):
    if request.role != 'faculty':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verify faculty is assigned to this subject and class
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id = result[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM faculty_classes 
            WHERE faculty_id = :faculty_id AND subject_id = :subject_id AND class_name = :class_name
        """, {'faculty_id': faculty_id, 'subject_id': subject_id, 'class_name': class_name})
        
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'You are not assigned to this subject and class'}), 403
        
        # Get date parameter (optional)
        date_str = request.args.get('date')
        
        if date_str:
            # Get attendance for specific date
            cursor.execute("""
                SELECT s.student_id, s.name, s.roll_number,
                       CASE WHEN a.status IS NULL THEN 'N' ELSE a.status END as status
                FROM students s
                LEFT JOIN attendance a ON s.student_id = a.student_id 
                    AND a.subject_id = :subject_id 
                    AND a.attendance_date = TO_DATE(:date_param, 'YYYY-MM-DD')
                WHERE s.class_name = :class_name
                ORDER BY s.roll_number
            """, {'subject_id': subject_id, 'class_name': class_name, 'date_param': date_str})
            
            students = []
            for row in cursor.fetchall():
                students.append({
                    'student_id': row[0],
                    'name': row[1],
                    'roll_number': row[2],
                    'status': row[3]
                })
            
            return jsonify({'date': date_str, 'students': students})
        else:
            # Get students with overall attendance stats
            cursor.execute("""
                SELECT s.student_id, s.name, s.roll_number,
                       COUNT(a.attendance_id) as total_classes,
                       SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
                FROM students s
                LEFT JOIN attendance a ON s.student_id = a.student_id AND a.subject_id = :subject_id
                WHERE s.class_name = :class_name
                GROUP BY s.student_id, s.name, s.roll_number
                ORDER BY s.roll_number
            """, {'subject_id': subject_id, 'class_name': class_name})
            
            students = []
            for row in cursor.fetchall():
                total = row[3] if row[3] else 0
                present = row[4] if row[4] else 0
                percentage = round((present / total) * 100, 2) if total > 0 else 0
                
                students.append({
                    'student_id': row[0],
                    'name': row[1],
                    'roll_number': row[2],
                    'total_classes': total,
                    'present': present,
                    'percentage': percentage
                })
            
            return jsonify(students)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/attendance/mark_batch', methods=['POST'])
@token_required
def mark_batch_attendance():
    if request.role != 'faculty':
        return jsonify({'message': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        data = request.get_json()
        subject_id = data.get('subject_id')
        class_name = data.get('class_name')
        date = data.get('date')
        attendance_records = data.get('attendance')  # [{student_id, status}, ...]
        
        # Verify faculty is assigned to this subject and class
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Faculty not found'}), 404
        
        faculty_id = result[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM faculty_classes 
            WHERE faculty_id = :faculty_id AND subject_id = :subject_id AND class_name = :class_name
        """, {'faculty_id': faculty_id, 'subject_id': subject_id, 'class_name': class_name})
        
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'You are not assigned to this subject and class'}), 403
        
        # Mark attendance for all students
        for record in attendance_records:
            student_id = record.get('student_id')
            status = record.get('status')
            
            # Verify student is in this class
            cursor.execute("""
                SELECT COUNT(*) FROM students WHERE student_id = :student_id AND class_name = :class_name
            """, {'student_id': student_id, 'class_name': class_name})
            
            if cursor.fetchone()[0] == 0:
                continue
            
            # Check if attendance already exists for this date
            cursor.execute("""
                SELECT attendance_id FROM attendance 
                WHERE student_id = :student_id AND subject_id = :subject_id 
                AND attendance_date = TO_DATE(:date_param, 'YYYY-MM-DD')
            """, {'student_id': student_id, 'subject_id': subject_id, 'date_param': date})
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing
                cursor.execute("""
                    UPDATE attendance SET status = :status
                    WHERE attendance_id = :attendance_id
                """, {'status': status, 'attendance_id': existing[0]})
            else:
                # Insert new
                cursor.execute("""
                    INSERT INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
                    VALUES (attendance_seq.NEXTVAL, :student_id, :subject_id, :class_name, TO_DATE(:date_param, 'YYYY-MM-DD'), :status)
                """, {
                    'student_id': student_id,
                    'subject_id': subject_id,
                    'class_name': class_name,
                    'date_param': date,
                    'status': status
                })
        
        conn.commit()
        
        # Update alerts based on new attendance
        update_attendance_alerts(cursor, conn, subject_id, class_name)
        
        return jsonify({'message': 'Attendance marked successfully'})
    except Exception as e:
        conn.rollback()
        print(f"Error marking attendance: {str(e)}")
        return jsonify({'message': f'Error marking attendance: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

def update_attendance_alerts(cursor, conn, subject_id, class_name):
    """Update alerts for students with low attendance"""
    try:
        # Get students with low attendance
        cursor.execute("""
            SELECT s.student_id, sub.subject_name,
                   COUNT(*) as total,
                   SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
            FROM students s
            JOIN attendance a ON s.student_id = a.student_id
            JOIN subjects sub ON a.subject_id = sub.subject_id
            WHERE s.class_name = :class_name AND a.subject_id = :subject_id
            GROUP BY s.student_id, sub.subject_name
            HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
        """, {'class_name': class_name, 'subject_id': subject_id})
        
        for student_id, subject_name, total, present in cursor.fetchall():
            percentage = round((present / total) * 100, 2)
            alert_type = 'Critical' if percentage < 50 else 'Warning'
            message = f"Low attendance in {subject_name}: {percentage}%"
            
            # Check if alert already exists
            cursor.execute("""
                SELECT alert_id FROM alerts 
                WHERE student_id = :student_id AND subject_id = :subject_id AND alert_type = :alert_type
            """, {'student_id': student_id, 'subject_id': subject_id, 'alert_type': alert_type})
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message, is_read, created_at)
                    VALUES (alerts_seq.NEXTVAL, :student_id, :subject_id, :alert_type, :message, 0, SYSDATE)
                """, {
                    'student_id': student_id,
                    'subject_id': subject_id,
                    'alert_type': alert_type,
                    'message': message
                })
        
        conn.commit()
    except Exception as e:
        print(f"Error updating alerts: {str(e)}")

# Download attachment endpoint
@app.route('/api/feedback/attachment/<int:message_id>', methods=['GET'])
@token_required
def download_attachment(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT attachment_path, attachment_name 
            FROM feedback_messages 
            WHERE message_id = :message_id
        """, {'message_id': message_id})
        
        result = cursor.fetchone()
        if not result or not result[0]:
            return jsonify({'message': 'Attachment not found'}), 404
        
        attachment_path, attachment_name = result
        
        if os.path.exists(attachment_path):
            directory = os.path.dirname(attachment_path)
            filename = os.path.basename(attachment_path)
            return send_from_directory(directory, filename, as_attachment=True, download_name=attachment_name)
        else:
            return jsonify({'message': 'File not found on server'}), 404
            
    except Exception as e:
        print(f"Error downloading attachment: {str(e)}")
        return jsonify({'message': 'Error downloading file'}), 500
    finally:
        cursor.close()
        conn.close()

# Clear Chat Endpoints (User-Specific)
@app.route('/api/student/feedback/clear/<int:faculty_id>/<int:subject_id>', methods=['DELETE'])
@token_required
def clear_student_chat(faculty_id, subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get student_id from user_id
        cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Student not found'}), 404
        student_id = result[0]
        
        print(f"Clear chat request - Student: {student_id}, Faculty: {faculty_id}, Subject: {subject_id}")
        
        # Find the thread
        cursor.execute("""
            SELECT thread_id FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if not thread:
            print(f"Thread not found for student {student_id}, faculty {faculty_id}, subject {subject_id}")
            return jsonify({'message': 'Chat not found'}), 404
        
        thread_id = thread[0]
        print(f"Found thread_id: {thread_id}")
        
        # Soft delete: Update cleared_by_student timestamp
        # Messages created before this timestamp will be hidden for student
        cursor.execute("""
            UPDATE feedback_threads 
            SET cleared_by_student = SYSDATE
            WHERE thread_id = :thread_id
        """, {'thread_id': thread_id})
        
        conn.commit()
        print(f"Chat cleared for student in thread {thread_id}")
        return jsonify({'message': 'Chat cleared successfully'}), 200
        
    except Exception as e:
        conn.rollback()
        print(f"Error clearing chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error clearing chat: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/faculty/feedback/clear/<int:student_id>/<int:subject_id>', methods=['DELETE'])
@token_required
def clear_faculty_chat(student_id, subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get faculty_id from user_id
        cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", {'user_id': request.user_id})
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Faculty not found'}), 404
        faculty_id = result[0]
        
        print(f"Clear chat request - Faculty: {faculty_id}, Student: {student_id}, Subject: {subject_id}")
        
        # Find the thread
        cursor.execute("""
            SELECT thread_id FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if not thread:
            print(f"Thread not found for student {student_id}, faculty {faculty_id}, subject {subject_id}")
            return jsonify({'message': 'Chat not found'}), 404
        
        thread_id = thread[0]
        print(f"Found thread_id: {thread_id}")
        
        # Soft delete: Update cleared_by_faculty timestamp
        # Messages created before this timestamp will be hidden for faculty
        cursor.execute("""
            UPDATE feedback_threads 
            SET cleared_by_faculty = SYSDATE
            WHERE thread_id = :thread_id
        """, {'thread_id': thread_id})
        
        conn.commit()
        print(f"Chat cleared for faculty in thread {thread_id}")
        return jsonify({'message': 'Chat cleared successfully'}), 200
        
    except Exception as e:
        conn.rollback()
        print(f"Error clearing chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error clearing chat: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
