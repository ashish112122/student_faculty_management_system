# Database Quick Reference Guide

## Quick Facts

- **Database**: Oracle Database 21c
- **Total Tables**: 11
- **Total Sequences**: 10
- **Total Indexes**: 5
- **Total Triggers**: 1
- **Python Library**: oracledb
- **Configuration**: backend/config.py

---

## All Tables at a Glance

| # | Table Name | Purpose | Records |
|---|------------|---------|---------|
| 1 | users | Authentication | 305 |
| 2 | students | Student info | 300 |
| 3 | faculty | Faculty info | 5 |
| 4 | subjects | Courses | 5 |
| 5 | faculty_classes | Teaching assignments | 15 |
| 6 | marks | Student marks | ~6,000 |
| 7 | attendance | Daily attendance | ~225,000 |
| 8 | alerts | Notifications | Varies |
| 9 | feedback_threads | Chat metadata | On-demand |
| 10 | feedback_messages | Chat messages | On-demand |

---

## Table Structures (Quick View)

### 1. USERS
```
user_id (PK), email (UNIQUE), password, name, role
```

### 2. STUDENTS
```
student_id (PK), user_id (FK), name, branch, semester, class_name, cgpa
```

### 3. FACULTY
```
faculty_id (PK), user_id (FK), name, department
```

### 4. SUBJECTS
```
subject_id (PK), subject_name, subject_code (UNIQUE)
```

### 5. FACULTY_CLASSES
```
faculty_class_id (PK), faculty_id (FK), subject_id (FK), class_name
```

### 6. MARKS
```
mark_id (PK), student_id (FK), subject_id (FK), class_name,
assessment_type, marks_obtained, max_marks
```

### 7. ATTENDANCE
```
attendance_id (PK), student_id (FK), subject_id (FK), class_name,
attendance_date, status
```

### 8. ALERTS
```
alert_id (PK), student_id (FK), subject_id (FK), alert_type,
message, is_read, created_at
```

### 9. FEEDBACK_THREADS
```
thread_id (PK), student_id (FK), faculty_id (FK), subject_id (FK),
thread_title, initiated_by, created_at, last_message_at,
cleared_by_student, cleared_by_faculty
```

### 10. FEEDBACK_MESSAGES
```
message_id (PK), thread_id (FK), sender_id (FK), sender_role,
message (CLOB), is_read, created_at,
attachment_path, attachment_name, attachment_type
```

---

## Common Queries

### Get Student Details
```sql
SELECT s.*, u.email 
FROM students s 
JOIN users u ON s.user_id = u.user_id 
WHERE s.student_id = :student_id;
```

### Get Student Marks
```sql
SELECT m.*, sub.subject_name, sub.subject_code
FROM marks m
JOIN subjects sub ON m.subject_id = sub.subject_id
WHERE m.student_id = :student_id
ORDER BY sub.subject_name, m.assessment_type;
```

### Calculate Attendance Percentage
```sql
SELECT 
    subject_id,
    (SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as percentage
FROM attendance
WHERE student_id = :student_id
GROUP BY subject_id;
```

### Get Unread Alerts
```sql
SELECT * FROM alerts
WHERE student_id = :student_id AND is_read = 0
ORDER BY created_at DESC;
```

### Get Faculty Classes
```sql
SELECT fc.*, s.subject_name, s.subject_code
FROM faculty_classes fc
JOIN subjects s ON fc.subject_id = s.subject_id
WHERE fc.faculty_id = :faculty_id;
```

### Get Chat Messages
```sql
SELECT * FROM feedback_messages
WHERE thread_id = :thread_id
  AND created_at > :cleared_timestamp
ORDER BY created_at ASC;
```

---

## File Locations

### Database Schema Files
```
backend/database/
├── schema.sql                    # Main schema (legacy)
├── schema_feedback_threads.sql   # Feedback system schema
└── complete_schema.sql           # All tables in one file
```

### Setup Scripts
```
backend/
├── setup_complete_system.py      # Initialize database
├── add_clear_chat_columns.py     # Migration for clear chat
└── cleanup_database.py           # Cleanup utility
```

### Configuration
```
backend/config.py                 # Database credentials
```

### Documentation
```
DATABASE_COMPLETE_DOCUMENTATION.md  # Full documentation
DATABASE_DIAGRAM.md                 # Visual diagrams
DATABASE_QUICK_REFERENCE.md         # This file
```

---

## Setup Commands

### Initialize Database
```bash
python backend/setup_complete_system.py
```

### Add Clear Chat Feature
```bash
python backend/add_clear_chat_columns.py
```

### Start Backend
```bash
python backend/app.py
```

### Install Dependencies
```bash
pip install -r backend/requirements.txt
```

---

## Sample Credentials

### Faculty
```
Email: dr.rajesh@thaparfac.edu
Password: pass123
```

### Student
```
Email: rohan.sharma.2q31.0@thapar.edu
Password: pass123
```

---

## Assessment Types

| Type | Max Marks |
|------|-----------|
| MST | 30 |
| EST | 40 |
| Quiz | 15 |
| Assignment | 15 |
| **Total** | **100** |

---

## Batches

10 batches total: 2Q31, 2Q32, 2Q33, 2Q34, 2Q35, 2Q36, 2Q37, 2Q38, 2Q39, 2Q40

Each batch has 30 students.

---

## Subjects

| ID | Name | Code |
|----|------|------|
| 1 | Data Structures | CS401 |
| 2 | Algorithms | CS402 |
| 3 | Database Management | CS403 |
| 4 | Operating Systems | CS404 |
| 5 | Computer Networks | CS405 |

---

## Alert Types

| Type | Condition |
|------|-----------|
| Warning | Attendance 65-75% |
| Alert | Attendance 50-65% |
| Critical | Attendance < 50% |

---

## Attendance Status

- **P** = Present
- **A** = Absent

---

## User Roles

- **student** = Student account
- **faculty** = Faculty account

---

## Foreign Key Relationships

```
users ─┬─> students
       └─> faculty

students ─┬─> marks
          ├─> attendance
          ├─> alerts
          └─> feedback_threads

faculty ─┬─> faculty_classes
         └─> feedback_threads

subjects ─┬─> marks
          ├─> attendance
          ├─> alerts
          ├─> faculty_classes
          └─> feedback_threads

feedback_threads ─> feedback_messages (CASCADE DELETE)

users ─> feedback_messages (as sender)
```

---

## Sequences

All sequences start at 1 and increment by 1:

1. users_seq
2. students_seq
3. faculty_seq
4. subjects_seq
5. faculty_classes_seq
6. marks_seq
7. attendance_seq
8. alerts_seq
9. feedback_threads_seq
10. feedback_messages_seq

---

## Indexes

1. idx_feedback_threads_student
2. idx_feedback_threads_faculty
3. idx_feedback_threads_subject
4. idx_feedback_messages_thread
5. idx_feedback_messages_sender

---

## Triggers

1. **update_thread_timestamp**
   - Fires: AFTER INSERT on feedback_messages
   - Action: Updates last_message_at in feedback_threads

---

## API Endpoints (Quick Reference)

### Authentication
- POST `/api/login` - User login

### Student APIs
- GET `/api/student/dashboard` - Dashboard data
- GET `/api/student/marks` - All marks
- GET `/api/student/attendance` - Attendance records
- GET `/api/student/alerts` - All alerts
- GET `/api/student/feedback/subjects` - Subjects list
- GET `/api/student/feedback/<faculty_id>/<subject_id>` - Messages
- POST `/api/student/feedback/send` - Send message
- DELETE `/api/student/feedback/clear/<faculty_id>/<subject_id>` - Clear chat

### Faculty APIs
- GET `/api/faculty/dashboard` - Dashboard data
- GET `/api/faculty/students` - Students list
- POST `/api/faculty/marks/add` - Add marks
- GET `/api/faculty/feedback/<student_id>/<subject_id>` - Messages
- POST `/api/faculty/feedback/send` - Send message
- DELETE `/api/faculty/feedback/clear/<student_id>/<subject_id>` - Clear chat

---

## Troubleshooting

### Cannot connect to database
- Check config.py credentials
- Verify Oracle Database is running
- Check firewall settings

### Tables already exist
- Run cleanup script first
- Or manually drop tables

### Module not found
```bash
pip install oracledb Flask Flask-CORS PyJWT
```

### Oracle Client not found
- Install Oracle Instant Client
- Add to PATH environment variable

---

## Viva Quick Answers

**Q: How many tables?**  
A: 11 tables

**Q: Which database?**  
A: Oracle Database 21c

**Q: Where are tables created?**  
A: backend/setup_complete_system.py

**Q: How many students?**  
A: 300 students (30 per batch × 10 batches)

**Q: How many faculty?**  
A: 5 faculty members

**Q: How is attendance calculated?**  
A: (Present count / Total count) × 100

**Q: What triggers are used?**  
A: 1 trigger - update_thread_timestamp

**Q: How does clear chat work?**  
A: User-specific soft delete using timestamps

**Q: What is the relationship between students and marks?**  
A: One-to-Many (one student has many marks)

**Q: How are alerts generated?**  
A: Automatically when attendance < 75%

---

**For detailed information, see**: DATABASE_COMPLETE_DOCUMENTATION.md
