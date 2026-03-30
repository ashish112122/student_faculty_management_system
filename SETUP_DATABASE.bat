@echo off
echo ========================================
echo Oracle Database Setup Script
echo ========================================
echo.

echo This script will:
echo 1. Connect to Oracle Database
echo 2. Create all tables (schema.sql)
echo 3. Insert demo data (demo_data.sql)
echo.

echo Connecting to Oracle...
echo Username: system
echo Password: Vanshi@Oracle1
echo Service: localhost:1521/XE
echo.

echo ========================================
echo Step 1: Creating Tables
echo ========================================
sqlplus -S system/Vanshi@Oracle1@localhost:1521/XE @backend/database/schema.sql

if errorlevel 1 (
    echo.
    echo ❌ Error creating tables!
    echo.
    echo Possible issues:
    echo 1. Oracle service not running - Check services.msc
    echo 2. Wrong password - Verify: Vanshi@Oracle1
    echo 3. Oracle not installed
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Tables created successfully!
echo.

echo ========================================
echo Step 2: Inserting Demo Data
echo ========================================
sqlplus -S system/Vanshi@Oracle1@localhost:1521/XE @backend/database/demo_data.sql

if errorlevel 1 (
    echo.
    echo ❌ Error inserting data!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ Database Setup Complete!
echo ========================================
echo.
echo Tables created:
echo - USERS (50 records)
echo - STUDENTS (40 records)
echo - FACULTY (10 records)
echo - SUBJECTS (5 records)
echo - STUDENT_SUBJECTS (200 records)
echo - MARKS (800 records)
echo - ATTENDANCE (6000 records)
echo - ALERTS (3 records)
echo - FEEDBACK (0 records - ready for use)
echo.
echo You can now run the application!
echo.
pause
