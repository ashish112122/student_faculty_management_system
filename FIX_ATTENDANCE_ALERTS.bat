@echo off
echo ========================================
echo   FIXING ATTENDANCE AND ALERTS
echo ========================================
echo.
echo This will:
echo 1. Change attendance range to 1 Jan - 1 April
echo 2. Fix alert timestamps (remove 00:00)
echo 3. Regenerate alerts with proper times
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

cd backend
python fix_attendance_and_alerts.py

echo.
echo ========================================
echo   DONE!
echo ========================================
echo.
echo Please restart the backend server:
echo 1. Close the backend window
echo 2. Double-click START_BACKEND.bat
echo.
pause
