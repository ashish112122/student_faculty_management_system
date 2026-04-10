@echo off
echo ========================================
echo   STUDENT FACULTY MANAGEMENT SYSTEM
echo   STARTING ALL SERVICES
echo ========================================
echo.

echo Starting Backend Server...
start "Backend Server - Port 5000" cmd /k "START_BACKEND.bat"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server - Port 8000" cmd /k "START_FRONTEND.bat"

echo Waiting 2 seconds for frontend to start...
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   ALL SERVICES STARTED!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000/login_test.html
echo.
echo Opening login page in browser...
echo.

timeout /t 2 /nobreak >nul

start http://localhost:8000/login_test.html

echo.
echo ========================================
echo   SYSTEM READY!
echo ========================================
echo.
echo Login Credentials:
echo.
echo Student:
echo   Email: rohan.sharma.2q34.3@thapar.edu
echo   Password: pass123
echo.
echo Faculty:
echo   Email: dr.rajesh@thaparfac.edu
echo   Password: pass123
echo.
echo ========================================
echo.
echo Two windows are now open:
echo   1. Backend Server (Port 5000)
echo   2. Frontend Server (Port 8000)
echo.
echo Keep both windows open while using the system.
echo Close this window when done.
echo.

pause
