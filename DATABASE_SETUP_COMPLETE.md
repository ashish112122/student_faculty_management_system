# 🗄️ Database Setup - Complete Guide

## 🎯 Choose Your Method

I've created **3 different ways** to set up your database. Pick the one that works best for you:

---

## ✅ Method 1: Python Script (Recommended - Easiest)

### Just run this:
```cmd
SETUP_DATABASE_PYTHON.bat
```

**What it does:**
- ✅ Connects to Oracle automatically
- ✅ Creates all 9 tables
- ✅ Inserts all demo data (6000+ records)
- ✅ Verifies everything worked
- ✅ Shows progress and errors clearly

**Time:** 2-3 minutes

**Advantages:**
- No need to install SQL Developer
- Clear progress messages
- Automatic error handling
- Works from any folder

---

## ✅ Method 2: SQL*Plus Batch Script

### Run this:
```cmd
SETUP_DATABASE.bat
```

**What it does:**
- Uses Oracle's SQL*Plus command-line tool
- Runs schema.sql and demo_data.sql
- Shows completion status

**Time:** 2-3 minutes

**Requirements:**
- SQL*Plus must be in PATH
- Oracle XE installed

---

## ✅ Method 3: SQL Developer (Visual)

### Manual steps:

1. **Open SQL Developer**

2. **Create Connection:**
   - Username: `system`
   - Password: `Vanshi@Oracle1`
   - Hostname: `localhost`
   - Port: `1521`
   - Service: `XE`

3. **Run schema.sql:**
   - File → Open → `backend/database/schema.sql`
   - Press **F5** (Run Script)
   - Wait for "PL/SQL procedure successfully completed"

4. **Run demo_data.sql:**
   - File → Open → `backend/database/demo_data.sql`
   - Press **F5** (Run Script)
   - Wait 1-2 minutes for completion

**Time:** 5 minutes

**Advantages:**
- Visual interface
- Can see tables in tree view
- Easy to browse data
- Good for debugging

---

## 🔍 Verify Setup

After running any method, verify with:

### Option A: Python Test
```cmd
cd backend
python test_connection.py
```

**Expected output:**
```
✓ Connection successful!
✓ Tables found:
  - USERS
  - STUDENTS
  - SUBJECTS
✓ Users in database: 50
```

### Option B: Verification Script
```cmd
VERIFY_DATABASE.bat
```

### Option C: SQL Query
In SQL Developer or SQL*Plus:
```sql
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT COUNT(*) FROM users;
```

---

## 📊 What Gets Created

### Tables Created (9):

| Table | Records | Description |
|-------|---------|-------------|
| **USERS** | 50 | Login credentials (40 students + 10 faculty) |
| **STUDENTS** | 40 | Student profiles with CGPA, branch, section |
| **FACULTY** | 10 | Faculty profiles with department |
| **SUBJECTS** | 5 | DBMS, OS, CN, DSA, SE |
| **STUDENT_SUBJECTS** | 200 | Enrollments (40 students × 5 subjects) |
| **MARKS** | 800 | Marks (40 × 5 × 4 assessments) |
| **ATTENDANCE** | 6000 | Attendance (40 × 5 × 30 days) |
| **ALERTS** | 3 | Sample attendance alerts |
| **FEEDBACK** | 0 | Ready for messages |

### Sequences Created (9):
- users_seq
- students_seq
- faculty_seq
- subjects_seq
- student_subjects_seq
- marks_seq
- attendance_seq
- alerts_seq
- feedback_seq

---

## 🎓 Demo Data Details

### Students (40):
- Rohan Sharma (rohan.sharma@thapar.edu)
- Rahul Verma (rahul.verma@thapar.edu)
- Simran Kaur (simran.kaur@thapar.edu)
- Aman Gupta (aman.gupta@thapar.edu)
- Priya Singh (priya.singh@thapar.edu)
- ... and 35 more

**All passwords:** `password123`

### Faculty (10):
- Dr. Rohan Sharma (rohan.sharma@thaparfac.edu)
- Dr. Neha Verma (neha.verma@thaparfac.edu)
- Dr. Amit Khanna (amit.khanna@thaparfac.edu)
- Dr. Priya Mehta (priya.mehta@thaparfac.edu)
- ... and 6 more

**All passwords:** `password123`

### Subjects (5):
1. Database Management Systems (DBMS)
2. Operating Systems (OS)
3. Computer Networks (CN)
4. Data Structures and Algorithms (DSA)
5. Software Engineering (SE)

### Marks:
- MST: 60-95 marks
- EST: 60-95 marks
- Assignment: 70-100 marks
- Quiz: 65-100 marks

### Attendance:
- 30 days of records per subject
- ~80% attendance rate (randomized)

---

## 🆘 Troubleshooting

### Error: "ORA-12541: TNS:no listener"

**Solution:**
1. Open `services.msc`
2. Start these services:
   - `OracleServiceXE`
   - `OracleTNSListener`
3. Try again

### Error: "ORA-01017: invalid username/password"

**Solution:**
Verify password is exactly: `Vanshi@Oracle1` (case-sensitive)

### Error: "ORA-00955: name is already used"

**Solution:**
Tables already exist! You can:
1. Skip this (tables are there)
2. Drop tables first:
   ```sql
   DROP TABLE feedback CASCADE CONSTRAINTS;
   DROP TABLE alerts CASCADE CONSTRAINTS;
   DROP TABLE attendance CASCADE CONSTRAINTS;
   DROP TABLE marks CASCADE CONSTRAINTS;
   DROP TABLE student_subjects CASCADE CONSTRAINTS;
   DROP TABLE faculty CASCADE CONSTRAINTS;
   DROP TABLE students CASCADE CONSTRAINTS;
   DROP TABLE subjects CASCADE CONSTRAINTS;
   DROP TABLE users CASCADE CONSTRAINTS;
   ```

### Error: "Module oracledb not found"

**Solution:**
```cmd
INSTALL_ORACLE_PACKAGE.bat
```

### Error: "sqlplus: command not found"

**Solution:**
Use Method 1 (Python script) or Method 3 (SQL Developer)

---

## ✅ Success Checklist

After setup, you should have:

- [x] 9 tables created
- [x] 9 sequences created
- [x] 50 users (40 students + 10 faculty)
- [x] 6000+ total records
- [x] No error messages
- [x] Test connection successful

---

## 🚀 Next Steps

Once database is set up:

### 1. Test Connection
```cmd
cd backend
python test_connection.py
```

### 2. Start Backend
```cmd
cd backend
python app.py
```

### 3. Start Frontend
```cmd
cd frontend
python -m http.server 8000
```

### 4. Login
Open: `http://localhost:8000/login.html`
- Email: `rohan.sharma@thapar.edu`
- Password: `password123`

**Or use the easy way:**
```cmd
RUN_PROJECT.bat
```

---

## 📞 Quick Commands

```cmd
# Setup database (Python - Recommended)
SETUP_DATABASE_PYTHON.bat

# Setup database (SQL*Plus)
SETUP_DATABASE.bat

# Verify setup
VERIFY_DATABASE.bat

# Test connection
cd backend
python test_connection.py

# Run application
RUN_PROJECT.bat
```

---

## 🎉 Summary

**Three easy ways to set up your database:**

1. **Easiest:** `SETUP_DATABASE_PYTHON.bat`
2. **Command-line:** `SETUP_DATABASE.bat`
3. **Visual:** SQL Developer

**All methods create the same result:**
- ✅ 9 tables
- ✅ 6000+ records
- ✅ Ready to use

**Choose your preferred method and run it now!** 🚀

---

## 📄 Files Created

- `SETUP_DATABASE_PYTHON.bat` - Python-based setup
- `SETUP_DATABASE.bat` - SQL*Plus setup
- `VERIFY_DATABASE.bat` - Verification script
- `backend/setup_database.py` - Python setup script
- `DATABASE_SETUP_GUIDE.md` - Detailed guide

**Everything is ready! Just pick a method and run it! ✅**
