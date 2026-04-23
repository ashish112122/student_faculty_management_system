-- Sample Data Insertion for Student-Faculty Management System
-- This file contains INSERT statements for populating the database with sample data

-- Note: For production use, run backend/setup_complete_system.py which generates
-- 300 students, 5 faculty, and complete attendance/marks data programmatically

-- Insert Sample Users (Faculty)
INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'dr.rajesh@thaparfac.edu', 'pass123', 'Dr. Rajesh Kumar', 'faculty');

INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'prof.meena@thaparfac.edu', 'pass123', 'Prof. Meena Sharma', 'faculty');

INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'dr.suresh@thaparfac.edu', 'pass123', 'Dr. Suresh Patel', 'faculty');

INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'prof.kavita@thaparfac.edu', 'pass123', 'Prof. Kavita Singh', 'faculty');

INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'dr.anil@thaparfac.edu', 'pass123', 'Dr. Anil Verma', 'faculty');

-- Insert Faculty Records
INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (faculty_seq.NEXTVAL, 1, 'Dr. Rajesh Kumar', 'CSE');

INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (faculty_seq.NEXTVAL, 2, 'Prof. Meena Sharma', 'CSE');

INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (faculty_seq.NEXTVAL, 3, 'Dr. Suresh Patel', 'CSE');

INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (faculty_seq.NEXTVAL, 4, 'Prof. Kavita Singh', 'CSE');

INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (faculty_seq.NEXTVAL, 5, 'Dr. Anil Verma', 'CSE');

-- Insert Subjects
INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (subjects_seq.NEXTVAL, 'Data Structures', 'CS401');

INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (subjects_seq.NEXTVAL, 'Algorithms', 'CS402');

INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (subjects_seq.NEXTVAL, 'Database Management', 'CS403');

INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (subjects_seq.NEXTVAL, 'Operating Systems', 'CS404');

INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (subjects_seq.NEXTVAL, 'Computer Networks', 'CS405');

-- Insert Faculty Class Assignments
-- Faculty 1: Data Structures for batches 2Q31, 2Q32, 2Q33
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 1, 1, '2Q31');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 1, 1, '2Q32');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 1, 1, '2Q33');

-- Faculty 2: Algorithms for batches 2Q33, 2Q34, 2Q35
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 2, 2, '2Q33');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 2, 2, '2Q34');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 2, 2, '2Q35');

-- Faculty 3: Database Management for batches 2Q35, 2Q36, 2Q37
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 3, 3, '2Q35');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 3, 3, '2Q36');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 3, 3, '2Q37');

-- Faculty 4: Operating Systems for batches 2Q37, 2Q38, 2Q39
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 4, 4, '2Q37');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 4, 4, '2Q38');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 4, 4, '2Q39');

-- Faculty 5: Computer Networks for batches 2Q39, 2Q40, 2Q31
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 5, 5, '2Q39');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 5, 5, '2Q40');

INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (faculty_classes_seq.NEXTVAL, 5, 5, '2Q31');

-- Insert Sample Students (showing pattern for 3 students, actual system has 300)
INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'rohan.sharma.2q31.0@thapar.edu', 'pass123', 'Rohan Sharma', 'student');

INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (students_seq.NEXTVAL, 6, 'Rohan Sharma', 'CSE', 4, '2Q31', 8.75);

INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'priya.patel.2q31.1@thapar.edu', 'pass123', 'Priya Patel', 'student');

INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (students_seq.NEXTVAL, 7, 'Priya Patel', 'CSE', 4, '2Q31', 9.10);

INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, 'amit.kumar.2q31.2@thapar.edu', 'pass123', 'Amit Kumar', 'student');

INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (students_seq.NEXTVAL, 8, 'Amit Kumar', 'CSE', 4, '2Q31', 7.85);

-- Insert Sample Marks (for student_id 1, subject_id 1)
INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
VALUES (marks_seq.NEXTVAL, 1, 1, '2Q31', 'MST', 25, 30);

INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
VALUES (marks_seq.NEXTVAL, 1, 1, '2Q31', 'EST', 35, 40);

INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
VALUES (marks_seq.NEXTVAL, 1, 1, '2Q31', 'Quiz', 12, 15);

INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
VALUES (marks_seq.NEXTVAL, 1, 1, '2Q31', 'Assignment', 13, 15);

-- Insert Sample Attendance (for student_id 1, subject_id 1)
INSERT INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
VALUES (attendance_seq.NEXTVAL, 1, 1, '2Q31', DATE '2026-01-02', 'P');

INSERT INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
VALUES (attendance_seq.NEXTVAL, 1, 1, '2Q31', DATE '2026-01-03', 'P');

INSERT INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
VALUES (attendance_seq.NEXTVAL, 1, 1, '2Q31', DATE '2026-01-06', 'A');

INSERT INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
VALUES (attendance_seq.NEXTVAL, 1, 1, '2Q31', DATE '2026-01-07', 'P');

-- Insert Sample Alert
INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message, is_read, created_at)
VALUES (alerts_seq.NEXTVAL, 1, 1, 'Warning', 'Low attendance in Data Structures: 72.5%', 0, CURRENT_TIMESTAMP);

COMMIT;

-- Note: For complete data population with 300 students, run:
-- python backend/setup_complete_system.py
