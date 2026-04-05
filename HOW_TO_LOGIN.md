# HOW TO ACCESS THE SYSTEM

## Quick Start

### Step 1: Make Sure Backend is Running
The backend should already be running. To verify:
```bash
# Check if backend is running
curl http://localhost:5000
```

If not running, start it:
```bash
python backend/app.py
```

### Step 2: Open Login Page

**Option 1: Double-click the file**
Navigate to: `frontend/login_test.html` and double-click it

**Option 2: Use full path in browser**
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/login_test.html
```

**Option 3: Open from command line**
```bash
start frontend/login_test.html
```

### Step 3: Login with Test Credentials

#### Student Login
```
Email: rohan.sharma.2q34.3@thapar.edu
Password: pass123
```

#### Faculty Login
```
Email: dr.rajesh@thaparfac.edu
Password: pass123
```

## All Available Credentials

### Students (Password: pass123 for all)
- rohan.sharma.2q34.3@thapar.edu
- anjali.reddy.2q31.0@thapar.edu
- varun.mehta.2q31.1@thapar.edu
- manish.kumar.2q31.2@thapar.edu
- arjun.nair.2q31.3@thapar.edu
- sanjay.mehta.2q31.4@thapar.edu

### Faculty (Password: pass123 for all)
- dr.rajesh@thaparfac.edu (Data Structures)
- prof.meena@thaparfac.edu (Algorithms)
- dr.suresh@thaparfac.edu (Database Management)
- prof.kavita@thaparfac.edu (Operating Systems)
- dr.anil@thaparfac.edu (Computer Networks)

## What You'll See

### After Student Login
- Redirects to Student Portal
- Shows: Name, Batch, Semester, CGPA
- 4 boxes: Marks, Attendance, Alerts, Feedback
- Click any box to explore

### After Faculty Login
- Redirects to Faculty Portal
- Shows: Name, Department, Subjects
- 3 sections: Marks, Attendance, Feedback
- Select batch to view/edit student data

## Troubleshooting

### "Connection error" message
- Backend is not running
- Start it: `python backend/app.py`

### Login page doesn't load
- Check file path is correct
- Try opening directly from File Explorer

### "Invalid email or password"
- Double-check credentials (case-sensitive)
- Make sure database is populated: `python check_users.py`

## Testing APIs Directly

To test all APIs without using the frontend:
```bash
python test_all_apis.py
```

This will test all endpoints and show you the responses.

---

**Backend URL**: http://localhost:5000
**Frontend Location**: frontend/login_test.html
