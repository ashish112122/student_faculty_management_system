-- Drop existing tables if they exist
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE feedback CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE alerts CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE attendance CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE marks CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE faculty_classes CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE subjects CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE students CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE faculty CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE users CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- Create Users table
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) NOT NULL CHECK (role IN ('student', 'faculty'))
);

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;

-- Create Students table
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    name VARCHAR2(100) NOT NULL,
    branch VARCHAR2(50) NOT NULL,
    year_of_study NUMBER NOT NULL,
    semester NUMBER NOT NULL,
    section VARCHAR2(10) NOT NULL,
    class_name VARCHAR2(20) NOT NULL,
    cgpa NUMBER(3,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1;

-- Create Faculty table
CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    name VARCHAR2(100) NOT NULL,
    department VARCHAR2(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1;

-- Create Subjects table
CREATE TABLE subjects (
    subject_id NUMBER PRIMARY KEY,
    subject_name VARCHAR2(100) NOT NULL,
    subject_code VARCHAR2(20) UNIQUE NOT NULL
);

CREATE SEQUENCE subjects_seq START WITH 1 INCREMENT BY 1;

-- Create Faculty Classes mapping
CREATE TABLE faculty_classes (
    faculty_class_id NUMBER PRIMARY KEY,
    faculty_id NUMBER NOT NULL,
    class_name VARCHAR2(20) NOT NULL,
    subject_id NUMBER NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE faculty_classes_seq START WITH 1 INCREMENT BY 1;

-- Create Marks table
CREATE TABLE marks (
    mark_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(20) NOT NULL,
    assessment_type VARCHAR2(20) NOT NULL CHECK (assessment_type IN ('MST', 'EST', 'Quiz', 'Assignment')),
    marks_obtained NUMBER NOT NULL,
    max_marks NUMBER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE marks_seq START WITH 1 INCREMENT BY 1;

-- Create Attendance table
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(20) NOT NULL,
    attendance_date DATE NOT NULL,
    status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1;

-- Create Alerts table with is_read status
CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER,
    alert_type VARCHAR2(20) NOT NULL CHECK (alert_type IN ('Warning', 'Critical')),
    message VARCHAR2(500) NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1;

-- Create Feedback table for threaded chat
CREATE TABLE feedback (
    feedback_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    faculty_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    sender_role VARCHAR2(20) NOT NULL CHECK (sender_role IN ('student', 'faculty')),
    message CLOB NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE feedback_seq START WITH 1 INCREMENT BY 1;

COMMIT;
