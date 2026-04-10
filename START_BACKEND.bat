@echo off
echo ========================================
echo   STARTING BACKEND SERVER
echo ========================================
echo.

cd backend

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Starting Flask backend on http://localhost:5000
echo.
echo Backend will run in this window.
echo Press Ctrl+C to stop the backend.
echo.
echo ========================================

python app.py

pause
