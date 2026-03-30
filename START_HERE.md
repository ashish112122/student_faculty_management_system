# 🚀 START HERE - Complete Setup Guide

Welcome! This guide will help you set up the Student Management System from scratch.

## 📋 What You Need

1. **Windows 10/11** (64-bit)
2. **Python 3.11** (already installed ✓)
3. **Oracle Database XE** (we'll install this)
4. **Your downloaded file:** `oracledb-3.4.2-cp311-cp311-win_amd64.whl` ✓

## 🎯 Quick Start (3 Simple Steps)

### Step 1: Install Oracle Database (15 minutes)

1. **Download Oracle XE:**
   - Go to: https://www.oracle.com/database/technologies/xe-downloads.html
   - Download: `OracleXE213_Win64.zip` (2.5 GB)
   - Create free Oracle account if needed

2. **Install:**
   - Extract ZIP file
   - Run `setup.exe` as Administrator
   - Set password (example: `Oracle123`)
   - **Write your password here:** ___________________
   - Wait for installation

3. **Verify:**
   - Press `Win + R`, type `services.msc`
   - Check `OracleServiceXE` is "Running"

📖 **Detailed guide:** See `ORACLE_SETUP_GUIDE.md`

### Step 2: Install Python Packages (2 minutes)

Open Command Prompt in project folder:

```cmd
cd backend
pip install Flask flask-cors PyJWT python-dotenv
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
```

**Or use the batch file:**
```cmd
QUICK_INSTALL.bat
```

### Step 3: Setup Database (5 minutes)

**Option A: Using SQL Developer (Recommended)**

1. Download SQL Developer: https://www.oracle.com/database/sqldeveloper/technologies/download/
2. Extract and run `sqldeveloper.exe`
3. Create connection:
   - Username: `system`
   - Password: [your Oracle password]
   - Hostname: `localhost`
   - Port: `1521`
   - Service: `xe`
4. Open and run `backend/database/schema.sql` (press F5)
5. Open and run `backend/database/demo_data.sql` (press F5)

**Option B: Using Command Line**

```cmd
sqlplus system/YOUR_PASSWORD@localhost:1521/xe
SQL> @backend/database/schema.sql
SQL> @backend/database/demo_data.sql
SQL> exit
```

## ✅ Test Everything Works

```cmd
cd backend
python test_connection.py
```

Should show:
```
✓ Connection successful!
✓ Tables found
✓ Users in database: 50
```

## 🎮 Run the Application

**Easy way:**
```cmd
RUN_PROJECT.bat
```

**Manual way:**

Terminal 1:
```cmd
cd backend
python app.py
```

Terminal 2:
```cmd
cd frontend
python -m http.server 8000
```

## 🌐 Open in Browser

Go to: http://localhost:8000/login.html

**Login with:**
- Email: `rohan.sharma@thapar.edu`
- Password: `password123`

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `START_HERE.md` | This file - quick overview |
| `STEP_BY_STEP.md` | Detailed step-by-step instructions |
| `ORACLE_SETUP_GUIDE.md` | Complete Oracle installation guide |
| `INSTALLATION_CHECKLIST.md` | Checklist to track progress |
| `INSTALLATION_GUIDE.md` | Technical installation details |
| `README.md` | Project overview and API docs |
| `TABLE_OWNERSHIP.md` | Database table structure |
| `INTEGRATION_GUIDE.md` | For team members 2 & 3 |

## 🆘 Having Problems?

### Problem: Can't download Oracle
- **Solution:** Create free Oracle account at oracle.com
- Alternative: Ask your instructor for installation files

### Problem: Oracle service won't start
- **Solution:** 
  1. Open `services.msc`
  2. Find `OracleServiceXE`
  3. Right-click → Start

### Problem: Python package installation fails
- **Solution:**
  ```cmd
  pip install --upgrade pip
  pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
  ```

### Problem: Database connection fails
- **Solution:** Check `backend/config.py` has correct password

### Problem: Port 5000 or 8000 already in use
- **Solution:** Close other applications or use different ports

## 🎯 What You'll Get

After setup, you'll have:

✅ **Login System**
- Student login: `name@thapar.edu`
- Faculty login: `name@thaparfac.edu`

✅ **Student Dashboard**
- Profile sidebar
- 4 modules: Marks, Attendance, Alerts, Feedback

✅ **Marks Module**
- Subject-wise marks
- MST, EST, Assignment, Quiz
- Charts comparing with class average

✅ **Attendance Module**
- Date-wise records
- Percentage calculation
- Color-coded progress bar

✅ **Alerts System**
- Auto-generated warnings
- Email notifications

✅ **Feedback Module**
- Chat with faculty
- Thread-based conversations

✅ **Database**
- 40 students
- 10 faculty members
- Complete demo data

## 📊 Project Structure

```
project/
├── frontend/          → HTML, CSS, JavaScript files
├── backend/           → Python Flask application
│   ├── app.py        → Main server
│   ├── config.py     → Configuration
│   └── database/     → SQL scripts
├── README.md         → Project documentation
└── START_HERE.md     → This file
```

## 🔧 Configuration

Edit `backend/config.py`:

```python
DB_USER = 'system'
DB_PASSWORD = 'YOUR_ORACLE_PASSWORD'  # Change this!
DB_DSN = 'localhost:1521/xe'
```

## 🧪 Demo Credentials

**Students (40 total):**
- rohan.sharma@thapar.edu / password123
- rahul.verma@thapar.edu / password123
- simran.kaur@thapar.edu / password123
- aman.gupta@thapar.edu / password123
- priya.singh@thapar.edu / password123

**Faculty (10 total):**
- rohan.sharma@thaparfac.edu / password123
- neha.verma@thaparfac.edu / password123
- amit.khanna@thaparfac.edu / password123
- priya.mehta@thaparfac.edu / password123

## 🎓 For Your Team

This is **Member 1's module** (Login & Student Dashboard).

**Member 2** will add: Faculty module, Marks entry
**Member 3** will add: Attendance entry, Alerts system

See `INTEGRATION_GUIDE.md` for team collaboration details.

## ⏱️ Time Estimate

- Oracle installation: 15 minutes
- Python packages: 2 minutes
- Database setup: 5 minutes
- Testing: 3 minutes
- **Total: ~25 minutes**

## 🎉 Success Checklist

- [ ] Oracle XE installed and running
- [ ] Python packages installed
- [ ] Database tables created
- [ ] Test connection successful
- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 8000
- [ ] Can login and see dashboard
- [ ] All 4 modules working

## 📞 Need Help?

1. Check `INSTALLATION_CHECKLIST.md` for troubleshooting
2. Read `STEP_BY_STEP.md` for detailed instructions
3. See `ORACLE_SETUP_GUIDE.md` for Oracle-specific help

## 🚀 Ready to Start?

1. Follow Step 1 above (Install Oracle)
2. Follow Step 2 above (Install Python packages)
3. Follow Step 3 above (Setup database)
4. Run `RUN_PROJECT.bat`
5. Open browser to http://localhost:8000/login.html

**Good luck! 🎯**
