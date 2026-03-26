# Oracle Database XE Installation - Complete Guide

## 📋 Before You Start

**Requirements:**
- Windows 10/11 (64-bit)
- 10 GB free disk space
- Administrator access
- Downloaded: OracleXE213_Win64.zip

**Time needed:** 15-20 minutes

## 🚀 Installation Steps

### Step 1: Extract the ZIP File

1. Go to your Downloads folder
2. Find `OracleXE213_Win64.zip`
3. Right-click → "Extract All..."
4. Choose location: `C:\Oracle\` (or keep default)
5. Click "Extract"
6. Wait for extraction (2-3 minutes)

### Step 2: Run the Installer

1. Open the extracted folder
2. Find `setup.exe`
3. **Right-click** on `setup.exe`
4. Select **"Run as administrator"**
5. Click "Yes" on User Account Control prompt

### Step 3: Installation Wizard

**Welcome Screen:**
- Click "Next"

**License Agreement:**
- Read the agreement
- Check "I accept the terms..."
- Click "Next"

**Choose Destination:**
- Default location: `C:\app\[username]\product\21c\`
- You can change if needed
- Click "Next"

**Set Password:**
- This is VERY IMPORTANT!
- Enter a password for database administrator
- **Example:** `Oracle123` (use something you'll remember!)
- **Write it down here:** _______________________
- Re-enter password to confirm
- Click "Next"

**Summary:**
- Review your settings
- Click "Install"

### Step 4: Wait for Installation

- Progress bar will show installation status
- This takes 10-15 minutes
- Don't close the window!
- You'll see:
  - Copying files...
  - Creating database...
  - Configuring services...

### Step 5: Installation Complete

- You'll see "Successfully installed Oracle Database XE"
- Click "Finish"
- Oracle services will start automatically

## ✅ Verify Installation

### Check 1: Services Running

1. Press `Win + R`
2. Type `services.msc`
3. Press Enter
4. Look for these services (should be "Running"):
   - **OracleServiceXE**
   - **OracleTNSListener**

If not running:
- Right-click → Start

### Check 2: Test Connection

Open Command Prompt and run:
```cmd
sqlplus system/YOUR_PASSWORD@localhost:1521/xe
```

Replace `YOUR_PASSWORD` with the password you set.

You should see:
```
Connected to:
Oracle Database 21c Express Edition Release 21.0.0.0.0
```

Type `exit` to quit.

### Check 3: Check Installation Folder

Navigate to:
```
C:\app\[your-username]\product\21c\
```

You should see folders like:
- dbhomeXE
- admin
- oradata

## 🔧 Post-Installation Configuration

### Set Environment Variables (Optional but Recommended)

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Advanced" tab
3. Click "Environment Variables"
4. Under "System variables", click "New"
5. Add:
   ```
   Variable name: ORACLE_HOME
   Variable value: C:\app\[username]\product\21c\dbhomeXE
   ```
6. Edit "Path" variable
7. Add: `%ORACLE_HOME%\bin`
8. Click OK on all windows

### Enable Automatic Startup

1. Open `services.msc`
2. Find `OracleServiceXE`
3. Right-click → Properties
4. Set "Startup type" to "Automatic"
5. Click OK
6. Repeat for `OracleTNSListener`

## 📝 Connection Details

Save these for your project:

```
Database Type: Oracle Database XE
Version: 21c
Username: system
Password: [your password]
Hostname: localhost
Port: 1521
Service Name: xe
SID: XE
Connection String: localhost:1521/xe
```

## 🎯 Next Steps

Now that Oracle is installed:

1. **Update your project config:**
   ```cmd
   Edit backend/config.py
   Set DB_PASSWORD to your Oracle password
   ```

2. **Install Python packages:**
   ```cmd
   INSTALL_ORACLE_PACKAGE.bat
   ```

3. **Setup database tables:**
   ```cmd
   Run backend/database/schema.sql in SQL Developer
   Run backend/database/demo_data.sql
   ```

4. **Test connection:**
   ```cmd
   cd backend
   python test_connection.py
   ```

5. **Run the application:**
   ```cmd
   RUN_PROJECT.bat
   ```

## 🆘 Troubleshooting

### Installation Failed

**Error: "Insufficient privileges"**
- Solution: Run setup.exe as Administrator

**Error: "Not enough disk space"**
- Solution: Free up at least 10 GB space

**Error: "Port 1521 already in use"**
- Solution: Close other database applications
- Or change port during installation

### Services Won't Start

**OracleServiceXE won't start:**
1. Open Event Viewer (eventvwr.msc)
2. Check Windows Logs → Application
3. Look for Oracle errors
4. Common fix: Restart computer

**Listener won't start:**
1. Check if port 1521 is free
2. Run: `netstat -ano | findstr 1521`
3. If port is used, stop that process

### Can't Connect

**"TNS: no listener"**
- Start OracleTNSListener service

**"Invalid username/password"**
- Reset password:
  ```cmd
  sqlplus / as sysdba
  ALTER USER system IDENTIFIED BY NewPassword123;
  exit
  ```

**"ORA-12154: TNS:could not resolve"**
- Check connection string format
- Use: `localhost:1521/xe` (not XE)

### Installation Hangs

If installation freezes:
1. Wait 5 minutes (it might be working)
2. Check Task Manager for Oracle processes
3. If truly frozen:
   - Cancel installation
   - Restart computer
   - Delete C:\app folder
   - Try again

## 🔄 Uninstall (if needed)

1. Control Panel → Programs and Features
2. Find "Oracle Database 21c Express Edition"
3. Click Uninstall
4. Follow wizard
5. Manually delete:
   - C:\app\
   - C:\Program Files\Oracle\ (if exists)

## 📚 Additional Resources

**Oracle Documentation:**
```
https://docs.oracle.com/en/database/oracle/oracle-database/21/xeinw/
```

**Video Tutorial:**
Search YouTube: "Install Oracle Database 21c XE Windows"

**Oracle Community:**
```
https://community.oracle.com/
```

## ✅ Installation Checklist

- [ ] Downloaded OracleXE213_Win64.zip
- [ ] Extracted ZIP file
- [ ] Ran setup.exe as Administrator
- [ ] Accepted license agreement
- [ ] Set administrator password
- [ ] Completed installation (10-15 min)
- [ ] Verified OracleServiceXE is running
- [ ] Verified OracleTNSListener is running
- [ ] Tested connection with sqlplus
- [ ] Updated backend/config.py with password

## 🎉 Success!

If all checks pass, Oracle is installed correctly!

Proceed to: **COMPLETE_SETUP_SUMMARY.md** for next steps.
