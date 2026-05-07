# Student-Faculty Management System

A web-based management system for educational institutions to manage students, faculty, marks, attendance, alerts, and communication.

---

## Features

- Student and Faculty login with JWT authentication
- Student dashboard: marks, attendance, alerts, feedback/chat
- Faculty dashboard: class management, marks entry, attendance marking, feedback
- Automated attendance alerts via database trigger
- Feedback/chat system between students and faculty with file attachments
- User-specific clear chat (each user clears only their own view)

---

## Technology Stack

- Backend: Python + Flask
- Database: Oracle Database 21c (via `oracledb` driver)
- Frontend: HTML, CSS, Vanilla JavaScript

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or above installed
- Oracle Database 21c running locally or remotely
- Oracle Instant Client installed (required by `oracledb`)
- A browser (Chrome/Firefox recommended)

---

## How to Run the Project

### Step 1 — Clone or Download the Project

```bash
git clone <your-repo-url>
cd student_faculty_management_system
```

---

### Step 2 — Create and Activate Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

- Windows:
```bash
venv\Scripts\activate
```
- Mac/Linux:
```bash
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### Step 4 — Configure Database Credentials

Open `backend/config.py` and fill in your Oracle database details:

```python
class Config:
    DB_USER     = 'your_oracle_username'
    DB_PASSWORD = 'your_oracle_password'
    DB_DSN      = 'localhost:1521/xe'   # or your host:port/service_name
    SECRET_KEY  = 'any-random-secret-key'
```

---

### Step 5 — Initialize the Database

This will create all tables, sequences, triggers, indexes, and insert sample data (300 students, 5 faculty, marks, attendance, alerts):

```bash
python backend/setup_complete_system.py
```

If that gives any error, try the corrected version:

```bash
python backend/setup_complete_system_corrected.py
```

---

### Step 6 — Start the Backend Server

```bash
python backend/app.py
```

You should see:
```
Running on http://localhost:5000
```

Keep this terminal running.

---

### Step 7 — Open the Frontend

Open a new terminal or file explorer and open these HTML files directly in your browser:

| Page | File |
|------|------|
| Login | `frontend/login_test.html` |
| Student Dashboard | `frontend/student_portal.html` |
| Faculty Dashboard | `frontend/faculty_portal.html` |

> Tip: Right-click the HTML file → Open With → Your Browser
> Or use VS Code Live Server extension for best experience.

---

## Login Credentials

### Student
| Email | Password |
|-------|----------|
| rohan.sharma.2q34.3@thapar.edu | pass123 |

### Faculty
| Email | Password | Subject |
|-------|----------|---------|
| dr.rajesh@thaparfac.edu | pass123 | Data Structures |


---

## Project Structure

```
student_faculty_management_system/
│
├── backend/
│   ├── app.py                          # All API endpoints (Flask)
│   ├── config.py                       # Database credentials
│   ├── requirements.txt                # Python dependencies
│   ├── setup_complete_system.py        # DB setup script
│   │
│   ├── database/
│   │   ├── complete_schema.sql         # All table definitions + triggers + indexes
│   │   ├── triggers.sql                # Database triggers
│   │   ├── insert_data.sql             # Sample data
│   │   ├── student_faculty_names.sql   # 300 students + 5 faculty data
│   │   └── tables_reference.md        # Quick table reference
│   │
│   └── utils/
│       ├── alert_checker.py            # Alert utility
│       └── email_service.py            # Email utility
│
├── frontend/
│   ├── login_test.html                 # Login page
│   ├── student_portal.html             # Student dashboard
│   ├── faculty_portal.html             # Faculty dashboard
│   │
│   ├── templates/                      # Individual page templates
│   ├── css/                            # Stylesheets
│   ├── js/                             # JavaScript files
│   └── assets/                         # Images (university logo etc.)
│
├── venv/                               # Virtual environment (do not commit)
├── .gitignore
└── README.md
```

---

## Database Overview

| Item | Count |
|------|-------|
| Tables | 10 |
| Sequences | 10 |
| Indexes | 5 |
| Triggers | 2 |

### Triggers
- `update_thread_timestamp` — fires after a new message is inserted, updates thread's last activity time
- `trg_attendance_alert` — fires after attendance is marked, auto-generates Warning/Alert/Critical alerts if attendance drops below 75%

---

## Common Issues

**Oracle connection error:**
- Make sure Oracle DB is running
- Check `config.py` credentials
- Ensure Oracle Instant Client is installed and in PATH

**Frontend not connecting to backend:**
- Make sure `python backend/app.py` is running
- Check that backend is on `http://localhost:5000`
- Open browser console (F12) to see any CORS or network errors

**Tables already exist error during setup:**
- Run `backend/cleanup_database.py` first to drop existing tables, then re-run setup
