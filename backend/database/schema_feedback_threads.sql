-- Feedback Threads Table (stores conversation metadata)
CREATE TABLE feedback_threads (
    thread_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    faculty_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    thread_title VARCHAR2(200),
    initiated_by VARCHAR2(20) NOT NULL CHECK (initiated_by IN ('student', 'faculty')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cleared_by_student TIMESTAMP DEFAULT NULL,
    cleared_by_faculty TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE feedback_threads_seq START WITH 1 INCREMENT BY 1;

-- Feedback Messages Table (stores individual messages in threads)
CREATE TABLE feedback_messages (
    message_id NUMBER PRIMARY KEY,
    thread_id NUMBER NOT NULL,
    sender_id NUMBER NOT NULL,
    sender_role VARCHAR2(20) NOT NULL CHECK (sender_role IN ('student', 'faculty')),
    message CLOB NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attachment_path VARCHAR2(500),
    attachment_name VARCHAR2(200),
    attachment_type VARCHAR2(50),
    FOREIGN KEY (thread_id) REFERENCES feedback_threads(thread_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
);

CREATE SEQUENCE feedback_messages_seq START WITH 1 INCREMENT BY 1;

-- Create indexes for better performance
CREATE INDEX idx_feedback_threads_student ON feedback_threads(student_id);
CREATE INDEX idx_feedback_threads_faculty ON feedback_threads(faculty_id);
CREATE INDEX idx_feedback_threads_subject ON feedback_threads(subject_id);
CREATE INDEX idx_feedback_messages_thread ON feedback_messages(thread_id);
CREATE INDEX idx_feedback_messages_sender ON feedback_messages(sender_id);

-- Trigger to update last_message_at when new message is added
CREATE OR REPLACE TRIGGER update_thread_timestamp
AFTER INSERT ON feedback_messages
FOR EACH ROW
BEGIN
    UPDATE feedback_threads
    SET last_message_at = CURRENT_TIMESTAMP
    WHERE thread_id = :NEW.thread_id;
END;
/
