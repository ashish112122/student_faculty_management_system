# Student-Faculty Management System - Complete Database Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Database Information](#database-information)
3. [Project Folder Structure](#project-folder-structure)
4. [Database Tables](#database-tables)
5. [Table Relationships](#table-relationships)
6. [SQL Operations Used](#sql-operations-used)
7. [Database Triggers](#database-triggers)
8. [File-by-File Explanation](#file-by-file-explanation)
9. [How to Setup Database](#how-to-setup-database)
10. [Sample Credentials](#sample-credentials)

---

## Project Overview

This is a comprehensive Student-Faculty Management System built for educational institutions.

**Technology Stack:**
- **Backend**: Python Flask
- **Database**: Oracle Database 21c
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: JWT (JSON Web Tokens)

**Key Features:**
- Student and Faculty Login
- Marks Management (MST, EST, Quiz, Assignment)
- Attendance Tracking
- Automated Alerts System
- Feedback/Chat System with Attachments
- User-specific Clear Chat

---

## Database Information

**Database Type**: Oracle Database 21c
**Connection Method**: Oracle Instant Client
**Python Library**: `oracledb` (formerly cx_Oracle)

**Database Configuration** (in `backend/config.py`):
```python
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_DSN = 'host:port/service_name'
```

**Database Location**: Remote Oracle Database (cloud-hosted)
**Connection String**: Configured in `backend/config.py`

---

## Project Folder Structure

```
student_faculty_management_system/
│
├── backend/                          # Backend Python Flask application
│   ├── app.py                        # Main Flask application (API endpoints)
│   ├── config.py                     # Database configuration
│   ├── setup_complete_system.py      # Database initialization script
│   ├── add_clear_chat_columns.py     # Migration script for clear chat
│   ├── cleanup_database.py           # Database cleanup utility
│   ├── requirements.txt              # Python dependencies
│   │
│   ├── database/                     # Database schema files
│   │   ├── schema.sql                # Main database schema (all tables)
│   │   └── schema_feedback_threads.sql  # Feedback system schema
│   │
│   ├── utils/                        # Utility modules
│   │   ├── alert_checker.py          # Attendance alert generation
│   │   ├── email_service.py          # Email notification service
│   │   └── __init__.py
│   │
│   ├── tests/                        # Test scripts
│   │   ├── test_connection.py        # Database connection test
│   │   ├── check_all_tables.py       # Verify all tables exist
│   │   └── ...
│   │
│   ├── uploads/                      # File uploads directory
│   │   └── feedback_attachments/     # Chat attachment files
│   │
│   └── archive/                      # Old/backup files
│
├── frontend/                         # Frontend files
│   ├── student_portal.html           # Student dashboard (single-page app)
│   ├── faculty_portal.html           # Faculty dashboard (single-page app)
│   ├── login_test.html               # Login page
│   │
│   ├── css/                          # Stylesheets
│   │   ├── login.css
│   │   ├── dashboard.css
│   │   ├── marks.css
│   │   ├── attendance.css
│   │   ├── alerts.css
│   │   └── feedback.css
│   │
│   ├── js/                           # JavaScript files
│   │   ├── login.js                  # Login functionality
│   │   ├── dashboard.js              # Student dashboard
│   │   ├── faculty_dashboard.js      # Faculty dashboard
│   │   ├── marks.js                  # Marks display
│   │   ├── attendance.js             # Attendance display
│   │   ├── alerts.js                 # Alerts display
│   │   └── feedback.js               # Feedback/chat
│   │
│   ├── assets/                       # Static assets
│   │   ├── university-logo.png
│   │   └── README.md
│   │
│   ├── templates/                    # HTML templates (archive)
│   └── archive/                      # Old frontend files
│
├── .gitignore                        # Git ignore file
├── README.md                         # Project README
├── PROJECT_STRUCTURE.md              # Project structure documentation
├── DATABASE_CREDENTIALS_REFERENCE.md # Database credentials guide
├── WORKING_LINKS.md                  # Working URLs reference
└── DATABASE_COMPLETE_DOCUMENTATION.md # This file
```

---

## Database Tables

### Overview
The system uses **11 main tables** organized into 4 modules:

1. **Authentication Module**: users
2. **Student Module**: students, subjects, student_subjects
3. **Faculty Module**: faculty, faculty_classes, marks
4. **Attendance & Alerts Module**: attendance, alerts
5. **Feedback Module**: feedback_threads, feedback_messages

---

### 1. USERS Table
**Purpose**: Central authentication table for all users (students and faculty)

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | NUMBER | PRIMARY KEY | Unique user identifier |
| email | VARCHAR2(100) | UNIQUE, NOT NULL | User email (login username) |
| password | VARCHAR2(100) | NOT NULL | User password (plain text) |
| name | VARCHAR2(100) | NOT NULL | Full name |
| role | VARCHAR2(20) | NOT NULL, CHECK | 'student' or 'faculty' |

**Sequence**: `users_seq` (starts at 1)

**Usage**: 
- Login authentication
- Role-based access control
- Referenced by students and faculty tables

**Sample Data**:
```
user_id: 1
email: rohan.sharma.2q31.0@thapar.edu
password: pass123
name: Rohan Sharma
role: student
```

---

### 2. STUDENTS Table
**Purpose**: Store student-specific information

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| student_id | NUMBER | PRIMARY KEY | Unique student identifier |
| user_id | NUMBER | UNIQUE, NOT NULL, FK | References users table |
| name | VARCHAR2(100) | NOT NULL | Student full name |
| branch | VARCHAR2(50) | NOT NULL | Department (e.g., 'CSE') |
| semester | NUMBER | NOT NULL | Current semester (e.g., 4) |
| class_name | VARCHAR2(10) | NOT NULL | Batch/class (e.g., '2Q31') |
| cgpa | NUMBER(3,2) | NOT NULL | CGPA (e.g., 8.75) |

**Sequence**: `students_seq` (starts at 1)

**Foreign Keys**:
- `user_id` → `users(user_id)`

**Usage**:
- Student profile information
- Class/batch assignment
- Academic performance tracking

**Sample Data**:
```
student_id: 1
user_id: 1
name: Rohan Sharma
branch: CSE
semester: 4
class_name: 2Q31
cgpa: 8.75
```

---

### 3. FACULTY Table
**Purpose**: Store faculty-specific information

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| faculty_id | NUMBER | PRIMARY KEY | Unique faculty identifier |
| user_id | NUMBER | UNIQUE, NOT NULL, FK | References users table |
| name | VARCHAR2(100) | NOT NULL | Faculty full name |
| department | VARCHAR2(50) | NOT NULL | Department (e.g., 'CSE') |

**Sequence**: `faculty_seq` (starts at 1)

**Foreign Keys**:
- `user_id` → `users(user_id)`

**Usage**:
- Faculty profile information
- Department assignment
- Teaching assignments

**Sample Data**:
```
faculty_id: 1
user_id: 301
name: Dr. Rajesh Kumar
department: CSE
```

---

### 4. SUBJECTS Table
**Purpose**: Store all subjects/courses offered

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| subject_id | NUMBER | PRIMARY KEY | Unique subject identifier |
| subject_name | VARCHAR2(100) | NOT NULL | Subject name |
| subject_code | VARCHAR2(20) | UNIQUE, NOT NULL | Subject code (e.g., 'CS401') |

**Sequence**: `subjects_seq` (starts at 1)

**Usage**:
- Course catalog
- Referenced by marks, attendance, feedback

**Sample Data**:
```
subject_id: 1
subject_name: Data Structures
subject_code: CS401
```

**Total Subjects**: 5
1. Data Structures (CS401)
2. Algorithms (CS402)
3. Database Management (CS403)
4. Operating Systems (CS404)
5. Computer Networks (CS405)

---

### 5. FACULTY_CLASSES Table
**Purpose**: Map faculty to subjects and classes they teach

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| faculty_class_id | NUMBER | PRIMARY KEY | Unique assignment identifier |
| faculty_id | NUMBER | NOT NULL, FK | References faculty table |
| subject_id | NUMBER | NOT NULL, FK | References subjects table |
| class_name | VARCHAR2(10) | NOT NULL | Batch/class (e.g., '2Q31') |

**Sequence**: `faculty_classes_seq` (starts at 1)

**Foreign Keys**:
- `faculty_id` → `faculty(faculty_id)`
- `subject_id` → `subjects(subject_id)`

**Usage**:
- Faculty teaching assignments
- Determines which students a faculty can see
- Used for marks entry and feedback

**Sample Data**:
```
faculty_class_id: 1
faculty_id: 1
subject_id: 1
class_name: 2Q31
```

**Assignment Pattern**:
- Each faculty teaches 1 subject
- Each faculty teaches 3 batches
- Total: 15 assignments (5 faculty × 3 batches)

---

### 6. MARKS Table
**Purpose**: Store student marks for all assessments

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| mark_id | NUMBER | PRIMARY KEY | Unique mark entry identifier |
| student_id | NUMBER | NOT NULL, FK | References students table |
| subject_id | NUMBER | NOT NULL, FK | References subjects table |
| class_name | VARCHAR2(10) | NOT NULL | Batch/class |
| assessment_type | VARCHAR2(20) | NOT NULL, CHECK | 'MST', 'EST', 'Quiz', 'Assignment' |
| marks_obtained | NUMBER | NOT NULL | Marks scored |
| max_marks | NUMBER | NOT NULL | Maximum marks possible |

**Sequence**: `marks_seq` (starts at 1)

**Foreign Keys**:
- `student_id` → `students(student_id)`
- `subject_id` → `subjects(subject_id)`

**Assessment Types**:
- MST (Mid-Semester Test): 30 marks
- EST (End-Semester Test): 40 marks
- Quiz: 15 marks
- Assignment: 15 marks

**Usage**:
- Student performance tracking
- Grade calculation
- Faculty marks entry

**Sample Data**:
```
mark_id: 1
student_id: 1
subject_id: 1
class_name: 2Q31
assessment_type: MST
marks_obtained: 25
max_marks: 30
```

**Total Records**: ~6000 (300 students × 5 subjects × 4 assessments)

---

### 7. ATTENDANCE Table
**Purpose**: Track daily attendance for each student in each subject

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| attendance_id | NUMBER | PRIMARY KEY | Unique attendance record ID |
| student_id | NUMBER | NOT NULL, FK | References students table |
| subject_id | NUMBER | NOT NULL, FK | References subjects table |
| class_name | VARCHAR2(10) | NOT NULL | Batch/class |
| attendance_date | DATE | NOT NULL | Date of attendance |
| status | CHAR(1) | NOT NULL, CHECK | 'P' (Present) or 'A' (Absent) |

**Sequence**: `attendance_seq` (starts at 1)

**Foreign Keys**:
- `student_id` → `students(student_id)`
- `subject_id` → `subjects(subject_id)`

**Date Range**: January 1, 2026 to April 1, 2026 (weekdays only)

**Usage**:
- Daily attendance tracking
- Attendance percentage calculation
- Alert generation for low attendance

**Sample Data**:
```
attendance_id: 1
student_id: 1
subject_id: 1
class_name: 2Q31
attendance_date: 2026-01-02
status: P
```

**Total Records**: ~225,000 (300 students × 5 subjects × ~150 days)

**Attendance Calculation**:
```sql
SELECT 
    (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as percentage
FROM attendance
WHERE student_id = :student_id AND subject_id = :subject_id
```

---

### 8. ALERTS Table
**Purpose**: Store automated alerts for students (low attendance, low marks, etc.)

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| alert_id | NUMBER | PRIMARY KEY | Unique alert identifier |
| student_id | NUMBER | NOT NULL, FK | References students table |
| subject_id | NUMBER | FK | References subjects table (nullable) |
| alert_type | VARCHAR2(20) | NOT NULL | 'Warning', 'Alert', 'Critical' |
| message | VARCHAR2(500) | NOT NULL | Alert message text |
| is_read | NUMBER(1) | DEFAULT 0 | 0 = unread, 1 = read |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Alert creation time |

**Sequence**: `alerts_seq` (starts at 1)

**Foreign Keys**:
- `student_id` → `students(student_id)`
- `subject_id` → `subjects(subject_id)` (optional)

**Alert Types**:
- **Warning**: Attendance 65-75%
- **Alert**: Attendance 50-65%
- **Critical**: Attendance < 50%

**Usage**:
- Notify students of low attendance
- Notify students of low marks
- System-generated notifications

**Sample Data**:
```
alert_id: 1
student_id: 1
subject_id: 1
alert_type: Warning
message: Low attendance in Data Structures: 72.5%
is_read: 0
created_at: 2026-04-05 10:30:00
```

**Alert Generation Logic**:
```sql
-- Generate alert if attendance < 75%
SELECT student_id, subject_id, 
       (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as percentage
FROM attendance
GROUP BY student_id, subject_id
HAVING (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
```

---

### 9. FEEDBACK_THREADS Table
**Purpose**: Store conversation metadata between students and faculty

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| thread_id | NUMBER | PRIMARY KEY | Unique thread identifier |
| student_id | NUMBER | NOT NULL, FK | References students table |
| faculty_id | NUMBER | NOT NULL, FK | References faculty table |
| subject_id | NUMBER | NOT NULL, FK | References subjects table |
| thread_title | VARCHAR2(200) | | Conversation title (optional) |
| initiated_by | VARCHAR2(20) | NOT NULL, CHECK | 'student' or 'faculty' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Thread creation time |
| last_message_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last message timestamp |
| cleared_by_student | TIMESTAMP | DEFAULT NULL | When student cleared chat |
| cleared_by_faculty | TIMESTAMP | DEFAULT NULL | When faculty cleared chat |

**Sequence**: `feedback_threads_seq` (starts at 1)

**Foreign Keys**:
- `student_id` → `students(student_id)`
- `faculty_id` → `faculty(faculty_id)`
- `subject_id` → `subjects(subject_id)`

**Indexes**:
- `idx_feedback_threads_student` on `student_id`
- `idx_feedback_threads_faculty` on `faculty_id`
- `idx_feedback_threads_subject` on `subject_id`

**Usage**:
- One thread per student-faculty-subject combination
- Tracks conversation metadata
- User-specific clear chat functionality

**Sample Data**:
```
thread_id: 1
student_id: 1
faculty_id: 1
subject_id: 1
thread_title: NULL
initiated_by: student
created_at: 2026-04-01 10:00:00
last_message_at: 2026-04-05 15:30:00
cleared_by_student: NULL
cleared_by_faculty: NULL
```

**Clear Chat Logic**:
- When student clears: `cleared_by_student` = current timestamp
- When faculty clears: `cleared_by_faculty` = current timestamp
- Messages before clear timestamp are hidden for that user
- Other user still sees all messages

---

### 10. FEEDBACK_MESSAGES Table
**Purpose**: Store individual messages in feedback conversations

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| message_id | NUMBER | PRIMARY KEY | Unique message identifier |
| thread_id | NUMBER | NOT NULL, FK | References feedback_threads |
| sender_id | NUMBER | NOT NULL, FK | References users table |
| sender_role | VARCHAR2(20) | NOT NULL, CHECK | 'student' or 'faculty' |
| message | CLOB | NOT NULL | Message text content |
| is_read | NUMBER(1) | DEFAULT 0 | 0 = unread, 1 = read |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Message sent time |
| attachment_path | VARCHAR2(500) | | File path (if attachment) |
| attachment_name | VARCHAR2(200) | | Original filename |
| attachment_type | VARCHAR2(50) | | File MIME type |

**Sequence**: `feedback_messages_seq` (starts at 1)

**Foreign Keys**:
- `thread_id` → `feedback_threads(thread_id)` ON DELETE CASCADE
- `sender_id` → `users(user_id)`

**Indexes**:
- `idx_feedback_messages_thread` on `thread_id`
- `idx_feedback_messages_sender` on `sender_id`

**Usage**:
- Store chat messages
- Support file attachments
- Track read/unread status

**Sample Data**:
```
message_id: 1
thread_id: 1
sender_id: 1
sender_role: student
message: Hello sir, I have a doubt about linked lists
is_read: 1
created_at: 2026-04-05 10:30:00
attachment_path: NULL
attachment_name: NULL
attachment_type: NULL
```

**Attachment Support**:
- Files stored in: `backend/uploads/feedback_attachments/`
- Filename format: `YYYYMMDD_HHMMSS_originalname.ext`
- Supported types: PDF, DOCX, images, etc.

---

## Table Relationships

### Entity Relationship Diagram (Text Format)

```
                                    USERS
                                      |
                    +----------------+----------------+
                    |                                 |
                STUDENTS                           FACULTY
                    |                                 |
        +-----------+-----------+                     |
        |           |           |                     |
    MARKS    ATTENDANCE    ALERTS              FACULTY_CLASSES
        |           |           |                     |
        |           |           |                     |
        +-----SUBJECTS----------+---------------------+
                    |
                    |
            FEEDBACK_THREADS
                    |
            FEEDBACK_MESSAGES
```

### Detailed Relationships

#### 1. Users → Students (One-to-One)
```sql
users.user_id (PK) ←→ students.user_id (FK, UNIQUE)
```
- Each user can be one student
- Each student has one user account

#### 2. Users → Faculty (One-to-One)
```sql
users.user_id (PK) ←→ faculty.user_id (FK, UNIQUE)
```
- Each user can be one faculty
- Each faculty has one user account

#### 3. Students → Marks (One-to-Many)
```sql
students.student_id (PK) ←→ marks.student_id (FK)
```
- One student has many mark entries
- Each mark belongs to one student

#### 4. Subjects → Marks (One-to-Many)
```sql
subjects.subject_id (PK) ←→ marks.subject_id (FK)
```
- One subject has many mark entries
- Each mark belongs to one subject

#### 5. Students → Attendance (One-to-Many)
```sql
students.student_id (PK) ←→ attendance.student_id (FK)
```
- One student has many attendance records
- Each attendance record belongs to one student

#### 6. Subjects → Attendance (One-to-Many)
```sql
subjects.subject_id (PK) ←→ attendance.subject_id (FK)
```
- One subject has many attendance records
- Each attendance record belongs to one subject

#### 7. Students → Alerts (One-to-Many)
```sql
students.student_id (PK) ←→ alerts.student_id (FK)
```
- One student has many alerts
- Each alert belongs to one student

#### 8. Subjects → Alerts (One-to-Many, Optional)
```sql
subjects.subject_id (PK) ←→ alerts.subject_id (FK, NULLABLE)
```
- One subject can have many alerts
- Each alert may belong to one subject (or none)

#### 9. Faculty → Faculty_Classes (One-to-Many)
```sql
faculty.faculty_id (PK) ←→ faculty_classes.faculty_id (FK)
```
- One faculty teaches many classes
- Each class assignment belongs to one faculty

#### 10. Subjects → Faculty_Classes (One-to-Many)
```sql
subjects.subject_id (PK) ←→ faculty_classes.subject_id (FK)
```
- One subject is taught in many classes
- Each class assignment has one subject

#### 11. Students → Feedback_Threads (One-to-Many)
```sql
students.student_id (PK) ←→ feedback_threads.student_id (FK)
```
- One student has many feedback threads
- Each thread belongs to one student

#### 12. Faculty → Feedback_Threads (One-to-Many)
```sql
faculty.faculty_id (PK) ←→ feedback_threads.faculty_id (FK)
```
- One faculty has many feedback threads
- Each thread belongs to one faculty

#### 13. Subjects → Feedback_Threads (One-to-Many)
```sql
subjects.subject_id (PK) ←→ feedback_threads.subject_id (FK)
```
- One subject has many feedback threads
- Each thread is about one subject

#### 14. Feedback_Threads → Feedback_Messages (One-to-Many)
```sql
feedback_threads.thread_id (PK) ←→ feedback_messages.thread_id (FK)
```
- One thread has many messages
- Each message belongs to one thread
- CASCADE DELETE: Deleting thread deletes all messages

#### 15. Users → Feedback_Messages (One-to-Many)
```sql
users.user_id (PK) ←→ feedback_messages.sender_id (FK)
```
- One user sends many messages
- Each message has one sender

---

## SQL Operations Used

### 1. SELECT Queries

#### Simple SELECT
```sql
-- Get all students
SELECT * FROM students;

-- Get student by ID
SELECT * FROM students WHERE student_id = :student_id;
```

#### SELECT with JOIN
```sql
-- Get student with user details
SELECT s.*, u.email, u.name 
FROM students s
JOIN users u ON s.user_id = u.user_id
WHERE s.student_id = :student_id;

-- Get marks with subject names
SELECT m.*, s.subject_name, s.subject_code
FROM marks m
JOIN subjects s ON m.subject_id = s.subject_id
WHERE m.student_id = :student_id;
```

#### SELECT with Aggregation
```sql
-- Calculate attendance percentage
SELECT 
    student_id,
    subject_id,
    COUNT(*) as total_classes,
    SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) as present,
    (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as percentage
FROM attendance
WHERE student_id = :student_id
GROUP BY student_id, subject_id;

-- Calculate total marks
SELECT 
    student_id,
    subject_id,
    SUM(marks_obtained) as total_obtained,
    SUM(max_marks) as total_max,
    (SUM(marks_obtained) / SUM(max_marks)) * 100 as percentage
FROM marks
WHERE student_id = :student_id
GROUP BY student_id, subject_id;
```

#### SELECT with Subquery
```sql
-- Get students with low attendance
SELECT s.student_id, s.name, sub.subject_name, att.percentage
FROM students s
JOIN (
    SELECT student_id, subject_id,
           (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as percentage
    FROM attendance
    GROUP BY student_id, subject_id
    HAVING (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 75
) att ON s.student_id = att.student_id
JOIN subjects sub ON att.subject_id = sub.subject_id;
```

---

### 2. INSERT Queries

#### Simple INSERT
```sql
-- Insert new user
INSERT INTO users (user_id, email, password, name, role)
VALUES (users_seq.NEXTVAL, :email, :password, :name, :role);

-- Insert new student
INSERT INTO students (student_id, user_id, name, branch, semester, class_name, cgpa)
VALUES (students_seq.NEXTVAL, :user_id, :name, :branch, :semester, :class_name, :cgpa);
```

#### INSERT with Sequence
```sql
-- Insert and get generated ID
INSERT INTO marks (mark_id, student_id, subject_id, class_name, assessment_type, marks_obtained, max_marks)
VALUES (marks_seq.NEXTVAL, :student_id, :subject_id, :class_name, :assessment_type, :marks_obtained, :max_marks);

-- Get the inserted ID
SELECT marks_seq.CURRVAL FROM dual;
```

#### Bulk INSERT
```sql
-- Insert multiple attendance records
INSERT ALL
    INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
    VALUES (attendance_seq.NEXTVAL, 1, 1, '2Q31', DATE '2026-01-02', 'P')
    INTO attendance (attendance_id, student_id, subject_id, class_name, attendance_date, status)
    VALUES (attendance_seq.NEXTVAL, 1, 2, '2Q31', DATE '2026-01-02', 'P')
SELECT * FROM dual;
```

---

### 3. UPDATE Queries

#### Simple UPDATE
```sql
-- Mark alert as read
UPDATE alerts 
SET is_read = 1 
WHERE alert_id = :alert_id;

-- Update student CGPA
UPDATE students 
SET cgpa = :new_cgpa 
WHERE student_id = :student_id;
```

#### UPDATE with Condition
```sql
-- Mark all messages as read in a thread
UPDATE feedback_messages 
SET is_read = 1 
WHERE thread_id = :thread_id 
  AND sender_role = 'student' 
  AND is_read = 0;

-- Update last message timestamp
UPDATE feedback_threads 
SET last_message_at = CURRENT_TIMESTAMP 
WHERE thread_id = :thread_id;
```

#### UPDATE for Clear Chat
```sql
-- Student clears chat
UPDATE feedback_threads 
SET cleared_by_student = SYSDATE 
WHERE thread_id = :thread_id;

-- Faculty clears chat
UPDATE feedback_threads 
SET cleared_by_faculty = SYSDATE 
WHERE thread_id = :thread_id;
```

---

### 4. DELETE Queries

#### Simple DELETE
```sql
-- Delete a specific alert
DELETE FROM alerts 
WHERE alert_id = :alert_id;

-- Delete old attendance records
DELETE FROM attendance 
WHERE attendance_date < DATE '2025-01-01';
```

#### DELETE with CASCADE
```sql
-- Delete feedback thread (automatically deletes all messages)
DELETE FROM feedback_threads 
WHERE thread_id = :thread_id;
-- This also deletes all feedback_messages due to ON DELETE CASCADE
```

---

### 5. Complex Queries

#### Multi-table JOIN
```sql
-- Get complete student dashboard data
SELECT 
    s.student_id,
    s.name,
    s.class_name,
    s.cgpa,
    sub.subject_name,
    sub.subject_code,
    m.assessment_type,
    m.marks_obtained,
    m.max_marks,
    att.percentage as attendance_percentage
FROM students s
JOIN marks m ON s.student_id = m.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
LEFT JOIN (
    SELECT student_id, subject_id,
           (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as percentage
    FROM attendance
    GROUP BY student_id, subject_id
) att ON s.student_id = att.student_id AND sub.subject_id = att.subject_id
WHERE s.student_id = :student_id;
```

#### Filtered Messages (Clear Chat)
```sql
-- Get messages for student (after clear timestamp)
SELECT message_id, sender_role, message, is_read, created_at
FROM feedback_messages
WHERE thread_id = :thread_id 
  AND created_at > :cleared_by_student
ORDER BY created_at ASC;
```

---

## Database Triggers

### 1. Update Thread Timestamp Trigger

**Trigger Name**: `update_thread_timestamp`

**Purpose**: Automatically update `last_message_at` in `feedback_threads` when a new message is added

**Type**: AFTER INSERT trigger on `feedback_messages`

**Code**:
```sql
CREATE OR REPLACE TRIGGER update_thread_timestamp
AFTER INSERT ON feedback_messages
FOR EACH ROW
BEGIN
    UPDATE feedback_threads
    SET last_message_at = CURRENT_TIMESTAMP
    WHERE thread_id = :NEW.thread_id;
END;
/
```

**How it Works**:
1. When a new message is inserted into `feedback_messages`
2. Trigger automatically fires
3. Updates the `last_message_at` column in `feedback_threads`
4. Uses the `thread_id` from the newly inserted message

**Usage Example**:
```sql
-- Insert a new message
INSERT INTO feedback_messages (message_id, thread_id, sender_id, sender_role, message)
VALUES (feedback_messages_seq.NEXTVAL, 1, 1, 'student', 'Hello sir');

-- Trigger automatically updates:
-- UPDATE feedback_threads SET last_message_at = CURRENT_TIMESTAMP WHERE thread_id = 1;
```

**Benefits**:
- Keeps thread metadata up-to-date automatically
- No need to manually update in application code
- Ensures data consistency
- Used for sorting threads by recent activity

---

### 2. Alert Generation (Application-Level)

**Note**: Alert generation is handled in application code, not database triggers

**Location**: `backend/utils/alert_checker.py`

**Logic**:
```python
# Check attendance and generate alerts
cursor.execute("""
    SELECT s.student_id, a.subject_id, sub.subject_name,
           COUNT(*) as total,
           SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
    FROM students s
    JOIN attendance a ON s.student_id = a.student_id
    JOIN subjects sub ON a.subject_id = sub.subject_id
    GROUP BY s.student_id, a.subject_id, sub.subject_name
    HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
""")

for student_id, subject_id, subject_name, total, present in cursor.fetchall():
    percentage = (present / total) * 100
    alert_type = 'Critical' if percentage < 50 else 'Warning'
    message = f"Low attendance in {subject_name}: {percentage:.2f}%"
    
    # Insert alert
    cursor.execute("""
        INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message)
        VALUES (alerts_seq.NEXTVAL, :student_id, :subject_id, :alert_type, :message)
    """, {...})
```

**Why Not a Trigger?**
- Complex business logic
- Requires aggregation across multiple records
- Better performance when run periodically
- Easier to test and maintain

---

## File-by-File Explanation

### Backend Files

#### 1. `backend/app.py`
**Purpose**: Main Flask application with all API endpoints

**Key Components**:
- **Authentication**: Login, JWT token generation
- **Student APIs**: Dashboard, marks, attendance, alerts, feedback
- **Faculty APIs**: Dashboard, students list, marks entry, feedback
- **File Upload**: Attachment handling for feedback

**Main Endpoints**:
```python
# Authentication
POST /api/login                          # User login

# Student APIs
GET  /api/student/dashboard              # Student dashboard data
GET  /api/student/marks                  # Student marks
GET  /api/student/attendance             # Student attendance
GET  /api/student/alerts                 # Student alerts
GET  /api/student/feedback/subjects      # Feedback subjects list
GET  /api/student/feedback/<fac>/<subj>  # Get messages
POST /api/student/feedback/send          # Send message
DELETE /api/student/feedback/clear/<f>/<s> # Clear chat

# Faculty APIs
GET  /api/faculty/dashboard              # Faculty dashboard
GET  /api/faculty/students               # Students in class
POST /api/faculty/marks/add              # Add marks
GET  /api/faculty/feedback/<s>/<subj>    # Get messages
POST /api/faculty/feedback/send          # Send message
DELETE /api/faculty/feedback/clear/<s>/<subj> # Clear chat
```

**Database Connection**:
```python
def get_db_connection():
    return oracledb.connect(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dsn=Config.DB_DSN
    )
```

**JWT Authentication**:
```python
@token_required
def protected_route():
    # request.user_id available
    # request.role available
```

---

#### 2. `backend/config.py`
**Purpose**: Database configuration and credentials

**Content**:
```python
class Config:
    DB_USER = 'your_username'
    DB_PASSWORD = 'your_password'
    DB_DSN = 'host:port/service_name'
    SECRET_KEY = 'your-secret-key-here'
```

**Usage**: Imported by all files needing database access

---

#### 3. `backend/setup_complete_system.py`
**Purpose**: Initialize database with schema and sample data

**What it Does**:
1. Drops existing tables (if any)
2. Creates all tables with correct schema
3. Creates sequences
4. Inserts 5 subjects
5. Inserts 5 faculty members
6. Creates faculty-class assignments
7. Inserts 300 students (30 per batch)
8. Generates marks for all students
9. Generates attendance records (Jan-Apr 2026)
10. Generates alerts for low attendance

**How to Run**:
```bash
python backend/setup_complete_system.py
```

**Output**:
```
Faculty: 5 (1 subject each, 3 batches each)
Students: 300 (30 per batch, semester 4)
Subjects: 5
Batches: 10 (2Q31-2Q40)
Marks: ~6000
Attendance: ~225000
Alerts: varies
```

---

#### 4. `backend/add_clear_chat_columns.py`
**Purpose**: Migration script to add user-specific clear chat columns

**What it Does**:
1. Adds `cleared_by_student` column to `feedback_threads`
2. Adds `cleared_by_faculty` column to `feedback_threads`
3. Verifies columns were added successfully

**How to Run**:
```bash
python backend/add_clear_chat_columns.py
```

**SQL Executed**:
```sql
ALTER TABLE feedback_threads ADD cleared_by_student TIMESTAMP DEFAULT NULL;
ALTER TABLE feedback_threads ADD cleared_by_faculty TIMESTAMP DEFAULT NULL;
```

---

#### 5. `backend/cleanup_database.py`
**Purpose**: Clean up database (remove test data, reset sequences)

**Usage**: For development/testing cleanup

---

#### 6. `backend/requirements.txt`
**Purpose**: Python package dependencies

**Content**:
```
Flask==3.0.0
Flask-CORS==4.0.0
oracledb==2.0.0
PyJWT==2.8.0
python-dotenv==1.0.0
```

**Installation**:
```bash
pip install -r backend/requirements.txt
```

---

#### 7. `backend/database/schema.sql`
**Purpose**: Complete database schema definition

**Contains**:
- All CREATE TABLE statements
- All CREATE SEQUENCE statements
- Table constraints (PRIMARY KEY, FOREIGN KEY, CHECK)
- Comments explaining each table

**Usage**: Reference document for database structure

---

#### 8. `backend/database/schema_feedback_threads.sql`
**Purpose**: Feedback system schema with threading support

**Contains**:
- `feedback_threads` table definition
- `feedback_messages` table definition
- Indexes for performance
- Trigger for updating `last_message_at`

**Features**:
- Thread-based conversations
- File attachment support
- User-specific clear chat
- Read/unread tracking

---

#### 9. `backend/utils/alert_checker.py`
**Purpose**: Generate attendance alerts

**Logic**:
1. Calculate attendance percentage for each student-subject
2. Identify students with < 75% attendance
3. Generate appropriate alerts (Warning/Critical)
4. Insert into alerts table

**Can be run**:
- Manually: `python backend/utils/alert_checker.py`
- Scheduled: Cron job or task scheduler
- On-demand: Called from API

---

#### 10. `backend/utils/email_service.py`
**Purpose**: Send email notifications (future feature)

**Status**: Placeholder for email functionality

---

### Frontend Files

#### 1. `frontend/student_portal.html`
**Purpose**: Complete student dashboard (single-page application)

**Sections**:
- **Dashboard**: Overview with cards for Marks, Attendance, Alerts, Feedback
- **Marks View**: Display all marks by subject and assessment type
- **Attendance View**: Display attendance percentage by subject
- **Alerts View**: Display all alerts with read/unread status
- **Feedback View**: Chat interface with faculty

**Features**:
- Single-page app (no page reloads)
- Real-time chat updates
- File attachment support
- User-specific clear chat
- Responsive design

**JavaScript Functions**:
```javascript
showDashboard()      // Show dashboard view
showMarks()          // Show marks view
showAttendance()     // Show attendance view
showAlerts()         // Show alerts view
showFeedback()       // Show feedback/chat view
loadChatMessages()   // Load chat messages
sendMessage()        // Send chat message
clearCurrentChat()   // Clear chat (user-specific)
```

---

#### 2. `frontend/faculty_portal.html`
**Purpose**: Complete faculty dashboard (single-page application)

**Sections**:
- **Dashboard**: Overview of classes taught
- **My Classes**: List of assigned classes
- **Add Marks**: Form to add student marks
- **Marks Report**: View marks by class and subject
- **Feedback**: Chat interface with students

**Features**:
- Class and student selection
- Marks entry form
- Marks report generation
- Chat with students
- File attachment support
- User-specific clear chat

**JavaScript Functions**:
```javascript
showDashboard()      // Show dashboard view
showMyClasses()      // Show classes list
showAddMarks()       // Show add marks form
showMarksReport()    // Show marks report
showFeedback()       // Show feedback/chat view
selectStudent()      // Select student for chat
loadChatMessages()   // Load chat messages
sendMessage()        // Send chat message
clearCurrentChat()   // Clear chat (user-specific)
```

---

#### 3. `frontend/login_test.html`
**Purpose**: Login page for both students and faculty

**Features**:
- Email and password input
- Role-based redirect (student/faculty portal)
- JWT token storage
- Error handling

**JavaScript**:
```javascript
async function login() {
    const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    localStorage.setItem('token', data.token);
    
    if (data.role === 'student') {
        window.location.href = 'student_portal.html';
    } else {
        window.location.href = 'faculty_portal.html';
    }
}
```

---

#### 4. CSS Files (`frontend/css/`)
**Purpose**: Styling for different sections

**Files**:
- `login.css`: Login page styles
- `dashboard.css`: Dashboard layout and cards
- `marks.css`: Marks table styling
- `attendance.css`: Attendance display
- `alerts.css`: Alert cards and badges
- `feedback.css`: Chat interface styling

---

#### 5. JavaScript Files (`frontend/js/`)
**Purpose**: Modular JavaScript for different features

**Note**: Most functionality is now in portal HTML files (student_portal.html, faculty_portal.html)

**Legacy Files** (in `frontend/js/`):
- `login.js`: Login functionality
- `dashboard.js`: Dashboard logic
- `marks.js`: Marks display
- `attendance.js`: Attendance display
- `alerts.js`: Alerts display
- `feedback.js`: Chat functionality

---

## How to Setup Database

### Prerequisites
1. Oracle Database 21c installed and running
2. Python 3.8+ installed
3. Oracle Instant Client installed
4. Database credentials (username, password, DSN)

---

### Step 1: Configure Database Credentials

Edit `backend/config.py`:
```python
class Config:
    DB_USER = 'your_oracle_username'
    DB_PASSWORD = 'your_oracle_password'
    DB_DSN = 'host:port/service_name'  # e.g., 'localhost:1521/XEPDB1'
    SECRET_KEY = 'your-secret-key-here'
```

---

### Step 2: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Packages Installed**:
- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- oracledb: Oracle database driver
- PyJWT: JWT token handling
- python-dotenv: Environment variables

---

### Step 3: Initialize Database

Run the setup script to create all tables and populate with sample data:

```bash
python backend/setup_complete_system.py
```

**This will**:
1. Drop existing tables (if any)
2. Create all 11 tables
3. Create sequences
4. Insert 5 subjects
5. Insert 5 faculty members
6. Create 15 faculty-class assignments
7. Insert 300 students (30 per batch)
8. Generate ~6000 marks records
9. Generate ~225000 attendance records
10. Generate alerts for low attendance

**Expected Output**:
```
================================================================================
SETTING UP COMPLETE SYSTEM
================================================================================

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

================================================================================
SETUP COMPLETE!
================================================================================

Summary:
  Faculty: 5 (1 subject each, 3 batches each)
  Students: 300 (30 per batch, semester 4)
  Subjects: 5
  Batches: 10 (2Q31-2Q40)
  Marks: 6000
  Attendance: 225000
  Alerts: XX

Sample Student: rohan.sharma.2q31.0@thapar.edu / pass123
Sample Faculty: dr.rajesh@thaparfac.edu / pass123
```

---

### Step 4: Add Feedback System (Optional)

If you want the threaded feedback system with clear chat:

```bash
python backend/add_clear_chat_columns.py
```

**This will**:
1. Add `cleared_by_student` column to `feedback_threads`
2. Add `cleared_by_faculty` column to `feedback_threads`
3. Verify columns were added

**Note**: The main setup script creates basic feedback table. This migration adds advanced features.

---

### Step 5: Start Backend Server

```bash
python backend/app.py
```

**Expected Output**:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

**Server will be accessible at**:
- Local: `http://localhost:5000`
- Network: `http://your-ip:5000`

---

### Step 6: Access Frontend

Open in browser:
- **Login**: `http://localhost:5000/login_test.html`
- **Student Portal**: `http://localhost:5000/student_portal.html`
- **Faculty Portal**: `http://localhost:5000/faculty_portal.html`

---

### Step 7: Test the System

#### Test Student Login
1. Go to `http://localhost:5000/login_test.html`
2. Email: `rohan.sharma.2q31.0@thapar.edu`
3. Password: `pass123`
4. Click Login
5. Should redirect to student portal

#### Test Faculty Login
1. Go to `http://localhost:5000/login_test.html`
2. Email: `dr.rajesh@thaparfac.edu`
3. Password: `pass123`
4. Click Login
5. Should redirect to faculty portal

---

### Troubleshooting

#### Error: "Module 'oracledb' not found"
```bash
pip install oracledb
```

#### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client library"
- Install Oracle Instant Client
- Add to PATH environment variable
- Restart terminal/IDE

#### Error: "ORA-12541: TNS:no listener"
- Check if Oracle Database is running
- Verify DSN in config.py
- Check firewall settings

#### Error: "ORA-01017: invalid username/password"
- Verify credentials in config.py
- Check if user has necessary privileges

#### Error: "Table already exists"
- Tables already created
- Run cleanup script first:
  ```bash
  python backend/cleanup_database.py
  ```

---

## Sample Credentials

### Faculty Accounts (5 total)

| Email | Password | Name | Department | Subject | Batches |
|-------|----------|------|------------|---------|---------|
| dr.rajesh@thaparfac.edu | pass123 | Dr. Rajesh Kumar | CSE | Data Structures | 2Q31, 2Q32, 2Q33 |
| prof.meena@thaparfac.edu | pass123 | Prof. Meena Sharma | CSE | Algorithms | 2Q33, 2Q34, 2Q35 |
| dr.suresh@thaparfac.edu | pass123 | Dr. Suresh Patel | CSE | Database Management | 2Q35, 2Q36, 2Q37 |
| prof.kavita@thaparfac.edu | pass123 | Prof. Kavita Singh | CSE | Operating Systems | 2Q37, 2Q38, 2Q39 |
| dr.anil@thaparfac.edu | pass123 | Dr. Anil Verma | CSE | Computer Networks | 2Q39, 2Q40, 2Q31 |

---

### Student Accounts (300 total)

**Pattern**: `firstname.lastname.batch.number@thapar.edu`

**Sample Students from Batch 2Q31**:
- `rohan.sharma.2q31.0@thapar.edu` / pass123
- `priya.patel.2q31.1@thapar.edu` / pass123
- `amit.kumar.2q31.2@thapar.edu` / pass123
- ... (30 students per batch)

**All Batches**: 2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40

**Student Details**:
- Branch: CSE
- Semester: 4
- CGPA: Random between 6.5 and 9.5

---

### Subjects (5 total)

| Subject ID | Subject Name | Subject Code |
|------------|--------------|--------------|
| 1 | Data Structures | CS401 |
| 2 | Algorithms | CS402 |
| 3 | Database Management | CS403 |
| 4 | Operating Systems | CS404 |
| 5 | Computer Networks | CS405 |

---

## Database Statistics

### Current Data Volume

| Table | Approximate Records |
|-------|---------------------|
| users | 305 (300 students + 5 faculty) |
| students | 300 |
| faculty | 5 |
| subjects | 5 |
| faculty_classes | 15 |
| marks | 6,000 (300 × 5 × 4) |
| attendance | 225,000 (300 × 5 × 150 days) |
| alerts | Varies (based on low attendance) |
| feedback_threads | Created on-demand |
| feedback_messages | Created on-demand |

---

### Storage Requirements

**Estimated Database Size**: ~50-100 MB

**Breakdown**:
- users: < 1 MB
- students: < 1 MB
- faculty: < 1 MB
- subjects: < 1 MB
- marks: ~2 MB
- attendance: ~30 MB
- alerts: ~1 MB
- feedback: Varies (depends on usage)
- Indexes: ~10 MB

---

## Viva Questions & Answers

### Q1: Which database are you using?
**A**: Oracle Database 21c

### Q2: Where are the tables created?
**A**: Tables are created by running `backend/setup_complete_system.py`. The schema is defined in `backend/database/schema.sql` and `backend/database/schema_feedback_threads.sql`.

### Q3: How many tables are there?
**A**: 11 tables total:
1. users
2. students
3. faculty
4. subjects
5. faculty_classes
6. marks
7. attendance
8. alerts
9. feedback_threads
10. feedback_messages
11. (student_subjects - optional)

### Q4: Explain the relationship between students and marks.
**A**: One-to-Many relationship. One student has many mark entries (multiple subjects × multiple assessment types). Foreign key: `marks.student_id` references `students.student_id`.

### Q5: How is attendance percentage calculated?
**A**: 
```sql
(COUNT of Present / COUNT of Total) × 100
= (SUM(CASE WHEN status='P' THEN 1 ELSE 0 END) / COUNT(*)) × 100
```

### Q6: What triggers are used?
**A**: One trigger: `update_thread_timestamp` - automatically updates `last_message_at` in `feedback_threads` when a new message is inserted.

### Q7: How does clear chat work?
**A**: User-specific soft delete. When a user clears chat, a timestamp is set (`cleared_by_student` or `cleared_by_faculty`). Messages created before this timestamp are hidden for that user only. The other user still sees all messages.

### Q8: What is the purpose of sequences?
**A**: Sequences generate unique auto-incrementing IDs for primary keys. Example: `users_seq.NEXTVAL` generates the next user_id.

### Q9: How are alerts generated?
**A**: Alerts are generated by checking attendance percentage. If a student's attendance in any subject falls below 75%, an alert is automatically created with type 'Warning' or 'Critical'.

### Q10: Explain the feedback system architecture.
**A**: Thread-based system. Each student-faculty-subject combination has one thread (`feedback_threads`). Multiple messages (`feedback_messages`) belong to each thread. Supports file attachments, read/unread tracking, and user-specific clear chat.

---

## Conclusion

This documentation provides a complete overview of the database structure, relationships, and implementation. All tables are clearly defined, relationships are documented, and setup instructions are provided.

**For any questions or issues, refer to**:
- `README.md` - Project overview
- `PROJECT_STRUCTURE.md` - File organization
- `DATABASE_CREDENTIALS_REFERENCE.md` - Credential management
- `WORKING_LINKS.md` - URL references

**Database files location**:
- Schema: `backend/database/schema.sql`
- Feedback Schema: `backend/database/schema_feedback_threads.sql`
- Setup Script: `backend/setup_complete_system.py`
- Migration: `backend/add_clear_chat_columns.py`

---

**Document Version**: 1.0  
**Last Updated**: April 2026  
**Author**: System Documentation  
**Status**: Complete and Ready for Viva
