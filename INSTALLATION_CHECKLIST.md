# Installation Checklist ✅

Follow this checklist to ensure everything is set up correctly.

## Prerequisites

- [ ] Windows 10/11 (64-bit)
- [ ] Python 3.11 installed
- [ ] Internet connection for downloads

## Step 1: Oracle Database

- [ ] Downloaded Oracle Database 21c XE from Oracle website
- [ ] Installed Oracle XE successfully
- [ ] Set password for SYSTEM user (write it down!)
- [ ] Oracle service `OracleServiceXE` is running in services.msc
- [ ] Oracle listener `OracleTNSListener` is running in services.msc

**Your Oracle Password:** _________________ (write it here)

## Step 2: Python Packages

Run these commands in Command Prompt:

```cmd
cd backend
```

- [ ] `pip install Flask==2.3.0`
- [ ] `pip install flask-cors==4.0.0`
- [ ] `pip install PyJWT==2.8.0`
- [ ] `pip install python-dotenv==1.0.0`
- [ ] `pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl`

**Verify:**
- [ ] Run: `python -c "import oracledb; print('OK')"` → Should print "OK"

## Step 3: Database Configuration

- [ ] Opened `backend/config.py`
- [ ] Updated `DB_PASSWORD` with your Oracle password
- [ ] Saved the file

## Step 4: SQL Developer (Optional but Recommended)

- [ ] Downloaded SQL Developer from Oracle website
- [ ] Extracted and opened `sqldeveloper.exe`
- [ ] Created connection to localhost:1521/xe
- [ ] Connection test successful

## Step 5: Database Schema

Choose ONE method:

### Method A: SQL Developer
- [ ] Opened `backend/database/schema.sql` in SQL Developer
- [ ] Clicked "Run Script" (F5)
- [ ] No errors shown
- [ ] Opened `backend/database/demo_data.sql`
- [ ] Clicked "Run Script" (F5)
- [ ] No errors shown

### Method B: SQL*Plus
- [ ] Ran: `sqlplus system/YOUR_PASSWORD@localhost:1521/xe`
- [ ] Ran: `@backend/database/schema.sql`
- [ ] Ran: `@backend/database/demo_data.sql`
- [ ] Typed: `exit`

## Step 6: Test Connection

```cmd
cd backend
python test_connection.py
```

- [ ] Saw "✓ Connection successful!"
- [ ] Saw "✓ Tables found"
- [ ] Saw "✓ Users in database: 50"

## Step 7: Run Application

### Terminal 1:
```cmd
cd backend
python app.py
```
- [ ] Saw "Running on http://127.0.0.1:5000"
- [ ] No errors shown

### Terminal 2:
```cmd
cd frontend
python -m http.server 8000
```
- [ ] Saw "Serving HTTP on :: port 8000"

## Step 8: Test in Browser

- [ ] Opened http://localhost:8000/login.html
- [ ] Login page loaded correctly
- [ ] Entered: `rohan.sharma@thapar.edu` / `password123`
- [ ] Clicked Login
- [ ] Redirected to dashboard
- [ ] Sidebar opens when clicking ☰
- [ ] Student info displayed correctly
- [ ] All 4 cards visible (Marks, Attendance, Alerts, Feedback)

## Step 9: Test Features

- [ ] Clicked "Marks" → Shows subjects
- [ ] Clicked a subject → Shows marks table and graph
- [ ] Clicked "Attendance" → Shows subjects
- [ ] Clicked a subject → Shows attendance records and percentage
- [ ] Clicked "Alerts" → Shows alert messages
- [ ] Clicked "Feedback" → Shows faculty list
- [ ] Clicked a faculty → Opens conversation window

## 🎉 All Done!

If all checkboxes are checked, your system is working perfectly!

---

## ⚠️ If Something Failed

### Oracle Service Not Running
1. Press `Win + R`
2. Type `services.msc`
3. Find `OracleServiceXE`
4. Right-click → Start

### Python Package Error
```cmd
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Database Connection Failed
1. Check Oracle password in `backend/config.py`
2. Verify Oracle is running
3. Try: `sqlplus system/YOUR_PASSWORD@localhost:1521/xe`

### Port Already in Use
- Backend (5000): Change port in `backend/app.py` last line
- Frontend (8000): Use different port: `python -m http.server 8080`

### Browser Shows Blank Page
1. Check both servers are running
2. Check browser console (F12) for errors
3. Verify URL is correct: http://localhost:8000/login.html

---

## Quick Commands Reference

**Start Everything (Easy Way):**
```cmd
RUN_PROJECT.bat
```

**Start Backend:**
```cmd
cd backend
python app.py
```

**Start Frontend:**
```cmd
cd frontend
python -m http.server 8000
```

**Test Database:**
```cmd
cd backend
python test_connection.py
```

**Check Oracle Service:**
```cmd
sc query OracleServiceXE
```
