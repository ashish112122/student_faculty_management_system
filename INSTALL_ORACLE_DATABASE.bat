@echo off
title Oracle Database XE Installation Guide
color 0A

echo ========================================
echo Oracle Database XE Installation Guide
echo ========================================
echo.

echo This script will guide you through installing Oracle Database XE
echo.

:CHECK_DOWNLOAD
echo Step 1: Checking for Oracle installer...
echo.

if exist "C:\Users\vansh\Downloads\OracleXE213_Win64.zip" (
    echo [OK] Found: OracleXE213_Win64.zip
    goto EXTRACT
) else (
    echo [!] Oracle installer not found in Downloads folder
    echo.
    echo Please download Oracle Database 21c XE from:
    echo https://www.oracle.com/database/technologies/xe-downloads.html
    echo.
    echo Save it to: C:\Users\vansh\Downloads\OracleXE213_Win64.zip
    echo.
    echo Opening download page in browser...
    start https://www.oracle.com/database/technologies/xe-downloads.html
    echo.
    echo After downloading, press any key to continue...
    pause >nul
    goto CHECK_DOWNLOAD
)

:EXTRACT
echo.
echo Step 2: Extracting Oracle installer...
echo.

if exist "C:\Oracle\OracleXE213_Win64" (
    echo [OK] Already extracted
    goto INSTALL
)

echo Creating extraction folder...
mkdir C:\Oracle 2>nul

echo Extracting ZIP file (this may take 2-3 minutes)...
powershell -command "Expand-Archive -Path 'C:\Users\vansh\Downloads\OracleXE213_Win64.zip' -DestinationPath 'C:\Oracle' -Force"

if errorlevel 1 (
    echo [!] Extraction failed
    echo Please extract manually:
    echo 1. Go to Downloads folder
    echo 2. Right-click OracleXE213_Win64.zip
    echo 3. Select "Extract All"
    echo 4. Extract to C:\Oracle\
    pause
    exit
)

echo [OK] Extraction complete
goto INSTALL

:INSTALL
echo.
echo Step 3: Running Oracle installer...
echo.

echo IMPORTANT: You will need to set a password for the database
echo.
echo Recommended password: Oracle123
echo (or choose your own - write it down!)
echo.
echo The installer will now open...
echo.
pause

if exist "C:\Oracle\OracleXE213_Win64\setup.exe" (
    echo Starting installer as Administrator...
    powershell -command "Start-Process 'C:\Oracle\OracleXE213_Win64\setup.exe' -Verb RunAs"
    echo.
    echo ========================================
    echo INSTALLATION INSTRUCTIONS:
    echo ========================================
    echo 1. Click "Next" on welcome screen
    echo 2. Accept license agreement
    echo 3. Choose installation location (default is fine)
    echo 4. SET A PASSWORD (write it down!)
    echo 5. Click "Install"
    echo 6. Wait 10-15 minutes
    echo 7. Click "Finish"
    echo.
    echo After installation completes, press any key here...
    pause >nul
    goto VERIFY
) else (
    echo [!] Setup.exe not found
    echo Please run manually:
    echo C:\Oracle\OracleXE213_Win64\setup.exe
    pause
    exit
)

:VERIFY
echo.
echo Step 4: Verifying installation...
echo.

echo Checking Oracle services...
sc query OracleServiceXE | find "RUNNING" >nul
if errorlevel 1 (
    echo [!] OracleServiceXE is not running
    echo Starting service...
    net start OracleServiceXE
) else (
    echo [OK] OracleServiceXE is running
)

sc query OracleTNSListener | find "RUNNING" >nul
if errorlevel 1 (
    echo [!] OracleTNSListener is not running
    echo Starting service...
    net start OracleTNSListener
) else (
    echo [OK] OracleTNSListener is running
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.

:CONFIG
echo Step 5: Configure your project...
echo.

echo Please enter the password you set during installation:
set /p ORACLE_PASSWORD="Password: "

echo.
echo Updating backend/config.py...

powershell -command "(Get-Content backend/config.py) -replace \"DB_PASSWORD = 'oracle'\", \"DB_PASSWORD = '%ORACLE_PASSWORD%'\" | Set-Content backend/config.py"

echo [OK] Configuration updated
echo.

:NEXT_STEPS
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Install Python packages:
echo    INSTALL_ORACLE_PACKAGE.bat
echo.
echo 2. Setup database tables:
echo    - Open SQL Developer
echo    - Run backend/database/schema.sql
echo    - Run backend/database/demo_data.sql
echo.
echo 3. Test connection:
echo    cd backend
echo    python test_connection.py
echo.
echo 4. Run application:
echo    RUN_PROJECT.bat
echo.
echo See COMPLETE_SETUP_SUMMARY.md for detailed instructions
echo.

pause
