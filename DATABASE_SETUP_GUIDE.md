# 🗄️ Database Setup Guide

## Quick Setup Options

Choose the method that works best for you:

---

## ✅ Option 1: Automated Batch Script (Easiest)

### Just run this:
```cmd
SETUP_DATABASE.bat
```

This will:
1. Connect to Oracle automatically
2. Create all tables
3. Insert all demo data
4. Verify everything worked

**Time:** 2-3 minutes

---

## ✅ Option 2: SQL Developer (Visual - Recommended)

### Step-by-Step:

#### 1. Open SQL Developer
- Download from: https://www.oracle.com/database/sqldeveloper/technologies/download/
- Or use the one that came with Oracle XE

#### 2. Create Connection
Click green **"+"** icon and enter:
```
Connection Name: Local XE
Username: system
Password: Vanshi@Oracle1
Hostname: localhost
Port: 1521
Service name: XE
```

Click **"Test"** → Should say "Status: Success"
Click **"Connect"**

#### 3. Run schema.sql
1. Click **File → Open**
2. Navigate to: `backend/database/schema.sql`
3. Click **"Run Script"** button (green play icon with document) or press **F5**
4. Wait for completion
5. Look for: "PL/SQL procedure successfully completed"

#### 4. Run demo_data.sql
1. Click **File → Open**
2. Navigate to: `backend/database/demo_data.sql`
3. Click **"Run Script"** button or press **F5**
4. Wait 1-2 minutes (it inserts 6000+ records)
5. Look for: "COMMIT complete"

**Time:** 5 minutes

---

## ✅ Option 3: SQL*Plus (Command Line)

### Manual Commands:

```cmd
sqlplus system/Vanshi@Oracle1@localhost:1521/XE

SQL> @backend/database/schema.sql
SQL> @backend/database/demo_data.sql
SQL> exit
```

**Time:** 3 minutes

---

## 🔍 Verify Setup

### Option A: Run Verification Script
```cmd
VERIFY_DATABASE.bat
```

### Option B: Manual Check in SQL Developer
```sql
-- Check tables exist
SELECT table_name FROM user_tables 
WHERE table_name IN ('USERS', 'STUDENTS', 'SUBJECTS', 'MARKS', 'ATTENDANCE');

-- Check record counts
SELECT COUNT(*) FROM users;      -- Should be 50
SELECT COUNT(*) FROM students;   -- Should be 40
SELECT COUNT(*) FROM marks;      -- Should be 800
SELECT COUNT(*) FROM attendance; -- Should be 6000
```

### Option C: Use Python Test Script
```cmd
cd backend
python test_connection.py
```

Should show:
```
✓ Connection successful!
✓ Tables found:
  - USERS
  - STUDENTS
  - SUBJECTS
✓ Users in database: 50
```

---

## 📊 What Gets Created

### Tables (9 total):

| Table | Records | Purpose |
|-------|---------|---------|
| USERS | 50 | Login credentials (40 students + 10 faculty) |
| STUDENTS | 40 | Student profiles |
| FACULTY | 10 | Faculty profiles |
| SUBJECTS | 5 | Course subjects (DBMS, OS, CN, DSA, SE) |
| STUDENT_SUBJECTS | 200 | Student enrollments (40 × 5) |
| MARKS | 800 | Student marks (40 × 5 × 4 assessments) |
| ATTENDANCE | 6000 | Attendance records (40 × 5 × 30 days) |
| ALERTS | 3 | Sample attendance alerts |
| FEEDBACK | 0 | Ready for messages |

### Sequences (9 total):
- users_seq
- students_seq
- subjects_seq
- student_subjects_seq
- feedback_seq
- faculty_seq
- marks_seq
- attendance_seq
- alerts_seq

---

## 🆘 Troubleshooting

### Error: "ORA-12541: TNS:no listener"

**Solution:**
1. Open `services.msc`
2. Find `OracleServiceXE` and `OracleTNSListener`
3. Right-click → Start both services
4. Try again

### Error: "ORA-01017: invalid username/password"

**Solution:**
1. Verify password is exactly: `Vanshi@Oracle1`
2. Try connecting with SQL Developer first
3. If needed, reset password:
   ```cmd
   sqlplus / as sysdba
   ALTER USER system IDENTIFIED BY Vanshi@Oracle1;
   exit
   ```

### Error: "ORA-00955: name is already used by an existing object"

**Solution:**
Tables already exist! You can either:
1. Skip this (tables are already there)
2. Drop and recreate:
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
   
   -- Then run schema.sql again
   ```

### Error: "sqlplus: command not found"

**Solution:**
SQL*Plus not in PATH. Use SQL Developer instead, or add to PATH:
1. Find Oracle installation: `C:\app\[username]\product\21c\dbhomeXE\bin`
2. Add to System PATH environment variable
3. Restart Command Prompt

### Script runs but no output

**Solution:**
Remove `-S` flag for verbose output:
```cmd
sqlplus system/Vanshi@Oracle1@localhost:1521/XE @backend/database/schema.sql
```

---

## ✅ Success Indicators

You'll know it worked when:

### In SQL Developer:
- ✅ No red error messages
- ✅ "PL/SQL procedure successfully completed"
- ✅ "COMMIT complete"
- ✅ Can see tables in left panel under "Tables"

### In SQL*Plus:
- ✅ "Table created" messages
- ✅ "Sequence created" messages
- ✅ "1 row created" messages (many times)
- ✅ "PL/SQL procedure successfully completed"
- ✅ "Commit complete"

### In Python Test:
```
✓ Connection successful!
✓ Tables found
✓ Users in database: 50
```

---

## 🎯 After Setup

Once database is set up, you can:

### 1. Test Connection
```cmd
cd backend
python test_connection.py
```

### 2. Run Application
```cmd
RUN_PROJECT.bat
```

### 3. Login
- Open: `http://localhost:8000/login.html`
- Email: `rohan.sharma@thapar.edu`
- Password: `password123`

---

## 📞 Quick Commands Reference

```cmd
# Automated setup
SETUP_DATABASE.bat

# Verify setup
VERIFY_DATABASE.bat

# Test connection
cd backend
python test_connection.py

# Run application
RUN_PROJECT.bat

# Manual SQL*Plus
sqlplus system/Vanshi@Oracle1@localhost:1521/XE
SQL> @backend/database/schema.sql
SQL> @backend/database/demo_data.sql
SQL> exit
```

---

## 🎉 Ready!

Choose your preferred method and run the scripts. The database will be ready in 2-5 minutes!

**Recommended:** Use `SETUP_DATABASE.bat` for the easiest experience.
