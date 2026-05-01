-- ============================================================================
-- COMPLETE DATABASE SCHEMA
-- Student-Faculty Management System
-- Oracle Database 21c
-- ============================================================================
-- This file contains ALL table definitions in one place for easy reference
-- ============================================================================

-- ============================================================================
-- 1. AUTHENTICATION MODULE
-- ============================================================================

-- Users Table (Central authentication for all users)
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) NOT NULL CHECK (role IN ('student', 'faculty'))
);

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;

-- ============================================================================
-- 2. STUDENT MODULE
-- ============================================================================

-- Students Table (Student-specific information)
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    name VARCHAR2(100) NOT NULL,
    branch VARCHAR2(50) NOT NULL,
    semester NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    cgpa NUMBER(3,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1;

-- Subjects Table (All courses/subjects)
CREATE TABLE subjects (
    subject_id NUMBER PRIMARY KEY,
    subject_name VARCHAR2(100) NOT NULL,
    subject_code VARCHAR2(20) UNIQUE NOT NULL
);

CREATE SEQUENCE subjects_seq START WITH 1 INCREMENT BY 1;

-- ============================================================================
-- 3. FACULTY MODULE
-- ============================================================================

-- Faculty Table (Faculty-specific information)
CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    name VARCHAR2(100) NOT NULL,
    department VARCHAR2(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1;

-- Faculty Classes Table (Faculty teaching assignments)
CREATE TABLE faculty_classes (
    faculty_class_id NUMBER PRIMARY KEY,
    faculty_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE faculty_classes_seq START WITH 1 INCREMENT BY 1;

-- ============================================================================
-- 4. MARKS MODULE
-- ============================================================================

-- Marks Table (Student assessment marks)
CREATE TABLE marks (
    mark_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    assessment_type VARCHAR2(20) NOT NULL CHECK (assessment_type IN ('MST', 'EST', 'Quiz', 'Assignment')),
    marks_obtained NUMBER NOT NULL,
    max_marks NUMBER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE marks_seq START WITH 1 INCREMENT BY 1;

-- ============================================================================
-- 5. ATTENDANCE MODULE
-- ============================================================================

-- Attendance Table (Daily attendance records)
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    attendance_date DATE NOT NULL,
    status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1;

-- ============================================================================
-- 6. ALERTS MODULE
-- ============================================================================

-- Alerts Table (System-generated notifications)
CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER,
    alert_type VARCHAR2(20) NOT NULL,
    message VARCHAR2(500) NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1;

-- ============================================================================
-- 7. FEEDBACK/CHAT MODULE
-- ============================================================================

-- Feedback Threads Table (Conversation metadata)
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

-- Feedback Messages Table (Individual chat messages)
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

-- ============================================================================
-- 8. INDEXES FOR PERFORMANCE
-- ============================================================================

-- Feedback system indexes
CREATE INDEX idx_feedback_threads_student ON feedback_threads(student_id);
CREATE INDEX idx_feedback_threads_faculty ON feedback_threads(faculty_id);
CREATE INDEX idx_feedback_threads_subject ON feedback_threads(subject_id);
CREATE INDEX idx_feedback_messages_thread ON feedback_messages(thread_id);
CREATE INDEX idx_feedback_messages_sender ON feedback_messages(sender_id);

-- ============================================================================
-- 9. TRIGGERS
-- ============================================================================

-- Trigger 1: Keep feedback thread last_message_at up to date
CREATE OR REPLACE TRIGGER update_thread_timestamp
AFTER INSERT ON feedback_messages
FOR EACH ROW
BEGIN
    UPDATE feedback_threads
    SET last_message_at = CURRENT_TIMESTAMP
    WHERE thread_id = :NEW.thread_id;
END;
/

-- Trigger 2: Auto-generate attendance alerts when attendance is inserted or updated
-- Calculates percentage in SQL and inserts/updates alert if below threshold
CREATE OR REPLACE TRIGGER trg_attendance_alert
AFTER INSERT OR UPDATE ON attendance
FOR EACH ROW
DECLARE
    v_total        NUMBER;
    v_present      NUMBER;
    v_percentage   NUMBER;
    v_alert_type   VARCHAR2(20);
    v_message      VARCHAR2(500);
    v_subject_name VARCHAR2(100);
    v_existing     NUMBER;
BEGIN
    SELECT COUNT(*),
           SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END)
    INTO v_total, v_present
    FROM attendance
    WHERE student_id = :NEW.student_id
      AND subject_id = :NEW.subject_id;

    IF v_total = 0 THEN RETURN; END IF;

    v_percentage := ROUND((v_present / v_total) * 100, 2);

    SELECT subject_name INTO v_subject_name
    FROM subjects WHERE subject_id = :NEW.subject_id;

    IF v_percentage < 50 THEN
        v_alert_type := 'Critical';
        v_message := 'Low attendance in ' || v_subject_name || ': ' || v_percentage || '%. Attendance is critically low.';
    ELSIF v_percentage < 65 THEN
        v_alert_type := 'Alert';
        v_message := 'Low attendance in ' || v_subject_name || ': ' || v_percentage || '%. Immediate action required.';
    ELSIF v_percentage < 75 THEN
        v_alert_type := 'Warning';
        v_message := 'Low attendance in ' || v_subject_name || ': ' || v_percentage || '%. Please improve attendance.';
    ELSE
        RETURN;
    END IF;

    SELECT COUNT(*) INTO v_existing
    FROM alerts
    WHERE student_id = :NEW.student_id
      AND subject_id = :NEW.subject_id
      AND alert_type = v_alert_type;

    IF v_existing = 0 THEN
        INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message, is_read, created_at)
        VALUES (alerts_seq.NEXTVAL, :NEW.student_id, :NEW.subject_id, v_alert_type, v_message, 0, SYSDATE);
    ELSE
        UPDATE alerts
        SET message = v_message, is_read = 0, created_at = SYSDATE
        WHERE student_id = :NEW.student_id
          AND subject_id  = :NEW.subject_id
          AND alert_type  = v_alert_type;
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN NULL;
    WHEN OTHERS THEN NULL;
END;
/

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- SUMMARY:
-- Total Tables: 11
-- 1. users (authentication)
-- 2. students (student info)
-- 3. faculty (faculty info)
-- 4. subjects (courses)
-- 5. faculty_classes (teaching assignments)
-- 6. marks (student marks)
-- 7. attendance (daily attendance)
-- 8. alerts (notifications)
-- 9. feedback_threads (chat metadata)
-- 10. feedback_messages (chat messages)
-- 11. (student_subjects - optional, not used in current implementation)

-- Total Sequences: 10
-- Total Indexes: 5
-- Total Triggers: 2
--   1. update_thread_timestamp  (AFTER INSERT ON feedback_messages)
--   2. trg_attendance_alert     (AFTER INSERT OR UPDATE ON attendance)

-- To initialize database with sample data, run:
-- python backend/setup_complete_system.py
