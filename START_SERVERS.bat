@echo off
cls
echo ========================================
echo Starting Student Management System
echo ========================================
echo.

echo Step 1: Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak >nul

echo Step 2: Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Opening login page in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000/login.html

echo.
echo ========================================
echo IMPORTANT NOTES:
echo ========================================
echo.
echo 1. Two terminal windows will open
echo 2. Keep both windows running
echo 3. Press Ctrl+C in each window to stop
echo.
echo 4. If login doesn't work:
echo    - Run: SETUP_DATABASE_PYTHON.bat (first time only)
echo    - Check browser console (F12) for errors
echo.
echo 5. Demo Credentials:
echo    Student: rohan.sharma@thapar.edu / password123
echo    Faculty: rohan.sharma@thaparfac.edu / password123
echo.
pause
