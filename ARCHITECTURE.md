# System Architecture - Student-Faculty Portal v2.0

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  Student Portal  │              │  Faculty Portal  │        │
│  │  - Dashboard     │              │  - Dashboard     │        │
│  │  - Marks         │              │  - My Classes    │        │
│  │  - Attendance    │              │  - Add Marks     │        │
│  │  - Feedback Chat │              │  - Attendance    │        │
│  │  - Alerts        │              │  - Feedback Chat │        │
│  └──────────────────┘              └──────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API (JSON)
                              │ JWT Authentication
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND LAYER                           │
│                      Flask Application                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                         │  │
│  │  • Authentication (Login/Logout)                         │  │
│  │  • Student APIs (9 endpoints)                            │  │
│  │  • Faculty APIs (14 endpoints)                           │  │
│  │  • Feedback APIs (Real-time messaging)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Business Logic                          │  │
│  │  • JWT Token Management                                  │  │
│  │  • Role-based Access Control                             │  │
│  │  • Data Validation                                       │  │
│  │  • Relationship Enforcement                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Oracle DB Driver (oracledb)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                            │
│                      Oracle Database                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Core Tables:                                            │  │
│  │  • users (students + faculty)                            │  │
│  │  • students (with class_name)                            │  │
│  │  • faculty                                               │  │
│  │  • subjects                                              │  │
│  │  • faculty_classes (many-to-many mapping)                │  │
│  │  • student_subjects                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Feature Tables:                                         │  │
│  │  • marks (class-based)                                   │  │
│  │  • attendance (with date range)                          │  │
│  │  • feedback (threaded messaging)                         │  │
│  │  • alerts (auto-generated)                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### 1. Student Feedback Flow

```
┌─────────────┐
│   Student   │
│  (2Q11)     │
└──────┬──────┘
       │ 1. Select Subject (DBMS)
       ▼
┌─────────────────────────────────────┐
│  Find Faculty for:                  │
│  - Student's Class (2Q11)           │
│  - Selected Subject (DBMS)          │
└──────┬──────────────────────────────┘
       │ 2. Query: faculty_classes
       │    WHERE class_name='2Q11'
       │    AND subject_id=1
       ▼
┌─────────────────────────────────────┐
│  Faculty Found:                     │
│  Dr. Rajesh Kumar (faculty_id=1)    │
└──────┬──────────────────────────────┘
       │ 3. Create/Retrieve Thread
       │    (student_id, faculty_id, subject_id)
       ▼
┌─────────────────────────────────────┐
│  Display Conversation History       │
│  ORDER BY created_at ASC            │
└──────┬──────────────────────────────┘
       │ 4. Student sends message
       ▼
┌─────────────────────────────────────┐
│  INSERT INTO feedback               │
│  - sender_id = student's user_id    │
│  - sender_role = 'student'          │
│  - message = "I have a doubt..."    │
└──────┬──────────────────────────────┘
       │ 5. Message appears instantly
       ▼
┌─────────────────────────────────────┐
│  Faculty sees message in their      │
│  feedback interface                 │
└─────────────────────────────────────┘
```

### 2. Faculty Marks Entry Flow

```
┌─────────────┐
│   Faculty   │
│ Dr. Rajesh  │
└──────┬──────┘
       │ 1. Select Class (2Q11)
       ▼
┌─────────────────────────────────────┐
│  Verify Faculty teaches this class  │
│  Query: faculty_classes             │
│  WHERE faculty_id=1                 │
│  AND class_name='2Q11'              │
└──────┬──────────────────────────────┘
       │ 2. Get Subjects for this class
       ▼
┌─────────────────────────────────────┐
│  Show Subjects:                     │
│  - DBMS (subject_id=1)              │
└──────┬──────────────────────────────┘
       │ 3. Select Subject
       ▼
┌─────────────────────────────────────┐
│  Get Students in 2Q11               │
│  Query: students                    │
│  WHERE class_name='2Q11'            │
└──────┬──────────────────────────────┘
       │ 4. Select Student
       ▼
┌─────────────────────────────────────┐
│  Enter Marks:                       │
│  - Assessment Type: MST             │
│  - Marks Obtained: 38               │
│  - Max Marks: 50                    │
└──────┬──────────────────────────────┘
       │ 5. Save Marks
       ▼
┌─────────────────────────────────────┐
│  INSERT/UPDATE marks                │
│  - student_id                       │
│  - subject_id                       │
│  - class_name='2Q11'                │
│  - assessment_type='MST'            │
└─────────────────────────────────────┘
```

### 3. Attendance Alert Generation Flow

```
┌─────────────────────────────────────┐
│  Daily Attendance Marked            │
│  (Faculty marks P/A for students)   │
└──────┬──────────────────────────────┘
       │ Periodic Check (e.g., daily)
       ▼
┌─────────────────────────────────────┐
│  Calculate Attendance %             │
│  For each student per subject:      │
│  percentage = (present/total) * 100 │
└──────┬──────────────────────────────┘
       │ Check threshold
       ▼
┌─────────────────────────────────────┐
│  Is percentage < 75%?               │
└──────┬──────────────────────────────┘
       │ YES
       ▼
┌─────────────────────────────────────┐
│  Determine Alert Type:              │
│  - < 60%: Critical                  │
│  - 60-70%: Alert                    │
│  - 70-75%: Warning                  │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  INSERT INTO alerts                 │
│  - student_id                       │
│  - subject_id                       │
│  - alert_type                       │
│  - message                          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Student sees alert in dashboard    │
└─────────────────────────────────────┘
```

## Entity Relationship Diagram

```
┌──────────────┐
│    users     │
│──────────────│
│ user_id (PK) │◄─────────┐
│ email        │          │
│ password     │          │
│ name         │          │
│ role         │          │
└──────────────┘          │
       │                  │
       │                  │
       ├──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   students   │   │   faculty    │   │   feedback   │
│──────────────│   │──────────────│   │──────────────│
│ student_id   │   │ faculty_id   │   │ feedback_id  │
│ user_id (FK) │   │ user_id (FK) │   │ sender_id(FK)│
│ class_name   │   │ department   │   │ student_id   │
│ branch       │   │ designation  │   │ faculty_id   │
│ cgpa         │   └──────┬───────┘   │ subject_id   │
└──────┬───────┘          │           │ message      │
       │                  │           │ sender_role  │
       │                  │           └──────────────┘
       │                  │
       │                  ▼
       │           ┌──────────────────┐
       │           │ faculty_classes  │
       │           │──────────────────│
       │           │ faculty_class_id │
       │           │ faculty_id (FK)  │
       │           │ class_name       │
       │           │ subject_id (FK)  │
       │           └──────┬───────────┘
       │                  │
       ▼                  ▼
┌──────────────────┐  ┌──────────────┐
│ student_subjects │  │   subjects   │
│──────────────────│  │──────────────│
│ student_id (FK)  │  │ subject_id   │
│ subject_id (FK)  │──┤ subject_name │
└──────────────────┘  │ subject_code │
                      └──────┬───────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│    marks     │      │  attendance  │     │    alerts    │
│──────────────│      │──────────────│     │──────────────│
│ mark_id      │      │ attendance_id│     │ alert_id     │
│ student_id   │      │ student_id   │     │ student_id   │
│ subject_id   │      │ subject_id   │     │ subject_id   │
│ class_name   │      │ class_name   │     │ alert_type   │
│ assessment   │      │ date         │     │ message      │
│ marks        │      │ status       │     └──────────────┘
└──────────────┘      └──────────────┘
```

## Class Structure

### 5 Classes with 30 Students Each

```
┌─────────────────────────────────────────────────────────────┐
│                        2Q11 (30 students)                   │
│  Faculty: Dr. Rajesh (DBMS), Prof. Meena (OS),             │
│           Prof. Vikram (Networks), Dr. Anjali (SE),         │
│           Dr. Anil (DS)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        2Q12 (30 students)                   │
│  Faculty: Dr. Rajesh (DBMS), Dr. Priya (OS),               │
│           Dr. Suresh (Networks), Dr. Anjali (SE),           │
│           Dr. Anil (DS)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        2Q13 (30 students)                   │
│  Faculty: Dr. Rajesh (DBMS), Dr. Priya (OS),               │
│           Dr. Suresh (Networks), Dr. Anjali (SE),           │
│           Dr. Anil (DS)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        2Q14 (30 students)                   │
│  Faculty: Prof. Deepak (DBMS), Prof. Meena (OS),           │
│           Prof. Vikram (Networks), Prof. Kavita (SE),       │
│           Dr. Anil (DS)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        2Q15 (30 students)                   │
│  Faculty: Prof. Deepak (DBMS), Dr. Priya (OS),             │
│           Dr. Suresh (Networks), Prof. Kavita (SE),         │
│           Dr. Anil (DS)                                     │
└─────────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Request                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  JWT Token Validation                       │
│  • Check if token exists                                    │
│  • Verify token signature                                   │
│  • Check expiration (24 hours)                              │
│  • Extract user_id and role                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Role-Based Access Control                  │
│  • Student endpoints: require role='student'                │
│  • Faculty endpoints: require role='faculty'                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Relationship Validation                        │
│  • Faculty: verify teaches this class/subject               │
│  • Student: verify enrolled in this subject                 │
│  • Feedback: verify student-faculty-subject relationship    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Execute Request                            │
│  • Query database                                           │
│  • Return filtered data                                     │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Production Environment                   │
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │  Web Server      │         │  Application     │        │
│  │  (Nginx/Apache)  │────────▶│  Server (Flask)  │        │
│  │  Port 80/443     │         │  Port 5000       │        │
│  └──────────────────┘         └────────┬─────────┘        │
│                                         │                   │
│                                         ▼                   │
│                              ┌──────────────────┐          │
│                              │  Oracle Database │          │
│                              │  Port 1521       │          │
│                              └──────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  • HTML5, CSS3, JavaScript                                  │
│  • AJAX for API calls                                       │
│  • Chart.js for graphs (recommended)                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         Backend                             │
│  • Python 3.8+                                              │
│  • Flask (Web Framework)                                    │
│  • Flask-CORS (Cross-Origin Resource Sharing)              │
│  • PyJWT (JWT Authentication)                               │
│  • oracledb (Oracle Database Driver)                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         Database                            │
│  • Oracle Database 11g+                                     │
│  • SQL for schema and queries                               │
└─────────────────────────────────────────────────────────────┘
```

## Performance Considerations

### Database Indexes
```sql
-- Feedback thread retrieval
CREATE INDEX idx_feedback_thread 
ON feedback(student_id, faculty_id, subject_id, created_at);

-- Attendance queries
CREATE INDEX idx_attendance_student 
ON attendance(student_id, subject_id, attendance_date);
```

### Caching Strategy
- Cache faculty-class assignments (rarely changes)
- Cache subject list (static data)
- Don't cache: marks, attendance, feedback (frequently updated)

### Real-Time Updates
- Frontend polls feedback endpoint every 3-5 seconds
- Use timestamp of last message to fetch only new messages
- Consider WebSocket for production (Socket.IO)

---

This architecture supports:
- ✅ 150+ concurrent users
- ✅ Real-time messaging
- ✅ Scalable class structure
- ✅ Secure data access
- ✅ Easy maintenance and updates
