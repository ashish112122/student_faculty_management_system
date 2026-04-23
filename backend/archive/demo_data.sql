-- Insert Subjects
INSERT INTO subjects VALUES (subjects_seq.NEXTVAL, 'Database Management Systems', 'DBMS');
INSERT INTO subjects VALUES (subjects_seq.NEXTVAL, 'Operating Systems', 'OS');
INSERT INTO subjects VALUES (subjects_seq.NEXTVAL, 'Computer Networks', 'CN');
INSERT INTO subjects VALUES (subjects_seq.NEXTVAL, 'Data Structures and Algorithms', 'DSA');
INSERT INTO subjects VALUES (subjects_seq.NEXTVAL, 'Software Engineering', 'SE');

-- Insert Faculty Users
INSERT INTO users VALUES (users_seq.NEXTVAL, 'rohan.sharma@thaparfac.edu', 'password123', 'Dr. Rohan Sharma', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'neha.verma@thaparfac.edu', 'password123', 'Dr. Neha Verma', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'amit.khanna@thaparfac.edu', 'password123', 'Dr. Amit Khanna', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'priya.mehta@thaparfac.edu', 'password123', 'Dr. Priya Mehta', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'rajesh.kumar@thaparfac.edu', 'password123', 'Dr. Rajesh Kumar', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'anita.singh@thaparfac.edu', 'password123', 'Dr. Anita Singh', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'vikram.patel@thaparfac.edu', 'password123', 'Dr. Vikram Patel', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'kavita.reddy@thaparfac.edu', 'password123', 'Dr. Kavita Reddy', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'suresh.nair@thaparfac.edu', 'password123', 'Dr. Suresh Nair', 'faculty');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'deepa.iyer@thaparfac.edu', 'password123', 'Dr. Deepa Iyer', 'faculty');

-- Insert Faculty Records
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 1, 'Computer Science', 'Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 2, 'Computer Science', 'Associate Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 3, 'Computer Science', 'Assistant Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 4, 'Computer Science', 'Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 5, 'Computer Science', 'Associate Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 6, 'Information Technology', 'Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 7, 'Information Technology', 'Assistant Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 8, 'Electronics', 'Associate Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 9, 'Mechanical', 'Professor');
INSERT INTO faculty VALUES (faculty_seq.NEXTVAL, 10, 'Civil', 'Assistant Professor');

COMMIT;

-- Insert 40 Student Users
INSERT INTO users VALUES (users_seq.NEXTVAL, 'rohan.sharma@thapar.edu', 'password123', 'Rohan Sharma', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'rahul.verma@thapar.edu', 'password123', 'Rahul Verma', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'simran.kaur@thapar.edu', 'password123', 'Simran Kaur', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'aman.gupta@thapar.edu', 'password123', 'Aman Gupta', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'priya.singh@thapar.edu', 'password123', 'Priya Singh', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'arjun.patel@thapar.edu', 'password123', 'Arjun Patel', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'neha.reddy@thapar.edu', 'password123', 'Neha Reddy', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'karan.mehta@thapar.edu', 'password123', 'Karan Mehta', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'ananya.nair@thapar.edu', 'password123', 'Ananya Nair', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'vikram.joshi@thapar.edu', 'password123', 'Vikram Joshi', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'pooja.agarwal@thapar.edu', 'password123', 'Pooja Agarwal', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'aditya.kumar@thapar.edu', 'password123', 'Aditya Kumar', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'riya.shah@thapar.edu', 'password123', 'Riya Shah', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'sanjay.rao@thapar.edu', 'password123', 'Sanjay Rao', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'divya.pillai@thapar.edu', 'password123', 'Divya Pillai', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'harsh.malhotra@thapar.edu', 'password123', 'Harsh Malhotra', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'sneha.desai@thapar.edu', 'password123', 'Sneha Desai', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'rohit.bansal@thapar.edu', 'password123', 'Rohit Bansal', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'kavya.iyer@thapar.edu', 'password123', 'Kavya Iyer', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'nikhil.chopra@thapar.edu', 'password123', 'Nikhil Chopra', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'tanvi.bhatt@thapar.edu', 'password123', 'Tanvi Bhatt', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'varun.saxena@thapar.edu', 'password123', 'Varun Saxena', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'ishita.kapoor@thapar.edu', 'password123', 'Ishita Kapoor', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'akash.pandey@thapar.edu', 'password123', 'Akash Pandey', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'megha.soni@thapar.edu', 'password123', 'Megha Soni', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'yash.tiwari@thapar.edu', 'password123', 'Yash Tiwari', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'shruti.mishra@thapar.edu', 'password123', 'Shruti Mishra', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'gaurav.jain@thapar.edu', 'password123', 'Gaurav Jain', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'nidhi.arora@thapar.edu', 'password123', 'Nidhi Arora', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'manish.bhatia@thapar.edu', 'password123', 'Manish Bhatia', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'swati.kulkarni@thapar.edu', 'password123', 'Swati Kulkarni', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'abhishek.yadav@thapar.edu', 'password123', 'Abhishek Yadav', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'anjali.dubey@thapar.edu', 'password123', 'Anjali Dubey', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'siddharth.ghosh@thapar.edu', 'password123', 'Siddharth Ghosh', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'preeti.das@thapar.edu', 'password123', 'Preeti Das', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'kunal.sethi@thapar.edu', 'password123', 'Kunal Sethi', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'ritika.bajaj@thapar.edu', 'password123', 'Ritika Bajaj', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'vishal.chawla@thapar.edu', 'password123', 'Vishal Chawla', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'sakshi.goyal@thapar.edu', 'password123', 'Sakshi Goyal', 'student');
INSERT INTO users VALUES (users_seq.NEXTVAL, 'deepak.sharma@thapar.edu', 'password123', 'Deepak Sharma', 'student');

-- Insert Student Records
INSERT INTO students VALUES (students_seq.NEXTVAL, 11, 'Computer Science', 2, 4, '2Q31', 8.5);
INSERT INTO students VALUES (students_seq.NEXTVAL, 12, 'Computer Science', 2, 4, '2Q32', 7.8);
INSERT INTO students VALUES (students_seq.NEXTVAL, 13, 'Computer Science', 2, 4, '2Q31', 9.1);
INSERT INTO students VALUES (students_seq.NEXTVAL, 14, 'Computer Science', 2, 4, '2W32', 8.2);
INSERT INTO students VALUES (students_seq.NEXTVAL, 15, 'Computer Science', 2, 4, '2Q32', 7.5);
INSERT INTO students VALUES (students_seq.NEXTVAL, 16, 'Information Technology', 2, 4, '2Q31', 8.7);
INSERT INTO students VALUES (students_seq.NEXTVAL, 17, 'Information Technology', 2, 4, '2W31', 7.9);
INSERT INTO students VALUES (students_seq.NEXTVAL, 18, 'Computer Science', 2, 4, '2Q31', 8.0);
INSERT INTO students VALUES (students_seq.NEXTVAL, 19, 'Information Technology', 2, 4, '2Q32', 9.0);
INSERT INTO students VALUES (students_seq.NEXTVAL, 20, 'Computer Science', 2, 4, '2W32', 7.3);
INSERT INTO students VALUES (students_seq.NEXTVAL, 21, 'Electronics', 2, 4, '2Q31', 8.4);
INSERT INTO students VALUES (students_seq.NEXTVAL, 22, 'Computer Science', 2, 4, '2Q32', 8.8);
INSERT INTO students VALUES (students_seq.NEXTVAL, 23, 'Information Technology', 2, 4, '2Q31', 7.6);
INSERT INTO students VALUES (students_seq.NEXTVAL, 24, 'Computer Science', 2, 4, '2W31', 9.2);
INSERT INTO students VALUES (students_seq.NEXTVAL, 25, 'Electronics', 2, 4, '2Q32', 7.7);
INSERT INTO students VALUES (students_seq.NEXTVAL, 26, 'Computer Science', 2, 4, '2Q31', 8.3);
INSERT INTO students VALUES (students_seq.NEXTVAL, 27, 'Information Technology', 2, 4, '2Q32', 8.9);
INSERT INTO students VALUES (students_seq.NEXTVAL, 28, 'Computer Science', 2, 4, '2W32', 7.4);
INSERT INTO students VALUES (students_seq.NEXTVAL, 29, 'Electronics', 2, 4, '2Q31', 8.6);
INSERT INTO students VALUES (students_seq.NEXTVAL, 30, 'Computer Science', 2, 4, '2Q32', 7.2);
INSERT INTO students VALUES (students_seq.NEXTVAL, 31, 'Information Technology', 2, 4, '2Q31', 8.1);
INSERT INTO students VALUES (students_seq.NEXTVAL, 32, 'Computer Science', 2, 4, '2W31', 9.3);
INSERT INTO students VALUES (students_seq.NEXTVAL, 33, 'Electronics', 2, 4, '2Q32', 7.8);
INSERT INTO students VALUES (students_seq.NEXTVAL, 34, 'Computer Science', 2, 4, '2Q31', 8.5);
INSERT INTO students VALUES (students_seq.NEXTVAL, 35, 'Information Technology', 2, 4, '2Q32', 7.9);
INSERT INTO students VALUES (students_seq.NEXTVAL, 36, 'Computer Science', 2, 4, '2W32', 8.7);
INSERT INTO students VALUES (students_seq.NEXTVAL, 37, 'Electronics', 2, 4, '2Q31', 7.5);
INSERT INTO students VALUES (students_seq.NEXTVAL, 38, 'Computer Science', 2, 4, '2Q32', 9.0);
INSERT INTO students VALUES (students_seq.NEXTVAL, 39, 'Information Technology', 2, 4, '2Q31', 8.2);
INSERT INTO students VALUES (students_seq.NEXTVAL, 40, 'Computer Science', 2, 4, '2W31', 7.6);
INSERT INTO students VALUES (students_seq.NEXTVAL, 41, 'Electronics', 2, 4, '2Q32', 8.8);
INSERT INTO students VALUES (students_seq.NEXTVAL, 42, 'Computer Science', 2, 4, '2Q31', 7.7);
INSERT INTO students VALUES (students_seq.NEXTVAL, 43, 'Information Technology', 2, 4, '2Q32', 8.4);
INSERT INTO students VALUES (students_seq.NEXTVAL, 44, 'Computer Science', 2, 4, '2W32', 9.1);
INSERT INTO students VALUES (students_seq.NEXTVAL, 45, 'Electronics', 2, 4, '2Q31', 7.3);
INSERT INTO students VALUES (students_seq.NEXTVAL, 46, 'Computer Science', 2, 4, '2Q32', 8.6);
INSERT INTO students VALUES (students_seq.NEXTVAL, 47, 'Information Technology', 2, 4, '2Q31', 7.8);
INSERT INTO students VALUES (students_seq.NEXTVAL, 48, 'Computer Science', 2, 4, '2W31', 8.9);
INSERT INTO students VALUES (students_seq.NEXTVAL, 49, 'Electronics', 2, 4, '2Q32', 7.4);
INSERT INTO students VALUES (students_seq.NEXTVAL, 50, 'Computer Science', 2, 4, '2Q31', 8.0);

COMMIT;

-- Assign subjects to all students (5 subjects each including DSA)
BEGIN
    FOR i IN 1..40 LOOP
        INSERT INTO student_subjects VALUES (student_subjects_seq.NEXTVAL, i, 1);
        INSERT INTO student_subjects VALUES (student_subjects_seq.NEXTVAL, i, 2);
        INSERT INTO student_subjects VALUES (student_subjects_seq.NEXTVAL, i, 3);
        INSERT INTO student_subjects VALUES (student_subjects_seq.NEXTVAL, i, 4);
        INSERT INTO student_subjects VALUES (student_subjects_seq.NEXTVAL, i, 5);
    END LOOP;
    COMMIT;
END;
/

-- Insert Sample Marks for Students
BEGIN
    FOR i IN 1..40 LOOP
        FOR j IN 1..5 LOOP
            INSERT INTO marks VALUES (marks_seq.NEXTVAL, i, j, 'MST', ROUND(DBMS_RANDOM.VALUE(60, 95)), 100);
            INSERT INTO marks VALUES (marks_seq.NEXTVAL, i, j, 'EST', ROUND(DBMS_RANDOM.VALUE(60, 95)), 100);
            INSERT INTO marks VALUES (marks_seq.NEXTVAL, i, j, 'Assignment', ROUND(DBMS_RANDOM.VALUE(70, 100)), 100);
            INSERT INTO marks VALUES (marks_seq.NEXTVAL, i, j, 'Quiz', ROUND(DBMS_RANDOM.VALUE(65, 100)), 100);
        END LOOP;
    END LOOP;
    COMMIT;
END;
/

-- Insert Sample Attendance Records (Last 30 days)
BEGIN
    FOR i IN 1..40 LOOP
        FOR j IN 1..5 LOOP
            FOR k IN 1..30 LOOP
                IF DBMS_RANDOM.VALUE(0, 100) > 20 THEN
                    INSERT INTO attendance VALUES (attendance_seq.NEXTVAL, i, j, SYSDATE - k, 'P');
                ELSE
                    INSERT INTO attendance VALUES (attendance_seq.NEXTVAL, i, j, SYSDATE - k, 'A');
                END IF;
            END LOOP;
        END LOOP;
    END LOOP;
    COMMIT;
END;
/

-- Insert Sample Alerts for students with low attendance
INSERT INTO alerts VALUES (alerts_seq.NEXTVAL, 5, 'Warning', 'Your attendance in DBMS is below 75%. Please improve.', SYSDATE - 5);
INSERT INTO alerts VALUES (alerts_seq.NEXTVAL, 10, 'Alert', 'Your attendance in Operating Systems is below 65%. Immediate action required.', SYSDATE - 3);
INSERT INTO alerts VALUES (alerts_seq.NEXTVAL, 15, 'Critical', 'Your attendance in Computer Networks is below 50%. Critical situation.', SYSDATE - 1);

COMMIT;
