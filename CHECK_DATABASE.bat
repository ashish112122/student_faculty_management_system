@echo off
cls
echo ========================================
echo Checking Database Setup
echo ========================================
echo.

cd backend

echo Testing connection and checking tables...
python -c "import oracledb; conn = oracledb.connect(user='system', password='Vanshi@Oracle1', dsn='localhost:1521/XE'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM users'); count = cursor.fetchone()[0]; print(f'✓ Connected! Found {count} users in database'); cursor.close(); conn.close()" 2>nul

if errorlevel 1 (
    echo.
    echo ❌ Database check failed!
    echo.
    echo Possible reasons:
    echo 1. Oracle database is not running
    echo 2. Tables are not created
    echo 3. Wrong credentials
    echo.
    echo To fix:
    echo 1. Check if Oracle service is running in services.msc
    echo 2. Run: SETUP_DATABASE_PYTHON.bat
    echo.
) else (
    echo.
    echo ✅ Database is working correctly!
    echo.
    echo If login still fails, restart the backend:
    echo 1. Stop backend (Ctrl+C in backend terminal)
    echo 2. Run: cd backend && python app.py
    echo.
)

cd ..
pause
