-- LOCAL TESTING ONLY — do not commit or use in production
-- Stub tables owned by other members, needed for FK constraints during local dev

CREATE TABLE users (
    email VARCHAR2(100) PRIMARY KEY
);

CREATE TABLE departments (
    dept_id NUMBER PRIMARY KEY
);

CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    name       VARCHAR2(100)
);

CREATE TABLE subjects (
    subject_id   NUMBER PRIMARY KEY,
    subject_name VARCHAR2(100),
    faculty_id   NUMBER
);

-- Seed data
INSERT INTO users VALUES ('faculty1@test.com');
INSERT INTO departments VALUES (1);
INSERT INTO departments VALUES (2);

INSERT INTO students VALUES (1, 'Alice Johnson');
INSERT INTO students VALUES (2, 'Bob Smith');
INSERT INTO students VALUES (3, 'Carol White');

INSERT INTO subjects VALUES (1, 'Mathematics', 1);
INSERT INTO subjects VALUES (2, 'Physics', 1);
INSERT INTO subjects VALUES (3, 'Chemistry', 2);

-- Faculty seed (your table)
INSERT INTO faculty (name, email, dept_id, designation)
VALUES ('Dr. Test Faculty', 'faculty1@test.com', 1, 'Professor');

COMMIT;
