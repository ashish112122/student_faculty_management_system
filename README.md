# Student-Faculty Management System

A web-based management system for educational institutions to manage students,
faculty, marks, attendance, alerts, and communication.

---

## Features

- Student and Faculty login with JWT authentication
- Student dashboard: marks, attendance, alerts, feedback
- Faculty dashboard: class management, marks entry, attendance marking, feedback
- Automated attendance alerts via database trigger (SQL-based)
- Feedback/chat system between students and faculty with file attachments
- User-specific clear chat (each user clears only their own view)

---

## Technology Stack

- Backend: Python, Flask
- Database: Oracle Database 21c
- Frontend: HTML, CSS, JavaScript

---

## How to Run

### Step 1: Configure Database

Edit `backend/config.py` and set your Oracle credentials:

```python
class Config:
    DB_USER     = 'your_username'
    DB_PASSWORD = 'your_password'
    DB_DSN      = 'host:port/service_name'
    SECRET_KEY  = 'your-secret-key'
```

### Step 2: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 3: Initialize Database

```bash
python backend/setup_complete_system.py
```

This creates all tables, sequences, triggers, and populates sample data
(300 students, 5 faculty, marks, attendance, alerts).

### Step 4: Run Backend Server

```bash
python backend/app.py
```

Server starts at: http://localhost:5000

### Step 5: Open Frontend

Open any of these in your browser:

- Login page: http://localhost:5000/login_test.html
- Student portal: http://localhost:5000/student_portal.html
- Faculty portal: http://localhost:5000/faculty_portal.html

---

## Login Credentials

### Student Login

| Email | Password |
|-------|----------|
| rohan.sharma.2q34.3@thapar.edu | pass123 |

### Faculty Login

| Email | Password | Subject |
|-------|----------|---------|
| dr.rajesh@thaparfac.edu | pass123 | Data Structures |

---

## Database

- 11 tables, 10 sequences, 5 indexes, 2 triggers
- Attendance alerts are generated automatically by the SQL trigger
  `trg_attendance_alert` (AFTER INSERT OR UPDATE ON attendance)
- Schema: `backend/database/complete_schema.sql`
- Triggers: `backend/database/triggers.sql`
- Alert rules: `backend/database/attendance_alert_rules.md`

---

## Project Structure

```
backend/
  app.py                    API endpoints
  config.py                 Database credentials
  setup_complete_system.py  Database initialization
  database/
    complete_schema.sql     All table definitions
    triggers.sql            Database triggers
    insert_data.sql         Sample data
    attendance_alert_rules.md  Alert threshold rules

frontend/
  student_portal.html       Student dashboard
  faculty_portal.html       Faculty dashboard
  login_test.html           Login page
```
