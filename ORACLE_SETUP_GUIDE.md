# Oracle Database Setup Guide for Windows

## What is Oracle Database?

Oracle Database is a powerful database management system. For this project, we'll use Oracle Database XE (Express Edition) - it's free and perfect for development.

## Download Links

### 1. Oracle Database 21c XE (Required)
**Link:** https://www.oracle.com/database/technologies/xe-downloads.html

**What to download:**
- File: `OracleXE213_Win64.zip` (approximately 2.5 GB)
- You'll need to create a free Oracle account to download

### 2. Oracle SQL Developer (Recommended)
**Link:** https://www.oracle.com/database/sqldeveloper/technologies/download/

**What to download:**
- File: `sqldeveloper-23.1.1.345.2114-x64.zip` (Windows 64-bit with JDK)
- No Oracle account needed

## Installation Steps

### Part 1: Install Oracle Database XE

1. **Extract the ZIP file**
   - Right-click `OracleXE213_Win64.zip`
   - Select "Extract All"
   - Choose a location (e.g., Downloads)

2. **Run the Installer**
   - Navigate to extracted folder
   - Right-click `setup.exe`
   - Select "Run as administrator"

3. **Follow Installation Wizard**
   - Click "Next" on welcome screen
   - Accept license agreement
   - Choose installation location (default is fine: `C:\app\`)
   - **IMPORTANT:** Set a password for database
     - Example: `Oracle123` (remember this!)
     - Write it down: ___________________
   - Click "Install"
   - Wait 5-10 minutes for installation

4. **Verify Installation**
   - Press `Win + R`
   - Type `services.msc` and press Enter
   - Look for these services:
     - `OracleServiceXE` → Should be "Running"
     - `OracleTNSListener` → Should be "Running"
   - If not running, right-click → Start

### Part 2: Install SQL Developer

1. **Extract SQL Developer**
   - Right-click the downloaded ZIP
   - Extract to `C:\sqldeveloper\`

2. **Run SQL Developer**
   - Navigate to `C:\sqldeveloper\`
   - Double-click `sqldeveloper.exe`
   - First time may take a minute to start

3. **Create Database Connection**
   - Click the green "+" icon (New Connection)
   - Fill in details:
     ```
     Connection Name: Local XE
     Username: system
     Password: [Your Oracle password from installation]
     Save Password: ✓ (check this)
     Hostname: localhost
     Port: 1521
     Service name: xe
     ```
   - Click "Test" button
   - Should show "Status: Success"
   - Click "Connect"

### Part 3: Setup Project Database

1. **Open Schema File**
   - In SQL Developer, click File → Open
   - Navigate to your project folder
   - Open `backend/database/schema.sql`

2. **Run Schema Script**
   - Click the "Run Script" button (or press F5)
   - Wait for completion (should take 10-20 seconds)
   - Check "Script Output" tab for any errors
   - Should see "PL/SQL procedure successfully completed"

3. **Open Demo Data File**
   - Click File → Open
   - Open `backend/database/demo_data.sql`

4. **Run Demo Data Script**
   - Click "Run Script" button (F5)
   - Wait for completion (may take 1-2 minutes)
   - Should see multiple "1 row inserted" messages
   - Should see "PL/SQL procedure successfully completed"

5. **Verify Data**
   - In SQL Developer, expand "Tables" in left panel
   - You should see:
     - USERS
     - STUDENTS
     - SUBJECTS
     - STUDENT_SUBJECTS
     - FEEDBACK
     - FACULTY
     - MARKS
     - ATTENDANCE
     - ALERTS
   - Right-click "USERS" → View Data
   - Should see 50 rows (40 students + 10 faculty)

## Connection Details Reference

Save these details - you'll need them:

```
Database Type: Oracle
Username: system
Password: [Your password]
Hostname: localhost
Port: 1521
Service Name: xe
Connection String: localhost:1521/xe
```

## Common Issues & Solutions

### Issue 1: "Oracle service not found"
**Cause:** Oracle not installed properly
**Solution:** 
- Reinstall Oracle XE
- Make sure to run installer as Administrator

### Issue 2: "TNS: no listener"
**Cause:** Oracle listener service not running
**Solution:**
1. Open `services.msc`
2. Find `OracleTNSListener`
3. Right-click → Start

### Issue 3: "Invalid username/password"
**Cause:** Wrong password or user locked
**Solution:**
1. Open Command Prompt as Administrator
2. Run: `sqlplus / as sysdba`
3. Run: `ALTER USER system IDENTIFIED BY NewPassword123;`
4. Run: `ALTER USER system ACCOUNT UNLOCK;`
5. Run: `exit`

### Issue 4: "Port 1521 already in use"
**Cause:** Another database using same port
**Solution:**
- Stop other database services
- Or change Oracle port in configuration

### Issue 5: SQL Developer won't start
**Cause:** Java not found
**Solution:**
- Download version "with JDK included"
- Or install Java JDK 11 or higher

## Testing Your Setup

### Test 1: Command Line Connection
```cmd
sqlplus system/YOUR_PASSWORD@localhost:1521/xe
```
Should show: `Connected to: Oracle Database 21c Express Edition`

### Test 2: Python Connection
```cmd
cd backend
python test_connection.py
```
Should show: `✓ Connection successful!`

### Test 3: Query Data
In SQL Developer:
```sql
SELECT COUNT(*) FROM users;
```
Should return: `50`

## What Gets Installed?

**Oracle Database XE includes:**
- Database engine
- SQL*Plus (command-line tool)
- Windows services
- Sample schemas

**Installation size:** ~3 GB

**Default locations:**
- Program files: `C:\app\[username]\product\21c\`
- Database files: `C:\app\[username]\oradata\XE\`

## Uninstall (if needed)

1. Control Panel → Programs → Uninstall
2. Find "Oracle Database 21c Express Edition"
3. Click Uninstall
4. Manually delete `C:\app\` folder if needed

## Next Steps

After Oracle is set up:
1. ✅ Install Python packages (see STEP_BY_STEP.md)
2. ✅ Configure backend/config.py
3. ✅ Run test_connection.py
4. ✅ Start the application

## Need More Help?

**Oracle Documentation:**
- https://docs.oracle.com/en/database/oracle/oracle-database/21/xeinw/

**Video Tutorials:**
- Search YouTube: "Install Oracle Database XE 21c Windows"

**Oracle Community:**
- https://community.oracle.com/

## Quick Reference Card

```
┌─────────────────────────────────────┐
│     ORACLE XE CONNECTION INFO       │
├─────────────────────────────────────┤
│ Username:     system                │
│ Password:     [your password]       │
│ Host:         localhost             │
│ Port:         1521                  │
│ Service:      xe                    │
│ Connection:   localhost:1521/xe     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│        IMPORTANT SERVICES           │
├─────────────────────────────────────┤
│ OracleServiceXE     → Must be ON    │
│ OracleTNSListener   → Must be ON    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         USEFUL COMMANDS             │
├─────────────────────────────────────┤
│ Start service:                      │
│   net start OracleServiceXE         │
│                                     │
│ Stop service:                       │
│   net stop OracleServiceXE          │
│                                     │
│ Connect via SQL*Plus:               │
│   sqlplus system/pass@localhost/xe  │
└─────────────────────────────────────┘
```
