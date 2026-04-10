@echo off
echo ========================================
echo   SYSTEM STATUS CHECK
echo ========================================
echo.

echo Checking Backend (Port 5000)...
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend is running on http://localhost:5000
) else (
    echo [X] Backend is NOT running
    echo     Start with: START_BACKEND.bat
)

echo.
echo Checking Frontend (Port 8000)...
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Frontend is running on http://localhost:8000
) else (
    echo [X] Frontend is NOT running
    echo     Start with: START_FRONTEND.bat
)

echo.
echo ========================================
echo   QUICK LINKS
echo ========================================
echo.
echo Login Page:
echo   http://localhost:8000/login_test.html
echo.
echo Backend API:
echo   http://localhost:5000
echo.
echo Test Connection:
echo   http://localhost:8000/test_backend_connection.html
echo.
echo ========================================
echo.
echo Press any key to open login page...
pause >nul

start http://localhost:8000/login_test.html

echo.
echo Login page opened in browser!
echo.
pause
