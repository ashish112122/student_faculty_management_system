# Step-by-Step Installation (Windows)

## ✅ STEP 1: Install Oracle Database XE

1. **Download Oracle Database 21c XE:**
   - Go to: https://www.oracle.com/database/technologies/xe-downloads.html
   - Click "Oracle Database 21c Express Edition for Windows x64"
   - Sign in with Oracle account (create free account if needed)
   - Download: `OracleXE213_Win64.zip`

2. **Install Oracle XE:**
   - Extract the ZIP file
   - Run `setup.exe` as Administrator
   - Follow the wizard
   - **IMPORTANT:** Set a password for database (remember this!)
   - Default settings are fine (Port: 1521, Service: XE)
   - Wait for installation (takes 5-10 minutes)

3. **Verify Oracle is Running:**
   - Press `Win + R`, type `services.msc`, press Enter
   - Look for `OracleServiceXE` - should be "Running"
   - If not running, right-click → Start

## ✅ STEP 2: Install Python Packages

Open Command Prompt in your project folder:

```cmd
cd backend
pip install Flask==2.3.0
pip install flask-cors==4.0.0
pip install PyJWT==2.8.0
pip install python-dotenv==1.0.0
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
```

**Verify installation:**
```cmd
python -c "import oracledb; print('oracledb installed:', oracledb.__version__)"
```

## ✅ STEP 3: Configure Database Connection

1. Open `backend/config.py`
2. Update the password:
```python
DB_USER = 'system'
DB_PASSWORD = 'YOUR_ORACLE_PASSWORD'  # Password you set during Oracle installation
DB_DSN = 'localhost:1521/xe'
```

## ✅ STEP 4: Setup Database Tables

### Option A: Using SQL Developer (Easier)

1. **Download SQL Developer:**
   - Go to: https://www.oracle.com/database/sqldeveloper/technologies/download/
   - Download "Windows 64-bit with JDK included"
   - Extract and run `sqldeveloper.exe`

2. **Connect to Database:**
   - Click green "+" icon (New Connection)
   - Name: `Local XE`
   - Username: `system`
   - Password: (your Oracle password)
   - Hostname: `localhost`
   - Port: `1521`
   - Service name: `xe`
   - Click "Test" → Should say "Success"
   - Click "Connect"

3. **Run SQL Scripts:**
   - Click File → Open
   - Navigate to `backend/database/schema.sql`
   - Click "Run Script" button (or press F5)
   - Wait for completion
   - Open `backend/database/demo_data.sql`
   - Click "Run Script" button (or press F5)
   - Wait for completion (may take 1-2 minutes)

### Option B: Using SQL*Plus (Command Line)

```cmd
sqlplus system/YOUR_PASSWORD@localhost:1521/xe

SQL> @backend/database/schema.sql
SQL> @backend/database/demo_data.sql
SQL> exit
```

## ✅ STEP 5: Test Database Connection

```cmd
cd backend
python test_connection.py
```

You should see:
```
✓ Connection successful!
✓ Tables found:
  - USERS
  - STUDENTS
  - SUBJECTS
✓ Users in database: 50
```

## ✅ STEP 6: Run the Application

### Terminal 1 - Backend:
```cmd
cd backend
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Terminal 2 - Frontend:
```cmd
cd frontend
python -m http.server 8000
```

You should see:
```
Serving HTTP on :: port 8000
```

## ✅ STEP 7: Open in Browser

1. Open browser
2. Go to: `http://localhost:8000/login.html`
3. Login with:
   - Email: `rohan.sharma@thapar.edu`
   - Password: `password123`

## 🎉 Success!

You should now see the student dashboard!

---

## ⚠️ Troubleshooting

### Problem: "Module 'oracledb' not found"
**Solution:**
```cmd
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
```

### Problem: "ORA-12541: TNS:no listener"
**Solution:**
1. Open `services.msc`
2. Find `OracleServiceXE` and `OracleTNSListener`
3. Right-click → Start both services

### Problem: "ORA-01017: invalid username/password"
**Solution:**
1. Reset password:
```cmd
sqlplus / as sysdba
ALTER USER system IDENTIFIED BY newpassword;
exit
```
2. Update `backend/config.py` with new password

### Problem: "Cannot connect to Oracle"
**Solution:**
1. Check Oracle is installed: Look for `C:\app\` folder
2. Check services are running: `services.msc`
3. Try connecting with SQL Developer first
4. Verify port 1521 is not blocked by firewall

### Problem: "CORS error in browser"
**Solution:**
Make sure backend is running on port 5000

---

## 📝 Quick Reference

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

**Demo Logins:**
- Student: `rohan.sharma@thapar.edu` / `password123`
- Faculty: `rohan.sharma@thaparfac.edu` / `password123`
