# Student-Faculty Management System - Master Documentation

## Table of Contents
1. Project Overview
2. Complete Folder Structure
3. Database Tables - Creation and Data Insertion Traceability
4. File-by-File Mapping
5. Database Relationships
6. Data Consistency Verification
7. Setup Instructions
8. Sample Credentials

---

## 1. Project Overview

A comprehensive web-based management system for educational institutions.

Technology Stack:
- Backend: Python Flask
- Database: Oracle Database 21c
- Frontend: HTML, CSS, JavaScript
- Authentication: JWT

Key Features:
- Student and Faculty Login
- Marks Management
- Attendance Tracking
- Automated Alerts
- Feedback/Chat System

---

## 2. Complete Folder Structure

Root Directory: student_faculty_management_system/

```
student_faculty_management_system/
├── backend/                    Backend Python application
├── frontend/                   Frontend HTML/CSS/JS files
├── sql/                        Legacy SQL files
├── static/                     Static CSS/JS files
├── templates/                  HTML template files
├── .gitignore                  Git ignore configuration
├── WORKING_LINKS.md            URLs and credentials reference
└── SYSTEM_DOCUMENTATION.md     This file
```

---

## 3. Database Tables - Creation and Data Insertion Traceability

Total Tables: 11
Database Type: Oracle Database 21c

---

### Table 1: users

Purpose: Central authentication table for all users (students and faculty)

Table Creation:
- Created in: backend/setup_complete_system.py (Line 63-70)
- Also defined in: backend/database/complete_schema.sql (Line 10-17)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) NOT NULL CHECK (role IN ('student', 'faculty'))
)
```

Sequence: users_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 8-17 for faculty)
- Method 2: backend/setup_complete_system.py (Lines 165-175 for faculty, Lines 230-245 for students)
- File path: backend/setup_complete_system.py

Sample Inserted Data (Faculty):
```
user_id: 1
email: dr.rajesh@thaparfac.edu
password: pass123
name: Dr. Rajesh Kumar
role: faculty
```

Sample Inserted Data (Student):
```
user_id: 6
email: rohan.sharma.2q31.0@thapar.edu
password: pass123
name: Rohan Sharma
role: student
```

Total Records: 305 (5 faculty + 300 students)

---

### Table 2: students

Purpose: Store student-specific information

Table Creation:
- Created in: backend/setup_complete_system.py (Line 73-82)
- Also defined in: backend/database/complete_schema.sql (Line 24-33)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    name VARCHAR2(100) NOT NULL,
    branch VARCHAR2(50) NOT NULL,
    semester NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    cgpa NUMBER(3,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

Sequence: students_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 119-127 sample)
- Method 2: backend/setup_complete_system.py (Lines 230-260)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
student_id: 1
user_id: 6
name: Rohan Sharma
branch: CSE
semester: 4
class_name: 2Q31
cgpa: 8.75
```

Data Generation Logic:
- 300 students total
- 30 students per batch
- 10 batches: 2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40
- Random names from predefined lists
- Random CGPA between 6.5 and 9.5
- All in CSE branch, semester 4

Total Records: 300

---

### Table 3: faculty

Purpose: Store faculty-specific information

Table Creation:
- Created in: backend/setup_complete_system.py (Line 85-92)
- Also defined in: backend/database/complete_schema.sql (Line 40-46)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    user_id NUMBER UNIQUE NOT NULL,
    name VARCHAR2(100) NOT NULL,
    department VARCHAR2(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

Sequence: faculty_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 20-29)
- Method 2: backend/setup_complete_system.py (Lines 165-185)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
faculty_id: 1
user_id: 1
name: Dr. Rajesh Kumar
department: CSE
```

Complete Faculty List:
1. Dr. Rajesh Kumar (CSE) - Data Structures
2. Prof. Meena Sharma (CSE) - Algorithms
3. Dr. Suresh Patel (CSE) - Database Management
4. Prof. Kavita Singh (CSE) - Operating Systems
5. Dr. Anil Verma (CSE) - Computer Networks

Total Records: 5

---

### Table 4: subjects

Purpose: Store all subjects/courses

Table Creation:
- Created in: backend/setup_complete_system.py (Line 95-100)
- Also defined in: backend/database/complete_schema.sql (Line 53-58)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE subjects (
    subject_id NUMBER PRIMARY KEY,
    subject_name VARCHAR2(100) NOT NULL,
    subject_code VARCHAR2(20) UNIQUE NOT NULL
)
```

Sequence: subjects_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 32-41)
- Method 2: backend/setup_complete_system.py (Lines 145-155)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
subject_id: 1
subject_name: Data Structures
subject_code: CS401
```

Complete Subject List:
1. Data Structures (CS401)
2. Algorithms (CS402)
3. Database Management (CS403)
4. Operating Systems (CS404)
5. Computer Networks (CS405)

Total Records: 5

---

### Table 5: faculty_classes

Purpose: Map faculty to subjects and classes they teach

Table Creation:
- Created in: backend/setup_complete_system.py (Line 103-110)
- Also defined in: backend/database/complete_schema.sql (Line 65-72)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE faculty_classes (
    faculty_class_id NUMBER PRIMARY KEY,
    faculty_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
```

Sequence: faculty_classes_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 44-73)
- Method 2: backend/setup_complete_system.py (Lines 190-210)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
faculty_class_id: 1
faculty_id: 1
subject_id: 1
class_name: 2Q31
```

Faculty-Batch Assignment Pattern (CORRECTED - DATABASE FIXED):
- Faculty 1 (Dr. Rajesh): Data Structures for ALL 10 batches
- Faculty 2 (Prof. Meena): Algorithms for ALL 10 batches
- Faculty 3 (Dr. Suresh): Database Management for ALL 10 batches
- Faculty 4 (Prof. Kavita): Operating Systems for ALL 10 batches
- Faculty 5 (Dr. Anil): Computer Networks for ALL 10 batches

Total Records: 50 (5 faculty x 10 batches each) - VERIFIED IN DATABASE

---

### Table 6: marks

Purpose: Store student marks for all assessments

Table Creation:
- Created in: backend/setup_complete_system.py (Line 113-122)
- Also defined in: backend/database/complete_schema.sql (Line 79-89)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE marks (
    mark_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    assessment_type VARCHAR2(20) NOT NULL CHECK (assessment_type IN ('MST', 'EST', 'Quiz', 'Assignment')),
    marks_obtained NUMBER NOT NULL,
    max_marks NUMBER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
```

Sequence: marks_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 130-141 sample)
- Method 2: backend/setup_complete_system.py (Lines 270-290)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
mark_id: 1
student_id: 1
subject_id: 1
class_name: 2Q31
assessment_type: MST
marks_obtained: 25
max_marks: 30
```

Assessment Types and Max Marks:
- MST (Mid-Semester Test): 30 marks
- EST (End-Semester Test): 40 marks
- Quiz: 15 marks
- Assignment: 15 marks
- Total: 100 marks per subject

Data Generation Logic:
- Each student gets marks for all 5 subjects
- Each subject has 4 assessment types
- Marks randomly generated between 50% and 95% of max marks
- Total records: 300 students x 5 subjects x 4 assessments = 6000 records

Total Records: 6000

---

### Table 7: attendance

Purpose: Track daily attendance for each student in each subject

Table Creation:
- Created in: backend/setup_complete_system.py (Line 125-133)
- Also defined in: backend/database/complete_schema.sql (Line 96-105)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    class_name VARCHAR2(10) NOT NULL,
    attendance_date DATE NOT NULL,
    status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
```

Sequence: attendance_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 144-151 sample)
- Method 2: backend/setup_complete_system.py (Lines 300-330)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
attendance_id: 1
student_id: 1
subject_id: 1
class_name: 2Q31
attendance_date: 2026-01-02
status: P
```

Status Values:
- P: Present
- A: Absent

Data Generation Logic:
- Date range: January 1, 2026 to April 1, 2026
- Only weekdays (Monday to Friday)
- Each student has attendance for all 5 subjects per day
- Random attendance rate between 60% and 95% per student
- Total records: 300 students x 5 subjects x ~150 days = ~225000 records

Total Records: Approximately 225000

---

### Table 8: alerts

Purpose: Store automated alerts for students

Table Creation:
- Created in: backend/setup_complete_system.py (Line 136-145)
- Also defined in: backend/database/complete_schema.sql (Line 112-121)
- File path: backend/setup_complete_system.py

SQL Query:
```sql
CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER,
    alert_type VARCHAR2(20) NOT NULL,
    message VARCHAR2(500) NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
```

Sequence: alerts_seq (starts at 1, increments by 1)

Data Insertion:
- Method 1: backend/database/insert_data.sql (Lines 154-155 sample)
- Method 2: backend/setup_complete_system.py (Lines 340-370)
- File path: backend/setup_complete_system.py

Sample Inserted Data:
```
alert_id: 1
student_id: 1
subject_id: 1
alert_type: Warning
message: Low attendance in Data Structures: 72.5%
is_read: 0
created_at: 2026-04-05 10:30:00
```

Alert Types:
- Warning: Attendance 65-75%
- Alert: Attendance 50-65%
- Critical: Attendance below 50%

Data Generation Logic:
- Calculated from attendance table
- Query finds students with attendance below 75%
- Alert type determined by percentage
- Alert dates spread over last 30 days
- Total records: Varies based on attendance (typically 50-100 alerts)

Total Records: Varies (generated based on low attendance)

---

### Table 9: feedback_threads

Purpose: Store conversation metadata between students and faculty

Table Creation:
- Created in: backend/database/schema_feedback_threads.sql (Line 14-27)
- Also defined in: backend/database/complete_schema.sql (Line 128-141)
- File path: backend/database/schema_feedback_threads.sql

SQL Query:
```sql
CREATE TABLE feedback_threads (
    thread_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    faculty_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    thread_title VARCHAR2(200),
    initiated_by VARCHAR2(20) NOT NULL CHECK (initiated_by IN ('student', 'faculty')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cleared_by_student TIMESTAMP DEFAULT NULL,
    cleared_by_faculty TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
```

Sequence: feedback_threads_seq (starts at 1, increments by 1)

Indexes:
- idx_feedback_threads_student on student_id
- idx_feedback_threads_faculty on faculty_id
- idx_feedback_threads_subject on subject_id

Data Insertion:
- Created dynamically when users start conversations
- No pre-populated data
- File path: backend/app.py (Lines 700-750 approximately)

Sample Data (created on-demand):
```
thread_id: 1
student_id: 1
faculty_id: 1
subject_id: 1
thread_title: NULL
initiated_by: student
created_at: 2026-04-05 10:00:00
last_message_at: 2026-04-05 15:30:00
cleared_by_student: NULL
cleared_by_faculty: NULL
```

Total Records: Created on-demand by users

---

### Table 10: feedback_messages

Purpose: Store individual messages in feedback conversations

Table Creation:
- Created in: backend/database/schema_feedback_threads.sql (Line 31-45)
- Also defined in: backend/database/complete_schema.sql (Line 145-159)
- File path: backend/database/schema_feedback_threads.sql

SQL Query:
```sql
CREATE TABLE feedback_messages (
    message_id NUMBER PRIMARY KEY,
    thread_id NUMBER NOT NULL,
    sender_id NUMBER NOT NULL,
    sender_role VARCHAR2(20) NOT NULL CHECK (sender_role IN ('student', 'faculty')),
    message CLOB NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attachment_path VARCHAR2(500),
    attachment_name VARCHAR2(200),
    attachment_type VARCHAR2(50),
    FOREIGN KEY (thread_id) REFERENCES feedback_threads(thread_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
)
```

Sequence: feedback_messages_seq (starts at 1, increments by 1)

Indexes:
- idx_feedback_messages_thread on thread_id
- idx_feedback_messages_sender on sender_id

Data Insertion:
- Created dynamically when users send messages
- No pre-populated data
- File path: backend/app.py (Lines 750-800 approximately)

Sample Data (created on-demand):
```
message_id: 1
thread_id: 1
sender_id: 6
sender_role: student
message: Hello sir, I have a doubt about linked lists
is_read: 0
created_at: 2026-04-05 10:30:00
attachment_path: NULL
attachment_name: NULL
attachment_type: NULL
```

Attachment Storage:
- Location: backend/uploads/feedback_attachments/
- Filename format: YYYYMMDD_HHMMSS_originalname.ext

Total Records: Created on-demand by users

---

### Database Trigger

Trigger Name: update_thread_timestamp
Type: AFTER INSERT on feedback_messages
Purpose: Automatically update last_message_at in feedback_threads

Created in: backend/database/schema_feedback_threads.sql (Line 54-61)
File path: backend/database/schema_feedback_threads.sql

SQL Query:
```sql
CREATE OR REPLACE TRIGGER update_thread_timestamp
AFTER INSERT ON feedback_messages
FOR EACH ROW
BEGIN
    UPDATE feedback_threads
    SET last_message_at = CURRENT_TIMESTAMP
    WHERE thread_id = :NEW.thread_id;
END;
```

---

## 4. File-by-File Mapping

### Backend Folder (backend/)

File: app.py
Location: backend/app.py
Purpose: Main Flask application containing all API endpoints
Size: Large (1500+ lines)
Key Functions:
- User authentication and JWT token generation
- Student API endpoints (dashboard, marks, attendance, alerts, feedback)
- Faculty API endpoints (dashboard, students, marks entry, feedback)
- File upload handling for attachments
- Database connection management

File: config.py
Location: backend/config.py
Purpose: Database configuration and credentials
Contents:
- DB_USER: Oracle database username
- DB_PASSWORD: Oracle database password
- DB_DSN: Database connection string
- SECRET_KEY: JWT secret key

File: setup_complete_system.py
Location: backend/setup_complete_system.py
Purpose: Complete database initialization script
Functions:
- Drops existing tables and sequences
- Creates all 11 tables with proper schema
- Inserts 5 faculty members
- Inserts 5 subjects
- Creates 15 faculty-class assignments
- Generates 300 students (30 per batch)
- Generates marks for all students
- Generates attendance records (Jan-Apr 2026)
- Generates alerts based on attendance
Usage: python backend/setup_complete_system.py

File: add_clear_chat_columns.py
Location: backend/add_clear_chat_columns.py
Purpose: Migration script to add user-specific clear chat columns
Functions:
- Adds cleared_by_student column to feedback_threads
- Adds cleared_by_faculty column to feedback_threads
- Verifies columns were added successfully
Usage: python backend/add_clear_chat_columns.py

File: requirements.txt
Location: backend/requirements.txt
Purpose: Python package dependencies
Contents:
- Flask==3.0.0
- Flask-CORS==4.0.0
- oracledb==2.0.0
- PyJWT==2.8.0
- python-dotenv==1.0.0

File: cleanup_database.py
Location: backend/cleanup_database.py
Purpose: Database cleanup utility
Function: Drops all tables and sequences for fresh start

File: verify_credentials.py
Location: backend/verify_credentials.py
Purpose: Test database connection and credentials
Function: Verifies database connectivity

---

### Backend Database Folder (backend/database/)

File: complete_schema.sql
Location: backend/database/complete_schema.sql
Purpose: Complete database schema with all 11 tables
Contents:
- All CREATE TABLE statements
- All CREATE SEQUENCE statements
- All CREATE INDEX statements
- CREATE TRIGGER statement
- Fully commented and organized by module
Lines: 200+ lines

File: schema.sql
Location: backend/database/schema.sql
Purpose: Original database schema
Contents: Basic table definitions (legacy)

File: schema_feedback_threads.sql
Location: backend/database/schema_feedback_threads.sql
Purpose: Feedback system schema with threading support
Contents:
- feedback_threads table definition
- feedback_messages table definition
- Indexes for performance
- Trigger for updating last_message_at

File: insert_data.sql
Location: backend/database/insert_data.sql
Purpose: Sample data insertion SQL queries
Contents:
- INSERT statements for 5 faculty users
- INSERT statements for 5 faculty records
- INSERT statements for 5 subjects
- INSERT statements for 15 faculty class assignments
- Sample INSERT statements for students (pattern shown)
- Sample INSERT statements for marks, attendance, alerts
Note: For complete data, use setup_complete_system.py

---

### Backend Utils Folder (backend/utils/)

File: alert_checker.py
Location: backend/utils/alert_checker.py
Purpose: Generate attendance alerts
Function: Calculates attendance percentage and creates alerts for students below 75%

File: email_service.py
Location: backend/utils/email_service.py
Purpose: Email notification service (future feature)
Status: Placeholder for email functionality

File: __init__.py
Location: backend/utils/__init__.py
Purpose: Python package initialization
Contents: Empty file to make utils a package

---

### Backend Tests Folder (backend/tests/)

File: test_connection.py
Location: backend/tests/test_connection.py
Purpose: Test database connection

File: check_all_tables.py
Location: backend/tests/check_all_tables.py
Purpose: Verify all tables exist in database

File: check_feedback_table.py
Location: backend/tests/check_feedback_table.py
Purpose: Verify feedback tables structure

File: check_schema.py
Location: backend/tests/check_schema.py
Purpose: Verify database schema

---

### Backend Uploads Folder (backend/uploads/)

Folder: feedback_attachments/
Location: backend/uploads/feedback_attachments/
Purpose: Store chat attachment files
File naming: YYYYMMDD_HHMMSS_originalname.ext

---

### Frontend Folder (frontend/)

File: student_portal.html
Location: frontend/student_portal.html
Purpose: Complete student dashboard (single-page application)
Size: Large (800+ lines)
Sections:
- Dashboard view with cards for Marks, Attendance, Alerts, Feedback
- Marks view displaying all marks by subject
- Attendance view showing attendance percentage
- Alerts view with read/unread status
- Feedback/Chat view with faculty
Features:
- Single-page app (no page reloads)
- Real-time chat updates
- File attachment support
- User-specific clear chat

File: faculty_portal.html
Location: frontend/faculty_portal.html
Purpose: Complete faculty dashboard (single-page application)
Size: Large (900+ lines)
Sections:
- Dashboard view with assigned classes
- My Classes view
- Add Marks form
- Marks Report view
- Feedback/Chat view with students
Features:
- Class and student selection
- Marks entry functionality
- Chat with students
- File attachment support
- User-specific clear chat

File: login_test.html
Location: frontend/login_test.html
Purpose: Login page for both students and faculty
Features:
- Email and password input
- Role-based redirect
- JWT token storage
- Error handling

File: test_backend_connection.html
Location: frontend/test_backend_connection.html
Purpose: Test backend API connectivity
Function: Verifies backend server is running

---

### Frontend CSS Folder (frontend/css/)

File: login.css
Location: frontend/css/login.css
Purpose: Login page styling

File: dashboard.css
Location: frontend/css/dashboard.css
Purpose: Dashboard layout and card styling

File: marks.css
Location: frontend/css/marks.css
Purpose: Marks table styling

File: attendance.css
Location: frontend/css/attendance.css
Purpose: Attendance display styling

File: alerts.css
Location: frontend/css/alerts.css
Purpose: Alert cards and badges styling

File: feedback.css
Location: frontend/css/feedback.css
Purpose: Chat interface styling

---

### Frontend JS Folder (frontend/js/)

File: login.js
Location: frontend/js/login.js
Purpose: Login functionality (legacy, now in HTML files)

File: dashboard.js
Location: frontend/js/dashboard.js
Purpose: Dashboard logic (legacy, now in HTML files)

File: faculty_dashboard.js
Location: frontend/js/faculty_dashboard.js
Purpose: Faculty dashboard logic (legacy, now in HTML files)

File: marks.js
Location: frontend/js/marks.js
Purpose: Marks display logic (legacy, now in HTML files)

File: attendance.js
Location: frontend/js/attendance.js
Purpose: Attendance display logic (legacy, now in HTML files)

File: alerts.js
Location: frontend/js/alerts.js
Purpose: Alerts display logic (legacy, now in HTML files)

File: feedback.js
Location: frontend/js/feedback.js
Purpose: Chat functionality (legacy, now in HTML files)

Note: Most JavaScript is now embedded in student_portal.html and faculty_portal.html

---

### Frontend Assets Folder (frontend/assets/)

File: university-logo.png
Location: frontend/assets/university-logo.png
Purpose: University logo for login page

File: README.md
Location: frontend/assets/README.md
Purpose: Assets folder documentation

---

### Static Folder (static/)

File: style.css
Location: static/style.css
Purpose: Global CSS styles (legacy)

File: app.js
Location: static/app.js
Purpose: Global JavaScript (legacy)

---

### Templates Folder (templates/)

File: base.html
Location: templates/base.html
Purpose: Base HTML template (legacy)

File: login.html
Location: templates/login.html
Purpose: Login page template (legacy)

File: student_dashboard.html
Location: templates/student_dashboard.html
Purpose: Student dashboard template (legacy)

File: faculty_dashboard.html
Location: templates/faculty_dashboard.html
Purpose: Faculty dashboard template (legacy)

File: faculty_dashboard_v2.html
Location: templates/faculty_dashboard_v2.html
Purpose: Updated faculty dashboard (legacy)

File: add_marks.html
Location: templates/add_marks.html
Purpose: Add marks form (legacy)

File: marks_report.html
Location: templates/marks_report.html
Purpose: Marks report view (legacy)

File: my_classes.html
Location: templates/my_classes.html
Purpose: Faculty classes view (legacy)

File: register.html
Location: templates/register.html
Purpose: Registration page (legacy)

Note: Templates folder contains legacy files. Current system uses frontend/ folder.

---

### SQL Folder (sql/)

File: create_tables.sql
Location: sql/create_tables.sql
Purpose: Legacy table creation script

File: insert_sample_data.sql
Location: sql/insert_sample_data.sql
Purpose: Legacy sample data insertion

File: member3_attendance_alerts.sql
Location: sql/member3_attendance_alerts.sql
Purpose: Legacy attendance and alerts queries

Note: SQL folder contains legacy files. Current system uses backend/database/ folder.

---

## 5. Database Relationships

Total Relationships: 15 foreign key relationships

### Relationship 1: users to students (One-to-One)
Connection: users.user_id (PK) connected to students.user_id (FK, UNIQUE)
Type: One-to-One
Description: Each user can be one student, each student has one user account
Defined in: backend/setup_complete_system.py (Line 73-82)

### Relationship 2: users to faculty (One-to-One)
Connection: users.user_id (PK) connected to faculty.user_id (FK, UNIQUE)
Type: One-to-One
Description: Each user can be one faculty, each faculty has one user account
Defined in: backend/setup_complete_system.py (Line 85-92)

### Relationship 3: students to marks (One-to-Many)
Connection: students.student_id (PK) connected to marks.student_id (FK)
Type: One-to-Many
Description: One student has many mark entries, each mark belongs to one student
Defined in: backend/setup_complete_system.py (Line 113-122)
Data Flow: Student -> Multiple marks across subjects and assessments

### Relationship 4: subjects to marks (One-to-Many)
Connection: subjects.subject_id (PK) connected to marks.subject_id (FK)
Type: One-to-Many
Description: One subject has many mark entries, each mark belongs to one subject
Defined in: backend/setup_complete_system.py (Line 113-122)
Data Flow: Subject -> Multiple marks across students and assessments

### Relationship 5: students to attendance (One-to-Many)
Connection: students.student_id (PK) connected to attendance.student_id (FK)
Type: One-to-Many
Description: One student has many attendance records, each record belongs to one student
Defined in: backend/setup_complete_system.py (Line 125-133)
Data Flow: Student -> Daily attendance records across subjects

### Relationship 6: subjects to attendance (One-to-Many)
Connection: subjects.subject_id (PK) connected to attendance.subject_id (FK)
Type: One-to-Many
Description: One subject has many attendance records, each record belongs to one subject
Defined in: backend/setup_complete_system.py (Line 125-133)
Data Flow: Subject -> Daily attendance records across students

### Relationship 7: students to alerts (One-to-Many)
Connection: students.student_id (PK) connected to alerts.student_id (FK)
Type: One-to-Many
Description: One student has many alerts, each alert belongs to one student
Defined in: backend/setup_complete_system.py (Line 136-145)
Data Flow: Student -> Multiple alerts based on attendance/marks

### Relationship 8: subjects to alerts (One-to-Many, Optional)
Connection: subjects.subject_id (PK) connected to alerts.subject_id (FK, NULLABLE)
Type: One-to-Many (Optional)
Description: One subject can have many alerts, each alert may belong to one subject or none
Defined in: backend/setup_complete_system.py (Line 136-145)
Data Flow: Subject -> Alerts related to that subject

### Relationship 9: faculty to faculty_classes (One-to-Many)
Connection: faculty.faculty_id (PK) connected to faculty_classes.faculty_id (FK)
Type: One-to-Many
Description: One faculty teaches many classes, each class assignment belongs to one faculty
Defined in: backend/setup_complete_system.py (Line 103-110)
Data Flow: Faculty -> Multiple class assignments (3 batches per faculty)

### Relationship 10: subjects to faculty_classes (One-to-Many)
Connection: subjects.subject_id (PK) connected to faculty_classes.subject_id (FK)
Type: One-to-Many
Description: One subject is taught in many classes, each class assignment has one subject
Defined in: backend/setup_complete_system.py (Line 103-110)
Data Flow: Subject -> Multiple class assignments across batches

### Relationship 11: students to feedback_threads (One-to-Many)
Connection: students.student_id (PK) connected to feedback_threads.student_id (FK)
Type: One-to-Many
Description: One student has many feedback threads, each thread belongs to one student
Defined in: backend/database/schema_feedback_threads.sql (Line 14-27)
Data Flow: Student -> Multiple conversation threads with different faculty

### Relationship 12: faculty to feedback_threads (One-to-Many)
Connection: faculty.faculty_id (PK) connected to feedback_threads.faculty_id (FK)
Type: One-to-Many
Description: One faculty has many feedback threads, each thread belongs to one faculty
Defined in: backend/database/schema_feedback_threads.sql (Line 14-27)
Data Flow: Faculty -> Multiple conversation threads with different students

### Relationship 13: subjects to feedback_threads (One-to-Many)
Connection: subjects.subject_id (PK) connected to feedback_threads.subject_id (FK)
Type: One-to-Many
Description: One subject has many feedback threads, each thread is about one subject
Defined in: backend/database/schema_feedback_threads.sql (Line 14-27)
Data Flow: Subject -> Conversations related to that subject

### Relationship 14: feedback_threads to feedback_messages (One-to-Many with CASCADE DELETE)
Connection: feedback_threads.thread_id (PK) connected to feedback_messages.thread_id (FK)
Type: One-to-Many with CASCADE DELETE
Description: One thread has many messages, each message belongs to one thread
Defined in: backend/database/schema_feedback_threads.sql (Line 31-45)
Data Flow: Thread -> Multiple messages in conversation
Special: Deleting thread automatically deletes all messages

### Relationship 15: users to feedback_messages (One-to-Many)
Connection: users.user_id (PK) connected to feedback_messages.sender_id (FK)
Type: One-to-Many
Description: One user sends many messages, each message has one sender
Defined in: backend/database/schema_feedback_threads.sql (Line 31-45)
Data Flow: User -> Multiple messages sent in various threads

---

## 6. Data Consistency Verification

### Faculty-Batch Assignment Verification

STATUS: CORRECTED - Database has been fixed

Each faculty is now correctly assigned to ALL 10 batches.
Total assignments: 50 (5 faculty x 10 batches)

Faculty-Batch Assignments (CORRECTED):

Faculty 1: Dr. Rajesh Kumar
- Subject: Data Structures (CS401)
- Batches: ALL 10 batches (2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40)
- Students: 300 (30 per batch x 10 batches)
- Verification: Database corrected on April 2026

Faculty 2: Prof. Meena Sharma
- Subject: Algorithms (CS402)
- Batches: ALL 10 batches (2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40)
- Students: 300 (30 per batch x 10 batches)
- Verification: Database corrected on April 2026

Faculty 3: Dr. Suresh Patel
- Subject: Database Management (CS403)
- Batches: ALL 10 batches (2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40)
- Students: 300 (30 per batch x 10 batches)
- Verification: Database corrected on April 2026

Faculty 4: Prof. Kavita Singh
- Subject: Operating Systems (CS404)
- Batches: ALL 10 batches (2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40)
- Students: 300 (30 per batch x 10 batches)
- Verification: Database corrected on April 2026

Faculty 5: Dr. Anil Verma
- Subject: Computer Networks (CS405)
- Batches: ALL 10 batches (2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40)
- Students: 300 (30 per batch x 10 batches)
- Verification: Database corrected on April 2026

Database Verification Completed:
- Total faculty_classes records: 50
- Each faculty has exactly 10 batch assignments
- All batches (2Q31 to 2Q40) are covered by all faculty
- System is now consistent with website functionality

### Student-Batch Assignment Verification

Total Students: 300
Students per Batch: 30
Total Batches: 10

Batch Distribution:
- 2Q31: Students 1-30
- 2Q32: Students 31-60
- 2Q33: Students 61-90
- 2Q34: Students 91-120
- 2Q35: Students 121-150
- 2Q36: Students 151-180
- 2Q37: Students 181-210
- 2Q38: Students 211-240
- 2Q39: Students 241-270
- 2Q40: Students 271-300

Verification: Lines 230-260 in backend/setup_complete_system.py

### Marks Data Consistency

Each Student:
- Has marks for all 5 subjects
- Has 4 assessment types per subject (MST, EST, Quiz, Assignment)
- Total marks entries per student: 20 (5 subjects x 4 assessments)

Total Marks Records: 6000 (300 students x 20 entries)
Verification: Lines 270-290 in backend/setup_complete_system.py

### Attendance Data Consistency

Each Student:
- Has attendance for all 5 subjects
- Has attendance for all weekdays from Jan 1 to Apr 1, 2026
- Approximately 150 days of attendance per subject

Total Attendance Records: Approximately 225000 (300 students x 5 subjects x 150 days)
Verification: Lines 300-330 in backend/setup_complete_system.py

### Alerts Data Consistency

Alert Generation Logic:
- Calculated from attendance table
- Generated for students with attendance below 75%
- Alert type based on percentage:
  - Critical: Below 50%
  - Alert: 50-65%
  - Warning: 65-75%

Total Alerts: Varies (typically 50-100 based on random attendance generation)
Verification: Lines 340-370 in backend/setup_complete_system.py

---

## 7. Setup Instructions

### Prerequisites
1. Oracle Database 21c installed and running
2. Python 3.8 or higher installed
3. Oracle Instant Client installed
4. Database credentials (username, password, connection string)

### Step 1: Configure Database Credentials

Edit file: backend/config.py

```python
class Config:
    DB_USER = 'your_oracle_username'
    DB_PASSWORD = 'your_oracle_password'
    DB_DSN = 'host:port/service_name'
    SECRET_KEY = 'your-secret-key-here'
```

Example:
```python
class Config:
    DB_USER = 'system'
    DB_PASSWORD = 'oracle123'
    DB_DSN = 'localhost:1521/XEPDB1'
    SECRET_KEY = 'my-secret-key-12345'
```

### Step 2: Install Python Dependencies

Open terminal in project root directory:

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (cross-origin resource sharing)
- oracledb (Oracle database driver)
- PyJWT (JWT token handling)
- python-dotenv (environment variables)

### Step 3: Initialize Database

The database has already been corrected with proper faculty-batch assignments.

If you need to reinitialize the database from scratch, use the corrected setup script:

```bash
python backend/setup_complete_system_corrected.py
```

This script will:
1. Drop existing tables (if any)
2. Create all 11 tables with proper schema
3. Create all 10 sequences
4. Insert 5 faculty members
5. Insert 5 subjects
6. Create 15 faculty-class assignments
7. Generate 300 students (30 per batch)
8. Generate marks for all students (6000 records)
9. Generate attendance records (225000 records)
10. Generate alerts based on attendance

Expected output:
```
--------------------------------------------------------------------------------
SETTING UP COMPLETE SYSTEM
--------------------------------------------------------------------------------

1. Setting up database schema...
   Dropped FEEDBACK
   Dropped ALERTS
   ...
   OK Schema created

2. Creating 5 subjects...
   OK Created 5 subjects

3. Creating 5 faculty...
   OK Created 5 faculty

4. Creating faculty assignments...
   OK Created 15 assignments

5. Creating 300 students...
   OK Created 300 students

6. Generating marks...
   OK Generated 6000 marks

7. Generating attendance...
   OK Generated 225000 attendance records

8. Generating alerts...
   OK Generated XX alerts

--------------------------------------------------------------------------------
SETUP COMPLETE!
--------------------------------------------------------------------------------

Summary:
  Faculty: 5 (1 subject each, 10 batches each - CORRECTED)
  Students: 300 (30 per batch, semester 4)
  Subjects: 5
  Batches: 10 (2Q31-2Q40)
  Faculty Assignments: 50 (5 faculty x 10 batches)
  Marks: 6000
  Attendance: 225000
  Alerts: XX

Sample Student: rohan.sharma.2q31.0@thapar.edu / pass123
Sample Faculty: dr.rajesh@thaparfac.edu / pass123
```

Note: If you used the original setup_complete_system.py, you will have only 15 faculty assignments instead of 50. Use the fix script to correct this.

### Step 4: Add Feedback System (Optional)

If you want the threaded feedback system with clear chat:

```bash
python backend/add_clear_chat_columns.py
```

This adds:
- cleared_by_student column to feedback_threads
- cleared_by_faculty column to feedback_threads

Note: The main setup script creates basic feedback tables. This migration adds advanced clear chat features.

### Step 5: Start Backend Server

```bash
python backend/app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

Server will be accessible at:
- Local: http://localhost:5000
- Network: http://your-ip-address:5000

### Step 6: Access Frontend

Open web browser and navigate to:

Login Page: http://localhost:5000/login_test.html

Or directly access:
- Student Portal: http://localhost:5000/student_portal.html
- Faculty Portal: http://localhost:5000/faculty_portal.html

### Step 7: Test the System

Test Student Login:
1. Go to http://localhost:5000/login_test.html
2. Email: rohan.sharma.2q31.0@thapar.edu
3. Password: pass123
4. Click Login
5. Should redirect to student portal

Test Faculty Login:
1. Go to http://localhost:5000/login_test.html
2. Email: dr.rajesh@thaparfac.edu
3. Password: pass123
4. Click Login
5. Should redirect to faculty portal

### Troubleshooting

Problem: Cannot connect to database
Solution: 
- Check config.py credentials
- Verify Oracle Database is running
- Check firewall settings
- Verify DSN format is correct

Problem: Module 'oracledb' not found
Solution: pip install oracledb

Problem: DPI-1047: Cannot locate Oracle Client library
Solution:
- Install Oracle Instant Client
- Add to PATH environment variable
- Restart terminal/IDE

Problem: ORA-01017: invalid username/password
Solution:
- Verify credentials in config.py
- Check if user has necessary privileges

Problem: Tables already exist
Solution:
- Run backend/cleanup_database.py first
- Or manually drop tables using SQL

Problem: Port 5000 already in use
Solution:
- Change port in backend/app.py (last line)
- Or stop other application using port 5000

---

## 8. Sample Credentials

### Faculty Accounts (5 total)

Account 1:
Email: dr.rajesh@thaparfac.edu
Password: pass123
Name: Dr. Rajesh Kumar
Department: CSE
Subject: Data Structures (CS401)
Batches: 2Q31, 2Q32, 2Q33

Account 2:
Email: prof.meena@thaparfac.edu
Password: pass123
Name: Prof. Meena Sharma
Department: CSE
Subject: Algorithms (CS402)
Batches: 2Q33, 2Q34, 2Q35

Account 3:
Email: dr.suresh@thaparfac.edu
Password: pass123
Name: Dr. Suresh Patel
Department: CSE
Subject: Database Management (CS403)
Batches: 2Q35, 2Q36, 2Q37

Account 4:
Email: prof.kavita@thaparfac.edu
Password: pass123
Name: Prof. Kavita Singh
Department: CSE
Subject: Operating Systems (CS404)
Batches: 2Q37, 2Q38, 2Q39

Account 5:
Email: dr.anil@thaparfac.edu
Password: pass123
Name: Dr. Anil Verma
Department: CSE
Subject: Computer Networks (CS405)
Batches: 2Q39, 2Q40, 2Q31

### Student Accounts (300 total)

Email Pattern: firstname.lastname.batch.number@thapar.edu
Password: pass123 (for all students)

Sample Students from Batch 2Q31:
1. rohan.sharma.2q31.0@thapar.edu / pass123 (Rohan Sharma)
2. priya.patel.2q31.1@thapar.edu / pass123 (Priya Patel)
3. amit.kumar.2q31.2@thapar.edu / pass123 (Amit Kumar)
... (30 students per batch)

Sample Students from Batch 2Q32:
1. rohan.sharma.2q32.0@thapar.edu / pass123
2. priya.patel.2q32.1@thapar.edu / pass123
... (30 students per batch)

All Students:
- Branch: CSE
- Semester: 4
- CGPA: Random between 6.5 and 9.5
- Total: 300 students (30 per batch x 10 batches)

Batches: 2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40

---

## API Endpoints Reference

Base URL: http://localhost:5000/api

### Authentication
POST /login
Request: { email, password }
Response: { token, role, name }

### Student Endpoints
GET /student/dashboard (requires JWT token)
GET /student/marks (requires JWT token)
GET /student/attendance (requires JWT token)
GET /student/alerts (requires JWT token)
GET /student/feedback/subjects (requires JWT token)
GET /student/feedback/:faculty_id/:subject_id (requires JWT token)
POST /student/feedback/send (requires JWT token)
DELETE /student/feedback/clear/:faculty_id/:subject_id (requires JWT token)

### Faculty Endpoints
GET /faculty/dashboard (requires JWT token)
GET /faculty/students (requires JWT token)
POST /faculty/marks/add (requires JWT token)
GET /faculty/feedback/:student_id/:subject_id (requires JWT token)
POST /faculty/feedback/send (requires JWT token)
DELETE /faculty/feedback/clear/:student_id/:subject_id (requires JWT token)

---

## Database Statistics

Total Tables: 11
Total Sequences: 10
Total Indexes: 5
Total Triggers: 1
Total Foreign Keys: 15

Data Volume:
- Users: 305 (300 students + 5 faculty)
- Students: 300
- Faculty: 5
- Subjects: 5
- Faculty Classes: 15
- Marks: 6000
- Attendance: 225000
- Alerts: Varies (50-100)
- Feedback Threads: Created on-demand
- Feedback Messages: Created on-demand

Estimated Database Size: 50-100 MB

---

## Important Notes

1. All passwords are stored in plain text (pass123). In production, use password hashing.
2. JWT secret key should be changed in production.
3. Database credentials should be stored in environment variables, not in code.
4. CORS is enabled for all origins. In production, restrict to specific domains.
5. File uploads are stored locally. In production, consider cloud storage.
6. Attendance dates are from Jan 1 to Apr 1, 2026. Update as needed.
7. Alert generation is based on 75% attendance threshold. Adjust as needed.
8. Each faculty teaches 3 batches. Some batches have multiple faculty.
9. All students are in CSE branch, semester 4. Modify as needed.
10. Feedback system creates threads and messages on-demand.

---

## Viva Preparation Quick Reference

Total Tables: 11
Database: Oracle Database 21c
Backend: Python Flask
Frontend: HTML, CSS, JavaScript

Table Creation: backend/setup_complete_system.py
Data Insertion: backend/setup_complete_system.py
Schema Reference: backend/database/complete_schema.sql
Sample SQL: backend/database/insert_data.sql

Faculty: 5 (each teaches 1 subject to ALL 10 batches)
Students: 300 (30 per batch, 10 batches)
Subjects: 5
Batches: 10 (2Q31 to 2Q40)
Faculty Assignments: 50 (5 faculty x 10 batches) - CORRECTED

Relationships: 15 foreign key relationships
Trigger: 1 (update_thread_timestamp)
Indexes: 5 (for feedback system performance)

Sample Credentials:
- Student: rohan.sharma.2q31.0@thapar.edu / pass123
- Faculty: dr.rajesh@thaparfac.edu / pass123

---

Document Version: 1.0
Last Updated: April 2026
Status: Production Ready
Prepared for: Viva and System Demonstration
