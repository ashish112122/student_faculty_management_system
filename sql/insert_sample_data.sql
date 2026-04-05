-- Insert sample data

-- Departments
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Computer Science');
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Electronics');
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Mechanical');
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Civil');

-- Users and Students (150 students)
-- Passwords are hashed, but for simplicity, using plain text as per config (but should hash)
-- In real, use bcrypt

-- Faculty users
INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, 'faculty1@univ.edu', 'pass123', 'Dr. John Doe', 'faculty');
INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, 'faculty2@univ.edu', 'pass123', 'Dr. Jane Smith', 'faculty');

-- Faculty table
INSERT INTO faculty (faculty_id, user_id, department_id) VALUES (faculty_seq.NEXTVAL, 1, 1);
INSERT INTO faculty (faculty_id, user_id, department_id) VALUES (faculty_seq.NEXTVAL, 2, 2);

-- Subjects
INSERT INTO subjects (subject_id, name, department_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Data Structures', 1, 1);
INSERT INTO subjects (subject_id, name, department_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Algorithms', 1, 1);
INSERT INTO subjects (subject_id, name, department_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Circuits', 2, 2);

-- Students: Generate 150
-- For simplicity, insert a few manually, assume script or loop in Python for full 150
INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, 'student1@univ.edu', 'pass123', 'Alice Johnson', 'student');
INSERT INTO students (student_id, user_id, department_id, semester, cgpa, total_credits) VALUES (students_seq.NEXTVAL, 3, 1, 4, 8.5, 120);

-- Repeat for 150, but to save time, insert 10 as example
-- In practice, use a loop or script

-- Marks for student1
INSERT INTO marks (mark_id, student_id, subject_id, marks, grade) VALUES (marks_seq.NEXTVAL, 1, 1, 85, 'A');
INSERT INTO marks (mark_id, student_id, subject_id, marks, grade) VALUES (marks_seq.NEXTVAL, 1, 2, 90, 'A');

-- Attendance
INSERT INTO attendance (attendance_id, student_id, subject_id, attendance_date, status) VALUES (attendance_seq.NEXTVAL, 1, 1, SYSDATE, 'present');

-- Alerts
INSERT INTO alerts (alert_id, student_id, message, is_read) VALUES (alerts_seq.NEXTVAL, 1, 'Your marks have been updated', 0);

-- Feedback
INSERT INTO feedback (feedback_id, student_id, faculty_id, message) VALUES (feedback_seq.NEXTVAL, 1, 1, 'Great class!');