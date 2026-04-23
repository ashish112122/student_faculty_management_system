# Database Entity Relationship Diagram

## Visual Representation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STUDENT-FACULTY MANAGEMENT SYSTEM                    │
│                              DATABASE STRUCTURE                              │
└─────────────────────────────────────────────────────────────────────────────┘


                              ┌──────────────┐
                              │    USERS     │
                              ├──────────────┤
                              │ user_id (PK) │
                              │ email        │
                              │ password     │
                              │ name         │
                              │ role         │
                              └──────┬───────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
         ┌──────────────────┐              ┌──────────────────┐
         │    STUDENTS      │              │     FACULTY      │
         ├──────────────────┤              ├──────────────────┤
         │ student_id (PK)  │              │ faculty_id (PK)  │
         │ user_id (FK)     │              │ user_id (FK)     │
         │ name             │              │ name             │
         │ branch           │              │ department       │
         │ semester         │              └────────┬─────────┘
         │ class_name       │                       │
         │ cgpa             │                       │
         └────────┬─────────┘                       │
                  │                                 │
                  │                                 ▼
                  │                    ┌──────────────────────┐
                  │                    │  FACULTY_CLASSES     │
                  │                    ├──────────────────────┤
                  │                    │ faculty_class_id(PK) │
                  │                    │ faculty_id (FK)      │
                  │                    │ subject_id (FK)      │
                  │                    │ class_name           │
                  │                    └──────────┬───────────┘
                  │                               │
                  │              ┌────────────────┴────────────────┐
                  │              │                                 │
                  │              ▼                                 │
                  │    ┌──────────────────┐                       │
                  │    │    SUBJECTS      │                       │
                  │    ├──────────────────┤                       │
                  │    │ subject_id (PK)  │                       │
                  │    │ subject_name     │                       │
                  │    │ subject_code     │                       │
                  │    └────────┬─────────┘                       │
                  │             │                                 │
         ┌────────┴─────────────┴──────────────┬─────────────────┘
         │                                     │
         │                                     │
         ▼                                     ▼
┌──────────────────┐                 ┌──────────────────┐
│      MARKS       │                 │   ATTENDANCE     │
├──────────────────┤                 ├──────────────────┤
│ mark_id (PK)     │                 │ attendance_id(PK)│
│ student_id (FK)  │                 │ student_id (FK)  │
│ subject_id (FK)  │                 │ subject_id (FK)  │
│ class_name       │                 │ class_name       │
│ assessment_type  │                 │ attendance_date  │
│ marks_obtained   │                 │ status (P/A)     │
│ max_marks        │                 └──────────────────┘
└──────────────────┘                          │
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │     ALERTS       │
                                     ├──────────────────┤
                                     │ alert_id (PK)    │
                                     │ student_id (FK)  │
                                     │ subject_id (FK)  │
                                     │ alert_type       │
                                     │ message          │
                                     │ is_read          │
                                     │ created_at       │
                                     └──────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          FEEDBACK/CHAT SYSTEM                                │
└─────────────────────────────────────────────────────────────────────────────┘

         ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
         │   STUDENTS   │         │   FACULTY    │         │   SUBJECTS   │
         └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
                │                        │                        │
                └────────────┬───────────┴────────────┬───────────┘
                             │                        │
                             ▼                        │
                  ┌──────────────────────┐            │
                  │  FEEDBACK_THREADS    │            │
                  ├──────────────────────┤            │
                  │ thread_id (PK)       │            │
                  │ student_id (FK)      │            │
                  │ faculty_id (FK)      │◄───────────┘
                  │ subject_id (FK)      │
                  │ thread_title         │
                  │ initiated_by         │
                  │ created_at           │
                  │ last_message_at      │
                  │ cleared_by_student   │ ◄─── User-specific clear chat
                  │ cleared_by_faculty   │ ◄─── User-specific clear chat
                  └──────────┬───────────┘
                             │
                             │ One-to-Many
                             │
                             ▼
                  ┌──────────────────────┐
                  │  FEEDBACK_MESSAGES   │
                  ├──────────────────────┤
                  │ message_id (PK)      │
                  │ thread_id (FK)       │
                  │ sender_id (FK)       │───────┐
                  │ sender_role          │       │
                  │ message (CLOB)       │       │
                  │ is_read              │       │
                  │ created_at           │       │
                  │ attachment_path      │       │
                  │ attachment_name      │       │
                  │ attachment_type      │       │
                  └──────────────────────┘       │
                                                 │
                                                 ▼
                                        ┌──────────────┐
                                        │    USERS     │
                                        │ (sender)     │
                                        └──────────────┘
```

## Table Relationships Summary

### Primary Relationships

1. **users → students** (1:1)
   - One user account per student
   - FK: students.user_id → users.user_id

2. **users → faculty** (1:1)
   - One user account per faculty
   - FK: faculty.user_id → users.user_id

3. **students → marks** (1:N)
   - One student has many mark entries
   - FK: marks.student_id → students.student_id

4. **subjects → marks** (1:N)
   - One subject has many mark entries
   - FK: marks.subject_id → subjects.subject_id

5. **students → attendance** (1:N)
   - One student has many attendance records
   - FK: attendance.student_id → students.student_id

6. **subjects → attendance** (1:N)
   - One subject has many attendance records
   - FK: attendance.subject_id → subjects.subject_id

7. **students → alerts** (1:N)
   - One student has many alerts
   - FK: alerts.student_id → students.student_id

8. **subjects → alerts** (1:N, optional)
   - One subject can have many alerts
   - FK: alerts.subject_id → subjects.subject_id (nullable)

9. **faculty → faculty_classes** (1:N)
   - One faculty teaches many classes
   - FK: faculty_classes.faculty_id → faculty.faculty_id

10. **subjects → faculty_classes** (1:N)
    - One subject taught in many classes
    - FK: faculty_classes.subject_id → subjects.subject_id

### Feedback System Relationships

11. **students → feedback_threads** (1:N)
    - One student has many threads
    - FK: feedback_threads.student_id → students.student_id

12. **faculty → feedback_threads** (1:N)
    - One faculty has many threads
    - FK: feedback_threads.faculty_id → faculty.faculty_id

13. **subjects → feedback_threads** (1:N)
    - One subject has many threads
    - FK: feedback_threads.subject_id → subjects.subject_id

14. **feedback_threads → feedback_messages** (1:N)
    - One thread has many messages
    - FK: feedback_messages.thread_id → feedback_threads.thread_id
    - CASCADE DELETE: Deleting thread deletes all messages

15. **users → feedback_messages** (1:N)
    - One user sends many messages
    - FK: feedback_messages.sender_id → users.user_id

## Cardinality Notation

- **1:1** = One-to-One
- **1:N** = One-to-Many
- **N:M** = Many-to-Many (not used in this schema)

## Constraints

### Primary Keys (PK)
- Unique identifier for each record
- Cannot be NULL
- Auto-generated using sequences

### Foreign Keys (FK)
- References primary key in another table
- Enforces referential integrity
- Some allow NULL (optional relationships)

### Check Constraints
- `users.role`: Must be 'student' or 'faculty'
- `marks.assessment_type`: Must be 'MST', 'EST', 'Quiz', or 'Assignment'
- `attendance.status`: Must be 'P' (Present) or 'A' (Absent)
- `feedback_threads.initiated_by`: Must be 'student' or 'faculty'
- `feedback_messages.sender_role`: Must be 'student' or 'faculty'

### Unique Constraints
- `users.email`: Each email must be unique
- `subjects.subject_code`: Each subject code must be unique
- `students.user_id`: Each student linked to one user
- `faculty.user_id`: Each faculty linked to one user

## Cascade Operations

### ON DELETE CASCADE
- `feedback_messages.thread_id → feedback_threads.thread_id`
  - When a thread is deleted, all its messages are automatically deleted

### No Cascade (Default)
- All other foreign keys prevent deletion if referenced
- Example: Cannot delete a student if they have marks records

## Indexes

Performance optimization indexes:

1. `idx_feedback_threads_student` on feedback_threads(student_id)
2. `idx_feedback_threads_faculty` on feedback_threads(faculty_id)
3. `idx_feedback_threads_subject` on feedback_threads(subject_id)
4. `idx_feedback_messages_thread` on feedback_messages(thread_id)
5. `idx_feedback_messages_sender` on feedback_messages(sender_id)

## Triggers

1. **update_thread_timestamp**
   - Type: AFTER INSERT on feedback_messages
   - Action: Updates last_message_at in feedback_threads
   - Purpose: Keep thread metadata current

## Data Flow Examples

### Student Login Flow
```
1. User enters email/password
2. Query: SELECT * FROM users WHERE email = ?
3. Verify password
4. If role = 'student':
   Query: SELECT * FROM students WHERE user_id = ?
5. Return student data
```

### Marks Display Flow
```
1. Student logged in (student_id known)
2. Query: 
   SELECT m.*, s.subject_name, s.subject_code
   FROM marks m
   JOIN subjects s ON m.subject_id = s.subject_id
   WHERE m.student_id = ?
3. Display marks grouped by subject
```

### Attendance Alert Flow
```
1. Calculate attendance percentage:
   SELECT student_id, subject_id,
          (SUM(CASE WHEN status='P' THEN 1 ELSE 0 END) / COUNT(*)) * 100
   FROM attendance
   GROUP BY student_id, subject_id
   HAVING percentage < 75

2. For each low attendance:
   INSERT INTO alerts (student_id, subject_id, alert_type, message)
   VALUES (?, ?, 'Warning', 'Low attendance: X%')
```

### Chat Message Flow
```
1. Student sends message to faculty
2. Find or create thread:
   SELECT thread_id FROM feedback_threads
   WHERE student_id = ? AND faculty_id = ? AND subject_id = ?

3. Insert message:
   INSERT INTO feedback_messages (thread_id, sender_id, sender_role, message)
   VALUES (?, ?, 'student', ?)

4. Trigger automatically updates:
   UPDATE feedback_threads SET last_message_at = CURRENT_TIMESTAMP
   WHERE thread_id = ?
```

---

**Legend:**
- (PK) = Primary Key
- (FK) = Foreign Key
- ─── = Relationship line
- ▼   = Direction of relationship
- │   = Connection
