-- STEP 1: subjects
INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (1, 'Data Structures', 'CS401');
INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (2, 'Algorithms', 'CS402');
INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (3, 'Database Management', 'CS403');
INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (4, 'Operating Systems', 'CS404');
INSERT INTO subjects (subject_id, subject_name, subject_code)
VALUES (5, 'Computer Networks', 'CS405');
COMMIT;

-- STEP 2: users table - faculty login credentials
INSERT INTO users (user_id, email, password, name, role)
VALUES (1, 'dr.rajesh@thaparfac.edu', 'pass123', 'Dr. Rajesh Kumar', 'faculty');
INSERT INTO users (user_id, email, password, name, role)
VALUES (2, 'prof.meena@thaparfac.edu', 'pass123', 'Prof. Meena Sharma', 'faculty');
INSERT INTO users (user_id, email, password, name, role)
VALUES (3, 'dr.suresh@thaparfac.edu', 'pass123', 'Dr. Suresh Patel', 'faculty');
INSERT INTO users (user_id, email, password, name, role)
VALUES (4, 'prof.kavita@thaparfac.edu', 'pass123', 'Prof. Kavita Singh', 'faculty');
INSERT INTO users (user_id, email, password, name, role)
VALUES (5, 'dr.anil@thaparfac.edu', 'pass123', 'Dr. Anil Verma', 'faculty');
COMMIT;

-- STEP 3: faculty table
INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (1, 1, 'Dr. Rajesh Kumar', 'CSE');
INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (2, 2, 'Prof. Meena Sharma', 'CSE');
INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (3, 3, 'Dr. Suresh Patel', 'CSE');
INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (4, 4, 'Prof. Kavita Singh', 'CSE');
INSERT INTO faculty (faculty_id, user_id, name, department)
VALUES (5, 5, 'Dr. Anil Verma', 'CSE');
COMMIT;

-- STEP 4: faculty_classes - faculty assigned to subjects and batches
-- 50 rows total: 5 faculty x 10 batches each
-- Faculty: Dr. Rajesh Kumar | Subject: Data Structures
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (141, 1, 1, '2Q31');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (142, 1, 1, '2Q32');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (143, 1, 1, '2Q33');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (144, 1, 1, '2Q34');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (145, 1, 1, '2Q35');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (146, 1, 1, '2Q36');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (147, 1, 1, '2Q37');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (148, 1, 1, '2Q38');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (149, 1, 1, '2Q39');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (150, 1, 1, '2Q40');
-- Faculty: Prof. Meena Sharma | Subject: Algorithms
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (151, 2, 2, '2Q31');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (152, 2, 2, '2Q32');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (153, 2, 2, '2Q33');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (154, 2, 2, '2Q34');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (155, 2, 2, '2Q35');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (156, 2, 2, '2Q36');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (157, 2, 2, '2Q37');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (158, 2, 2, '2Q38');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (159, 2, 2, '2Q39');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (160, 2, 2, '2Q40');
-- Faculty: Dr. Suresh Patel | Subject: Database Management
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (161, 3, 3, '2Q31');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (162, 3, 3, '2Q32');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (163, 3, 3, '2Q33');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (164, 3, 3, '2Q34');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (165, 3, 3, '2Q35');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (166, 3, 3, '2Q36');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (167, 3, 3, '2Q37');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (168, 3, 3, '2Q38');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (169, 3, 3, '2Q39');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (170, 3, 3, '2Q40');
-- Faculty: Prof. Kavita Singh | Subject: Operating Systems
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (171, 4, 4, '2Q31');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (172, 4, 4, '2Q32');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (173, 4, 4, '2Q33');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (174, 4, 4, '2Q34');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (175, 4, 4, '2Q35');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (176, 4, 4, '2Q36');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (177, 4, 4, '2Q37');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (178, 4, 4, '2Q38');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (179, 4, 4, '2Q39');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (180, 4, 4, '2Q40');
-- Faculty: Dr. Anil Verma | Subject: Computer Networks
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (181, 5, 5, '2Q31');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (182, 5, 5, '2Q32');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (183, 5, 5, '2Q33');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (184, 5, 5, '2Q34');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (185, 5, 5, '2Q35');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (186, 5, 5, '2Q36');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (187, 5, 5, '2Q37');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (188, 5, 5, '2Q38');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (189, 5, 5, '2Q39');
INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
VALUES (190, 5, 5, '2Q40');
COMMIT;

-- STEP 5: users table - student login credentials (300 students)
INSERT INTO users (user_id, email, password, name, role)
VALUES (6, 'anjali.reddy.2q31.0@thapar.edu', 'pass123', 'Anjali Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (7, 'varun.mehta.2q31.1@thapar.edu', 'pass123', 'Varun Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (8, 'manish.kumar.2q31.2@thapar.edu', 'pass123', 'Manish Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (9, 'arjun.nair.2q31.3@thapar.edu', 'pass123', 'Arjun Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (10, 'sanjay.mehta.2q31.4@thapar.edu', 'pass123', 'Sanjay Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (11, 'aditya.patel.2q31.5@thapar.edu', 'pass123', 'Aditya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (12, 'megha.nair.2q31.6@thapar.edu', 'pass123', 'Megha Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (13, 'vikram.sharma.2q31.7@thapar.edu', 'pass123', 'Vikram Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (14, 'karan.mehta.2q31.8@thapar.edu', 'pass123', 'Karan Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (15, 'tanvi.mehta.2q31.9@thapar.edu', 'pass123', 'Tanvi Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (16, 'neha.sharma.2q31.10@thapar.edu', 'pass123', 'Neha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (17, 'akash.joshi.2q31.11@thapar.edu', 'pass123', 'Akash Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (18, 'rahul.verma.2q31.12@thapar.edu', 'pass123', 'Rahul Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (19, 'megha.joshi.2q31.13@thapar.edu', 'pass123', 'Megha Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (20, 'rohan.verma.2q31.14@thapar.edu', 'pass123', 'Rohan Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (21, 'shruti.kumar.2q31.15@thapar.edu', 'pass123', 'Shruti Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (22, 'pooja.patel.2q31.16@thapar.edu', 'pass123', 'Pooja Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (23, 'priya.mehta.2q31.17@thapar.edu', 'pass123', 'Priya Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (24, 'arjun.kumar.2q31.18@thapar.edu', 'pass123', 'Arjun Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (25, 'harsh.sharma.2q31.19@thapar.edu', 'pass123', 'Harsh Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (26, 'kavya.patel.2q31.20@thapar.edu', 'pass123', 'Kavya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (27, 'akash.gupta.2q31.21@thapar.edu', 'pass123', 'Akash Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (28, 'karan.nair.2q31.22@thapar.edu', 'pass123', 'Karan Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (29, 'amit.singh.2q31.23@thapar.edu', 'pass123', 'Amit Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (30, 'preeti.reddy.2q31.24@thapar.edu', 'pass123', 'Preeti Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (31, 'rahul.verma.2q31.25@thapar.edu', 'pass123', 'Rahul Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (32, 'harsh.patel.2q31.26@thapar.edu', 'pass123', 'Harsh Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (33, 'aditya.reddy.2q31.27@thapar.edu', 'pass123', 'Aditya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (34, 'ishita.mehta.2q31.28@thapar.edu', 'pass123', 'Ishita Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (35, 'kavya.patel.2q31.29@thapar.edu', 'pass123', 'Kavya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (36, 'varun.nair.2q32.0@thapar.edu', 'pass123', 'Varun Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (37, 'shruti.joshi.2q32.1@thapar.edu', 'pass123', 'Shruti Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (38, 'neha.mehta.2q32.2@thapar.edu', 'pass123', 'Neha Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (39, 'karan.patel.2q32.3@thapar.edu', 'pass123', 'Karan Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (40, 'karan.gupta.2q32.4@thapar.edu', 'pass123', 'Karan Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (41, 'tanvi.joshi.2q32.5@thapar.edu', 'pass123', 'Tanvi Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (42, 'neha.reddy.2q32.6@thapar.edu', 'pass123', 'Neha Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (43, 'nisha.sharma.2q32.7@thapar.edu', 'pass123', 'Nisha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (44, 'rohan.joshi.2q32.8@thapar.edu', 'pass123', 'Rohan Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (45, 'nisha.reddy.2q32.9@thapar.edu', 'pass123', 'Nisha Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (46, 'karan.nair.2q32.10@thapar.edu', 'pass123', 'Karan Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (47, 'tanvi.kumar.2q32.11@thapar.edu', 'pass123', 'Tanvi Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (48, 'amit.mehta.2q32.12@thapar.edu', 'pass123', 'Amit Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (49, 'sanjay.verma.2q32.13@thapar.edu', 'pass123', 'Sanjay Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (50, 'rohan.kumar.2q32.14@thapar.edu', 'pass123', 'Rohan Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (51, 'varun.singh.2q32.15@thapar.edu', 'pass123', 'Varun Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (52, 'ishita.joshi.2q32.16@thapar.edu', 'pass123', 'Ishita Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (53, 'harsh.kumar.2q32.17@thapar.edu', 'pass123', 'Harsh Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (54, 'rohan.joshi.2q32.18@thapar.edu', 'pass123', 'Rohan Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (55, 'rohan.reddy.2q32.19@thapar.edu', 'pass123', 'Rohan Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (56, 'megha.nair.2q32.20@thapar.edu', 'pass123', 'Megha Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (57, 'rohit.gupta.2q32.21@thapar.edu', 'pass123', 'Rohit Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (58, 'priya.patel.2q32.22@thapar.edu', 'pass123', 'Priya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (59, 'neha.singh.2q32.23@thapar.edu', 'pass123', 'Neha Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (60, 'aditya.joshi.2q32.24@thapar.edu', 'pass123', 'Aditya Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (61, 'harsh.sharma.2q32.25@thapar.edu', 'pass123', 'Harsh Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (62, 'sneha.sharma.2q32.26@thapar.edu', 'pass123', 'Sneha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (63, 'manish.reddy.2q32.27@thapar.edu', 'pass123', 'Manish Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (64, 'anjali.joshi.2q32.28@thapar.edu', 'pass123', 'Anjali Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (65, 'karan.gupta.2q32.29@thapar.edu', 'pass123', 'Karan Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (66, 'kavya.nair.2q33.0@thapar.edu', 'pass123', 'Kavya Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (67, 'neha.gupta.2q33.1@thapar.edu', 'pass123', 'Neha Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (68, 'arjun.nair.2q33.2@thapar.edu', 'pass123', 'Arjun Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (69, 'megha.kumar.2q33.3@thapar.edu', 'pass123', 'Megha Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (70, 'harsh.gupta.2q33.4@thapar.edu', 'pass123', 'Harsh Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (71, 'gaurav.patel.2q33.5@thapar.edu', 'pass123', 'Gaurav Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (72, 'ritu.singh.2q33.6@thapar.edu', 'pass123', 'Ritu Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (73, 'vikram.nair.2q33.7@thapar.edu', 'pass123', 'Vikram Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (74, 'ishita.mehta.2q33.8@thapar.edu', 'pass123', 'Ishita Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (75, 'shruti.mehta.2q33.9@thapar.edu', 'pass123', 'Shruti Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (76, 'harsh.verma.2q33.10@thapar.edu', 'pass123', 'Harsh Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (77, 'sneha.sharma.2q33.11@thapar.edu', 'pass123', 'Sneha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (78, 'sanjay.reddy.2q33.12@thapar.edu', 'pass123', 'Sanjay Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (79, 'tanvi.gupta.2q33.13@thapar.edu', 'pass123', 'Tanvi Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (80, 'ritu.mehta.2q33.14@thapar.edu', 'pass123', 'Ritu Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (81, 'rahul.verma.2q33.15@thapar.edu', 'pass123', 'Rahul Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (82, 'preeti.verma.2q33.16@thapar.edu', 'pass123', 'Preeti Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (83, 'swati.sharma.2q33.17@thapar.edu', 'pass123', 'Swati Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (84, 'divya.reddy.2q33.18@thapar.edu', 'pass123', 'Divya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (85, 'priya.kumar.2q33.19@thapar.edu', 'pass123', 'Priya Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (86, 'amit.singh.2q33.20@thapar.edu', 'pass123', 'Amit Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (87, 'manish.verma.2q33.21@thapar.edu', 'pass123', 'Manish Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (88, 'kavya.singh.2q33.22@thapar.edu', 'pass123', 'Kavya Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (89, 'divya.verma.2q33.23@thapar.edu', 'pass123', 'Divya Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (90, 'manish.mehta.2q33.24@thapar.edu', 'pass123', 'Manish Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (91, 'sneha.reddy.2q33.25@thapar.edu', 'pass123', 'Sneha Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (92, 'preeti.gupta.2q33.26@thapar.edu', 'pass123', 'Preeti Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (93, 'swati.sharma.2q33.27@thapar.edu', 'pass123', 'Swati Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (94, 'kavya.patel.2q33.28@thapar.edu', 'pass123', 'Kavya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (95, 'varun.nair.2q33.29@thapar.edu', 'pass123', 'Varun Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (96, 'preeti.patel.2q34.0@thapar.edu', 'pass123', 'Preeti Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (97, 'akash.patel.2q34.1@thapar.edu', 'pass123', 'Akash Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (98, 'manish.reddy.2q34.2@thapar.edu', 'pass123', 'Manish Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (99, 'rohan.sharma.2q34.3@thapar.edu', 'pass123', 'Rohan Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (100, 'shruti.nair.2q34.4@thapar.edu', 'pass123', 'Shruti Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (101, 'nikhil.joshi.2q34.5@thapar.edu', 'pass123', 'Nikhil Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (102, 'karan.joshi.2q34.6@thapar.edu', 'pass123', 'Karan Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (103, 'anjali.joshi.2q34.7@thapar.edu', 'pass123', 'Anjali Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (104, 'nisha.sharma.2q34.8@thapar.edu', 'pass123', 'Nisha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (105, 'aditya.sharma.2q34.9@thapar.edu', 'pass123', 'Aditya Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (106, 'arjun.kumar.2q34.10@thapar.edu', 'pass123', 'Arjun Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (107, 'priya.nair.2q34.11@thapar.edu', 'pass123', 'Priya Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (108, 'preeti.singh.2q34.12@thapar.edu', 'pass123', 'Preeti Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (109, 'divya.joshi.2q34.13@thapar.edu', 'pass123', 'Divya Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (110, 'swati.reddy.2q34.14@thapar.edu', 'pass123', 'Swati Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (111, 'shruti.mehta.2q34.15@thapar.edu', 'pass123', 'Shruti Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (112, 'arjun.mehta.2q34.16@thapar.edu', 'pass123', 'Arjun Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (113, 'varun.nair.2q34.17@thapar.edu', 'pass123', 'Varun Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (114, 'divya.reddy.2q34.18@thapar.edu', 'pass123', 'Divya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (115, 'megha.gupta.2q34.19@thapar.edu', 'pass123', 'Megha Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (116, 'kavya.reddy.2q34.20@thapar.edu', 'pass123', 'Kavya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (117, 'sneha.patel.2q34.21@thapar.edu', 'pass123', 'Sneha Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (118, 'kavya.mehta.2q34.22@thapar.edu', 'pass123', 'Kavya Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (119, 'sanjay.verma.2q34.23@thapar.edu', 'pass123', 'Sanjay Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (120, 'pooja.reddy.2q34.24@thapar.edu', 'pass123', 'Pooja Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (121, 'rahul.singh.2q34.25@thapar.edu', 'pass123', 'Rahul Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (122, 'megha.nair.2q34.26@thapar.edu', 'pass123', 'Megha Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (123, 'nikhil.nair.2q34.27@thapar.edu', 'pass123', 'Nikhil Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (124, 'swati.gupta.2q34.28@thapar.edu', 'pass123', 'Swati Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (125, 'kavya.patel.2q34.29@thapar.edu', 'pass123', 'Kavya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (126, 'megha.sharma.2q35.0@thapar.edu', 'pass123', 'Megha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (127, 'preeti.mehta.2q35.1@thapar.edu', 'pass123', 'Preeti Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (128, 'vikram.reddy.2q35.2@thapar.edu', 'pass123', 'Vikram Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (129, 'swati.gupta.2q35.3@thapar.edu', 'pass123', 'Swati Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (130, 'ritu.reddy.2q35.4@thapar.edu', 'pass123', 'Ritu Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (131, 'shruti.sharma.2q35.5@thapar.edu', 'pass123', 'Shruti Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (132, 'sanjay.gupta.2q35.6@thapar.edu', 'pass123', 'Sanjay Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (133, 'aditya.patel.2q35.7@thapar.edu', 'pass123', 'Aditya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (134, 'megha.sharma.2q35.8@thapar.edu', 'pass123', 'Megha Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (135, 'sanjay.gupta.2q35.9@thapar.edu', 'pass123', 'Sanjay Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (136, 'sneha.gupta.2q35.10@thapar.edu', 'pass123', 'Sneha Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (137, 'amit.mehta.2q35.11@thapar.edu', 'pass123', 'Amit Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (138, 'preeti.nair.2q35.12@thapar.edu', 'pass123', 'Preeti Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (139, 'anjali.kumar.2q35.13@thapar.edu', 'pass123', 'Anjali Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (140, 'amit.singh.2q35.14@thapar.edu', 'pass123', 'Amit Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (141, 'neha.gupta.2q35.15@thapar.edu', 'pass123', 'Neha Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (142, 'aditya.kumar.2q35.16@thapar.edu', 'pass123', 'Aditya Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (143, 'varun.verma.2q35.17@thapar.edu', 'pass123', 'Varun Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (144, 'swati.verma.2q35.18@thapar.edu', 'pass123', 'Swati Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (145, 'vikram.sharma.2q35.19@thapar.edu', 'pass123', 'Vikram Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (146, 'aditya.gupta.2q35.20@thapar.edu', 'pass123', 'Aditya Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (147, 'ritu.reddy.2q35.21@thapar.edu', 'pass123', 'Ritu Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (148, 'varun.kumar.2q35.22@thapar.edu', 'pass123', 'Varun Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (149, 'anjali.singh.2q35.23@thapar.edu', 'pass123', 'Anjali Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (150, 'rohan.mehta.2q35.24@thapar.edu', 'pass123', 'Rohan Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (151, 'preeti.kumar.2q35.25@thapar.edu', 'pass123', 'Preeti Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (152, 'neha.joshi.2q35.26@thapar.edu', 'pass123', 'Neha Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (153, 'varun.sharma.2q35.27@thapar.edu', 'pass123', 'Varun Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (154, 'shruti.singh.2q35.28@thapar.edu', 'pass123', 'Shruti Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (155, 'gaurav.singh.2q35.29@thapar.edu', 'pass123', 'Gaurav Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (156, 'pooja.sharma.2q36.0@thapar.edu', 'pass123', 'Pooja Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (157, 'karan.mehta.2q36.1@thapar.edu', 'pass123', 'Karan Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (158, 'megha.gupta.2q36.2@thapar.edu', 'pass123', 'Megha Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (159, 'ritu.mehta.2q36.3@thapar.edu', 'pass123', 'Ritu Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (160, 'rohit.sharma.2q36.4@thapar.edu', 'pass123', 'Rohit Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (161, 'gaurav.gupta.2q36.5@thapar.edu', 'pass123', 'Gaurav Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (162, 'swati.nair.2q36.6@thapar.edu', 'pass123', 'Swati Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (163, 'amit.joshi.2q36.7@thapar.edu', 'pass123', 'Amit Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (164, 'manish.nair.2q36.8@thapar.edu', 'pass123', 'Manish Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (165, 'pooja.gupta.2q36.9@thapar.edu', 'pass123', 'Pooja Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (166, 'nikhil.verma.2q36.10@thapar.edu', 'pass123', 'Nikhil Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (167, 'sneha.kumar.2q36.11@thapar.edu', 'pass123', 'Sneha Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (168, 'vikram.singh.2q36.12@thapar.edu', 'pass123', 'Vikram Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (169, 'akash.kumar.2q36.13@thapar.edu', 'pass123', 'Akash Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (170, 'preeti.singh.2q36.14@thapar.edu', 'pass123', 'Preeti Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (171, 'preeti.gupta.2q36.15@thapar.edu', 'pass123', 'Preeti Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (172, 'nisha.singh.2q36.16@thapar.edu', 'pass123', 'Nisha Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (173, 'amit.patel.2q36.17@thapar.edu', 'pass123', 'Amit Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (174, 'nisha.reddy.2q36.18@thapar.edu', 'pass123', 'Nisha Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (175, 'sneha.reddy.2q36.19@thapar.edu', 'pass123', 'Sneha Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (176, 'gaurav.nair.2q36.20@thapar.edu', 'pass123', 'Gaurav Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (177, 'sanjay.kumar.2q36.21@thapar.edu', 'pass123', 'Sanjay Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (178, 'arjun.kumar.2q36.22@thapar.edu', 'pass123', 'Arjun Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (179, 'vikram.singh.2q36.23@thapar.edu', 'pass123', 'Vikram Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (180, 'manish.verma.2q36.24@thapar.edu', 'pass123', 'Manish Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (181, 'swati.mehta.2q36.25@thapar.edu', 'pass123', 'Swati Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (182, 'rahul.gupta.2q36.26@thapar.edu', 'pass123', 'Rahul Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (183, 'pooja.reddy.2q36.27@thapar.edu', 'pass123', 'Pooja Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (184, 'manish.kumar.2q36.28@thapar.edu', 'pass123', 'Manish Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (185, 'ritu.mehta.2q36.29@thapar.edu', 'pass123', 'Ritu Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (186, 'rahul.kumar.2q37.0@thapar.edu', 'pass123', 'Rahul Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (187, 'ishita.verma.2q37.1@thapar.edu', 'pass123', 'Ishita Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (188, 'gaurav.nair.2q37.2@thapar.edu', 'pass123', 'Gaurav Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (189, 'rohan.mehta.2q37.3@thapar.edu', 'pass123', 'Rohan Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (190, 'akash.kumar.2q37.4@thapar.edu', 'pass123', 'Akash Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (191, 'kavya.singh.2q37.5@thapar.edu', 'pass123', 'Kavya Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (192, 'neha.nair.2q37.6@thapar.edu', 'pass123', 'Neha Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (193, 'priya.mehta.2q37.7@thapar.edu', 'pass123', 'Priya Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (194, 'anjali.sharma.2q37.8@thapar.edu', 'pass123', 'Anjali Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (195, 'aditya.verma.2q37.9@thapar.edu', 'pass123', 'Aditya Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (196, 'rahul.kumar.2q37.10@thapar.edu', 'pass123', 'Rahul Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (197, 'ishita.gupta.2q37.11@thapar.edu', 'pass123', 'Ishita Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (198, 'neha.reddy.2q37.12@thapar.edu', 'pass123', 'Neha Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (199, 'ritu.patel.2q37.13@thapar.edu', 'pass123', 'Ritu Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (200, 'arjun.singh.2q37.14@thapar.edu', 'pass123', 'Arjun Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (201, 'manish.mehta.2q37.15@thapar.edu', 'pass123', 'Manish Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (202, 'varun.singh.2q37.16@thapar.edu', 'pass123', 'Varun Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (203, 'ishita.joshi.2q37.17@thapar.edu', 'pass123', 'Ishita Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (204, 'preeti.gupta.2q37.18@thapar.edu', 'pass123', 'Preeti Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (205, 'anjali.singh.2q37.19@thapar.edu', 'pass123', 'Anjali Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (206, 'harsh.nair.2q37.20@thapar.edu', 'pass123', 'Harsh Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (207, 'swati.joshi.2q37.21@thapar.edu', 'pass123', 'Swati Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (208, 'preeti.kumar.2q37.22@thapar.edu', 'pass123', 'Preeti Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (209, 'ishita.mehta.2q37.23@thapar.edu', 'pass123', 'Ishita Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (210, 'sneha.singh.2q37.24@thapar.edu', 'pass123', 'Sneha Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (211, 'preeti.nair.2q37.25@thapar.edu', 'pass123', 'Preeti Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (212, 'rohit.gupta.2q37.26@thapar.edu', 'pass123', 'Rohit Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (213, 'tanvi.mehta.2q37.27@thapar.edu', 'pass123', 'Tanvi Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (214, 'anjali.verma.2q37.28@thapar.edu', 'pass123', 'Anjali Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (215, 'divya.reddy.2q37.29@thapar.edu', 'pass123', 'Divya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (216, 'sneha.singh.2q38.0@thapar.edu', 'pass123', 'Sneha Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (217, 'preeti.mehta.2q38.1@thapar.edu', 'pass123', 'Preeti Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (218, 'aditya.joshi.2q38.2@thapar.edu', 'pass123', 'Aditya Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (219, 'priya.verma.2q38.3@thapar.edu', 'pass123', 'Priya Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (220, 'rohan.gupta.2q38.4@thapar.edu', 'pass123', 'Rohan Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (221, 'ishita.singh.2q38.5@thapar.edu', 'pass123', 'Ishita Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (222, 'gaurav.patel.2q38.6@thapar.edu', 'pass123', 'Gaurav Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (223, 'neha.verma.2q38.7@thapar.edu', 'pass123', 'Neha Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (224, 'divya.sharma.2q38.8@thapar.edu', 'pass123', 'Divya Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (225, 'akash.reddy.2q38.9@thapar.edu', 'pass123', 'Akash Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (226, 'manish.patel.2q38.10@thapar.edu', 'pass123', 'Manish Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (227, 'vikram.reddy.2q38.11@thapar.edu', 'pass123', 'Vikram Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (228, 'karan.singh.2q38.12@thapar.edu', 'pass123', 'Karan Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (229, 'nikhil.gupta.2q38.13@thapar.edu', 'pass123', 'Nikhil Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (230, 'shruti.gupta.2q38.14@thapar.edu', 'pass123', 'Shruti Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (231, 'akash.gupta.2q38.15@thapar.edu', 'pass123', 'Akash Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (232, 'kavya.gupta.2q38.16@thapar.edu', 'pass123', 'Kavya Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (233, 'aditya.mehta.2q38.17@thapar.edu', 'pass123', 'Aditya Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (234, 'manish.gupta.2q38.18@thapar.edu', 'pass123', 'Manish Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (235, 'preeti.verma.2q38.19@thapar.edu', 'pass123', 'Preeti Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (236, 'sanjay.sharma.2q38.20@thapar.edu', 'pass123', 'Sanjay Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (237, 'divya.verma.2q38.21@thapar.edu', 'pass123', 'Divya Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (238, 'varun.nair.2q38.22@thapar.edu', 'pass123', 'Varun Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (239, 'preeti.joshi.2q38.23@thapar.edu', 'pass123', 'Preeti Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (240, 'ishita.singh.2q38.24@thapar.edu', 'pass123', 'Ishita Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (241, 'swati.sharma.2q38.25@thapar.edu', 'pass123', 'Swati Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (242, 'pooja.kumar.2q38.26@thapar.edu', 'pass123', 'Pooja Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (243, 'swati.patel.2q38.27@thapar.edu', 'pass123', 'Swati Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (244, 'kavya.verma.2q38.28@thapar.edu', 'pass123', 'Kavya Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (245, 'gaurav.singh.2q38.29@thapar.edu', 'pass123', 'Gaurav Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (246, 'arjun.mehta.2q39.0@thapar.edu', 'pass123', 'Arjun Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (247, 'anjali.reddy.2q39.1@thapar.edu', 'pass123', 'Anjali Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (248, 'akash.nair.2q39.2@thapar.edu', 'pass123', 'Akash Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (249, 'varun.gupta.2q39.3@thapar.edu', 'pass123', 'Varun Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (250, 'pooja.mehta.2q39.4@thapar.edu', 'pass123', 'Pooja Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (251, 'gaurav.kumar.2q39.5@thapar.edu', 'pass123', 'Gaurav Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (252, 'amit.sharma.2q39.6@thapar.edu', 'pass123', 'Amit Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (253, 'arjun.kumar.2q39.7@thapar.edu', 'pass123', 'Arjun Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (254, 'tanvi.kumar.2q39.8@thapar.edu', 'pass123', 'Tanvi Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (255, 'sneha.kumar.2q39.9@thapar.edu', 'pass123', 'Sneha Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (256, 'priya.reddy.2q39.10@thapar.edu', 'pass123', 'Priya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (257, 'preeti.gupta.2q39.11@thapar.edu', 'pass123', 'Preeti Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (258, 'gaurav.joshi.2q39.12@thapar.edu', 'pass123', 'Gaurav Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (259, 'shruti.sharma.2q39.13@thapar.edu', 'pass123', 'Shruti Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (260, 'aditya.reddy.2q39.14@thapar.edu', 'pass123', 'Aditya Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (261, 'kavya.singh.2q39.15@thapar.edu', 'pass123', 'Kavya Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (262, 'varun.gupta.2q39.16@thapar.edu', 'pass123', 'Varun Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (263, 'rahul.reddy.2q39.17@thapar.edu', 'pass123', 'Rahul Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (264, 'nikhil.mehta.2q39.18@thapar.edu', 'pass123', 'Nikhil Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (265, 'nikhil.singh.2q39.19@thapar.edu', 'pass123', 'Nikhil Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (266, 'sanjay.verma.2q39.20@thapar.edu', 'pass123', 'Sanjay Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (267, 'tanvi.sharma.2q39.21@thapar.edu', 'pass123', 'Tanvi Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (268, 'arjun.singh.2q39.22@thapar.edu', 'pass123', 'Arjun Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (269, 'amit.gupta.2q39.23@thapar.edu', 'pass123', 'Amit Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (270, 'aditya.nair.2q39.24@thapar.edu', 'pass123', 'Aditya Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (271, 'shruti.nair.2q39.25@thapar.edu', 'pass123', 'Shruti Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (272, 'harsh.gupta.2q39.26@thapar.edu', 'pass123', 'Harsh Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (273, 'shruti.nair.2q39.27@thapar.edu', 'pass123', 'Shruti Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (274, 'priya.nair.2q39.28@thapar.edu', 'pass123', 'Priya Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (275, 'amit.singh.2q39.29@thapar.edu', 'pass123', 'Amit Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (276, 'harsh.joshi.2q40.0@thapar.edu', 'pass123', 'Harsh Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (277, 'divya.patel.2q40.1@thapar.edu', 'pass123', 'Divya Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (278, 'anjali.verma.2q40.2@thapar.edu', 'pass123', 'Anjali Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (279, 'harsh.singh.2q40.3@thapar.edu', 'pass123', 'Harsh Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (280, 'sneha.joshi.2q40.4@thapar.edu', 'pass123', 'Sneha Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (281, 'preeti.verma.2q40.5@thapar.edu', 'pass123', 'Preeti Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (282, 'karan.verma.2q40.6@thapar.edu', 'pass123', 'Karan Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (283, 'shruti.verma.2q40.7@thapar.edu', 'pass123', 'Shruti Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (284, 'swati.gupta.2q40.8@thapar.edu', 'pass123', 'Swati Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (285, 'megha.nair.2q40.9@thapar.edu', 'pass123', 'Megha Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (286, 'manish.mehta.2q40.10@thapar.edu', 'pass123', 'Manish Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (287, 'manish.singh.2q40.11@thapar.edu', 'pass123', 'Manish Singh', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (288, 'anjali.gupta.2q40.12@thapar.edu', 'pass123', 'Anjali Gupta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (289, 'akash.joshi.2q40.13@thapar.edu', 'pass123', 'Akash Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (290, 'anjali.mehta.2q40.14@thapar.edu', 'pass123', 'Anjali Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (291, 'preeti.reddy.2q40.15@thapar.edu', 'pass123', 'Preeti Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (292, 'neha.nair.2q40.16@thapar.edu', 'pass123', 'Neha Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (293, 'nisha.verma.2q40.17@thapar.edu', 'pass123', 'Nisha Verma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (294, 'shruti.patel.2q40.18@thapar.edu', 'pass123', 'Shruti Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (295, 'rahul.nair.2q40.19@thapar.edu', 'pass123', 'Rahul Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (296, 'nisha.patel.2q40.20@thapar.edu', 'pass123', 'Nisha Patel', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (297, 'sneha.joshi.2q40.21@thapar.edu', 'pass123', 'Sneha Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (298, 'manish.mehta.2q40.22@thapar.edu', 'pass123', 'Manish Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (299, 'vikram.joshi.2q40.23@thapar.edu', 'pass123', 'Vikram Joshi', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (300, 'neha.kumar.2q40.24@thapar.edu', 'pass123', 'Neha Kumar', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (301, 'priya.sharma.2q40.25@thapar.edu', 'pass123', 'Priya Sharma', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (302, 'rahul.mehta.2q40.26@thapar.edu', 'pass123', 'Rahul Mehta', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (303, 'rohit.nair.2q40.27@thapar.edu', 'pass123', 'Rohit Nair', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (304, 'anjali.reddy.2q40.28@thapar.edu', 'pass123', 'Anjali Reddy', 'student');
INSERT INTO users (user_id, email, password, name, role)
VALUES (305, 'arjun.sharma.2q40.29@thapar.edu', 'pass123', 'Arjun Sharma', 'student');
COMMIT;

-- STEP 6: students table (300 students)
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (1, 6, 'Anjali Reddy', 'CSE', 4, '2Q31', 7.91);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (2, 7, 'Varun Mehta', 'CSE', 4, '2Q31', 8.12);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (3, 8, 'Manish Kumar', 'CSE', 4, '2Q31', 7.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (4, 9, 'Arjun Nair', 'CSE', 4, '2Q31', 9.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (5, 10, 'Sanjay Mehta', 'CSE', 4, '2Q31', 6.55);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (6, 11, 'Aditya Patel', 'CSE', 4, '2Q31', 8.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (7, 12, 'Megha Nair', 'CSE', 4, '2Q31', 6.55);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (8, 13, 'Vikram Sharma', 'CSE', 4, '2Q31', 6.8);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (9, 14, 'Karan Mehta', 'CSE', 4, '2Q31', 6.81);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (10, 15, 'Tanvi Mehta', 'CSE', 4, '2Q31', 7.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (11, 16, 'Neha Sharma', 'CSE', 4, '2Q31', 7.19);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (12, 17, 'Akash Joshi', 'CSE', 4, '2Q31', 7.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (13, 18, 'Rahul Verma', 'CSE', 4, '2Q31', 6.51);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (14, 19, 'Megha Joshi', 'CSE', 4, '2Q31', 9.07);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (15, 20, 'Rohan Verma', 'CSE', 4, '2Q31', 8.83);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (16, 21, 'Shruti Kumar', 'CSE', 4, '2Q31', 8.23);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (17, 22, 'Pooja Patel', 'CSE', 4, '2Q31', 7.97);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (18, 23, 'Priya Mehta', 'CSE', 4, '2Q31', 7.74);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (19, 24, 'Arjun Kumar', 'CSE', 4, '2Q31', 8.91);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (20, 25, 'Harsh Sharma', 'CSE', 4, '2Q31', 7.91);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (21, 26, 'Kavya Patel', 'CSE', 4, '2Q31', 8.02);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (22, 27, 'Akash Gupta', 'CSE', 4, '2Q31', 8.56);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (23, 28, 'Karan Nair', 'CSE', 4, '2Q31', 6.9);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (24, 29, 'Amit Singh', 'CSE', 4, '2Q31', 8.83);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (25, 30, 'Preeti Reddy', 'CSE', 4, '2Q31', 8.74);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (26, 31, 'Rahul Verma', 'CSE', 4, '2Q31', 8.02);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (27, 32, 'Harsh Patel', 'CSE', 4, '2Q31', 6.97);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (28, 33, 'Aditya Reddy', 'CSE', 4, '2Q31', 9.23);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (29, 34, 'Ishita Mehta', 'CSE', 4, '2Q31', 9.48);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (30, 35, 'Kavya Patel', 'CSE', 4, '2Q31', 8.49);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (31, 36, 'Varun Nair', 'CSE', 4, '2Q32', 6.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (32, 37, 'Shruti Joshi', 'CSE', 4, '2Q32', 7.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (33, 38, 'Neha Mehta', 'CSE', 4, '2Q32', 7.09);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (34, 39, 'Karan Patel', 'CSE', 4, '2Q32', 7.46);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (35, 40, 'Karan Gupta', 'CSE', 4, '2Q32', 8.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (36, 41, 'Tanvi Joshi', 'CSE', 4, '2Q32', 8.76);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (37, 42, 'Neha Reddy', 'CSE', 4, '2Q32', 9.02);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (38, 43, 'Nisha Sharma', 'CSE', 4, '2Q32', 7.23);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (39, 44, 'Rohan Joshi', 'CSE', 4, '2Q32', 7.35);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (40, 45, 'Nisha Reddy', 'CSE', 4, '2Q32', 6.51);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (41, 46, 'Karan Nair', 'CSE', 4, '2Q32', 8.93);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (42, 47, 'Tanvi Kumar', 'CSE', 4, '2Q32', 6.97);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (43, 48, 'Amit Mehta', 'CSE', 4, '2Q32', 7.36);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (44, 49, 'Sanjay Verma', 'CSE', 4, '2Q32', 6.77);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (45, 50, 'Rohan Kumar', 'CSE', 4, '2Q32', 8.85);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (46, 51, 'Varun Singh', 'CSE', 4, '2Q32', 7.49);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (47, 52, 'Ishita Joshi', 'CSE', 4, '2Q32', 8.46);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (48, 53, 'Harsh Kumar', 'CSE', 4, '2Q32', 8.32);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (49, 54, 'Rohan Joshi', 'CSE', 4, '2Q32', 8.74);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (50, 55, 'Rohan Reddy', 'CSE', 4, '2Q32', 8.66);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (51, 56, 'Megha Nair', 'CSE', 4, '2Q32', 6.72);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (52, 57, 'Rohit Gupta', 'CSE', 4, '2Q32', 8.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (53, 58, 'Priya Patel', 'CSE', 4, '2Q32', 7.67);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (54, 59, 'Neha Singh', 'CSE', 4, '2Q32', 7.99);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (55, 60, 'Aditya Joshi', 'CSE', 4, '2Q32', 6.65);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (56, 61, 'Harsh Sharma', 'CSE', 4, '2Q32', 7.91);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (57, 62, 'Sneha Sharma', 'CSE', 4, '2Q32', 7.99);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (58, 63, 'Manish Reddy', 'CSE', 4, '2Q32', 7.68);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (59, 64, 'Anjali Joshi', 'CSE', 4, '2Q32', 9.09);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (60, 65, 'Karan Gupta', 'CSE', 4, '2Q32', 9.36);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (61, 66, 'Kavya Nair', 'CSE', 4, '2Q33', 6.52);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (62, 67, 'Neha Gupta', 'CSE', 4, '2Q33', 7.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (63, 68, 'Arjun Nair', 'CSE', 4, '2Q33', 8.1);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (64, 69, 'Megha Kumar', 'CSE', 4, '2Q33', 7.16);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (65, 70, 'Harsh Gupta', 'CSE', 4, '2Q33', 7.4);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (66, 71, 'Gaurav Patel', 'CSE', 4, '2Q33', 7.08);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (67, 72, 'Ritu Singh', 'CSE', 4, '2Q33', 8.24);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (68, 73, 'Vikram Nair', 'CSE', 4, '2Q33', 9.31);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (69, 74, 'Ishita Mehta', 'CSE', 4, '2Q33', 8.21);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (70, 75, 'Shruti Mehta', 'CSE', 4, '2Q33', 7.83);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (71, 76, 'Harsh Verma', 'CSE', 4, '2Q33', 9.48);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (72, 77, 'Sneha Sharma', 'CSE', 4, '2Q33', 6.51);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (73, 78, 'Sanjay Reddy', 'CSE', 4, '2Q33', 7.58);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (74, 79, 'Tanvi Gupta', 'CSE', 4, '2Q33', 6.7);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (75, 80, 'Ritu Mehta', 'CSE', 4, '2Q33', 7.34);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (76, 81, 'Rahul Verma', 'CSE', 4, '2Q33', 8.49);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (77, 82, 'Preeti Verma', 'CSE', 4, '2Q33', 7.34);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (78, 83, 'Swati Sharma', 'CSE', 4, '2Q33', 9.04);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (79, 84, 'Divya Reddy', 'CSE', 4, '2Q33', 6.7);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (80, 85, 'Priya Kumar', 'CSE', 4, '2Q33', 8.05);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (81, 86, 'Amit Singh', 'CSE', 4, '2Q33', 8.36);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (82, 87, 'Manish Verma', 'CSE', 4, '2Q33', 7.77);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (83, 88, 'Kavya Singh', 'CSE', 4, '2Q33', 7.89);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (84, 89, 'Divya Verma', 'CSE', 4, '2Q33', 7.09);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (85, 90, 'Manish Mehta', 'CSE', 4, '2Q33', 8.13);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (86, 91, 'Sneha Reddy', 'CSE', 4, '2Q33', 9.17);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (87, 92, 'Preeti Gupta', 'CSE', 4, '2Q33', 7.47);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (88, 93, 'Swati Sharma', 'CSE', 4, '2Q33', 7.01);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (89, 94, 'Kavya Patel', 'CSE', 4, '2Q33', 7.99);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (90, 95, 'Varun Nair', 'CSE', 4, '2Q33', 7.45);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (91, 96, 'Preeti Patel', 'CSE', 4, '2Q34', 8.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (92, 97, 'Akash Patel', 'CSE', 4, '2Q34', 8.31);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (93, 98, 'Manish Reddy', 'CSE', 4, '2Q34', 6.77);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (94, 99, 'Rohan Sharma', 'CSE', 4, '2Q34', 6.56);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (95, 100, 'Shruti Nair', 'CSE', 4, '2Q34', 9.2);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (96, 101, 'Nikhil Joshi', 'CSE', 4, '2Q34', 7.65);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (97, 102, 'Karan Joshi', 'CSE', 4, '2Q34', 7.44);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (98, 103, 'Anjali Joshi', 'CSE', 4, '2Q34', 7.32);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (99, 104, 'Nisha Sharma', 'CSE', 4, '2Q34', 8.45);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (100, 105, 'Aditya Sharma', 'CSE', 4, '2Q34', 8.86);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (101, 106, 'Arjun Kumar', 'CSE', 4, '2Q34', 9.18);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (102, 107, 'Priya Nair', 'CSE', 4, '2Q34', 8.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (103, 108, 'Preeti Singh', 'CSE', 4, '2Q34', 9.16);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (104, 109, 'Divya Joshi', 'CSE', 4, '2Q34', 7.14);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (105, 110, 'Swati Reddy', 'CSE', 4, '2Q34', 7.5);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (106, 111, 'Shruti Mehta', 'CSE', 4, '2Q34', 9.4);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (107, 112, 'Arjun Mehta', 'CSE', 4, '2Q34', 7.66);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (108, 113, 'Varun Nair', 'CSE', 4, '2Q34', 7.46);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (109, 114, 'Divya Reddy', 'CSE', 4, '2Q34', 7.37);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (110, 115, 'Megha Gupta', 'CSE', 4, '2Q34', 8.25);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (111, 116, 'Kavya Reddy', 'CSE', 4, '2Q34', 8.49);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (112, 117, 'Sneha Patel', 'CSE', 4, '2Q34', 7.79);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (113, 118, 'Kavya Mehta', 'CSE', 4, '2Q34', 6.81);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (114, 119, 'Sanjay Verma', 'CSE', 4, '2Q34', 7.1);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (115, 120, 'Pooja Reddy', 'CSE', 4, '2Q34', 8.12);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (116, 121, 'Rahul Singh', 'CSE', 4, '2Q34', 8.72);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (117, 122, 'Megha Nair', 'CSE', 4, '2Q34', 8.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (118, 123, 'Nikhil Nair', 'CSE', 4, '2Q34', 9.45);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (119, 124, 'Swati Gupta', 'CSE', 4, '2Q34', 9.41);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (120, 125, 'Kavya Patel', 'CSE', 4, '2Q34', 8.52);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (121, 126, 'Megha Sharma', 'CSE', 4, '2Q35', 7.02);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (122, 127, 'Preeti Mehta', 'CSE', 4, '2Q35', 9.49);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (123, 128, 'Vikram Reddy', 'CSE', 4, '2Q35', 8.76);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (124, 129, 'Swati Gupta', 'CSE', 4, '2Q35', 8.92);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (125, 130, 'Ritu Reddy', 'CSE', 4, '2Q35', 9.17);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (126, 131, 'Shruti Sharma', 'CSE', 4, '2Q35', 8.39);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (127, 132, 'Sanjay Gupta', 'CSE', 4, '2Q35', 8.48);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (128, 133, 'Aditya Patel', 'CSE', 4, '2Q35', 9.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (129, 134, 'Megha Sharma', 'CSE', 4, '2Q35', 9.16);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (130, 135, 'Sanjay Gupta', 'CSE', 4, '2Q35', 8.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (131, 136, 'Sneha Gupta', 'CSE', 4, '2Q35', 8.7);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (132, 137, 'Amit Mehta', 'CSE', 4, '2Q35', 7.71);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (133, 138, 'Preeti Nair', 'CSE', 4, '2Q35', 6.78);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (134, 139, 'Anjali Kumar', 'CSE', 4, '2Q35', 6.57);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (135, 140, 'Amit Singh', 'CSE', 4, '2Q35', 9.07);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (136, 141, 'Neha Gupta', 'CSE', 4, '2Q35', 7.64);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (137, 142, 'Aditya Kumar', 'CSE', 4, '2Q35', 6.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (138, 143, 'Varun Verma', 'CSE', 4, '2Q35', 7.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (139, 144, 'Swati Verma', 'CSE', 4, '2Q35', 8.51);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (140, 145, 'Vikram Sharma', 'CSE', 4, '2Q35', 8.26);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (141, 146, 'Aditya Gupta', 'CSE', 4, '2Q35', 8.79);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (142, 147, 'Ritu Reddy', 'CSE', 4, '2Q35', 7.44);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (143, 148, 'Varun Kumar', 'CSE', 4, '2Q35', 8.54);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (144, 149, 'Anjali Singh', 'CSE', 4, '2Q35', 6.7);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (145, 150, 'Rohan Mehta', 'CSE', 4, '2Q35', 7.86);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (146, 151, 'Preeti Kumar', 'CSE', 4, '2Q35', 7.43);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (147, 152, 'Neha Joshi', 'CSE', 4, '2Q35', 7.7);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (148, 153, 'Varun Sharma', 'CSE', 4, '2Q35', 7.82);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (149, 154, 'Shruti Singh', 'CSE', 4, '2Q35', 8.17);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (150, 155, 'Gaurav Singh', 'CSE', 4, '2Q35', 6.87);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (151, 156, 'Pooja Sharma', 'CSE', 4, '2Q36', 8.89);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (152, 157, 'Karan Mehta', 'CSE', 4, '2Q36', 8.89);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (153, 158, 'Megha Gupta', 'CSE', 4, '2Q36', 8.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (154, 159, 'Ritu Mehta', 'CSE', 4, '2Q36', 9.14);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (155, 160, 'Rohit Sharma', 'CSE', 4, '2Q36', 7.74);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (156, 161, 'Gaurav Gupta', 'CSE', 4, '2Q36', 6.77);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (157, 162, 'Swati Nair', 'CSE', 4, '2Q36', 7.64);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (158, 163, 'Amit Joshi', 'CSE', 4, '2Q36', 7.51);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (159, 164, 'Manish Nair', 'CSE', 4, '2Q36', 8.19);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (160, 165, 'Pooja Gupta', 'CSE', 4, '2Q36', 7.64);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (161, 166, 'Nikhil Verma', 'CSE', 4, '2Q36', 9.34);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (162, 167, 'Sneha Kumar', 'CSE', 4, '2Q36', 8.96);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (163, 168, 'Vikram Singh', 'CSE', 4, '2Q36', 8.81);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (164, 169, 'Akash Kumar', 'CSE', 4, '2Q36', 7.23);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (165, 170, 'Preeti Singh', 'CSE', 4, '2Q36', 6.71);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (166, 171, 'Preeti Gupta', 'CSE', 4, '2Q36', 9.35);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (167, 172, 'Nisha Singh', 'CSE', 4, '2Q36', 9.09);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (168, 173, 'Amit Patel', 'CSE', 4, '2Q36', 9.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (169, 174, 'Nisha Reddy', 'CSE', 4, '2Q36', 8.55);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (170, 175, 'Sneha Reddy', 'CSE', 4, '2Q36', 6.93);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (171, 176, 'Gaurav Nair', 'CSE', 4, '2Q36', 9.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (172, 177, 'Sanjay Kumar', 'CSE', 4, '2Q36', 7.78);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (173, 178, 'Arjun Kumar', 'CSE', 4, '2Q36', 7.94);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (174, 179, 'Vikram Singh', 'CSE', 4, '2Q36', 9.21);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (175, 180, 'Manish Verma', 'CSE', 4, '2Q36', 7.53);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (176, 181, 'Swati Mehta', 'CSE', 4, '2Q36', 8.14);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (177, 182, 'Rahul Gupta', 'CSE', 4, '2Q36', 9.0);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (178, 183, 'Pooja Reddy', 'CSE', 4, '2Q36', 8.09);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (179, 184, 'Manish Kumar', 'CSE', 4, '2Q36', 9.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (180, 185, 'Ritu Mehta', 'CSE', 4, '2Q36', 8.24);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (181, 186, 'Rahul Kumar', 'CSE', 4, '2Q37', 6.88);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (182, 187, 'Ishita Verma', 'CSE', 4, '2Q37', 6.88);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (183, 188, 'Gaurav Nair', 'CSE', 4, '2Q37', 8.58);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (184, 189, 'Rohan Mehta', 'CSE', 4, '2Q37', 6.85);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (185, 190, 'Akash Kumar', 'CSE', 4, '2Q37', 7.45);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (186, 191, 'Kavya Singh', 'CSE', 4, '2Q37', 6.94);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (187, 192, 'Neha Nair', 'CSE', 4, '2Q37', 7.66);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (188, 193, 'Priya Mehta', 'CSE', 4, '2Q37', 6.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (189, 194, 'Anjali Sharma', 'CSE', 4, '2Q37', 7.09);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (190, 195, 'Aditya Verma', 'CSE', 4, '2Q37', 7.86);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (191, 196, 'Rahul Kumar', 'CSE', 4, '2Q37', 6.7);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (192, 197, 'Ishita Gupta', 'CSE', 4, '2Q37', 7.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (193, 198, 'Neha Reddy', 'CSE', 4, '2Q37', 7.37);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (194, 199, 'Ritu Patel', 'CSE', 4, '2Q37', 7.02);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (195, 200, 'Arjun Singh', 'CSE', 4, '2Q37', 7.54);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (196, 201, 'Manish Mehta', 'CSE', 4, '2Q37', 8.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (197, 202, 'Varun Singh', 'CSE', 4, '2Q37', 8.55);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (198, 203, 'Ishita Joshi', 'CSE', 4, '2Q37', 7.39);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (199, 204, 'Preeti Gupta', 'CSE', 4, '2Q37', 7.21);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (200, 205, 'Anjali Singh', 'CSE', 4, '2Q37', 7.58);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (201, 206, 'Harsh Nair', 'CSE', 4, '2Q37', 6.77);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (202, 207, 'Swati Joshi', 'CSE', 4, '2Q37', 8.55);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (203, 208, 'Preeti Kumar', 'CSE', 4, '2Q37', 7.08);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (204, 209, 'Ishita Mehta', 'CSE', 4, '2Q37', 7.92);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (205, 210, 'Sneha Singh', 'CSE', 4, '2Q37', 6.89);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (206, 211, 'Preeti Nair', 'CSE', 4, '2Q37', 7.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (207, 212, 'Rohit Gupta', 'CSE', 4, '2Q37', 8.65);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (208, 213, 'Tanvi Mehta', 'CSE', 4, '2Q37', 6.61);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (209, 214, 'Anjali Verma', 'CSE', 4, '2Q37', 8.97);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (210, 215, 'Divya Reddy', 'CSE', 4, '2Q37', 8.86);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (211, 216, 'Sneha Singh', 'CSE', 4, '2Q38', 6.61);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (212, 217, 'Preeti Mehta', 'CSE', 4, '2Q38', 7.53);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (213, 218, 'Aditya Joshi', 'CSE', 4, '2Q38', 7.32);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (214, 219, 'Priya Verma', 'CSE', 4, '2Q38', 7.21);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (215, 220, 'Rohan Gupta', 'CSE', 4, '2Q38', 8.86);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (216, 221, 'Ishita Singh', 'CSE', 4, '2Q38', 9.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (217, 222, 'Gaurav Patel', 'CSE', 4, '2Q38', 6.92);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (218, 223, 'Neha Verma', 'CSE', 4, '2Q38', 8.5);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (219, 224, 'Divya Sharma', 'CSE', 4, '2Q38', 8.21);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (220, 225, 'Akash Reddy', 'CSE', 4, '2Q38', 6.72);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (221, 226, 'Manish Patel', 'CSE', 4, '2Q38', 8.41);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (222, 227, 'Vikram Reddy', 'CSE', 4, '2Q38', 9.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (223, 228, 'Karan Singh', 'CSE', 4, '2Q38', 8.19);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (224, 229, 'Nikhil Gupta', 'CSE', 4, '2Q38', 7.68);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (225, 230, 'Shruti Gupta', 'CSE', 4, '2Q38', 7.2);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (226, 231, 'Akash Gupta', 'CSE', 4, '2Q38', 9.26);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (227, 232, 'Kavya Gupta', 'CSE', 4, '2Q38', 9.24);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (228, 233, 'Aditya Mehta', 'CSE', 4, '2Q38', 7.2);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (229, 234, 'Manish Gupta', 'CSE', 4, '2Q38', 7.38);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (230, 235, 'Preeti Verma', 'CSE', 4, '2Q38', 9.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (231, 236, 'Sanjay Sharma', 'CSE', 4, '2Q38', 7.29);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (232, 237, 'Divya Verma', 'CSE', 4, '2Q38', 8.21);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (233, 238, 'Varun Nair', 'CSE', 4, '2Q38', 7.77);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (234, 239, 'Preeti Joshi', 'CSE', 4, '2Q38', 7.39);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (235, 240, 'Ishita Singh', 'CSE', 4, '2Q38', 9.25);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (236, 241, 'Swati Sharma', 'CSE', 4, '2Q38', 7.54);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (237, 242, 'Pooja Kumar', 'CSE', 4, '2Q38', 9.0);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (238, 243, 'Swati Patel', 'CSE', 4, '2Q38', 8.47);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (239, 244, 'Kavya Verma', 'CSE', 4, '2Q38', 7.57);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (240, 245, 'Gaurav Singh', 'CSE', 4, '2Q38', 7.98);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (241, 246, 'Arjun Mehta', 'CSE', 4, '2Q39', 8.26);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (242, 247, 'Anjali Reddy', 'CSE', 4, '2Q39', 8.99);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (243, 248, 'Akash Nair', 'CSE', 4, '2Q39', 7.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (244, 249, 'Varun Gupta', 'CSE', 4, '2Q39', 6.63);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (245, 250, 'Pooja Mehta', 'CSE', 4, '2Q39', 8.07);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (246, 251, 'Gaurav Kumar', 'CSE', 4, '2Q39', 6.95);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (247, 252, 'Amit Sharma', 'CSE', 4, '2Q39', 8.55);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (248, 253, 'Arjun Kumar', 'CSE', 4, '2Q39', 7.01);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (249, 254, 'Tanvi Kumar', 'CSE', 4, '2Q39', 8.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (250, 255, 'Sneha Kumar', 'CSE', 4, '2Q39', 7.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (251, 256, 'Priya Reddy', 'CSE', 4, '2Q39', 9.2);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (252, 257, 'Preeti Gupta', 'CSE', 4, '2Q39', 9.43);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (253, 258, 'Gaurav Joshi', 'CSE', 4, '2Q39', 8.65);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (254, 259, 'Shruti Sharma', 'CSE', 4, '2Q39', 6.61);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (255, 260, 'Aditya Reddy', 'CSE', 4, '2Q39', 8.08);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (256, 261, 'Kavya Singh', 'CSE', 4, '2Q39', 8.98);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (257, 262, 'Varun Gupta', 'CSE', 4, '2Q39', 7.01);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (258, 263, 'Rahul Reddy', 'CSE', 4, '2Q39', 8.45);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (259, 264, 'Nikhil Mehta', 'CSE', 4, '2Q39', 9.39);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (260, 265, 'Nikhil Singh', 'CSE', 4, '2Q39', 9.44);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (261, 266, 'Sanjay Verma', 'CSE', 4, '2Q39', 9.12);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (262, 267, 'Tanvi Sharma', 'CSE', 4, '2Q39', 8.59);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (263, 268, 'Arjun Singh', 'CSE', 4, '2Q39', 8.98);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (264, 269, 'Amit Gupta', 'CSE', 4, '2Q39', 9.0);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (265, 270, 'Aditya Nair', 'CSE', 4, '2Q39', 7.66);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (266, 271, 'Shruti Nair', 'CSE', 4, '2Q39', 7.52);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (267, 272, 'Harsh Gupta', 'CSE', 4, '2Q39', 8.6);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (268, 273, 'Shruti Nair', 'CSE', 4, '2Q39', 8.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (269, 274, 'Priya Nair', 'CSE', 4, '2Q39', 9.04);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (270, 275, 'Amit Singh', 'CSE', 4, '2Q39', 9.07);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (271, 276, 'Harsh Joshi', 'CSE', 4, '2Q40', 7.04);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (272, 277, 'Divya Patel', 'CSE', 4, '2Q40', 9.46);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (273, 278, 'Anjali Verma', 'CSE', 4, '2Q40', 6.78);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (274, 279, 'Harsh Singh', 'CSE', 4, '2Q40', 9.07);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (275, 280, 'Sneha Joshi', 'CSE', 4, '2Q40', 9.22);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (276, 281, 'Preeti Verma', 'CSE', 4, '2Q40', 7.33);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (277, 282, 'Karan Verma', 'CSE', 4, '2Q40', 7.1);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (278, 283, 'Shruti Verma', 'CSE', 4, '2Q40', 9.48);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (279, 284, 'Swati Gupta', 'CSE', 4, '2Q40', 9.43);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (280, 285, 'Megha Nair', 'CSE', 4, '2Q40', 9.15);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (281, 286, 'Manish Mehta', 'CSE', 4, '2Q40', 9.25);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (282, 287, 'Manish Singh', 'CSE', 4, '2Q40', 6.73);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (283, 288, 'Anjali Gupta', 'CSE', 4, '2Q40', 8.67);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (284, 289, 'Akash Joshi', 'CSE', 4, '2Q40', 7.2);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (285, 290, 'Anjali Mehta', 'CSE', 4, '2Q40', 7.46);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (286, 291, 'Preeti Reddy', 'CSE', 4, '2Q40', 6.88);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (287, 292, 'Neha Nair', 'CSE', 4, '2Q40', 7.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (288, 293, 'Nisha Verma', 'CSE', 4, '2Q40', 9.47);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (289, 294, 'Shruti Patel', 'CSE', 4, '2Q40', 8.71);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (290, 295, 'Rahul Nair', 'CSE', 4, '2Q40', 9.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (291, 296, 'Nisha Patel', 'CSE', 4, '2Q40', 7.57);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (292, 297, 'Sneha Joshi', 'CSE', 4, '2Q40', 9.28);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (293, 298, 'Manish Mehta', 'CSE', 4, '2Q40', 9.07);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (294, 299, 'Vikram Joshi', 'CSE', 4, '2Q40', 8.65);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (295, 300, 'Neha Kumar', 'CSE', 4, '2Q40', 8.26);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (296, 301, 'Priya Sharma', 'CSE', 4, '2Q40', 8.83);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (297, 302, 'Rahul Mehta', 'CSE', 4, '2Q40', 8.62);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (298, 303, 'Rohit Nair', 'CSE', 4, '2Q40', 6.61);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (299, 304, 'Anjali Reddy', 'CSE', 4, '2Q40', 8.38);
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (300, 305, 'Arjun Sharma', 'CSE', 4, '2Q40', 9.33);
COMMIT;

-- ============================================================================
-- END OF SEED DATA
-- subjects: 5 rows
-- users (faculty): 5 rows
-- faculty: 5 rows
-- faculty_classes: 50 rows
-- users (students): 300 rows
-- students: 300 rows
-- marks + attendance: generated by setup_complete_system.py (too large for SQL file)
-- ============================================================================