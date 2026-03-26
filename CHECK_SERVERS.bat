@echo off
cls
echo ========================================
echo Server Status Check
echo ========================================
echo.

echo Checking Backend (Port 5000)...
netstat -ano | findstr :5000 >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend is NOT running on port 5000
    echo.
    echo TO FIX: Open a terminal and run:
    echo   cd backend
    echo   python app.py
    echo.
    set BACKEND_OK=0
) else (
    echo ✓ Backend is running on port 5000
    set BACKEND_OK=1
)

echo.
echo Checking Frontend (Port 8000)...
netstat -ano | findstr :8000 >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend is NOT running on port 8000
    echo.
    echo TO FIX: Open a NEW terminal and run:
    echo   cd frontend
    echo   python -m http.server 8000
    echo.
    set FRONTEND_OK=0
) else (
    echo ✓ Frontend is running on port 8000
    set FRONTEND_OK=1
)

echo.
echo ========================================
echo Summary
echo ========================================

if %BACKEND_OK%==1 if %FRONTEND_OK%==1 (
    echo.
    echo ✅ Both servers are running!
    echo.
    echo You can now open:
    echo   http://localhost:8000/login.html
    echo.
    echo If you still get connection errors:
    echo 1. Clear browser cache (Ctrl+Shift+Delete)
    echo 2. Try Incognito mode (Ctrl+Shift+N)
    echo 3. Check browser console (F12) for errors
    echo.
) else (
    echo.
    echo ❌ One or more servers are not running!
    echo.
    echo Please start the missing server(s) as shown above.
    echo.
    echo OR use the easy way:
    echo   RUN_PROJECT.bat
    echo.
)

pause
