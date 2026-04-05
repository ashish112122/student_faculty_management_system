-- Insert sample data

-- Departments
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Computer Science');
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Electronics');
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Mechanical');
INSERT INTO departments (department_id, name) VALUES (departments_seq.NEXTVAL, 'Civil');

-- Batches (30 students per batch = 5 batches for 150 students)
INSERT INTO batches (batch_id, name) VALUES (batches_seq.NEXTVAL, '2Q31');
INSERT INTO batches (batch_id, name) VALUES (batches_seq.NEXTVAL, '2Q32');
INSERT INTO batches (batch_id, name) VALUES (batches_seq.NEXTVAL, '2Q33');
INSERT INTO batches (batch_id, name) VALUES (batches_seq.NEXTVAL, '2Q34');
INSERT INTO batches (batch_id, name) VALUES (batches_seq.NEXTVAL, '2Q35');

-- Faculty Users
INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, 'faculty1@univ.edu', 'pass123', 'Dr. John Doe', 'faculty');
INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, 'faculty2@univ.edu', 'pass123', 'Dr. Jane Smith', 'faculty');
INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, 'faculty3@univ.edu', 'pass123', 'Dr. Mike Johnson', 'faculty');

-- Faculty table (3 faculty)
INSERT INTO faculty (faculty_id, user_id, department_id) VALUES (faculty_seq.NEXTVAL, 1, 1);
INSERT INTO faculty (faculty_id, user_id, department_id) VALUES (faculty_seq.NEXTVAL, 2, 1);
INSERT INTO faculty (faculty_id, user_id, department_id) VALUES (faculty_seq.NEXTVAL, 3, 1);

-- Subjects (5 subjects for each batch taught by different faculty)
-- Batch 1 (2Q31)
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Data Structures', 1, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Algorithms', 1, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Database Systems', 1, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Web Development', 1, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Software Engineering', 1, 3);

-- Batch 2 (2Q32)
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Data Structures', 2, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Algorithms', 2, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Database Systems', 2, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Web Development', 2, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Software Engineering', 2, 3);

-- Batch 3-5 (similar structure)
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Data Structures', 3, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Algorithms', 3, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Database Systems', 3, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Web Development', 3, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Software Engineering', 3, 3);

INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Data Structures', 4, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Algorithms', 4, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Database Systems', 4, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Web Development', 4, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Software Engineering', 4, 3);

INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Data Structures', 5, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Algorithms', 5, 1);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Database Systems', 5, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Web Development', 5, 2);
INSERT INTO subjects (subject_id, name, batch_id, faculty_id) VALUES (subjects_seq.NEXTVAL, 'Software Engineering', 5, 3);

COMMIT;