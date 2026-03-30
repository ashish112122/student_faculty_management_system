# Entity-Relationship Diagram
## Student-Faculty Management System

## ER Diagram (Text Representation)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STUDENT-FACULTY MANAGEMENT SYSTEM                         │
│                         Entity-Relationship Diagram                          │
└─────────────────────────────────────────────────────────────────────────────┘


┌──────────────────┐
│      USERS       │
├──────────────────┤
│ PK: user_id      │
│     email        │◄────────────────────────────────────┐
│     password     │                                     │
│     name         │                                     │
│     role         │                                     │
└────────┬─────────┘                                     │
         │                                               │
         │ 1                                             │
         │                                               │
    ┌────┴────┐                                          │
    │         │                                          │
    │ 1       │ 1                                        │
    │         │                                          │
┌───▼─────────────┐                  ┌──────────────────▼───┐
│    STUDENTS     │                  │      FACULTY         │
├─────────────────┤                  ├──────────────────────┤
│ PK: student_id  │                  │ PK: faculty_id       │
│ FK: user_id     │                  │ FK: user_id          │
│     name        │                  │     name             │
│     branch      │                  │     department       │
│     year_of_    │                  │     designation      │
│     study       │                  └──────────┬───────────┘
│     semester    │                             │
│     section     │                             │ 1
│     cgpa        │                             │
│     total_      │                             │
│     credits     │                             │
└────────┬────────┘                             │
         │                                      │
         │ M                                    │
         │                                      │
         │                                      │
┌────────▼────────────────────────────────┐    │
│     STUDENT_SUBJECTS (Junction)         │    │
├─────────────────────────────────────────┤    │
│ PK: (student_id, subject_id)            │    │
│ FK: student_id ──────────────────┐      │    │
│ FK: subject_id                   │      │    │
└──────────────────────┬───────────┘      │    │
                       │                  │    │
                       │ M                │    │
                       │                  │    │
                ┌──────▼──────────────────▼────▼──┐
                │         SUBJECTS                 │
                ├──────────────────────────────────┤
                │ PK: subject_id                   │
                │ FK: faculty_id ──────────────────┤ (Teaches)
                │     subject_name                 │
                │     subject_code                 │
                │     credits                      │
                └──────────┬───────────────────────┘
                           │
                           │ 1
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            │ M            │ M            │ M
            │              │              │
    ┌───────▼──────┐  ┌───▼──────────┐  ┌▼──────────────┐
    │    MARKS     │  │  ATTENDANCE  │  │   FEEDBACK    │
    ├──────────────┤  ├──────────────┤  ├───────────────┤
    │ PK: mark_id  │  │ PK: attend_  │  │ PK: feedback_ │
    │ FK: student_ │  │     ance_id  │  │     id        │
    │     id       │  │ FK: student_ │  │ FK: student_  │
    │ FK: subject_ │  │     id       │  │     id        │
    │     id       │  │ FK: subject_ │  │ FK: subject_  │
    │     assess_  │  │     id       │  │     id        │
    │     ment_    │  │     attend_  │  │ FK: sender_id │
    │     type     │  │     ance_date│  │     message   │
    │     marks_   │  │     status   │  │     created_  │
    │     obtained │  │              │  │     at        │
    │     max_marks│  └──────────────┘  └───────────────┘
    │     grade    │           │
    └──────────────┘           │
                               │ (Triggers)
                               │
                               │ M
                               │
                        ┌──────▼──────┐
                        │   ALERTS    │
                        ├─────────────┤
                        │ PK: alert_  │
                        │     id      │
                        │ FK: student_│
                        │     id      │
                        │     alert_  │
                        │     type    │
                        │     message │
                        │     created_│
                        │     at      │
                        └─────────────┘


LEGEND:
───────
PK = Primary Key
FK = Foreign Key
1  = One (Cardinality)
M  = Many (Cardinality)
─► = Relationship Direction
```

---

## Detailed Entity Descriptions

### 1. USERS (Central Authentication Entity)
**Purpose:** Stores login credentials for all system users

**Attributes:**
- `user_id` (PK) - Unique identifier
- `email` - Login email (UNIQUE, validated domain)
- `password` - User password
- `name` - Full name
- `role` - User role ('student' or 'faculty')

**Relationships:**
- 1:1 with STUDENTS (one user can be one student)
- 1:1 with FACULTY (one user can be one faculty)

**Business Rules:**
- Email must end with @thapar.edu (students) or @thaparfac.edu (faculty)
- Role must match email domain
- Email is unique across system

---

### 2. STUDENTS
**Purpose:** Stores student profile information

**Attributes:**
- `student_id` (PK) - Unique student identifier
- `user_id` (FK) - References USERS table
- `name` - Student name
- `branch` - Academic branch (e.g., CSE)
- `year_of_study` - Current year (1-4)
- `semester` - Current semester (1-8)
- `section` - Class section (e.g., 2Q31)
- `cgpa` - Cumulative GPA (0.00-10.00)
- `total_credits` - Total credits earned

**Relationships:**
- M:M with SUBJECTS (via STUDENT_SUBJECTS)
- 1:M with MARKS (one student has many marks)
- 1:M with ATTENDANCE (one student has many attendance records)
- 1:M with ALERTS (one student has many alerts)
- 1:M with FEEDBACK (one student sends many feedback messages)

**Business Rules:**
- Each student must be enrolled in at least one subject
- CGPA must be between 0.00 and 10.00
- Semester must match year_of_study

---

### 3. FACULTY
**Purpose:** Stores faculty profile information

**Attributes:**
- `faculty_id` (PK) - Unique faculty identifier
- `user_id` (FK) - References USERS table
- `name` - Faculty name
- `department` - Department name
- `designation` - Position (Professor, Associate Professor, etc.)

**Relationships:**
- 1:M with SUBJECTS (one faculty teaches many subjects)

**Business Rules:**
- Each faculty must be assigned to at least one subject
- Faculty can only access data for their assigned subjects

---

### 4. SUBJECTS
**Purpose:** Stores course/subject information

**Attributes:**
- `subject_id` (PK) - Unique subject identifier
- `subject_name` - Full subject name
- `subject_code` - Short code (e.g., DBMS, OS)
- `faculty_id` (FK) - References FACULTY table (who teaches this)
- `credits` - Credit hours for this subject

**Relationships:**
- M:1 with FACULTY (many subjects taught by one faculty)
- M:M with STUDENTS (via STUDENT_SUBJECTS)
- 1:M with MARKS (one subject has many marks records)
- 1:M with ATTENDANCE (one subject has many attendance records)
- 1:M with FEEDBACK (one subject has many feedback messages)

**Business Rules:**
- Each subject must be assigned to exactly one faculty
- Subject code must be unique
- Credits typically 3-4

---

### 5. STUDENT_SUBJECTS (Junction Table)
**Purpose:** Maps students to their enrolled subjects

**Attributes:**
- `student_id` (PK, FK) - References STUDENTS
- `subject_id` (PK, FK) - References SUBJECTS
- Composite Primary Key: (student_id, subject_id)

**Relationships:**
- M:1 with STUDENTS
- M:1 with SUBJECTS

**Business Rules:**
- A student can enroll in multiple subjects
- A subject can have multiple students
- No duplicate enrollments

---

### 6. MARKS
**Purpose:** Stores student marks/grades

**Attributes:**
- `mark_id` (PK) - Unique marks record identifier
- `student_id` (FK) - References STUDENTS
- `subject_id` (FK) - References SUBJECTS
- `assessment_type` - Type of assessment (MST, EST, Assignment, Quiz)
- `marks_obtained` - Marks scored
- `max_marks` - Maximum possible marks
- `grade` - Letter grade (A, B, C, D, F)

**Relationships:**
- M:1 with STUDENTS (many marks for one student)
- M:1 with SUBJECTS (many marks for one subject)

**Business Rules:**
- marks_obtained must be ≤ max_marks
- Grade calculated automatically based on percentage
- Only assigned faculty can add/modify marks
- Assessment types: MST, EST, Assignment, Quiz

**Grade Calculation:**
- A: ≥90%
- B: ≥75%
- C: ≥60%
- D: ≥45%
- F: <45%

---

### 7. ATTENDANCE
**Purpose:** Tracks student attendance

**Attributes:**
- `attendance_id` (PK) - Unique attendance record identifier
- `student_id` (FK) - References STUDENTS
- `subject_id` (FK) - References SUBJECTS
- `attendance_date` - Date of class
- `status` - Present ('P') or Absent ('A')

**Relationships:**
- M:1 with STUDENTS (many attendance records for one student)
- M:1 with SUBJECTS (many attendance records for one subject)
- Triggers ALERTS (when percentage < 75%)

**Business Rules:**
- Only assigned faculty can mark attendance
- One record per student per subject per date
- Status must be 'P' or 'A'
- Automatically triggers alert generation

**Alert Triggers:**
- <50%: Critical alert
- <65%: Alert
- <75%: Warning

---

### 8. ALERTS
**Purpose:** Stores system-generated alerts for students

**Attributes:**
- `alert_id` (PK) - Unique alert identifier
- `student_id` (FK) - References STUDENTS
- `alert_type` - Type of alert (Warning, Alert, Critical)
- `message` - Alert message text
- `created_at` - Timestamp of alert creation

**Relationships:**
- M:1 with STUDENTS (many alerts for one student)
- Triggered by ATTENDANCE records

**Business Rules:**
- Auto-generated when attendance < 75%
- Alert types based on attendance percentage
- Cannot be manually created
- Read-only for students

**Alert Types:**
- Warning: 65% ≤ attendance < 75%
- Alert: 50% ≤ attendance < 65%
- Critical: attendance < 50%

---

### 9. FEEDBACK
**Purpose:** Enables communication between students and faculty

**Attributes:**
- `feedback_id` (PK) - Unique feedback identifier
- `student_id` (FK) - References STUDENTS (which student)
- `subject_id` (FK) - References SUBJECTS (which subject)
- `sender_id` (FK) - References USERS (who sent the message)
- `message` - Message text
- `created_at` - Timestamp of message

**Relationships:**
- M:1 with STUDENTS (many messages from one student)
- M:1 with SUBJECTS (many messages about one subject)
- M:1 with USERS (many messages from one user)

**Business Rules:**
- Students can send feedback for their enrolled subjects
- Faculty can view feedback for their assigned subjects
- Faculty determined via subject's faculty_id
- Bidirectional communication (student ↔ faculty)
- Messages stored in chronological order

---

## Relationship Details

### 1. USERS → STUDENTS (1:1)
- **Type:** One-to-One
- **Description:** Each user account can be linked to one student profile
- **Constraint:** user_id is UNIQUE in STUDENTS table
- **Business Rule:** Only users with role='student' can have student profile

### 2. USERS → FACULTY (1:1)
- **Type:** One-to-One
- **Description:** Each user account can be linked to one faculty profile
- **Constraint:** user_id is UNIQUE in FACULTY table
- **Business Rule:** Only users with role='faculty' can have faculty profile

### 3. FACULTY → SUBJECTS (1:M)
- **Type:** One-to-Many
- **Description:** One faculty member teaches multiple subjects
- **Constraint:** faculty_id in SUBJECTS references FACULTY
- **Business Rule:** Each subject must have exactly one assigned faculty

### 4. STUDENTS ↔ SUBJECTS (M:M via STUDENT_SUBJECTS)
- **Type:** Many-to-Many
- **Description:** Students enroll in multiple subjects, subjects have multiple students
- **Junction Table:** STUDENT_SUBJECTS
- **Business Rule:** A student must be enrolled in at least one subject

### 5. STUDENTS → MARKS (1:M)
- **Type:** One-to-Many
- **Description:** One student has multiple marks records
- **Constraint:** student_id in MARKS references STUDENTS
- **Business Rule:** Marks can only be added by assigned faculty

### 6. SUBJECTS → MARKS (1:M)
- **Type:** One-to-Many
- **Description:** One subject has multiple marks records
- **Constraint:** subject_id in MARKS references SUBJECTS
- **Business Rule:** Marks must be for enrolled students only

### 7. STUDENTS → ATTENDANCE (1:M)
- **Type:** One-to-Many
- **Description:** One student has multiple attendance records
- **Constraint:** student_id in ATTENDANCE references STUDENTS
- **Business Rule:** Attendance can only be marked by assigned faculty

### 8. SUBJECTS → ATTENDANCE (1:M)
- **Type:** One-to-Many
- **Description:** One subject has multiple attendance records
- **Constraint:** subject_id in ATTENDANCE references SUBJECTS
- **Business Rule:** One record per student per subject per date

### 9. STUDENTS → ALERTS (1:M)
- **Type:** One-to-Many
- **Description:** One student has multiple alerts
- **Constraint:** student_id in ALERTS references STUDENTS
- **Business Rule:** Alerts auto-generated, not manually created

### 10. ATTENDANCE → ALERTS (Trigger)
- **Type:** Trigger Relationship
- **Description:** Attendance records trigger alert generation
- **Logic:** When attendance < 75%, system creates alert
- **Business Rule:** Automatic, cannot be disabled

### 11. STUDENTS → FEEDBACK (1:M)
- **Type:** One-to-Many
- **Description:** One student sends multiple feedback messages
- **Constraint:** student_id in FEEDBACK references STUDENTS
- **Business Rule:** Students can only send feedback for enrolled subjects

### 12. SUBJECTS → FEEDBACK (1:M)
- **Type:** One-to-Many
- **Description:** One subject has multiple feedback messages
- **Constraint:** subject_id in FEEDBACK references SUBJECTS
- **Business Rule:** Faculty sees feedback for their assigned subjects only

### 13. USERS → FEEDBACK (1:M)
- **Type:** One-to-Many
- **Description:** One user (student or faculty) sends multiple messages
- **Constraint:** sender_id in FEEDBACK references USERS
- **Business Rule:** Identifies who sent each message in conversation

---

## Cardinality Summary

```
USERS (1) ──────────── (1) STUDENTS
USERS (1) ──────────── (1) FACULTY
FACULTY (1) ──────────── (M) SUBJECTS
STUDENTS (M) ──────────── (M) SUBJECTS [via STUDENT_SUBJECTS]
STUDENTS (1) ──────────── (M) MARKS
SUBJECTS (1) ──────────── (M) MARKS
STUDENTS (1) ──────────── (M) ATTENDANCE
SUBJECTS (1) ──────────── (M) ATTENDANCE
STUDENTS (1) ──────────── (M) ALERTS
ATTENDANCE (M) ─[triggers]─► (M) ALERTS
STUDENTS (1) ──────────── (M) FEEDBACK
SUBJECTS (1) ──────────── (M) FEEDBACK
USERS (1) ──────────── (M) FEEDBACK
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA FLOW                               │
└─────────────────────────────────────────────────────────────┘

1. MARKS FLOW:
   Faculty → MARKS table → Student views
   
   Faculty (adds marks)
      ↓
   MARKS (stores with grade calculation)
      ↓
   Student (views marks for enrolled subjects)


2. ATTENDANCE FLOW:
   Faculty → ATTENDANCE table → Alert generation → Student views
   
   Faculty (marks attendance)
      ↓
   ATTENDANCE (stores P/A status)
      ↓
   System (calculates percentage)
      ↓
   ALERTS (auto-generated if < 75%)
      ↓
   Student (views attendance & alerts)


3. FEEDBACK FLOW:
   Student ↔ FEEDBACK table ↔ Faculty
   
   Student (sends message for subject)
      ↓
   FEEDBACK (stores with subject_id)
      ↓
   System (routes to faculty via subject.faculty_id)
      ↓
   Faculty (views and replies)
      ↓
   FEEDBACK (stores reply)
      ↓
   Student (views conversation)


4. ENROLLMENT FLOW:
   Student → STUDENT_SUBJECTS → SUBJECTS → Faculty
   
   Student (enrolled in subjects)
      ↓
   STUDENT_SUBJECTS (junction table)
      ↓
   SUBJECTS (with assigned faculty_id)
      ↓
   Faculty (can access enrolled students)
```

---

## Constraints & Integrity Rules

### Primary Key Constraints
- All tables have primary keys
- Primary keys are auto-generated using sequences
- Primary keys are immutable

### Foreign Key Constraints
- All foreign keys reference existing records
- Cascade rules prevent orphaned records
- Referential integrity maintained

### Unique Constraints
- users.email (UNIQUE)
- subjects.subject_code (UNIQUE)
- students.user_id (UNIQUE)
- faculty.user_id (UNIQUE)

### Check Constraints
- users.role IN ('student', 'faculty')
- marks.assessment_type IN ('MST', 'EST', 'Assignment', 'Quiz')
- attendance.status IN ('P', 'A')
- alerts.alert_type IN ('Warning', 'Alert', 'Critical')
- students.cgpa BETWEEN 0.00 AND 10.00

### Business Logic Constraints
- Email domain validation (application level)
- Grade calculation (application level)
- Alert generation (application level)
- Authorization checks (application level)

---

## Database Statistics (Demo Data)

```
Table Name          | Records | Purpose
--------------------|---------|----------------------------------
USERS               | 10      | 5 students + 5 faculty
STUDENTS            | 5       | Student profiles
FACULTY             | 5       | Faculty profiles
SUBJECTS            | 5       | Course offerings
STUDENT_SUBJECTS    | 25      | 5 students × 5 subjects each
MARKS               | 0       | Initially empty (faculty adds)
ATTENDANCE          | 0       | Initially empty (faculty marks)
ALERTS              | 0       | Auto-generated based on attendance
FEEDBACK            | 0       | Created by students/faculty
--------------------|---------|----------------------------------
TOTAL               | 45      | Initial records
```

---

## ER Diagram Notes

### Design Principles
1. **Normalization:** Database is in 3NF (Third Normal Form)
2. **No Redundancy:** No duplicate data across tables
3. **Referential Integrity:** All foreign keys properly defined
4. **Scalability:** Design supports growth in users and data
5. **Security:** Role-based access control at application level

### Key Design Decisions
1. **Separate USERS table:** Centralizes authentication
2. **Junction table:** STUDENT_SUBJECTS for M:M relationship
3. **faculty_id in SUBJECTS:** Enables subject-faculty mapping
4. **sender_id in FEEDBACK:** Tracks message sender (student or faculty)
5. **Auto-generated ALERTS:** Triggered by attendance percentage

### Future Enhancements (Not Implemented)
1. **DEPARTMENTS table:** For faculty department management
2. **COURSES table:** Separate from subjects for course catalog
3. **SEMESTERS table:** For academic term management
4. **GRADES_HISTORY table:** For historical grade tracking
5. **NOTIFICATIONS table:** For system-wide announcements

---

## SQL Schema Summary

```sql
-- Core Tables
CREATE TABLE users (user_id, email, password, name, role);
CREATE TABLE students (student_id, user_id, name, branch, ...);
CREATE TABLE faculty (faculty_id, user_id, name, department, ...);
CREATE TABLE subjects (subject_id, subject_name, faculty_id, ...);

-- Junction Table
CREATE TABLE student_subjects (student_id, subject_id);

-- Transaction Tables
CREATE TABLE marks (mark_id, student_id, subject_id, ...);
CREATE TABLE attendance (attendance_id, student_id, subject_id, ...);
CREATE TABLE alerts (alert_id, student_id, alert_type, ...);
CREATE TABLE feedback (feedback_id, student_id, subject_id, ...);

-- Sequences (for auto-increment)
CREATE SEQUENCE users_seq;
CREATE SEQUENCE students_seq;
CREATE SEQUENCE faculty_seq;
CREATE SEQUENCE subjects_seq;
CREATE SEQUENCE marks_seq;
CREATE SEQUENCE attendance_seq;
CREATE SEQUENCE alerts_seq;
CREATE SEQUENCE feedback_seq;
```

---

## Conclusion

This ER diagram represents a complete, normalized database design for the Student-Faculty Management System with:

- ✅ 9 tables with proper relationships
- ✅ Clear cardinality (1:1, 1:M, M:M)
- ✅ Referential integrity
- ✅ Business rule enforcement
- ✅ Scalable architecture
- ✅ Support for all system features

The design supports all three members' modules:
- **Member 1 (VANSHIKA):** Login, Students, Feedback
- **Member 2 (ASHISH/RAHUL):** Faculty, Marks
- **Member 3 (GURLEEN):** Attendance, Alerts

**Status:** Production-ready database design ✅
