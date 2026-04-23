# Alerts System - Complete Documentation

## Table of Contents
1. Alert System Overview
2. Attendance Alert Logic
3. Trigger Details
4. Code Location and File Paths
5. How Alerts Work - Step-by-Step Flow
6. Database Table Structure
7. Alert Types and Thresholds
8. Alert Generation Methods
9. Alert Display and Management
10. Viva Quick Reference

---

## 1. Alert System Overview

### What the Alert System Does
The alert system automatically monitors student attendance and generates notifications when attendance falls below acceptable thresholds. It provides early warnings to students about their attendance status, allowing them to take corrective action before facing academic consequences.

### Purpose in the Project
- Automated monitoring of student attendance
- Early warning system for low attendance
- Helps students maintain minimum attendance requirements
- Reduces manual monitoring effort for faculty
- Provides real-time notifications to students

### Who Receives Alerts
- Students: Receive alerts about their own attendance
- Faculty: Can view student alerts (if implemented)
- System: Stores all alerts in database for tracking

### Alert Visibility
- Students see alerts on their dashboard
- Alerts are categorized by severity (Warning, Alert, Critical)
- Unread alerts are highlighted
- Alerts can be marked as read

---

## 2. Attendance Alert Logic

### Alert Thresholds

The system uses THREE attendance percentage thresholds:

Threshold 1: Below 75% (Warning)
- Alert Type: Warning
- Condition: Attendance percentage >= 65% AND < 75%
- Message: "Low attendance in [Subject]: [Percentage]%"
- Action: Student should improve attendance
- Severity: Low

Threshold 2: Below 65% (Alert)
- Alert Type: Alert
- Condition: Attendance percentage >= 50% AND < 65%
- Message: "Your attendance in [Subject] is [Percentage]% (below 65%). Immediate action required."
- Action: Immediate attention needed
- Severity: Medium

Threshold 3: Below 50% (Critical)
- Alert Type: Critical
- Condition: Attendance percentage < 50%
- Message: "Your attendance in [Subject] is [Percentage]% (below 50%). Critical situation."
- Action: Urgent action required
- Severity: High

### Calculation Formula

Attendance Percentage = (Total Present / Total Classes) × 100

Example:
- Total Classes: 100
- Present: 70
- Absent: 30
- Percentage: (70 / 100) × 100 = 70%
- Result: Warning alert generated (below 75%)

---

## 3. Trigger Details

### Database Triggers

IMPORTANT: The current system does NOT use database triggers for alert generation.

Trigger Name: None (No automatic database trigger)
Table: N/A
Event: N/A
Reason: Alerts are generated programmatically, not via database triggers

### Why No Trigger?

The system uses programmatic alert generation instead of database triggers because:
1. Complex calculation logic (attendance percentage across multiple records)
2. Need to aggregate data from multiple attendance records
3. Flexibility to add additional conditions
4. Easier to test and maintain
5. Can include email notifications and other actions

### Existing Trigger (Not for Alerts)

The only trigger in the system is:

Trigger Name: update_thread_timestamp
Purpose: Update last message timestamp in feedback threads
Table: feedback_messages
Event: AFTER INSERT
File: backend/database/schema_feedback_threads.sql (Lines 54-61)

This trigger is NOT related to the alert system.

---

## 4. Code Location and File Paths

### Alert Generation Code

File 1: backend/setup_complete_system.py
Location: Lines 365-400
Purpose: Initial alert generation during database setup
Description: Generates alerts for all students with attendance below 75%

File 2: backend/utils/alert_checker.py
Location: Complete file (Lines 1-70)
Purpose: Periodic alert checking and generation
Description: Can be run periodically to check attendance and generate new alerts

### Alert Display Code

File 3: backend/app.py
Location: Lines 274-312
Purpose: API endpoint to retrieve student alerts
Endpoint: GET /api/student/alerts
Description: Returns all alerts for logged-in student

File 4: backend/app.py
Location: Lines 314-340
Purpose: API endpoint to mark alert as read
Endpoint: POST /api/student/alerts/mark_read/:alert_id
Description: Marks specific alert as read

### Alert Database Schema

File 5: backend/database/complete_schema.sql
Location: Lines 112-121
Purpose: Alerts table definition
Description: Defines structure of alerts table

File 6: backend/setup_complete_system.py
Location: Lines 136-145
Purpose: Creates alerts table during setup
Description: SQL CREATE TABLE statement for alerts

### Frontend Alert Display

File 7: frontend/student_portal.html
Location: Lines 200-250 (approximately)
Purpose: Display alerts in student dashboard
Description: Shows alerts with color coding based on type

---

## 5. How Alerts Work - Step-by-Step Flow

### Method 1: Initial Setup (During Database Initialization)

Step 1: Database Setup
- File: backend/setup_complete_system.py
- Action: Creates alerts table
- Code: Lines 136-145

Step 2: Attendance Data Generation
- File: backend/setup_complete_system.py
- Action: Generates attendance records for all students
- Code: Lines 300-330
- Data: ~225,000 attendance records (300 students × 5 subjects × 150 days)

Step 3: Attendance Percentage Calculation
- File: backend/setup_complete_system.py
- Action: Calculates attendance percentage for each student-subject combination
- Code: Lines 365-375
- SQL Query:
```sql
SELECT s.student_id, a.subject_id, sub.subject_name,
       COUNT(*) as total,
       SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
FROM students s
JOIN attendance a ON s.student_id = a.student_id
JOIN subjects sub ON a.subject_id = sub.subject_id
GROUP BY s.student_id, a.subject_id, sub.subject_name
HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
```

Step 4: Condition Evaluation
- File: backend/setup_complete_system.py
- Action: Checks if percentage is below 75%
- Code: Line 375
- Logic: HAVING clause filters students with attendance < 75%

Step 5: Alert Type Determination
- File: backend/setup_complete_system.py
- Action: Determines alert type based on percentage
- Code: Line 380
- Logic:
```python
alert_type = 'Critical' if percentage < 50 else 'Warning'
```

Step 6: Alert Generation
- File: backend/setup_complete_system.py
- Action: Inserts alert into database
- Code: Lines 390-398
- SQL:
```sql
INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message, is_read, created_at)
VALUES (alerts_seq.NEXTVAL, :student_id, :subject_id, :alert_type, :message, 0, :created_at)
```

Step 7: Alert Storage
- Table: alerts
- Status: is_read = 0 (unread)
- Timestamp: created_at = current date/time

### Method 2: Periodic Alert Checking (Runtime)

Step 1: Trigger Alert Check
- File: backend/utils/alert_checker.py
- Action: Run alert checker script
- Command: python backend/utils/alert_checker.py
- Frequency: Can be scheduled (cron job, task scheduler)

Step 2: Fetch Student Attendance Data
- File: backend/utils/alert_checker.py
- Action: Query all students and their attendance
- Code: Lines 18-28

Step 3: Calculate Attendance Percentage
- File: backend/utils/alert_checker.py
- Action: Calculate percentage for each student-subject
- Code: Lines 30-35
- Formula: (present / total) × 100

Step 4: Evaluate Thresholds
- File: backend/utils/alert_checker.py
- Action: Check against three thresholds
- Code: Lines 40-50
- Thresholds: 75%, 65%, 50%

Step 5: Check for Duplicate Alerts
- File: backend/utils/alert_checker.py
- Action: Prevent duplicate alerts within 15 days
- Code: Lines 52-57
- Logic: Only create alert if no similar alert in last 15 days

Step 6: Generate New Alert
- File: backend/utils/alert_checker.py
- Action: Insert alert into database
- Code: Lines 59-62

Step 7: Send Email Notification (Optional)
- File: backend/utils/alert_checker.py
- Action: Send email to student
- Code: Line 64
- Note: Email service is placeholder (not fully implemented)

### Method 3: Student Views Alerts

Step 1: Student Logs In
- File: frontend/student_portal.html
- Action: Student authenticates
- Result: JWT token stored

Step 2: Dashboard Loads
- File: frontend/student_portal.html
- Action: Fetch alerts from API
- Endpoint: GET /api/student/alerts

Step 3: API Retrieves Alerts
- File: backend/app.py
- Action: Query alerts for student
- Code: Lines 274-312
- SQL:
```sql
SELECT alert_id, alert_type, message, is_read, created_at
FROM alerts
WHERE student_id = :student_id
ORDER BY created_at DESC
```

Step 4: Alerts Displayed
- File: frontend/student_portal.html
- Action: Show alerts with color coding
- Display: Type, message, timestamp, read status

Step 5: Student Marks Alert as Read
- File: frontend/student_portal.html
- Action: Click on alert
- Endpoint: POST /api/student/alerts/mark_read/:alert_id

Step 6: Alert Status Updated
- File: backend/app.py
- Action: Update is_read to 1
- Code: Lines 314-340
- SQL:
```sql
UPDATE alerts SET is_read = 1 WHERE alert_id = :alert_id
```

---

## 6. Database Table Structure

### Alerts Table

Table Name: alerts
Created In: backend/setup_complete_system.py (Lines 136-145)
Schema File: backend/database/complete_schema.sql (Lines 112-121)

Column Structure:

Column 1: alert_id
- Type: NUMBER
- Constraint: PRIMARY KEY
- Description: Unique identifier for each alert
- Generated By: alerts_seq sequence
- Example: 1, 2, 3, ...

Column 2: student_id
- Type: NUMBER
- Constraint: NOT NULL, FOREIGN KEY
- Description: References student who receives the alert
- Foreign Key: students(student_id)
- Example: 1 (refers to student with student_id = 1)

Column 3: subject_id
- Type: NUMBER
- Constraint: FOREIGN KEY (nullable)
- Description: Subject related to the alert
- Foreign Key: subjects(subject_id)
- Example: 1 (refers to Data Structures)
- Note: Can be NULL for general alerts

Column 4: alert_type
- Type: VARCHAR2(20)
- Constraint: NOT NULL
- Description: Severity level of alert
- Possible Values: 'Warning', 'Alert', 'Critical'
- Example: 'Warning'

Column 5: message
- Type: VARCHAR2(500)
- Constraint: NOT NULL
- Description: Alert message text
- Example: "Low attendance in Data Structures: 72.5%"
- Format: "Low attendance in [Subject]: [Percentage]%"

Column 6: is_read
- Type: NUMBER(1)
- Constraint: DEFAULT 0
- Description: Read status of alert
- Values: 0 = unread, 1 = read
- Example: 0 (unread)

Column 7: created_at
- Type: TIMESTAMP
- Constraint: DEFAULT CURRENT_TIMESTAMP
- Description: When alert was created
- Example: 2026-04-05 10:30:00
- Format: YYYY-MM-DD HH:MM:SS

### Sample Data

Sample Alert 1:
```
alert_id: 1
student_id: 15
subject_id: 1
alert_type: Warning
message: Low attendance in Data Structures: 72.5%
is_read: 0
created_at: 2026-04-05 10:30:00
```

Sample Alert 2:
```
alert_id: 2
student_id: 15
subject_id: 2
alert_type: Critical
message: Low attendance in Algorithms: 45.0%
is_read: 0
created_at: 2026-04-04 14:20:00
```

Sample Alert 3:
```
alert_id: 3
student_id: 28
subject_id: 3
alert_type: Alert
message: Your attendance in Database Management is 62.0% (below 65%). Immediate action required.
is_read: 1
created_at: 2026-04-03 09:15:00
```

### Sequence

Sequence Name: alerts_seq
Start Value: 1
Increment: 1
Purpose: Generate unique alert_id values
Created In: backend/setup_complete_system.py

---

## 7. Alert Types and Thresholds

### Alert Type 1: Warning

Attendance Range: 65% to 74.99%
Alert Type: Warning
Color Code: Yellow/Orange (in UI)
Severity: Low
Message Format: "Low attendance in [Subject]: [Percentage]%"
Action Required: Student should improve attendance
Example: "Low attendance in Data Structures: 72.5%"

Trigger Condition:
```python
if 65 <= percentage < 75:
    alert_type = 'Warning'
```

### Alert Type 2: Alert

Attendance Range: 50% to 64.99%
Alert Type: Alert
Color Code: Orange/Red (in UI)
Severity: Medium
Message Format: "Your attendance in [Subject] is [Percentage]% (below 65%). Immediate action required."
Action Required: Immediate attention needed
Example: "Your attendance in Algorithms is 62.0% (below 65%). Immediate action required."

Trigger Condition:
```python
if 50 <= percentage < 65:
    alert_type = 'Alert'
```

### Alert Type 3: Critical

Attendance Range: Below 50%
Alert Type: Critical
Color Code: Red (in UI)
Severity: High
Message Format: "Your attendance in [Subject] is [Percentage]% (below 50%). Critical situation."
Action Required: Urgent action required
Example: "Your attendance in Operating Systems is 45.0% (below 50%). Critical situation."

Trigger Condition:
```python
if percentage < 50:
    alert_type = 'Critical'
```

### Threshold Summary Table

| Attendance % | Alert Type | Severity | Color | Action |
|--------------|------------|----------|-------|--------|
| >= 75% | None | N/A | Green | No action needed |
| 65% - 74.99% | Warning | Low | Yellow | Improve attendance |
| 50% - 64.99% | Alert | Medium | Orange | Immediate action |
| < 50% | Critical | High | Red | Urgent action |

---

## 8. Alert Generation Methods

### Method 1: Initial Setup Generation

When: During database initialization
File: backend/setup_complete_system.py
Lines: 365-400
Trigger: Manual execution of setup script
Command: python backend/setup_complete_system.py

Process:
1. Attendance data is generated for all students
2. System calculates attendance percentage for each student-subject
3. SQL query filters students with attendance < 75%
4. Alerts are generated for all matching records
5. Alerts are inserted into database with random timestamps (last 30 days)

Advantages:
- Generates historical alerts
- Populates database with sample data
- One-time execution

Disadvantages:
- Only runs during setup
- Not automatic
- Requires manual execution

### Method 2: Periodic Alert Checker

When: Scheduled execution (cron job, task scheduler)
File: backend/utils/alert_checker.py
Lines: 1-70
Trigger: Scheduled task or manual execution
Command: python backend/utils/alert_checker.py

Process:
1. Script connects to database
2. Fetches all students and their attendance data
3. Calculates attendance percentage for each student-subject
4. Evaluates against three thresholds (75%, 65%, 50%)
5. Checks for duplicate alerts (within last 15 days)
6. Generates new alerts if needed
7. Optionally sends email notifications

Advantages:
- Can run periodically
- Prevents duplicate alerts
- Includes email notifications
- More sophisticated logic (three thresholds)

Disadvantages:
- Requires scheduling
- Not real-time
- Email service not fully implemented

### Method 3: Real-Time Generation (Not Implemented)

When: After attendance is marked
File: Would be in backend/app.py (not currently implemented)
Trigger: AFTER INSERT or UPDATE on attendance table
Implementation: Database trigger or application logic

Process (if implemented):
1. Attendance is marked for a student
2. System immediately calculates updated percentage
3. Checks if percentage crosses threshold
4. Generates alert if needed
5. Student sees alert immediately

Status: NOT CURRENTLY IMPLEMENTED

To implement:
- Add logic to attendance marking endpoint
- Calculate percentage after each attendance update
- Generate alert if threshold crossed
- Or create database trigger

---

## 9. Alert Display and Management

### Student Dashboard Display

Location: frontend/student_portal.html
Section: Alerts View
Access: Click "Alerts" card on dashboard

Display Features:
- List of all alerts (newest first)
- Color coding by alert type
- Unread alerts highlighted
- Alert message and timestamp
- Subject name
- Mark as read functionality

Alert Card Structure:
```html
<div class="alert-card [alert-type]">
    <div class="alert-header">
        <span class="alert-type">[Warning/Alert/Critical]</span>
        <span class="alert-date">[Date and Time]</span>
    </div>
    <div class="alert-message">[Message Text]</div>
    <div class="alert-subject">[Subject Name]</div>
</div>
```

Color Coding:
- Warning: Yellow/Orange background
- Alert: Orange background
- Critical: Red background
- Unread: Bold text, darker background
- Read: Normal text, lighter background

### API Endpoints

Endpoint 1: Get Student Alerts
- URL: GET /api/student/alerts
- File: backend/app.py (Lines 274-312)
- Authentication: Required (JWT token)
- Response: JSON array of alerts
- Sorting: Newest first (ORDER BY created_at DESC)

Response Format:
```json
[
    {
        "alert_id": 1,
        "type": "Warning",
        "message": "Low attendance in Data Structures: 72.5%",
        "is_read": 0,
        "created_at": "05 Apr 2026 — 10:30 AM"
    }
]
```

Endpoint 2: Mark Alert as Read
- URL: POST /api/student/alerts/mark_read/:alert_id
- File: backend/app.py (Lines 314-340)
- Authentication: Required (JWT token)
- Action: Updates is_read to 1
- Response: Success message

### Alert Notification Badge

Location: Student dashboard
Display: Number of unread alerts
Update: Real-time when alerts are fetched
Position: On "Alerts" card

Logic:
```javascript
const unreadCount = alerts.filter(a => a.is_read === 0).length;
```

---

## 10. Viva Quick Reference

### Quick Facts

Total Alert Types: 3 (Warning, Alert, Critical)
Thresholds: 75%, 65%, 50%
Database Table: alerts
Sequence: alerts_seq
Triggers: None (programmatic generation)

### Alert Generation

Primary File: backend/setup_complete_system.py (Lines 365-400)
Secondary File: backend/utils/alert_checker.py (Complete file)
Method: SQL query with HAVING clause
Condition: Attendance percentage < 75%

### Alert Display

API Endpoint: GET /api/student/alerts
File: backend/app.py (Lines 274-312)
Frontend: frontend/student_portal.html
Sorting: Newest first

### Thresholds Explained

Below 75%: Warning alert
Below 65%: Alert (medium severity)
Below 50%: Critical alert

### Calculation Formula

Attendance % = (Present / Total) × 100

Example:
- Present: 70 classes
- Total: 100 classes
- Percentage: 70%
- Result: Warning alert (below 75%)

### Key SQL Query

```sql
SELECT s.student_id, a.subject_id, sub.subject_name,
       COUNT(*) as total,
       SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
FROM students s
JOIN attendance a ON s.student_id = a.student_id
JOIN subjects sub ON a.subject_id = sub.subject_id
GROUP BY s.student_id, a.subject_id, sub.subject_name
HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
```

### Important Notes

1. No database trigger for alerts (programmatic generation)
2. Alerts are generated during setup and can be regenerated periodically
3. Students see only their own alerts
4. Alerts can be marked as read
5. Duplicate alerts prevented (15-day window in alert_checker.py)
6. Email notifications are placeholder (not fully implemented)

### File Locations Summary

Alert Generation:
- backend/setup_complete_system.py (Lines 365-400)
- backend/utils/alert_checker.py (Complete file)

Alert Display:
- backend/app.py (Lines 274-340)
- frontend/student_portal.html (Alerts section)

Database Schema:
- backend/database/complete_schema.sql (Lines 112-121)
- backend/setup_complete_system.py (Lines 136-145)

### Common Viva Questions

Q: How are alerts generated?
A: Programmatically by calculating attendance percentage and comparing against thresholds (75%, 65%, 50%)

Q: Is there a database trigger?
A: No, alerts are generated by Python scripts, not database triggers

Q: What are the alert thresholds?
A: Three thresholds: 75% (Warning), 65% (Alert), 50% (Critical)

Q: Where is the alert generation code?
A: backend/setup_complete_system.py (Lines 365-400) and backend/utils/alert_checker.py

Q: How do students see alerts?
A: Through API endpoint GET /api/student/alerts displayed on student dashboard

Q: Can alerts be marked as read?
A: Yes, using POST /api/student/alerts/mark_read/:alert_id endpoint

---

Document Version: 1.0
Last Updated: April 2026
Status: Complete and Viva-Ready
