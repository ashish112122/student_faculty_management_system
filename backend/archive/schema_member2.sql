-- Member 2 (RAHUL branch) — Faculty & Marks Module
-- Oracle SQL — creates ONLY the tables owned by Member 2.
-- Do NOT add DDL for users, students, subjects, student_subjects,
-- feedback, attendance, or alerts — those belong to other members.
--
-- Run this AFTER Member 1 has created: users, departments, students, subjects

-- faculty table
CREATE TABLE faculty (
    faculty_id  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR2(100) NOT NULL,
    email       VARCHAR2(100) UNIQUE,
    dept_id     NUMBER,
    designation VARCHAR2(50),
    CONSTRAINT fk_faculty_email   FOREIGN KEY (email)    REFERENCES users(email),
    CONSTRAINT fk_faculty_dept_id FOREIGN KEY (dept_id)  REFERENCES departments(dept_id)
);

-- marks table
CREATE TABLE marks (
    marks_id       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id     NUMBER NOT NULL,
    subject_id     NUMBER NOT NULL,
    marks_obtained NUMBER(5,2) NOT NULL,
    grade          VARCHAR2(2),
    exam_type      VARCHAR2(50) NOT NULL,
    CONSTRAINT chk_marks_range CHECK (marks_obtained BETWEEN 0 AND 100),
    CONSTRAINT fk_marks_student FOREIGN KEY (student_id) REFERENCES students(student_id),
    CONSTRAINT fk_marks_subject FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
