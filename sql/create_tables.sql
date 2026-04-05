-- Drop tables if exist
DROP TABLE feedback CASCADE CONSTRAINTS;
DROP TABLE alerts CASCADE CONSTRAINTS;
DROP TABLE attendance CASCADE CONSTRAINTS;
DROP TABLE marks CASCADE CONSTRAINTS;
DROP TABLE subjects CASCADE CONSTRAINTS;
DROP TABLE faculty CASCADE CONSTRAINTS;
DROP TABLE students CASCADE CONSTRAINTS;
DROP TABLE users CASCADE CONSTRAINTS;
DROP TABLE departments CASCADE CONSTRAINTS;
DROP SEQUENCE users_seq;
DROP SEQUENCE students_seq;
DROP SEQUENCE faculty_seq;
DROP SEQUENCE subjects_seq;
DROP SEQUENCE marks_seq;
DROP SEQUENCE attendance_seq;
DROP SEQUENCE alerts_seq;
DROP SEQUENCE feedback_seq;
DROP SEQUENCE departments_seq;

-- Create tables for Student-Faculty Management System

-- Departments
CREATE TABLE departments (
    department_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL
);

-- Users
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password VARCHAR2(255) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) CHECK (role IN ('student', 'faculty')) NOT NULL
);

-- Students
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    department_id NUMBER REFERENCES departments(department_id),
    semester NUMBER,
    cgpa NUMBER(3,2),
    total_credits NUMBER
);

-- Faculty
CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    department_id NUMBER REFERENCES departments(department_id)
);

-- Subjects
CREATE TABLE subjects (
    subject_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    department_id NUMBER REFERENCES departments(department_id),
    faculty_id NUMBER REFERENCES faculty(faculty_id)
);

-- Marks
CREATE TABLE marks (
    mark_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    subject_id NUMBER REFERENCES subjects(subject_id),
    marks NUMBER,
    grade VARCHAR2(2)
);

-- Attendance
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    subject_id NUMBER REFERENCES subjects(subject_id),
    attendance_date DATE NOT NULL,
    status VARCHAR2(10) CHECK (status IN ('present', 'absent')) NOT NULL
);

-- Alerts
CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    message VARCHAR2(500) NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feedback
CREATE TABLE feedback (
    feedback_id NUMBER PRIMARY KEY,
    student_id NUMBER REFERENCES students(student_id),
    faculty_id NUMBER REFERENCES faculty(faculty_id),
    message VARCHAR2(500) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sequences for auto-increment
CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE faculty_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE subjects_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE marks_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE feedback_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE departments_seq START WITH 1 INCREMENT BY 1;