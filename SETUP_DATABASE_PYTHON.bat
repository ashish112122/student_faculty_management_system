@echo off
echo ========================================
echo Oracle Database Setup (Python Method)
echo ========================================
echo.

echo This will:
echo 1. Create all database tables
echo 2. Insert 40 students + 10 faculty
echo 3. Insert sample marks and attendance
echo.

echo Make sure Oracle service is running!
echo.
pause

cd backend
python setup_database.py

if errorlevel 1 (
    echo.
    echo ❌ Setup failed!
    echo.
    echo Check the error messages above.
    echo.
) else (
    echo.
    echo ========================================
    echo ✅ Database Setup Complete!
    echo ========================================
    echo.
    echo Next step: Run the application
    echo   RUN_PROJECT.bat
    echo.
)

cd ..
pause
