# Feedback API with Thread Support
# Both students and faculty can initiate conversations
# Multiple independent threads supported

from flask import request, jsonify, send_from_directory
from functools import wraps
import datetime
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================
# STUDENT FEEDBACK APIs
# ============================================

def get_student_threads(app, get_db_connection, token_required):
    """Get all feedback threads for a student"""
    @app.route('/api/student/feedback/threads', methods=['GET'])
    @token_required
    def student_feedback_threads():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get student_id from user_id
            cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", 
                          {'user_id': request.user_id})
            result = cursor.fetchone()
            if not result:
                return jsonify([])
            
            student_id = result[0]
            
            # Get all threads for this student
            cursor.execute("""
                SELECT 
                    ft.thread_id,
                    ft.thread_title,
                    ft.subject_id,
                    s.subject_name,
                    ft.faculty_id,
                    f.name as faculty_name,
                    ft.initiated_by,
                    ft.created_at,
                    ft.last_message_at,
                    (SELECT COUNT(*) FROM feedback_messages fm 
                     WHERE fm.thread_id = ft.thread_id 
                     AND fm.sender_role = 'faculty' AND fm.is_read = 0) as unread_count
                FROM feedback_threads ft
                JOIN subjects s ON ft.subject_id = s.subject_id
                JOIN faculty f ON ft.faculty_id = f.faculty_id
                WHERE ft.student_id = :student_id
                ORDER BY ft.last_message_at DESC
            """, {'student_id': student_id})
            
            threads = []
            for row in cursor.fetchall():
                threads.append({
                    'thread_id': row[0],
                    'thread_title': row[1] or 'Untitled Thread',
                    'subject_id': row[2],
                    'subject_name': row[3],
                    'faculty_id': row[4],
                    'faculty_name': row[5],
                    'initiated_by': row[6],
                    'created_at': row[7].strftime('%Y-%m-%d %H:%M'),
                    'last_message_at': row[8].strftime('%Y-%m-%d %H:%M'),
                    'unread_count': row[9]
                })
            
            return jsonify(threads)
        finally:
            cursor.close()
            conn.close()

def get_student_faculty_list(app, get_db_connection, token_required):
    """Get list of faculty for student to start new thread"""
    @app.route('/api/student/feedback/faculty_list', methods=['GET'])
    @token_required
    def student_faculty_list():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT student_id, class_name FROM students WHERE user_id = :user_id", 
                          {'user_id': request.user_id})
            result = cursor.fetchone()
            if not result:
                return jsonify([])
            
            student_id, class_name = result
            
            # Get faculty teaching this student's class
            cursor.execute("""
                SELECT DISTINCT 
                    f.faculty_id,
                    f.name,
                    f.faculty_code,
                    s.subject_id,
                    s.subject_name,
                    s.subject_code
                FROM faculty_classes fc
                JOIN faculty f ON fc.faculty_id = f.faculty_id
                JOIN subjects s ON fc.subject_id = s.subject_id
                WHERE fc.class_name = :class_name
                ORDER BY s.subject_name
            """, {'class_name': class_name})
            
            faculty_list = []
            for row in cursor.fetchall():
                faculty_list.append({
                    'faculty_id': row[0],
                    'faculty_name': row[1],
                    'faculty_code': row[2],
                    'subject_id': row[3],
                    'subject_name': row[4],
                    'subject_code': row[5]
                })
            
            return jsonify(faculty_list)
        finally:
            cursor.close()
            conn.close()


def create_student_thread(app, get_db_connection, token_required):
    """Student creates a new thread"""
    @app.route('/api/student/feedback/create_thread', methods=['POST'])
    @token_required
    def student_create_thread():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            data = request.get_json()
            faculty_id = data.get('faculty_id')
            subject_id = data.get('subject_id')
            thread_title = data.get('thread_title', 'New Conversation')
            initial_message = data.get('message')
            
            cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", 
                          {'user_id': request.user_id})
            result = cursor.fetchone()
            if not result:
                return jsonify({'message': 'Student not found'}), 404
            
            student_id = result[0]
            
            # Create new thread
            cursor.execute("""
                INSERT INTO feedback_threads 
                (thread_id, student_id, faculty_id, subject_id, thread_title, initiated_by)
                VALUES (feedback_threads_seq.NEXTVAL, :student_id, :faculty_id, :subject_id, :thread_title, 'student')
                RETURNING thread_id INTO :thread_id
            """, {
                'student_id': student_id,
                'faculty_id': faculty_id,
                'subject_id': subject_id,
                'thread_title': thread_title
            })
            
            # Get the new thread_id
            cursor.execute("SELECT feedback_threads_seq.CURRVAL FROM DUAL")
            thread_id = cursor.fetchone()[0]
            
            # Add initial message if provided
            if initial_message:
                cursor.execute("""
                    INSERT INTO feedback_messages
                    (message_id, thread_id, sender_id, sender_role, message, is_read)
                    VALUES (feedback_messages_seq.NEXTVAL, :thread_id, :sender_id, 'student', :message, 0)
                """, {
                    'thread_id': thread_id,
                    'sender_id': request.user_id,
                    'message': initial_message
                })
            
            conn.commit()
            return jsonify({'message': 'Thread created', 'thread_id': thread_id})
        except Exception as e:
            conn.rollback()
            print(f"Error creating thread: {str(e)}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()


def get_thread_messages(app, get_db_connection, token_required):
    """Get all messages in a thread"""
    @app.route('/api/feedback/thread/<int:thread_id>/messages', methods=['GET'])
    @token_required
    def get_thread_messages_api(thread_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verify user has access to this thread
            if request.role == 'student':
                cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", 
                              {'user_id': request.user_id})
                result = cursor.fetchone()
                if not result:
                    return jsonify({'message': 'Unauthorized'}), 403
                user_ref_id = result[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM feedback_threads 
                    WHERE thread_id = :thread_id AND student_id = :student_id
                """, {'thread_id': thread_id, 'student_id': user_ref_id})
            else:  # faculty
                cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", 
                              {'user_id': request.user_id})
                result = cursor.fetchone()
                if not result:
                    return jsonify({'message': 'Unauthorized'}), 403
                user_ref_id = result[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM feedback_threads 
                    WHERE thread_id = :thread_id AND faculty_id = :faculty_id
                """, {'thread_id': thread_id, 'faculty_id': user_ref_id})
            
            if cursor.fetchone()[0] == 0:
                return jsonify({'message': 'Unauthorized'}), 403
            
            # Get messages
            cursor.execute("""
                SELECT 
                    fm.message_id,
                    fm.sender_role,
                    fm.message,
                    fm.is_read,
                    fm.created_at,
                    fm.attachment_path,
                    fm.attachment_name,
                    fm.attachment_type,
                    u.name as sender_name
                FROM feedback_messages fm
                JOIN users u ON fm.sender_id = u.user_id
                WHERE fm.thread_id = :thread_id
                ORDER BY fm.created_at ASC
            """, {'thread_id': thread_id})
            
            messages = []
            for row in cursor.fetchall():
                message_text = row[2].read() if hasattr(row[2], 'read') else str(row[2])
                messages.append({
                    'message_id': row[0],
                    'sender_role': row[1],
                    'message': message_text,
                    'is_read': row[3],
                    'created_at': row[4].strftime('%Y-%m-%d %H:%M'),
                    'attachment_name': row[6],
                    'attachment_type': row[7],
                    'has_attachment': row[6] is not None,
                    'sender_name': row[8]
                })
            
            # Mark messages as read for current user
            opposite_role = 'faculty' if request.role == 'student' else 'student'
            cursor.execute("""
                UPDATE feedback_messages 
                SET is_read = 1
                WHERE thread_id = :thread_id AND sender_role = :opposite_role AND is_read = 0
            """, {'thread_id': thread_id, 'opposite_role': opposite_role})
            conn.commit()
            
            return jsonify(messages)
        finally:
            cursor.close()
            conn.close()


def send_message_to_thread(app, get_db_connection, token_required):
    """Send a message to an existing thread"""
    @app.route('/api/feedback/thread/<int:thread_id>/send', methods=['POST'])
    @token_required
    def send_message_api(thread_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if request has file
            if 'attachment' in request.files:
                file = request.files['attachment']
                message = request.form.get('message', '')
                
                attachment_path = None
                attachment_name = None
                attachment_type = None
                
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    upload_folder = 'uploads/feedback_attachments'
                    os.makedirs(upload_folder, exist_ok=True)
                    filepath = os.path.join(upload_folder, unique_filename)
                    file.save(filepath)
                    
                    attachment_path = filepath
                    attachment_name = filename
                    attachment_type = filename.rsplit('.', 1)[1].lower()
            else:
                data = request.get_json()
                message = data.get('message')
                attachment_path = None
                attachment_name = None
                attachment_type = None
            
            if not message:
                return jsonify({'message': 'Message is required'}), 400
            
            # Verify user has access to this thread
            if request.role == 'student':
                cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", 
                              {'user_id': request.user_id})
                result = cursor.fetchone()
                if not result:
                    return jsonify({'message': 'Unauthorized'}), 403
                user_ref_id = result[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM feedback_threads 
                    WHERE thread_id = :thread_id AND student_id = :student_id
                """, {'thread_id': thread_id, 'student_id': user_ref_id})
            else:  # faculty
                cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", 
                              {'user_id': request.user_id})
                result = cursor.fetchone()
                if not result:
                    return jsonify({'message': 'Unauthorized'}), 403
                user_ref_id = result[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM feedback_threads 
                    WHERE thread_id = :thread_id AND faculty_id = :faculty_id
                """, {'thread_id': thread_id, 'faculty_id': user_ref_id})
            
            if cursor.fetchone()[0] == 0:
                return jsonify({'message': 'Unauthorized'}), 403
            
            # Insert message
            cursor.execute("""
                INSERT INTO feedback_messages
                (message_id, thread_id, sender_id, sender_role, message, is_read,
                 attachment_path, attachment_name, attachment_type)
                VALUES (feedback_messages_seq.NEXTVAL, :thread_id, :sender_id, :sender_role, :message, 0,
                       :attachment_path, :attachment_name, :attachment_type)
            """, {
                'thread_id': thread_id,
                'sender_id': request.user_id,
                'sender_role': request.role,
                'message': message,
                'attachment_path': attachment_path,
                'attachment_name': attachment_name,
                'attachment_type': attachment_type
            })
            
            conn.commit()
            return jsonify({'message': 'Message sent successfully'})
        except Exception as e:
            conn.rollback()
            print(f"Error sending message: {str(e)}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()


# ============================================
# FACULTY FEEDBACK APIs
# ============================================

def get_faculty_threads(app, get_db_connection, token_required):
    """Get all feedback threads for a faculty"""
    @app.route('/api/faculty/feedback/threads', methods=['GET'])
    @token_required
    def faculty_feedback_threads():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", 
                          {'user_id': request.user_id})
            result = cursor.fetchone()
            if not result:
                return jsonify([])
            
            faculty_id = result[0]
            
            # Get all threads for this faculty
            cursor.execute("""
                SELECT 
                    ft.thread_id,
                    ft.thread_title,
                    ft.subject_id,
                    s.subject_name,
                    ft.student_id,
                    st.name as student_name,
                    st.roll_number,
                    st.class_name,
                    ft.initiated_by,
                    ft.created_at,
                    ft.last_message_at,
                    (SELECT COUNT(*) FROM feedback_messages fm 
                     WHERE fm.thread_id = ft.thread_id 
                     AND fm.sender_role = 'student' AND fm.is_read = 0) as unread_count
                FROM feedback_threads ft
                JOIN subjects s ON ft.subject_id = s.subject_id
                JOIN students st ON ft.student_id = st.student_id
                WHERE ft.faculty_id = :faculty_id
                ORDER BY ft.last_message_at DESC
            """, {'faculty_id': faculty_id})
            
            threads = []
            for row in cursor.fetchall():
                threads.append({
                    'thread_id': row[0],
                    'thread_title': row[1] or 'Untitled Thread',
                    'subject_id': row[2],
                    'subject_name': row[3],
                    'student_id': row[4],
                    'student_name': row[5],
                    'roll_number': row[6],
                    'class_name': row[7],
                    'initiated_by': row[8],
                    'created_at': row[9].strftime('%Y-%m-%d %H:%M'),
                    'last_message_at': row[10].strftime('%Y-%m-%d %H:%M'),
                    'unread_count': row[11]
                })
            
            return jsonify(threads)
        finally:
            cursor.close()
            conn.close()


def get_faculty_student_list(app, get_db_connection, token_required):
    """Get list of students for faculty to start new thread"""
    @app.route('/api/faculty/feedback/student_list', methods=['GET'])
    @token_required
    def faculty_student_list():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", 
                          {'user_id': request.user_id})
            result = cursor.fetchone()
            if not result:
                return jsonify([])
            
            faculty_id = result[0]
            
            # Get subject_id and class_name from query params (optional filters)
            subject_id = request.args.get('subject_id', type=int)
            class_name = request.args.get('class_name')
            
            # Get students in classes taught by this faculty
            query = """
                SELECT DISTINCT 
                    s.student_id,
                    s.name,
                    s.roll_number,
                    s.class_name,
                    s.branch,
                    sub.subject_id,
                    sub.subject_name
                FROM students s
                JOIN faculty_classes fc ON s.class_name = fc.class_name
                JOIN subjects sub ON fc.subject_id = sub.subject_id
                WHERE fc.faculty_id = :faculty_id
            """
            
            params = {'faculty_id': faculty_id}
            
            if subject_id:
                query += " AND sub.subject_id = :subject_id"
                params['subject_id'] = subject_id
            
            if class_name:
                query += " AND s.class_name = :class_name"
                params['class_name'] = class_name
            
            query += " ORDER BY s.class_name, s.roll_number"
            
            cursor.execute(query, params)
            
            students = []
            for row in cursor.fetchall():
                students.append({
                    'student_id': row[0],
                    'student_name': row[1],
                    'roll_number': row[2],
                    'class_name': row[3],
                    'branch': row[4],
                    'subject_id': row[5],
                    'subject_name': row[6]
                })
            
            return jsonify(students)
        finally:
            cursor.close()
            conn.close()

def create_faculty_thread(app, get_db_connection, token_required):
    """Faculty creates a new thread"""
    @app.route('/api/faculty/feedback/create_thread', methods=['POST'])
    @token_required
    def faculty_create_thread():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            data = request.gerequired)
    create_student_thread(app, get_db_connection, token_required)
    get_thread_messages(app, get_db_connection, token_required)
    send_message_to_thread(app, get_db_connection, token_required)
    get_faculty_threads(app, get_db_connection, token_required)
    get_faculty_student_list(app, get_db_connection, token_required)
    create_faculty_thread(app, get_db_connection, token_required)
    search_threads(app, get_db_connection, token_required)
     'thread_title': row[1] or 'Untitled Thread',
                    'last_message_at': row[2].strftime('%Y-%m-%d %H:%M')
                })
            
            return jsonify(results)
        finally:
            cursor.close()
            conn.close()

# Register all routes
def register_feedback_routes(app, get_db_connection, token_required):
    """Register all feedback routes"""
    get_student_threads(app, get_db_connection, token_required)
    get_student_faculty_list(app, get_db_connection, token_ack_messages fm ON ft.thread_id = fm.thread_id
                WHERE ft.{user_field} = :user_id
                AND (UPPER(ft.thread_title) LIKE UPPER(:keyword) 
                     OR UPPER(fm.message) LIKE UPPER(:keyword))
                ORDER BY ft.last_message_at DESC
            """, {'user_id': user_ref_id, 'keyword': f'%{keyword}%'})
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'thread_id': row[0],
               user_id", 
                              {'user_id': request.user_id})
                result = cursor.fetchone()
                if not result:
                    return jsonify([])
                user_ref_id = result[0]
                user_field = 'faculty_id'
            
            # Search in thread titles and messages
            cursor.execute(f"""
                SELECT DISTINCT ft.thread_id, ft.thread_title, ft.last_message_at
                FROM feedback_threads ft
                LEFT JOIN feedb  return jsonify([])
            
            if request.role == 'student':
                cursor.execute("SELECT student_id FROM students WHERE user_id = :user_id", 
                              {'user_id': request.user_id})
                result = cursor.fetchone()
                if not result:
                    return jsonify([])
                user_ref_id = result[0]
                user_field = 'student_id'
            else:
                cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :)
            return jsonify({'message': f'Error: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()

def search_threads(app, get_db_connection, token_required):
    """Search threads by keyword"""
    @app.route('/api/feedback/search', methods=['GET'])
    @token_required
    def search_threads_api():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            keyword = request.args.get('q', '')
            if not keyword:
                        VALUES (feedback_messages_seq.NEXTVAL, :thread_id, :sender_id, 'faculty', :message, 0)
                """, {
                    'thread_id': thread_id,
                    'sender_id': request.user_id,
                    'message': initial_message
                })
            
            conn.commit()
            return jsonify({'message': 'Thread created', 'thread_id': thread_id})
        except Exception as e:
            conn.rollback()
            print(f"Error creating thread: {str(e)}": subject_id,
                'thread_title': thread_title
            })
            
            # Get the new thread_id
            cursor.execute("SELECT feedback_threads_seq.CURRVAL FROM DUAL")
            thread_id = cursor.fetchone()[0]
            
            # Add initial message if provided
            if initial_message:
                cursor.execute("""
                    INSERT INTO feedback_messages
                    (message_id, thread_id, sender_id, sender_role, message, is_read)
                      
            faculty_id = result[0]
            
            # Create new thread
            cursor.execute("""
                INSERT INTO feedback_threads 
                (thread_id, student_id, faculty_id, subject_id, thread_title, initiated_by)
                VALUES (feedback_threads_seq.NEXTVAL, :student_id, :faculty_id, :subject_id, :thread_title, 'faculty')
            """, {
                'student_id': student_id,
                'faculty_id': faculty_id,
                'subject_id't_json()
            student_id = data.get('student_id')
            subject_id = data.get('subject_id')
            thread_title = data.get('thread_title', 'New Conversation')
            initial_message = data.get('message')
            
            cursor.execute("SELECT faculty_id FROM faculty WHERE user_id = :user_id", 
                          {'user_id': request.user_id})
            result = cursor.fetchone()
            if not result:
                return jsonify({'message': 'Faculty not found'}), 404
