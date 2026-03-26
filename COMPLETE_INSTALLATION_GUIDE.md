# Complete Installation Guide - From Zero to Running

## 🎯 Overview

This guide will take you from nothing installed to a fully working Student Management System.

**Total Time:** ~30 minutes
**Difficulty:** Easy (just follow the steps)

## 📋 What You'll Install

1. Oracle Database XE (if not installed)
2. Python packages (oracledb, Flask, etc.)
3. Database tables and demo data
4. Your application

## 🚀 Installation Process

### Phase 1: Download Oracle (5 minutes)

**Option A: Already Downloaded?**
- Check if you have `OracleXE213_Win64.zip` in Downloads
- If yes, skip to Phase 2

**Option B: Need to Download?**
1. Read: **DOWNLOAD_ORACLE.md**
2. Go to: https://www.oracle.com/database/technologies/xe-downloads.html
3. Create free Oracle account
4. Download: OracleXE213_Win64.zip (2.5 GB)
5. Save to: C:\Users\vansh\Downloads\

### Phase 2: Install Oracle Database (15 minutes)

**Automated Way (Recommended):**
```cmd
INSTALL_ORACLE_DATABASE.bat
```
This script will:
- Check if Oracle installer exists
- Extract the ZIP file
- Run the installer
- Verify installation
- Update your config

**Manual Way:**
1. Read: **ORACLE_INSTALLATION_STEPS.md**
2. Extract OracleXE213_Win64.zip
3. Run setup.exe as Administrator
4. Set password (write it down!)
5. Wait for installation
6. Verify services are running

**Important:** Remember the password you set!

### Phase 3: Install Python Packages (2 minutes)

```cmd
INSTALL_ORACLE_PACKAGE.bat
```

This installs:
- oracledb (from your downloaded wheel)
- Flask
- flask-cors
- PyJWT
- python-dotenv

**Verify:**
```cmd
python -c "import oracledb; print('OK')"
```

### Phase 4: Configure Database Connection (1 minute)

Edit `backend/config.py`:
```python
DB_USER = 'system'
DB_PASSWORD = 'YOUR_ORACLE_PASSWORD'  # Change this!
DB_DSN = 'localhost:1521/xe'
```

Replace `YOUR_ORACLE_PASSWORD` with the password you set during Oracle installation.

### Phase 5: Setup Database Tables (5 minutes)

**Option A: Using SQL Developer (Recommended)**

1. **Download SQL Developer:**
   - Go to: https://www.oracle.com/database/sqldeveloper/technologies/download/
   - Download: "Windows 64-bit with JDK included"
   - Extract and run sqldeveloper.exe

2. **Create Connection:**
   - Click green "+" icon
   - Name: Local XE
   - Username: system
   - Password: [your Oracle password]
   - Hostname: localhost
   - Port: 1521
   - Service name: xe
   - Click "Test" → Should say "Success"
   - Click "Connect"

3. **Run SQL Scripts:**
   - File → Open → `backend/database/schema.sql`
   - Click "Run Script" (F5)
   - Wait for completion
   - File → Open → `backend/database/demo_data.sql`
   - Click "Run Script" (F5)
   - Wait for completion (1-2 minutes)

**Option B: Using SQL*Plus (Command Line)**

```cmd
sqlplus system/YOUR_PASSWORD@localhost:1521/xe

SQL> @backend/database/schema.sql
SQL> @backend/database/demo_data.sql
SQL> exit
```

### Phase 6: Test Everything (2 minutes)

```cmd
cd backend
python test_connection.py
```

**Expected Output:**
```
✓ Connection successful!
✓ Tables found:
  - USERS
  - STUDENTS
  - SUBJECTS
✓ Users in database: 50
```

If you see this, everything is working!

### Phase 7: Run the Application (1 minute)

**Easy Way:**
```cmd
RUN_PROJECT.bat
```

**Manual Way:**

Terminal 1 - Backend:
```cmd
cd backend
python app.py
```

Terminal 2 - Frontend:
```cmd
cd frontend
python -m http.server 8000
```

### Phase 8: Open in Browser

1. Open browser
2. Go to: http://localhost:8000/login.html
3. Login with:
   - Email: `rohan.sharma@thapar.edu`
   - Password: `password123`

## ✅ Success Checklist

Go through this checklist:

### Oracle Installation
- [ ] Downloaded OracleXE213_Win64.zip
- [ ] Extracted ZIP file
- [ ] Ran setup.exe as Administrator
- [ ] Set administrator password
- [ ] Installation completed successfully
- [ ] OracleServiceXE is running (check services.msc)
- [ ] OracleTNSListener is running

### Python Setup
- [ ] Installed oracledb package
- [ ] Installed Flask and other packages
- [ ] Can import oracledb without errors

### Database Configuration
- [ ] Updated backend/config.py with password
- [ ] Ran schema.sql successfully
- [ ] Ran demo_data.sql successfully
- [ ] test_connection.py shows success

### Application Running
- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 8000
- [ ] Can access login page
- [ ] Can login successfully
- [ ] Dashboard loads correctly
- [ ] All 4 modules work (Marks, Attendance, Alerts, Feedback)

## 🎯 Quick Command Reference

```cmd
# Check Oracle service
sc query OracleServiceXE

# Start Oracle service
net start OracleServiceXE

# Install Python packages
INSTALL_ORACLE_PACKAGE.bat

# Test database connection
cd backend
python test_connection.py

# Run application
RUN_PROJECT.bat

# Or manually:
cd backend
python app.py

# In new terminal:
cd frontend
python -m http.server 8000
```

## 🆘 Troubleshooting

### Oracle Won't Install
- Run setup.exe as Administrator
- Check you have 10 GB free space
- Disable antivirus temporarily
- Restart computer and try again

### Services Won't Start
- Open services.msc
- Find OracleServiceXE
- Right-click → Start
- If fails, check Event Viewer for errors

### Can't Connect to Database
- Verify password in backend/config.py
- Check Oracle services are running
- Try: `sqlplus system/password@localhost:1521/xe`
- Reset password if needed

### Python Package Errors
- Update pip: `pip install --upgrade pip`
- Install manually: `pip install oracledb Flask flask-cors PyJWT python-dotenv`
- Use your wheel: `pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl`

### Port Already in Use
- Backend (5000): Change in app.py
- Frontend (8000): Use `python -m http.server 8080`

### Browser Shows Errors
- Check both servers are running
- Open browser console (F12) for errors
- Verify URL: http://localhost:8000/login.html
- Clear browser cache

## 📚 Documentation Reference

| Issue | Read This |
|-------|-----------|
| Downloading Oracle | DOWNLOAD_ORACLE.md |
| Installing Oracle | ORACLE_INSTALLATION_STEPS.md |
| Oracle problems | ORACLE_SETUP_GUIDE.md |
| Step-by-step guide | STEP_BY_STEP.md |
| Quick overview | START_HERE.md |
| Track progress | INSTALLATION_CHECKLIST.md |
| Complete summary | COMPLETE_SETUP_SUMMARY.md |

## ⏱️ Time Breakdown

| Phase | Task | Time |
|-------|------|------|
| 1 | Download Oracle | 5 min |
| 2 | Install Oracle | 15 min |
| 3 | Install Python packages | 2 min |
| 4 | Configure database | 1 min |
| 5 | Setup tables | 5 min |
| 6 | Test connection | 2 min |
| 7 | Run application | 1 min |
| 8 | Open browser | 1 min |
| **Total** | | **~30 min** |

## 🎉 You're Done!

If you completed all phases, you now have:

✅ Oracle Database XE installed and running
✅ Python packages installed
✅ Database with 8 tables
✅ 40 students + 10 faculty demo data
✅ Working login system
✅ Student dashboard with 4 modules
✅ Marks with graphs
✅ Attendance tracking
✅ Alert system
✅ Feedback messaging

## 🚀 Next Steps

Now you can:
1. Explore all features
2. Test different student logins
3. View marks and attendance
4. Send feedback messages
5. Show it to your team
6. Start your DBMS project!

## 📞 Still Need Help?

1. Check the specific guide for your issue
2. Review INSTALLATION_CHECKLIST.md
3. Read COMPLETE_SETUP_SUMMARY.md
4. Check Oracle documentation

---

**Good luck! Your system is ready to use! 🎯**
