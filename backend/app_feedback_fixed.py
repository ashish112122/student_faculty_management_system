# Fixed Feedback API endpoints using threading tables
# Replace the feedback endpoints in app.py with these

# Student Feedback APIs

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
        
        # Get or create thread
        cursor.execute("""
            SELECT thread_id FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if not thread:
            # No thread exists yet, return empty
            return jsonify([])
        
        thread_id = thread[0]
        
        # Get messages
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
        
        # Mark messages as read
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
            faculty_id = request.form.get('faculty_id')
            subject_id = request.form.get('subject_id')
            message = request.form.get('message', '')
            
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
            message = data.get('message')
            attachment_path = None
            attachment_name = None
            attachment_type = None
        
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
                RETURNING thread_id INTO :thread_id
            """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id, 'thread_id': cursor.var(oracledb.NUMBER)})
            thread_id = cursor.getvalue(0)[0]
        
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
        
        # Update thread last_message_at
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

# Faculty Feedback APIs

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
            SELECT DISTINCT s.student_id, s.name, s.class_name, sub.subject_id, sub.subject_name,
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
                'class_name': row[2],
                'subject_id': row[3],
                'subject_name': row[4],
                'unread_count': row[5]
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
        
        # Get or create thread
        cursor.execute("""
            SELECT thread_id FROM feedback_threads
            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
        """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
        
        thread = cursor.fetchone()
        if not thread:
            return jsonify([])
        
        thread_id = thread[0]
        
        # Get messages
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
        
        # Mark messages as read
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
            student_id = request.form.get('student_id')
            subject_id = request.form.get('subject_id')
            message = request.form.get('message', '')
            
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
            message = data.get('message')
            attachment_path = None
            attachment_name = None
            attachment_type = None
        
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
                RETURNING thread_id INTO :thread_id
            """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id, 'thread_id': cursor.var(oracledb.NUMBER)})
            thread_id = cursor.getvalue(0)[0]
        
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
        
        # Update thread last_message_at
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
