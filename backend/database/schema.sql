-- Member 1 Tables (Login & Student Module)

-- Users Table (Shared by all members)
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) NOT NULL CHECK (role IN ('student', 'faculty'))
);

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;

-- Students Table
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    branch VARCHAR2(50) NOT NULL,
    year_of_study NUMBER NOT NULL,
    semester NUMBER NOT NULL,
    section VARCHAR2(10) NOT NULL,
    cgpa NUMBER(3,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1;

-- Subjects Table (Shared)
CREATE TABLE subjects (
    subject_id NUMBER PRIMARY KEY,
    subject_name VARCHAR2(100) NOT NULL,
    subject_code VARCHAR2(20) UNIQUE NOT NULL
);

CREATE SEQUENCE subjects_seq START WITH 1 INCREMENT BY 1;

-- Student Subjects Mapping
CREATE TABLE student_subjects (
    student_subject_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE student_subjects_seq START WITH 1 INCREMENT BY 1;

-- Feedback Table
CREATE TABLE feedback (
    feedback_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    faculty_id NUMBER NOT NULL,
    sender_id NUMBER NOT NULL,
    message CLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (faculty_id) REFERENCES users(user_id),
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
);

CREATE SEQUENCE feedback_seq START WITH 1 INCREMENT BY 1;

-- Member 2 Tables (Faculty & Marks Module)
CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    department VARCHAR2(100) NOT NULL,
    designation VARCHAR2(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE marks (
    mark_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    assessment_type VARCHAR2(20) NOT NULL CHECK (assessment_type IN ('MST', 'EST', 'Assignment', 'Quiz')),
    marks_obtained NUMBER NOT NULL,
    max_marks NUMBER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE marks_seq START WITH 1 INCREMENT BY 1;

-- Member 3 Tables (Attendance & Alerts)
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    attendance_date DATE NOT NULL,
    status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    alert_type VARCHAR2(20) NOT NULL CHECK (alert_type IN ('Warning', 'Alert', 'Critical')),
    message VARCHAR2(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1;
