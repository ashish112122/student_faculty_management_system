@echo off
echo ============================================================
echo STARTING STUDENT-FACULTY PORTAL
echo ============================================================
echo.

echo Starting backend server...
start "Backend Server" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Opening login page...
start "" "frontend\templates\login.html"

echo.
echo ============================================================
echo Portal Started!
echo ============================================================
echo.
echo Backend: http://localhost:5000
echo Login Page: Opened in browser
echo.
echo Press any key to close this window...
pause >nul
