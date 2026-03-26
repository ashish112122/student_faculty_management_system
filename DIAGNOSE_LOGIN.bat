@echo off
cls
echo ========================================
echo Login Issue Diagnostic Tool
echo ========================================
echo.

echo [1/5] Checking if Backend is running...
netstat -ano | findstr :5000 >nul 2>&1
if errorlevel 1 (
    echo ❌ PROBLEM: Backend is NOT running
    echo.
    echo FIX: Open terminal and run:
    echo   cd backend
    echo   python app.py
    echo.
    set ISSUE_FOUND=1
) else (
    echo ✓ Backend is running
)

echo.
echo [2/5] Checking if Frontend is running...
netstat -ano | findstr :8000 >nul 2>&1
if errorlevel 1 (
    echo ❌ PROBLEM: Frontend is NOT running
    echo.
    echo FIX: Open terminal and run:
    echo   cd frontend
    echo   python -m http.server 8000
    echo.
    set ISSUE_FOUND=1
) else (
    echo ✓ Frontend is running
)

echo.
echo [3/5] Checking if oracledb package is installed...
python -c "import oracledb" 2>nul
if errorlevel 1 (
    echo ❌ PROBLEM: oracledb package not installed
    echo.
    echo FIX: Run this command:
    echo   pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
    echo.
    set ISSUE_FOUND=1
) else (
    echo ✓ oracledb package is installed
)

echo.
echo [4/5] Checking if Flask is installed...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ PROBLEM: Flask not installed
    echo.
    echo FIX: Run this command:
    echo   cd backend
    echo   pip install -r requirements.txt
    echo.
    set ISSUE_FOUND=1
) else (
    echo ✓ Flask is installed
)

echo.
echo [5/5] Checking if database tables exist...
cd backend
python -c "import oracledb; conn = oracledb.connect(user='system', password='Vanshi@Oracle1', dsn='localhost:1521/XE'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM users'); print('✓ Database tables exist')" 2>nul
if errorlevel 1 (
    echo ❌ PROBLEM: Database tables not created
    echo.
    echo FIX: Run this command:
    echo   SETUP_DATABASE_PYTHON.bat
    echo.
    set ISSUE_FOUND=1
)
cd ..

echo.
echo ========================================
echo Diagnostic Complete
echo ========================================
echo.

if defined ISSUE_FOUND (
    echo ❌ Issues found! Fix the problems above.
    echo.
    echo After fixing, try logging in again with:
    echo   Email: rohan.sharma@thapar.edu
    echo   Password: password123
) else (
    echo ✅ All checks passed!
    echo.
    echo If login still doesn't work:
    echo 1. Open browser console (F12)
    echo 2. Try to login
    echo 3. Look for error messages in console
    echo 4. Share the error message for help
)

echo.
pause
