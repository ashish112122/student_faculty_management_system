# 🚀 WORKING LINKS - STUDENT FACULTY MANAGEMENT SYSTEM

## ✅ BACKEND STATUS: RUNNING ✅

**Backend URL:** http://localhost:5000

**Status Check:** http://127.0.0.1:5000

**Alternative IP:** http://172.31.9.70:5000

**Verified:** Backend is responding correctly with CORS enabled

### 🧪 Test Backend Connection First

**Open this test page to verify backend:**
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/test_backend_connection.html
```

This page will automatically test the backend connection and show you if everything is working.

---

## 🌐 FRONTEND LINKS

### 🔐 Login Page (Main Entry Point)

**File Path:**
```
C:\Users\vansh\student_faculty_management_system\frontend\login_test.html
```

**Browser Link (Copy & Paste):**
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/login_test.html
```

**Quick Open Command (Run in CMD/PowerShell):**
```powershell
start C:\Users\vansh\student_faculty_management_system\frontend\login_test.html
```

---

## 👤 TEST CREDENTIALS

### 🎓 Student Login

**Email:**
```
rohan.sharma.2q34.3@thapar.edu
```

**Password:**
```
pass123
```

**What You'll Access:**
- Student Dashboard
- Marks (MST:30, EST:40, Quiz:15, Assignment:15)
- Attendance (1 Jan - 1 May 2026)
- Alerts (Red/Yellow based on attendance)
- Feedback Chat with Faculty

---

### 👨‍🏫 Faculty Login

**Email:**
```
dr.rajesh@thaparfac.edu
```

**Password:**
```
pass123
```

**What You'll Access:**
- Faculty Dashboard
- Marks Entry for 10 Batches (2Q31-2Q40)
- Date-wise Attendance Marking
- Feedback Threads with Students

---

## 🔗 DIRECT PORTAL LINKS

### Student Portal (After Login)
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/student_portal.html
```
⚠️ Note: Requires valid token from login

### Faculty Portal (After Login)
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/faculty_portal.html
```
⚠️ Note: Requires valid token from login

---

## 🧪 BACKEND API ENDPOINTS

### Test Backend Connection
```
http://localhost:5000/
```
Expected Response: "Backend running successfully"

### Login API
```
POST http://localhost:5000/api/login
```

### Student Dashboard API
```
GET http://localhost:5000/api/student/dashboard
```

### Faculty Dashboard API
```
GET http://localhost:5000/api/faculty/dashboard
```

---

## 📊 SYSTEM INFORMATION

### Database
- **Type:** Oracle Database XE
- **Host:** localhost:1521/XE
- **User:** system
- **Status:** ✅ Connected

### Data Populated
- **Students:** 300 (30 per batch × 10 batches)
- **Faculty:** 5 (1 subject each, all 10 batches)
- **Subjects:** 5 (Data Structures, Algorithms, DBMS, OS, Networks)
- **Marks Records:** 6,000
- **Attendance Records:** 130,500
- **Alerts:** 626

---

## 🎯 QUICK START GUIDE

### Step 1: Verify Backend
Open in browser:
```
http://localhost:5000
```
Should show: "Backend running successfully"

### Step 2: Open Login Page
Click or paste in browser:
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/login_test.html
```

### Step 3: Login as Student
- Email: `rohan.sharma.2q34.3@thapar.edu`
- Password: `pass123`

### Step 4: Explore Features
- Click Dashboard boxes (Marks, Attendance, Alerts, Feedback)
- View subjects with faculty names
- Check attendance percentage
- Read alerts (click to mark as read)
- Send feedback messages

---

## 🔄 RESTART BACKEND (If Needed)

### Stop Backend
```powershell
# Press Ctrl+C in the terminal where backend is running
```

### Start Backend
```powershell
cd C:\Users\vansh\student_faculty_management_system\backend
python app.py
```

Backend will start on: http://localhost:5000

---

## 📱 MORE TEST ACCOUNTS

### Additional Students
```
anjali.reddy.2q31.0@thapar.edu / pass123
varun.mehta.2q31.1@thapar.edu / pass123
manish.kumar.2q31.2@thapar.edu / pass123
priya.singh.2q32.0@thapar.edu / pass123
```

### Additional Faculty
```
prof.meena@thaparfac.edu / pass123 (Algorithms)
dr.suresh@thaparfac.edu / pass123 (DBMS)
prof.kavita@thaparfac.edu / pass123 (OS)
dr.anil@thaparfac.edu / pass123 (Networks)
```

---

## 🎨 FEATURES TO TEST

### Student Portal
✅ View marks with charts (blue/teal colors)
✅ Daily attendance grid (green=present, red=absent)
✅ Alerts with color coding (red=unread, yellow=read)
✅ Real-time feedback chat
✅ Subject display: "Subject Name — Faculty Name"

### Faculty Portal
✅ Batch selection (10 batches)
✅ Marks entry with validation (max: MST:30, EST:40, Quiz:15, Assignment:15)
✅ Date-wise attendance (1 Jan - 1 May 2026)
✅ Load → Mark → Save workflow
✅ Feedback thread management

---

## 🔍 TROUBLESHOOTING

### If You See "Connection Error" in Login Page

**Solution 1: Clear Browser Cache**
1. Press `Ctrl + Shift + Delete`
2. Clear cached images and files
3. Refresh the page (`Ctrl + F5`)

**Solution 2: Test Backend First**
Open the test page:
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/test_backend_connection.html
```
This will verify if backend is responding.

**Solution 3: Check Browser Console**
1. Press `F12` to open Developer Tools
2. Go to Console tab
3. Look for any error messages
4. Common issues:
   - CORS errors (backend should have CORS enabled)
   - Network errors (backend not running)
   - Mixed content errors (use http:// not https://)

**Solution 4: Try Different Browser**
- Chrome/Edge: Usually works best
- Firefox: May have stricter CORS policies
- Try opening in incognito/private mode

### Backend Not Responding
```powershell
# Check if running
netstat -ano | findstr :5000

# Restart backend
cd backend
python app.py
```

### Login Page Not Opening
1. Copy the file path link
2. Paste directly in browser address bar
3. Or double-click: `frontend\login_test.html`

### Login Fails
1. Verify backend is running: http://localhost:5000
2. Check browser console (F12) for errors
3. Verify credentials are correct (case-sensitive)

---

## 📂 FILE STRUCTURE

```
student_faculty_management_system/
├── backend/
│   ├── app.py (✅ RUNNING on port 5000)
│   ├── config.py
│   └── setup_complete_system.py
├── frontend/
│   ├── login_test.html (🔐 START HERE)
│   ├── student_portal.html
│   └── faculty_portal.html
└── WORKING_LINKS.md (📄 THIS FILE)
```

---

## ✅ CURRENT STATUS

- **Backend:** ✅ RUNNING on http://localhost:5000
- **Frontend:** ✅ READY (Open login_test.html)
- **Database:** ✅ CONNECTED (Oracle XE)
- **Data:** ✅ POPULATED (300 students, 5 faculty)

---

## 🎯 RECOMMENDED WORKFLOW

1. **Open Backend Check:** http://localhost:5000
2. **Open Login Page:** file:///C:/Users/vansh/student_faculty_management_system/frontend/login_test.html
3. **Login as Student:** rohan.sharma.2q34.3@thapar.edu / pass123
4. **Test Features:** Marks → Attendance → Alerts → Feedback
5. **Logout and Login as Faculty:** dr.rajesh@thaparfac.edu / pass123
6. **Test Faculty Features:** Marks Entry → Attendance Marking → Feedback

---

**Last Updated:** April 7, 2026
**Backend Status:** ✅ RUNNING
**System Status:** ✅ FULLY OPERATIONAL

---

## 🚀 COPY-PASTE READY LINKS

**Backend:**
```
http://localhost:5000
```

**Login Page:**
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/login_test.html
```

**Student Email:**
```
rohan.sharma.2q34.3@thapar.edu
```

**Faculty Email:**
```
dr.rajesh@thaparfac.edu
```

**Password (Both):**
```
pass123
```

---

**EVERYTHING IS READY TO USE! 🎉**
